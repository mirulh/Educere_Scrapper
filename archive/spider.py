import scrapy
import json
import os
import re
import random
import openai
import os
from dotenv import load_dotenv
from transformers import pipeline
import uuid
import urltextscrapper.spiders.filters as filters


# summarizer tool
summarizer = pipeline("summarization", model="t5-small")

class TextSpider(scrapy.Spider):
    name = 'textspider2'

# IMPORT user agent list and .env file
    user_agent_list = filters.user_agent_list
    load_dotenv()


# OPEN file and get url
    def start_requests(self):
        #import urls.json
        json_file_path = os.path.join(os.path.dirname(__file__), '..', 'urls.json')
        # read urls .json
        with open(json_file_path, 'r') as file:
            urls_data = json.load(file)
        # Create requests for each URL in the JSON file
        for entry in urls_data:
            url = entry['url']
            yield scrapy.Request(url=url, callback=self.parse, meta={'entry': entry}, headers={"User": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})

# IMPORT all filters from filters.py
    miscellaneous = filters.miscellaneous        
    subjects = filters.subjects
    subjectsMerged = filters.subjectsMerged
    subjectsSingled = filters.subjectsSingled
    languages = filters.languages
    languagesMerged = filters.languagesMerged
    materialsFormat = filters.materialsFormat
    isCertificated = filters.isCertificated
    costIndicator = filters.costIndicator

# FUNCTIONS ---------------------------------------------------
    def generate_slug(self, name):
        unique_string = f"{name.lower()}-{uuid.uuid1().hex}"
        return unique_string
    
    def generate_placeholder(self, name):
        letter = name[0].upper()
        image = f"/images/letters_placeholder/default_{letter}.png"
        return image
    
    def label_subject(self, trim_text, subjects, subjectsMerged, subjectsSingled):
        # remove comma
        # title method capitalized every word
        text = trim_text.replace(',', '').lower()
        categories = []
        result = []
        for subject in subjects:
            if subject in text:
                categories.append(subject.title())

        for subject, subjectItems in subjectsMerged.items():
            if any(word in text for word in subjectItems):
                categories.append(subject)

        for subject, subjectItems in subjectsSingled.items():
            if any(word in text.split() for word in subjectItems):
                categories.append(subject)

        if len(categories) < 1:
            categories.append("Other")

        for x in categories:
            x_raw = x.lower().split()
            s = "-".join(x_raw)
            result.append({"label": x, "value": s})

        return result

# START ---------------------------------------------------
# INITIATE the process iteratively
    def parse(self, response):
        # Extract text from the page (body + title + description) and name from entry
        body = response.xpath('//body//text()[not(ancestor::script) and not(ancestor::style) and not (ancestor::footer) and not(ancestor::nav) and not(ancestor::head)]').getall()
        title = response.xpath('//title/text()').get()
        description = response.xpath('//meta[@name="description"]/@content').get()
        entry = response.meta['entry']


    # CLEAN body text
        # remove leading and trailing whitespace and join
        page_text = ' '.join(body).strip()
        # spit into array and join
        clean_text = ' '.join(page_text.split())  
        filter_text = self.remove_words(clean_text, self.miscellaneous)
        body_text = ' '.join(filter_text.split())


    # COMBINE title, description, and body texts
        # get title
        if title:
            getTitle = title.strip()
        else:
            getTitle = "N/A"
        # get description
        if description:
            getDescription = description.strip()
        else:
            getDescription = "N/A"
        # get body text
        if len(body_text) == 0:
            body_text = "N/A"
        # combine all
        whole_text = f"TITLE: {getTitle} || DESCRIPTION: {getDescription} || BODY: {body_text}"

        
    # TRIM whole_text to be below the word limit
        word_limit = 200
        words = whole_text.split()
        if len(words) > word_limit:
            trim_text = ' '.join(words[:word_limit])
        else:
            trim_text = whole_text


    # ASSIGN to the output in sequence
        name = entry.get('name', '')
        slug = self.generate_slug(name)
        image = self.generate_placeholder(name)
        categories = self.label_subject(trim_text, self.subjects, self.subjectsMerged, self.subjectsSingled)
        techStack = self.label_language(trim_text, self.languages, self.languagesMerged)
        materialType = self.label_type(trim_text, self.materialsFormat)
        cost = self.check_cost(trim_text, self.costIndicator)
        certificate = self.check_certificate(trim_text, self.isCertificated)
        # description = self.generate_description(trim_text)
        raw_description = self.summarize_text(trim_text, self.instruction)
        description = self.capitalize_text(raw_description)
        url = response.url
   
# APPEND ---------------------------------------------------
        yield {
            'name': name,
            'slug': slug,
            'image': image,
            'category': categories,
            'techStack': techStack,
            'type': materialType,
            'cost' : cost,
            'hasCert': certificate,
            'description' : description,
            'url': url,
            'letterLength': len(description),
            'wordLength': len(description.split()),
            # "length": len(trim_text.split()),
            'trimmed_text': trim_text
            # 'raw_url': entry.get('raw_url', ''),
        }    