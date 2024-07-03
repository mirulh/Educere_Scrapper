import scrapy
import json
import os
import re

class TextSpider(scrapy.Spider):
    name = 'textspider'

    def start_requests(self):
        # Get the path to the urls_test.json file
        json_file_path = os.path.join(os.path.dirname(__file__), '..', 'urls_test.json')
        
        # Read URLs from the JSON file
        with open(json_file_path, 'r') as file:
            urls_data = json.load(file)
        
        # Create requests for each URL in the JSON file
        for entry in urls_data:
            url = entry['url']
            yield scrapy.Request(url=url, callback=self.parse, meta={'entry': entry})
            
    filters =  ["twitter"]



    def parse(self, response):
        # Extract text from the page
        text = response.xpath('//body//text()[not(ancestor::script) and not(ancestor::style)]').getall()
        page_text = ' '.join(text).strip()
        clean_text = ' '.join(page_text.split())  # Remove extra whitespace and newlines

        # page_text = page_text.replace('*', '')
        # Get additional metadata from the JSON entry
        entry = response.meta['entry']
        print(f'ENTRY HERE: {entry}')   

        cleaned_text = remove_words(clean_text)
        
        # Yield the data
        yield {
            'url': response.url,
            'name': entry.get('name', ''),
            'raw_url': entry.get('raw_url', ''),
            'text': cleaned_text
        }