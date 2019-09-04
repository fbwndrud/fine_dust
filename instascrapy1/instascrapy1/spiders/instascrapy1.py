# -*- coding: utf-8 -*-
import scrapy
import requests
import json
import urllib.request
import datetime as dt
import pandas as pd
import csv
from instascrapy1.items import Instascrapy1Item


class Isntascrapy1Spider(scrapy.Spider):
    name = 'instascrapy1'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    keyword = "육아소통환영"
    after = ""
    url = ""


    def start_requests(self):
        
        self.url = 'https://www.instagram.com/graphql/query/?query_hash=174a5243287c5f3a7de741089750ab3b&variables={"tag_name":"' + self.keyword + '","first": 50 ,"after": "' + self.after + '"}'
        print("self.url : " + self.url)
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        print('response.url : ' + response.url)
        json_data = json.loads(response.body)
        
        print("json_data : " + str(json_data))
        self.after = json_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        for edge in json_data['data']['hashtag']['edge_hashtag_to_media']['edges']:
            item = Instascrapy1Item()
            
            item['after'] = self.after

            try:
                item['text'] = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']
            except:
                item['text'] = ''
            
            timestamp = edge['node']['taken_at_timestamp']
            item['date']= dt.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            item['like_count']= edge['node']['edge_liked_by']['count']

            if edge['node']["is_video"]:
                item['explain'] = 'Video'
            else:
                item['explain']= edge['node']['accessibility_caption']

            shortcode = edge['node']['shortcode']
            item['each_url']= 'https://www.instagram.com/graphql/query/?query_hash=477b65a610463740ccdb83135b2014db&variables={"shortcode":"' + shortcode + '"}'

            yield item
        
        hasNext = json_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
        
        if hasNext is not None:
            self.url = 'https://www.instagram.com/graphql/query/?query_hash=174a5243287c5f3a7de741089750ab3b&variables={"tag_name":"' + self.keyword + '","first": 50 ,"after": "' + self.after + '"}'
            yield response.follow(url=self.url, callback=self.parse)

        

        # yield response.follow(href, callback=self.parse)

