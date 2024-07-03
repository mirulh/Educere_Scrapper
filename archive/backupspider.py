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

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = pipeline("summarization", model="t5-small")

class TextSpider(scrapy.Spider):
    name = 'textspider'

    # import user agent list and .env file
    user_agent_list = filters.user_agent_list
    load_dotenv()

    def start_requests(self):
        # Get the path to the urls_test.json file
        json_file_path = os.path.join(os.path.dirname(__file__), '..', 'urls.json')
        
        # Read URLs from the JSON file
        with open(json_file_path, 'r') as file:
            urls_data = json.load(file)
        
        # Create requests for each URL in the JSON file
        for entry in urls_data:
            url = entry['url']
            yield scrapy.Request(url=url, callback=self.parse, meta={'entry': entry}, headers={"User": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})

    # import all filters from filters.py
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

    def label_language(self, trim_text, languages, languagesMerged):
        # capitalize method capitalized first word only
        text = trim_text.replace(',', '').lower()
        techStack = []
        result = []
        for language in languages:
            if language in text.split():
                techStack.append(language.capitalize())

        for language, languageItems in languagesMerged.items():
            if any(word in text for word in languageItems):
                techStack.append(language) 

        if len(techStack) < 1:
            techStack.append("Other")

        for x in techStack:
            x_lower = x.lower()
            if (x_lower == 'c++'):
                s = 'cpp'
            elif (x_lower == 'c#'):
                s = 'c-sharp'
            else:
                x_raw = x_lower.split()
                s = "-".join(x_raw)

            result.append({"label": x, "value": s})

        return result
    

    def label_type(self, trim_text, materialsFormat):
        text = trim_text.replace(',', '').lower()
        formatType = []
        result = []

        for format, formatItems in materialsFormat.items():
            if any(word in text for word in formatItems):
                formatType.append(format)

        if len(formatType) < 1:
            formatType.append("Other")

        for x in formatType:
            x_raw = x.lower().split()
            s = "-".join(x_raw)
            result.append({"label": x, "value": s})

        return result
    

    def check_certificate(self, trim_text, isCertificated):
        text = trim_text.replace(',', '').lower()
        for cert in isCertificated:
            if cert in text:
                return True
            else:
                return False
            

    def check_cost(self, trim_text, costIndicator):
        text = trim_text.replace(',','').lower()
        for cost, costItems in costIndicator.items():
            if any(word in text for word in costItems):
                return cost
            
        return "Free/Paid"
    
    def generate_description(trim_text, max_length=100):
        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for text summarization.",
                },
                {
                    "role": "user",
                    "content": f"I need to write a short description of a website from this text that was created from webscraping using Scrapy. Ignore the irrelevant, random words, and the N/A from the text. Focus only on relevant information that describe what the website is about and what it offers. This is the text: {trim_text}"
                },
            ],
        )
        return res["choices"][0]["message"]["content"]



    def summarize_text(self, text, instruction):
        # input_text = f"{instruction}\n\n{text}"
        input_text = text
        summary = summarizer(input_text, max_length=150, min_length=100, do_sample=False)
        return summary[0]['summary_text']
    

    def capitalize_text(self, text):
        result = '. '.join(map(lambda s: s.strip().capitalize(), text.split('.')))
        return result


    def remove_words(self, text, miscellaneous):
        pattern = re.compile('|'.join(re.escape(word) for word in miscellaneous), re.IGNORECASE)
        return pattern.sub('', text)

    def parse(self, response):
        # Extract text from the page (body + title + description)
        body = response.xpath('//body//text()[not(ancestor::script) and not(ancestor::style) and not (ancestor::footer) and not(ancestor::nav) and not(ancestor::head)]').getall()
        title = response.xpath('//title/text()').get()
        description = response.xpath('//meta[@name="description"]/@content').get()

        # remove leading and trailing whitespace and join
        page_text = ' '.join(body).strip()
        # spit into array and join
        clean_text = ' '.join(page_text.split())  
        filter_text = self.remove_words(clean_text, self.miscellaneous)
        get_text = ' '.join(filter_text.split())

        # Get additional metadata from the JSON entry``
        entry = response.meta['entry']

        # combine title, description, and body texts

        if title:
            getTitle = title.strip()
        else:
            getTitle = "N/A"

        if description:
            getDescription = description.strip()
        else:
            getDescription = "N/A"

        if len(get_text) == 0:
            get_text = "N/A"

        whole_text = f"TITLE: {getTitle} || DESCRIPTION: {getDescription} || BODY: {get_text}" 

        
        # Trim filter_text to be below the word limit
        word_limit = 200
        words = whole_text.split()
        if len(words) > word_limit:
            trim_text = ' '.join(words[:word_limit])
        else:
            trim_text = whole_text


        name = entry.get('name', '')

        slug = self.generate_slug(name)

        image = self.generate_placeholder(name)

        # Categorized and label from the original text
        categories = self.label_subject(trim_text, self.subjects, self.subjectsMerged, self.subjectsSingled)

        techStack = self.label_language(trim_text, self.languages, self.languagesMerged)

        materialType = self.label_type(trim_text, self.materialsFormat)

        certificate = self.check_certificate(trim_text, self.isCertificated)
        
        cost = self.check_cost(trim_text, self.costIndicator)

        # trim the text for LLM
        # description_limit = 200
        # text_words = whole_text.split()
        # if len(text_words) > description_limit:
        #     trim_text = ' '.join(words[:description_limit])
        # else:
        #     trim_text = whole_text
            

        # description = self.generate_description(trim_text)
        raw_description = self.summarize_text(trim_text, self.instruction)

        description = self.capitalize_text(raw_description)
   
        # Yield the data
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
            'url': response.url,
            'letterLength': len(description),
            'wordLength': len(description.split()),
            # "length": len(trim_text.split()),
            'trimmed_text': trim_text
            # 'raw_url': entry.get('raw_url', ''),
        }
