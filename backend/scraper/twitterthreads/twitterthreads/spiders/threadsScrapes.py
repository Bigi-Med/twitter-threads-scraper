import scrapy
from nested_lookup import nested_lookup
import json
import  jmespath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ThreadsScraper(scrapy.Spider):
    name = 'ThreadsScraper'
    start_urls = ["https://www.threads.net/@hormozi"]

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # Uncomment for headless mode
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse_thread(self,data ):
        # """Parse Twitter tweet JSON dataset for the most important fields"""
        # result = jmespath.search(
        #     """{
        #     text: post.caption.text,
        #     id: post.id,
        #     pk: post.pk,
        #     code: post.code,
        #     username: post.user.username,
        #     has_audio: post.has_audio,
        #     reply_count: view_replies_cta_string,
        #     like_count: post.like_count,
        # }""",
        #     data,
        text = jmespath.search('post.caption.text', data)
        id = jmespath.search('post.id', data)
        pk = jmespath.search('post.pk', data)
        code = jmespath.search('post.code', data)
        username = jmespath.search('post.user.username', data)
        has_audio = jmespath.search('post.has_audio', data)
        reply_count = jmespath.search('view_replies_cta_string', data)
        like_count = jmespath.search('post.like_count', data)

        # Construct the result object
        result = {
            'text': text,
            'id': id,
            'pk': pk,
            'code': code,
            'username': username,
            'has_audio': has_audio,
            'reply_count': reply_count,
            'like_count': like_count,
        }
        if result["reply_count"] and type(result["reply_count"]) != int:
            result["reply_count"] = int(result["reply_count"].split(" ")[0])
        result[
            "url"
        ] = f"https://www.threads.net/@{result['username']}/post/{result['code']}"
        return result

    def parse(self, response):
        self.driver.get(response.url)

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
                return {
                    # the first parsed thread is the main post:
                    "thread": threads[0],
                    # other threads are replies:
                    "replies": threads[1:],
                }
            raise ValueError("could not find thread data in page")


