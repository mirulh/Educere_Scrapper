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
            
    filters = [

        # social media platform
        "twitter", "facebook", "instagram", "linkedin", "snapchat",
        "tiktok", "youtube", "pinterest", "reddit", "whatsapp",
        "wechat", "tumblr", "flickr", "discord", "telegram",
        "viber", "line", "wechat", "qq", "quora",
        "vine", "periscope", "clubhouse", "twitch", "myspace",

        # other irrelevant terms
        "|" ,"advertisement", "sponsored", "click here", "read more", "terms of service", "privacy policy", "cookie policy", "subscribe", "sign up", "log in", "contact us", 'contact',  "about us", "careers", "site map", "footer", "navbar", "©", "all rights reserved", "follow us", "share this", "previous", "next", "related articles", "comments", "disclaimer", "back to top", "search", "menu", "trending", "most popular", "FAQ", "help", "support", "customer service", "newsletter", "feedback", "social media", "home", "blog", "latest news", "contact information", "download", "watch now", "buy now", "sale", "discount", "promo", "terms and conditions", "return policy", "shipping information", "affiliate link", "posted on", "updated on", "follow us on", "like us on", "join our mailing list", "subscribe to our newsletter", "leave a comment", "view all", "learn more", "read full story", "get started", "find out more", "apply now", "enter your email", "submit", "more details", "see more", "view gallery", "shop now", "play video", "join now", "explore",
        "try for free", "terms of use", "icon", "logo", 'sidebar', "button", "sign in", "about us", "about about", "light mode", "dark mode", "privacy notice", "slavery", "copyright", "email to", "emailing"

    ]

    subjects = [
        "artificial intelligence", "machine learning", "deep learning", "natural language processing", "computer vision", "robotics", "data science", "big data", "data mining", "data analysis", "data engineering", "databases", "sql", "nosql", "cloud computing", "distributed systems", "network security", "cybersecurity", "cryptography", "information security", "software engineering", "software development", "software testing", "devops", "agile methodologies", "web development", "mobile development", "ios development", "android development", "systems programming", "operating systems", "computer architecture", "embedded systems", "internet of things", "networks", "wireless networks", "blockchain", "quantum computing", "parallel computing", "high-performance computing", "human-computer interaction", "user interface design", "user experience", "augmented reality", "virtual reality", "game development", "computer graphics", "digital signal processing", "algorithm design", "data structures", "theoretical computer science", "computational theory", "automata theory", "formal languages", "discrete mathematics", "linear algebra", "numerical methods", "scientific computing", "bioinformatics", "health informatics", "geographic information systems", "it management", "it governance", "enterprise architecture", "project management", "business analysis", "e-commerce", "it strategy", "it service management", "it support", "technical support", "help desk", "network administration", "system administration", "it infrastructure", "virtualization", "storage management", "cloud services", "saas", "paas", "iaas", "network protocols", "tcp/ip", "http/https", "ftp", "dns", "email protocols", "ldap", "vpn", "firewall management", "intrusion detection systems", "penetration testing", "digital forensics", "compliance", "regulatory requirements", "it auditing", "business continuity planning", "disaster recovery", "itil", "cobit", "togaf", "scrum", "kanban", "lean it", "six sigma", "it training", "technical writing", "documentation", 'UI design'
    ]

    subFilters = {
        'FullStack Development': ['fullstack', 'full stack', 'fullstack', 'full stack development'],
        'Frontend Development': ['frontend', 'frontend development'],
        'Backend Development': ['backend', 'backend development'],
    }


    languages = [
        # programming languages
        'javascript', 'python', 'java', 'c++', 'cpp', 'c#', 'ruby', 'php', 'swift', 'go', 'typescript', 
        'kotlin', 'rust', 'r', 'scala', 'objective-c', 'perl', 'haskell', 'elixir', 'dart', 'lua', 
        'matlab', 'groovy', 'visual basic', 'assembly', 'sql', 'sass', 'less', 'mongodb', 'rest api', 'graphql',
        
        # frameworks
        'django', 'flask', 'spring', 'laravel', 'rails', 'asp.net', 'symfony', 'phoenix', 'ember', 'backbone', 'svelte', 'gatsby', 'meteor', 'aurelia', 'pyramid', 'bottle', 'tornado', 'fastapi', 'nestjs', 'redux', 'mobx', 'apollo', 'relay', 'vuex', 'tailwind', 'bootstrap', 'foundation', 'semantic ui', 'bulma', 'materialize', 'material-ui', 'chakra ui', 'quasar', 'primefaces', 'ant design', 'element ui'
    ]

    langFilters = {
        'React.js' : ['react', 'react.js', 'reactjs'],
        'Vue.js' : ['vue', 'vue.js', 'vuejs'],
        'Next.js' : ['nextjs', 'next.js'],
        'Angular.js': ['angualr', 'angular.js'],
        'Express.js': ['express','expressjs', 'express.js'],
        'Node.js': ['node', 'nodejs', 'node.js'],
        'Nuxt.js': ['nuxt', 'nuxtjs', 'nuxt.js'],
        'HTML/CSS': ['html', 'css', 'html/css', 'css/html']
    }

    def label_subject(self, text, subjects, subFilters):
        # remove comma
        text = text.replace(',', '')
        categories = []
        for subject in subjects:
            if subject in text.lower():
                categories.append(subject.title())

        for subject, words in subFilters.items():
            if any(word in text.lower() for word in words):
                categories.append(subject) 

        return categories

    def label_language(self, text, languages, langFilters):
        text = text.replace(',', '')
        techStack = []
        for language in languages:
            if language in text.lower().split():
                techStack.append(language.capitalize())

        for language, words in langFilters.items():
            if any(word in text.lower() for word in words):
                techStack.append(language) 

        return techStack
 
    def remove_words(self, text, filters):
        pattern = re.compile('|'.join(re.escape(word) for word in filters), re.IGNORECASE)
        return pattern.sub('', text)

    def parse(self, response):
        # Extract text from the page
        text = response.xpath('//title/text() | //meta[@name="description"]/@content | //body//text()[not(ancestor::script) and not(ancestor::style) and not (ancestor::footer) and not(ancestor::nav) and not(ancestor::head)]').getall()

        # remove leading and trailing whitespace and join
        page_text = ' '.join(text).strip()
        # spit into array and join
        clean_text = ' '.join(page_text.split())  
        filter_text = self.remove_words(clean_text, self.filters)
        filter_text = ' '.join(filter_text.split())

        # Get additional metadata from the JSON entry
        entry = response.meta['entry']
        
        # Trim filter_text to be below the word limit
        word_limit = 450
        words = filter_text.split()
        if len(words) > word_limit:
            trim_text = ' '.join(words[:word_limit])
        else:
            trim_text = filter_text   

        # Categorized and label
        categories = self.label_subject(trim_text, self.subjects, self.subFilters)
        techStack = self.label_language(trim_text, self.languages, self.langFilters)

        # Yield the data
        yield {
            'url': response.url,
            'name': entry.get('name', ''),
            'raw_url': entry.get('raw_url', ''),
            "length": len(trim_text.split()),
            'category': categories,
            'techStack': techStack,
            'trimmed_text': trim_text
        }


""" 
    def parse(self, response):
        # Extract text from the page
        text = response.xpath('//body//text()[not(ancestor::script) and not(ancestor::style) and not (ancestor::footer) and not(ancestor::nav) and not(ancestor::head)]').getall()

                title = response.xpath('//title/text()').get()
        description = response.xpath('//meta[@name="description"]/@content').get()
        body = response.xpath('//body//text()[not(ancestor::script) and not(ancestor::style) and not (ancestor::footer) and not(ancestor::nav) and not(ancestor::head)]').getall()

        mainHeader = ""

        if title or description:
            mainHeader = f" TITLE: {title}. \\nDESCRIPTION: {description}."

 """