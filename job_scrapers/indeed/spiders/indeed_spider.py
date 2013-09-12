from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from indeed.items import JobItem

class IndeedSpider(BaseSpider):
	name = 'indeed'
	allowed_domains = ['indeed.co.uk']
	start_urls = ['http://www.indeed.co.uk/jobs?q=&l=Dundee']

	def __init__(self, q='', l=''):
	        self.start_urls = ['http://www.indeed.co.uk/jobs?q=%s&l=%s' % (q, l)]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		job_results = hxs.select('//div[@itemtype = "http://schema.org/JobPosting"]')

		for job in job_results:
			item = JobItem()

			item['title'] = job.select("./*[@class='jobtitle']//text()").extract()
			item['link'] = job.select("./*[@class='jobtitle']/a/@href").extract()
			item['desc'] = job.select(".//span[@class='summary']//text()").extract()	
			item['location'] = job.select(".//span[@class='location']//text()").extract()
			item['employer'] = job.select(".//span[@class='company']//text()").extract()

			#Put the list of strings into one big string
			for k, v in item.iteritems():
				item[k] = ''.join(v).strip()

			item['link'] = 'http://www.indeed.co.uk' + item['link']

			yield item
		
