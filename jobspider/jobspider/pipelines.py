# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JobspiderPipeline(object):
    def process_item(self, item, spider):
        with open('jobs.txt', 'a') as file:
            line = ','.join([item["job"], item["company"], item["location"], item["salary"], item["public_date"], item["link"]]) + '\n'
            # line = u"job: {0}, company: {1}, location: {2}, salary: {3}, date: {4}, link: {5}\n".format(item["job"], item["company"], item["location"], item["salary"], item["public_date"], item["link"])
            file.write(line)
        return item
