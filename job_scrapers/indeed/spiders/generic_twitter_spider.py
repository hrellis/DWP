from scrapy.spider import BaseSpider
from indeed.items import JobItem
from datetime import datetime
import twitter
import re

url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&#+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

class TwitterSpider(BaseSpider):
    allowed_domains = ['twitter.com']
    start_urls = ['https://www.twitter.com']    
    
    def valid_job(self, status):
        '''Looks for known job hash tags to decide if the tweet is a job ad or not'''
        for hash_tag in self.job_hash_tags:
            if re.findall(r"#%s\b" % hash_tag, status.text, re.IGNORECASE):
                return True
            
        return False
    
    def parse(self, response):       
        api = twitter.Api(consumer_secret="CIdjqtGOakUDyt70BLeiZPEHAN9Ps4MzwPqGUVT71Q", 
                          consumer_key="O6jRxGVilkJVFmOeWIDb4g", 
                          access_token_key="1110145321-bnh4yg7046ixFy1GOW6BbqXrdz6vSdGXp4ZUvOI",
                          access_token_secret="l59JgdNFuN2PrWwUDZUiUTn5pDXv1dLb5DtchlvcM")
        jcp_timeline = api.GetUserTimeline(screen_name=self.screen_name, exclude_replies=True)
        jcp_job_posts = [status for status in jcp_timeline if self.valid_job(status)] 

        for job in jcp_job_posts:
            item = JobItem()

            item['title'] = self.title
            item['link'] = "https://www.twitter.com/%s/status/%s" % (job.user.name, job.id)
            item['desc'] = job.text
            item['location'] = self.location
            item['employer'] = job.user.name
            item['industry'] = self.industry
            item['long'] = self.long
            item['lat'] = self.lat
            item['date_time'] = datetime.fromtimestamp(job.created_at_in_seconds)

            yield item
