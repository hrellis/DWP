from scrapy.spider import BaseSpider
from indeed.items import JobItem
from scrapy.http import Request
from sets import Set
from json import loads, dumps
from datetime import datetime 
import facebook
from re import findall
from time import sleep

url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&#+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

class FacebookSpider(BaseSpider):
    name = 'facebook'
    allowed_domains = ['graph.facebook.com']
    start_urls = ['http://www.facebook.com']
    graph = facebook.GraphAPI()
    
    def __init__(self):        
        self.graph.access_token = facebook.get_app_access_token('1379244598975239', 
                                                                'cf601ab7afd846d736601704787435fe')

    def parse(self, response):
        for id, jobs in self.make_api_calls():
            print(id, jobs)
            employer_info = self.make_id_object_call(id)
            
            for job in jobs:
                item = JobItem()
                
                if findall(url_regex, job['message']):
                    item['title'] = "facebook job"
                    item['link'] = "http://www.facebook.com"
                    item['desc'] = job['message']    
                    item['location'] = employer_info['location']['city']
                    item['employer'] = employer_info['name']
                    item['industry'] = employer_info['category']
                    item['long'] = employer_info['location']['longitude']
                    item['lat'] = employer_info['location']['latitude']
                    item['date_time'] = datetime.fromtimestamp(job['created_time'])
        
                    yield item
        
    def make_id_object_call(self, id):
        print str(id)
        info = self.graph.get_object(str(id))

        return info
     
    def make_api_calls(self):
        #Read id ids from file
        file = open('location_output.json', 'r')
        locations = file.read()
        file.close()

        locations = loads(locations)
        
        for id in locations:
            response = self.graph.fql("""SELECT message, created_time 
                                FROM stream 
                                WHERE source_id=%s 
                                AND actor_id=source_id 
                                AND (%s)""" 
                                % (id, 
                                   self.generate_fql_keyword_search(['job', 'hiring', 'vacancy', 'position'])))
            
            sleep(1)
            
            print (id, response)
            
            if response:  #Only return if it isn't empty
                yield (id, response)
        
        
    
    def generate_fql_keyword_search(self, keywords):
        fql = ''
        
        for keyword in keywords:
            fql += ("strpos(message, '%s') >=0 OR " % keyword)

        return fql[:-4]
