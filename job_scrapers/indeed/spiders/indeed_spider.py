from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from indeed.items import JobItem
from datetime import datetime

class IndeedSpider(BaseSpider):
	name = 'indeed'
	allowed_domains = ['indeed.com']

	def __init__(self, q='', l=''):
		self.industry = q
		self.start_urls = ["http://api.indeed.com/ads/apisearch?publisher=6848272948898688&q=%s&l=%s&sort=&radius=&st=&jt=&start=&limit=50&fromage=&filter=&latlong=1&co=uk&v=2"  % (q, l)]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		job_results = hxs.select('//result')

		for job in job_results:
			item = JobItem()

			item['title'] = job.select("./jobtitle/text()").extract()
			item['link'] = job.select("./url/text()").extract()
			item['desc'] = job.select("./snippet/text()").extract()	
			item['location'] = job.select("./city/text()").extract()
			item['employer'] = job.select("./company/text()").extract()
			item['industry'] = self.industry 
			item['long'] = job.select("./longitude/text()").extract()
			item['lat'] = job.select("./latitude/text()").extract()
			item['date_time'] = job.select("./date/text()").extract()
			
			#Put the list of strings into one big string
			for k, v in item.iteritems():
				item[k] = ''.join(v).strip()
				
			#Sat, 07 Sep 2013 08:57:00 GMT
			item['date_time'] = datetime.strptime(item['date_time'], '%a, %d %b %Y %X %Z') 

			item['link'] = item['link'].replace('viewjob', 'rc/clk')

			yield item
		
