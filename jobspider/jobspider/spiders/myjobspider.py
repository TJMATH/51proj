# -*- coding: utf-8 -*-

import scrapy
import urllib
from jobspider.items import JobspiderItem
from scrapy.selector import Selector
from jobspider.keyword import KEYWORD

# change keyword for different jobs
keyword = KEYWORD
keywordcode = urllib.parse.quote(keyword)

class JobSpider(scrapy.Spider):
    name = "myjobspider"
    allowed_domains = ["51job.com"]
    # jobarea = 010000 for beijing
    # jobarea = 020000 for shanghai
    # jobarea = 080200 for hangzhou
    start_urls = ["http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=080200&keyword=" + "%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98"]
    

    def parse(self, response):
        respon = Selector(response)
        infos = respon.xpath('//body/div[@class="dw_wp"]/div[@class="dw_table"]/div[@class="el"]')
        for info in infos:
            item = JobspiderItem()
            path_dic = {'job': './/p[@class="t1 "]/span/a/text()', 'link': './/p[@class="t1 "]/span/a/@href', 'company': './/span[@class="t2"]/a/text()', 'location': './/span[@class="t3"]/text()', 'salary': './/span[@class="t4"]/text()', 'public_date': './/span[@class="t5"]/text()'}
            for k in path_dic.keys():
                # deal with null value
                if(len(info.xpath(path_dic[k]).extract())>0):
                    item[k] = info.xpath(path_dic[k]).extract()[0].strip()
                else:
                    item[k] = ''
            yield item

        next_page = respon.xpath('//div[@class="rt"]/a[@id="rtNext"]/@href')
        if next_page:
            next_page = next_page.extract()[0]
            self.log('page_url: %s' % next_page)
            yield scrapy.Request(next_page, callback=self.parse)
