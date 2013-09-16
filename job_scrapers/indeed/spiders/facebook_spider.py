from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from indeed.items import JobItem
from scrapy.http import Request
from sets import Set
from json import loads
from json import dumps
import facebook

class FacebookSpider(BaseSpider):
    name = 'facebook'
    allowed_domains = ['graph.facebook.com']
    #url for listing of page ids with locations nearby
    start_urls = ['https://graph.facebook.com/search?type=place&center=56.457331238956,-2.9763746796287&distance=50000&limit=1000&access_token=1379244598975239|cf601ab7afd846d736601704787435fe']

    def parse(self, response):     
        graph = facebook.GraphAPI()
        graph.access_token = facebook.get_app_access_token('1379244598975239', 'cf601ab7afd846d736601704787435fe')

        location_set = Set()
        lat, long = 56.350, -3.150

        for long_i in range(30):
            for lat_i in range(20):
                locations = graph.fql("""SELECT page_id 
                                        FROM place 
                                        WHERE distance(latitude, longitude, "%s", "%s") < 50000 
                                        LIMIT 100""" % (lat, long))
                
                for location in locations:
                    location_set.add(location['page_id'])

                print location_set
                
                lat += 0.01
            lat = 56.350
            long += 0.01
            
        print location_set
        file = open('location_output.json', 'w')
        file.write(dumps(list(location_set)))
        file.close()
        
#         locations = loads(response.body)
#         locations = locations['data']
        
        for location in location_set:
            print location
            print graph.fql("""SELECT message, created_time 
                FROM stream 
                WHERE source_id=%s 
                AND actor_id=%s 
                AND (%s)""" 
                % (location, 
                   location, 
                   self.generate_fql_keyword_search(['job', 'hiring', 'vacancy'])))
        
        i = JobItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i
    
    def generate_fql_keyword_search(self, keywords):
        fql = ''
        
        for keyword in keywords:
            fql += ("strpos(message, '%s') >=0 OR " % keyword)

        return fql[:-4]
