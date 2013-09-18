from scrapy.spider import BaseSpider
from indeed.items import JobItem
from scrapy.http import Request
from sets import Set
from json import loads
from json import dumps
import facebook
from facebook_spider import FacebookSpider
from time import sleep

class FacebookLocationSpider(BaseSpider):
    name = 'facebook_location'
    allowed_domains = ['facebook.com']
    start_urls = ['http://www.facebook.com/']

    def parse(self, response): 
        graph = FacebookSpider().graph
        
        location_set = Set()
        lat, long = 56.350, -3.150

        for long_i in range(60):
            for lat_i in range(40):
                locations = graph.fql("""SELECT page_id 
                                        FROM place 
                                        WHERE distance(latitude, longitude, "%s", "%s") < 50000 
                                        LIMIT 100""" % (lat, long))
                
                for location in locations:
                    location_set.add(location['page_id'])

                print location_set
                sleep(1)
                
                lat += 0.005
            lat = 56.350
            long += 0.005
            
        print location_set
        file = open('location_output.json', 'w')
        file.write(dumps(list(location_set)))
        file.close()