import scrapy
import json
import os
import re
import random
from openai import OpenAI
import os
from dotenv import load_dotenv
from transformers import pipeline
import urltextscrapper.filters as filters
import urltextscrapper.functions as functions


from openai import OpenAI
client = OpenAI()

# summarizer tool
summarizer = pipeline("summarization", model="t5-small")

class TextSpider(scrapy.Spider):
    name = 'textspider'

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

    instruction = "This is a text of a website generated using scrapy.Please summarize the following text into a concise, readable paragraph, highlighting what the website is about, what it does, and what it offers. Ignore the incoherent sentences,any person names, any 'review-like' sentences, any incomplete sentences, and N/A. If there is not enough information about the website then return 'Need more details' instead"

# FUNCTIONS ---------------------------------------------------


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
        filter_text = functions.remove_words(clean_text, self.miscellaneous)
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
        url = response.url
        name = entry.get('name', '')
        slug = functions.generate_slug(name)
        image = functions.generate_placeholder(name)
        categories = functions.label_subject(trim_text, self.subjects, self.subjectsMerged, self.subjectsSingled)
        techStack = functions.label_language(trim_text, self.languages, self.languagesMerged)
        materialType = functions.label_type(trim_text, self.materialsFormat)
        cost = functions.check_cost(trim_text, self.costIndicator)
        certificate = functions.check_certificate(trim_text, self.isCertificated)
        descriptionOAI = functions.summarize_text_OpenAI(trim_text)
        descriptionT5 = functions.summarize_text_T5(trim_text, self.instruction)

        # description = self.generate_description(trim_text)
        # raw_description = self.summarize_text(trim_text, self.instruction)
        # description = self.capitalize_text(raw_description)
        # openAIDescription = self.summarize_text(trim_text)
        # summary = self.summarize_text(incoherent_text
   
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
            'url': url,
            'original_text': trim_text,
            'wordLength1': len(trim_text.split()),
            'description_T5': descriptionT5,
            'wordLength2': len(descriptionT5.split()),
            'description' : descriptionOAI,
            'wordLength3': len(descriptionOAI.split()),

            # "openAI_generated": summary
            # # 'raw_url': entry.get('raw_url', ''),
            # 'raw_description': raw_description
        }    
