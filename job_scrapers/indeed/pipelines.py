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
		        self.cursor.execute("""INSERT INTO table_jobs 
						(title, url_link, description, employer) 
						VALUES (%s, %s, %s, %s)""",
						(item['title'].encode('utf-8'),
                		        	item['link'].encode('utf-8'),
						item['desc'].encode('utf-8'),
						item['employer'].encode('utf-8')))
        		self.conn.commit()

    		except MySQLdb.Error, e:
        		print "Error %d: %s" % (e.args[0], e.args[1])

    		return item
