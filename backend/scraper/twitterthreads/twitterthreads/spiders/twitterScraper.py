import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TwitterScraper(scrapy.Spider):
    name = 'TwitterScraper'
    start_urls = ["https://twitter.com/AlexHormozi"]

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # Uncomment for headless mode
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)

        # XPath to target the span elements
        xpath = "//div[contains(@class, 'css-175oi2r')]//div[contains(@data-testid,'tweetText')]//span"

        # Wait for the elements to load
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )

        # Extract data
        spans = self.driver.find_elements(By.XPATH, xpath)
        for span in spans[:20]:  # Limiting to first 20 elements
            yield {'tweets': span.text}

        self.driver.quit()

