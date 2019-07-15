# -*- coding: utf-8 -*-
import scrapy
import pandas
from Blog.items import BlogItem
import requests
import re

class BlogspiderSpider(scrapy.Spider):
    name = 'blogspider'
    allowed_domains = ['naver.com']

    def start_requests(self):    
        dt_index = pandas.date_range(start='20180701', end='20190709')
        dt_list = dt_index.strftime("%Y%m%d").tolist()
        dt_list.reverse()
        for idx in range(0, len(dt_list)):
            todt = dt_list[idx]
            fromdt = dt_list[idx+1]
            url = 'https://search.naver.com/search.naver?where=post&query=%EB%A7%88%EB%9D%BC%ED%83%95&st=sim&sm=tab_opt&date_from={}&date_to={}&date_option=8'.format(fromdt, todt)
            yield scrapy.Request(url=url, callback=self.parse)
    

    # def parse(self, response):
    #     for pages in response.css('.title_num ::text'):
    #         temp1 = pages.split('/')
    #         temp2 = temp1[1]
    #     for idx in range(11, temp2, 10):
    #         url =url[0] + '&start={}'.format(idx)
    #         yield scrapy.Request(url=url, callback=self.parse_scrap)

    def parse(self, response):
        item = BlogItem()
        for blogs in response.css('li.sh_blog_top'):
            # add = 'https://blog.naver.com' + blogs.css('iframe.mainFrame::attr(src)').get()
            item['title']= blogs.css('a.sh_blog_title::text').get()
            item['author']= blogs.css('a.txt84::text').get()
            item['url']= blogs.css('a.sh_blog_title::attr(href)').get()
            item['days']= blogs.css('dd.txt_inline::text').get()
            yield item
            
    #         if 'blog.naver.com' in add.url :
    #             content = str(add.xpath("//div[@class='se-main-container']").get())

    #             if content == 'None' :
    #                 content = str(add.xpath("//div[contains(@class, 'sect_dsc')]").get())

    #             if content == 'None' :
    #                 content = str(add.xpath("//div[@id='postViewArea']/div").get())

    #         content = re.sub(' +', ' ', str(re.sub(re.compile('<.*?>'), ' ', content.replace('"','')).replace('\r\n','').replace('\n','').replace('\t','').replace('\u200b','').strip()))
    #         item['body'] = content      
    #         yield item

    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.follow(next_page, self.parse)

    # for href in response.css('.sh_blog_title _sp_each_url _sp_each_title::attr(href)'):
    #     yield response.follow(href, self.parse)





    # def parse_author(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).get(default='').strip()

    #     yield {
    #         'name': extract_with_css('h3.author-title::text'),
    #         'birthdate': extract_with_css('.author-born-date::text'),
    #         'bio': extract_with_css('.author-description::text'),
    #     }

# #======================================================================================================================
# #======================================================================================================================

# import scrapy
# import pandas as pd
# from datetime import date
# import time

# end = date.today()

# class BlogspiderSpider(scrapy.Spider):
#     name = 'BlogSpider'
#     start_urls=[]

#     for i in pd.date_range(periods=2, end=end):
#         date=i.strftime('%Y%m%d')
#         query='마라탕'
#         # keyword = getattr(self, 'key', None)
#         url='https://search.naver.com/search.naver?where=post&st=date&query={0}&date_from={1}&date_to={1}&date_option=8'.format(query, date)           
#         start_urls.append(url)
                

#     def parse(self, response):

#         for item in response.css('li.sh_blog_top'):

#             title = item.css('a.sh_blog_title::attr(title)').get()

#             if item.css('a.sh_blog_title::attr(title)').get() == '':
#                 title = item.css('a.sh_blog_title::text').get()

#             yield {
#                 'title': title,
#                 'author': item.css('span.inline a::text').get(),
#                 # 'content' : content,
#                 'date' : item.css('dd.txt_inline::text').get(),
#                 'url' : item.css('a::attr(href)').get()
#             }
        
#         next_page=response.css('div.paging a.next::attr(href)').get()
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)


#             # for href in response.css('a::attr(href)'):
#             #     yield response.follow(href, self.parse_contentes)
        
#     # def parse_contents(self, response):
#     #     return response.css(query).get(default='').strip()