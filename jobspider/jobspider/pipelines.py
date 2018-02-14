# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JobspiderPipeline(object):
    def process_item(self, item, spider):
        # change the file name to store other cities' data
        with open('jobs3.txt', 'a') as file:
            line = ',sep'.join([item["job"], item["company"], item["location"], item["salary"], item["public_date"], item["link"]]) + '\n'
            file.write(line)
        return item
