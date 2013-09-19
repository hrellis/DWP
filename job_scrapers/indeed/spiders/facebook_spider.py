from scrapy.spider import BaseSpider
from indeed.items import JobItem
from scrapy.http import Request
from sets import Set
from json import loads, dumps
from datetime import datetime 
import facebook
from re import compile

MAX_REQUESTS_PER_BATCH = 50

class FacebookSpider(BaseSpider):
    name = 'facebook'
    allowed_domains = ['graph.facebook.com']
    start_urls = ['http://www.facebook.com']
    graph = facebook.GraphAPI()
    
    #If any regexes match then it's a job 
    job_regexes = ['http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&#+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', #url
                   '(\d\s?){6,12}',    #Phone number
                   '[^@]+@[^@]+\.[^@]+'] #Email
    
    def __init__(self, start_page_id=0):        
        self.start_page_id = start_page_id
        self.graph.access_token = facebook.get_app_access_token('1379244598975239', 'cf601ab7afd846d736601704787435fe')
        self.job_regexes = map(compile, self.job_regexes)

    def parse(self, response):
        for jobs in self.make_api_calls():
            jobs = loads(jobs)      
            
            for job in jobs:
                print "job"
                print job
                
                item = JobItem()
                
                if any(regex.search(job['message']) for regex in self.job_regexes):
                    employer_info = self.make_id_object_call(job['source_id'])
                    print employer_info
                    
                    user_id, post_id = job['post_id'].split("_")
                    
                    item['title'] = "facebook job"
                    item['link'] = "http://www.facebook.com/%s/posts/%s" % (user_id, post_id)
                    item['desc'] = job['message']
                    item['location'] = employer_info['location']['city']
                    item['employer'] = employer_info['name']
                    item['industry'] = employer_info['category']
                    item['long'] = employer_info['location']['longitude']
                    item['lat'] = employer_info['location']['latitude']
                    item['date_time'] = datetime.fromtimestamp(job['created_time'])
        
                    yield item
        
    def make_id_object_call(self, id):
        info = self.graph.get_object(str(id))
        return info
     
    def make_api_calls(self):
        #Read id ids from file
        file = open('location_output.json', 'r')
        locations = file.read()
        file.close()

        locations = loads(locations)
        locations = locations[ locations.index(int(self.start_page_id)) - 1: ] #cut to the chase
        
        fql_batch_requests = []
        
        i = 0
        
        for id in locations:
            i += 1
            if i >= MAX_REQUESTS_PER_BATCH:
                print id
                for result in self.make_batch_request(fql_batch_requests):
                    yield result
                fql_batch_requests = []
                i = 0

            fql_batch_request = {}
            fql_batch_request['method'] = 'GET'
            fql_batch_request['relative_url'] = """method/fql.query?query=SELECT message, created_time, post_id, source_id FROM stream WHERE source_id=%s AND actor_id=source_id AND (%s)""" % (id, self.generate_fql_keyword_search(['job', 'hiring', 'vacancy', 'position']))

            fql_batch_request['relative_url'] = fql_batch_request['relative_url'].replace(" ", "+")
            
            fql_batch_requests.append(fql_batch_request)
        
        
        for result in self.make_batch_request(fql_batch_requests):
            yield result
                
    def make_batch_request(self, batch_requests):
        batch_requests = dumps(batch_requests)
        for response in self.graph.request("", post_args = {"batch": batch_requests}):
            yield response['body']
        
    
    def generate_fql_keyword_search(self, keywords):
        fql = ''
        
        for keyword in keywords:
            fql += ("strpos(message, '%s') >=0 OR " % keyword)

        return fql[:-4]
