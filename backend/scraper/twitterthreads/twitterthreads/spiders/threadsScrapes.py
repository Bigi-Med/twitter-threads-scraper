import scrapy
import time
from nested_lookup import nested_lookup
import json
import  jmespath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ThreadsScraper(scrapy.Spider):
    name = 'ThreadsScraper'

    def start_requests(self):
        profile = getattr(self,'profile',None)
        url=f'https://www.threads.net/{profile}'
        yield scrapy.Request(url, callback=self.parse_account)

    def parse_thread(self,data ):
        text = jmespath.search('post.caption.text', data)
        username = jmespath.search('post.user.username', data)

        # Construct the result object
        result = {
            'text': text,
            'username': username,
        }
        return result

    def parse(self, response):
        self.driver.get(response.url)
        page_source = self.driver.page_source
        new_response = scrapy.http.HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')
        yield scrapy.Request(self.driver.current_url,callback=self.parse_account)
        self.driver.quit()


    def parse_account(self,response):
            hidden_datasets= response.css('script[type="application/json"][data-sjs]::text').getall()
            for hidden_dataset in hidden_datasets:
                # skip loading datasets that clearly don't contain threads data
                if '"ScheduledServerJS"' not in hidden_dataset:
                    continue
                if "thread_items" not in hidden_dataset:
                    continue
                data = json.loads(hidden_dataset)
                # datasets are heavily nested, use nested_lookup to find 
                # the thread_items key for thread data
                thread_items = nested_lookup("thread_items", data)
                if not thread_items:
                    continue
                # use our jmespath parser to reduce the dataset to the most important fields
                threads = [self.parse_thread(t) for thread in thread_items for t in thread]
                file_path = 'profile.json'
                with open(file_path,'w') as file:
                    json.dump(threads,file)
            raise ValueError("could not find thread data in page")