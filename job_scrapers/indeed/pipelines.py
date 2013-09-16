# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class DatabasePipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect(user="12ac3u05", 
						passwd="abc321", 
						db="12ac3d05", 
						host="arlia.computing.dundee.ac.uk")

		self.cursor = self.conn.cursor()


	def process_item(self, item, spider):
		try:
			'''tTitle, tDescription, tLocation, tIndustry, tEmployment ,tEmployer , tContactNumber , tContactEmail , 
			tContactAddress, tDate_Added, tUrl_link, tLongitude, tLatitude'''
			self.cursor.callproc('insert_job',
									(item['title'].encode('utf-8'),
									item['desc'].encode('utf-8'),
									item['location'].encode('utf-8'),
									item['industry'].encode('utf-8'),
									None,
									item['employer'].encode('utf-8'),
									None, 
									None, 
									None,
									item['date_time'].isoformat().encode('utf-8'),
									item['link'].encode('utf-8'),
									float(item['long']),
									float(item['lat']))
								)
			self.conn.commit()

		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])

		return item
