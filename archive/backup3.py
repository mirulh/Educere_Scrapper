import scrapy
import json
import os
import re
import random

class TextSpider(scrapy.Spider):
    name = 'textspider'

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A5341f Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36"
    ]

    def start_requests(self):
        # Get the path to the urls_test.json file
        json_file_path = os.path.join(os.path.dirname(__file__), '..', 'coding_practices_urls.json')
        
        # Read URLs from the JSON file
        with open(json_file_path, 'r') as file:
            urls_data = json.load(file)
        
        # Create requests for each URL in the JSON file
        for entry in urls_data:
            url = entry['url']
            yield scrapy.Request(url=url, callback=self.parse, meta={'entry': entry}, headers={"User": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})


            
    filters = [

        # social media platform
        "twitter", "facebook", "instagram", "linkedin", "snapchat",
        "tiktok", "youtube", "pinterest", "reddit", "whatsapp",
        "wechat", "tumblr", "flickr", "discord", "telegram",
        "viber", "line", "wechat", "qq", "quora",
        "vine", "periscope", "clubhouse", "twitch", "myspace",

        # other irrelevant terms
        "|" ,"advertisement", "sponsored", "click here", "read more", "terms of service", "privacy policy", "cookie policy", "subscribe", "sign up", "log in", "login", "join", "contact us", 'contact',  "about us", "careers", "site map", "footer", "navbar", "©", "all rights reserved", "follow us", "share this", "previous", "next", "related articles", "comments", "disclaimer", "back to top", "search", "menu", "trending", "most popular", "FAQ", "help", "support", "customer service", "newsletter", "feedback", "social media", "home", "blog", "latest news", "contact information", "download", "watch now", "buy now", "sale", "discount", "promo", "terms and conditions", "return policy", "shipping information", "affiliate link", "posted on", "updated on", "follow us on", "like us on", "join our mailing list", "subscribe to our newsletter", "leave a comment", "view all", "learn more", "read full story", "get started", "find out more", "apply now", "enter your email", "submit", "more details", "see more", "view gallery", "shop now", "play video", "join now", "explore", "try for free", "terms of use", "icon", "logo", 'sidebar', "button", "sign in", "about us", "about about", "light mode", "dark mode", "privacy notice", "slavery", "copyright", "email to", "emailing", "not found", "skip to content", "skip to main content"
    ]

    subjects = [
        "artificial intelligence", "machine learning", "deep learning", "natural language processing", "computer vision", "robotics", "data science", "big data", "data mining", "data analysis", "data engineering", "databases", "sql", "nosql", "cloud computing", "distributed systems", "network security", "cybersecurity", "cryptography", "information security", "software engineering", "software development", "software testing", "devops", "agile methodologies", "web development", "mobile development", "ios development", "android development", "systems programming", "operating systems", "computer architecture", "embedded systems", "internet of things", "networks", "wireless networks", "blockchain", "quantum computing", "parallel computing", "high-performance computing", "human-computer interaction", "user interface design", "user experience", "augmented reality", "virtual reality", "game development", "computer graphics", "digital signal processing", "algorithm design", "data structures", "theoretical computer science", "computational theory", "automata theory", "formal languages", "discrete mathematics", "linear algebra", "numerical methods", "scientific computing", "bioinformatics", "health informatics", "geographic information systems", "it management", "it governance", "enterprise architecture", "project management", "business analysis", "e-commerce", "it strategy", "it service management", "it support", "technical support", "help desk", "network administration", "system administration", "it infrastructure", "virtualization", "storage management", "cloud services", "saas", "paas", "iaas", "network protocols", "tcp/ip", "ftp", "dns", "email protocols", "ldap", "vpn", "firewall management", "intrusion detection systems", "penetration testing", "digital forensics", "compliance", "regulatory requirements", "it auditing", "business continuity planning", "disaster recovery", "itil", "cobit", "togaf", "scrum", "kanban", "lean it", "six sigma", "it training", "technical writing", "documentation"
    ]

    subjectsMerged = {
        'FullStack Development': ['fullstack', 'full stack', 'fullstack', 'full stack development'],
        'Frontend Development': ['frontend', 'frontend development'],
        'Backend Development': ['backend', 'backend development'],
        'Software Development': ['software', 'software development']
    }

    subjectsSingled = {
        'UI Design': ['ui'],
        'UX Design': ['ux']
    }


    languages = [
        # programming languages
        'javascript', 'python', 'java', 'c++', 'cpp', 'c#', 'ruby', 'php', 'swift', 'go', 'typescript', 
        'kotlin', 'rust', 'r', 'scala', 'objective-c', 'perl', 'haskell', 'elixir', 'dart', 'lua', 
        'matlab', 'groovy', 'visual basic', 'assembly', 'sql', 'sass', 'less', 'mongodb', 'rest api', 'graphql',
        
        # frameworks
        "flutter", 'django', 'flask', 'spring', 'laravel', 'rails', 'asp.net', 'symfony', 'phoenix', 'ember', 'backbone', 'svelte', 'gatsby', 'meteor', 'aurelia', 'pyramid', 'bottle', 'tornado', 'fastapi', 'nestjs', 'redux', 'mobx', 'apollo', 'relay', 'vuex', 'tailwind', 'bootstrap', 'foundation', 'semantic ui', 'bulma', 'materialize', 'material-ui', 'chakra ui', 'quasar', 'primefaces', 'ant design', 'element ui'
    ]

    languagesMerged = {
        'React.js' : ['react', 'react.js', 'reactjs'],
        'Vue.js' : ['vue', 'vue.js', 'vuejs'],
        'Next.js' : ['nextjs', 'next.js'],
        'Angular.js': ['angualr', 'angular.js'],
        'Express.js': ['express','expressjs', 'express.js'],
        'Node.js': ['node', 'nodejs', 'node.js'],
        'Nuxt.js': ['nuxt', 'nuxtjs', 'nuxt.js'],
        'HTML/CSS': ['html', 'css', 'html/css', 'css/html']
    }

    materialsFormat = {
        "Video Courses": ['video', 'videos', 'lectures', 'lecture'],
        "Text-Based": ['book', 'books', 'article', 'articles'],
        "Hands-On Practice": ['hands on', 'hands-on', 'project', 'projects'],
        "Project-Based": ['project', 'projects'],
        "MOOC": ['mooc', 'online course', 'online courses', 'online-course', 'online-courses'],
        "Interactive Content": ['interactive', 'interactivity', 'quiz', 'quizzes'],
        "Coding Practice": ['coding', 'problem solving', 'problem-solving', 'coding challenges', 'coding challenge', 'exercise', 'exercises', 'coding exercises', 'coding exercise'],
        "Bootcamps": ['bootcamp', 'bootcamps']
    }

    isCertificated = [
        'certificate', 'certificates', 'certificated', 'certification', 'certifications', 'certified', 'degree', 'degrees'
    ]

    costIndicator = {
        'Paid': ['paid', 'payment', 'pay', 'subscription', 'subscriptions'],
        'Free' : ['free'],
    }

    def label_subject(self, trim_text, subjects, subjectsMerged, subjectsSingled):
        # remove comma
        # title method capitalized every word
        text = trim_text.replace(',', '').lower()
        categories = []
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

        return categories

    def label_language(self, trim_text, languages, languagesMerged):
        # capitalize method capitalized first word only
        text = trim_text.replace(',', '').lower()
        techStack = []
        for language in languages:
            if language in text.split():
                techStack.append(language.capitalize())

        for language, languageItems in languagesMerged.items():
            if any(word in text for word in languageItems):
                techStack.append(language) 

        if len(techStack) < 1:
            techStack.append("Other")

        return techStack
    

    def label_type(self, trim_text, materialsFormat):
        text = trim_text.replace(',', '').lower()
        formatType = []

        for format, formatItems in materialsFormat.items():
            if any(word in text for word in formatItems):
                formatType.append(format)

        if len(formatType) < 1:
            formatType.append("Other")

        return formatType
    
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
    
 
    def remove_words(self, text, filters):
        pattern = re.compile('|'.join(re.escape(word) for word in filters), re.IGNORECASE)
        return pattern.sub('', text)

    def parse(self, response):
        # Extract text from the page
        text = response.xpath('//body//text()[not(ancestor::script) and not(ancestor::style) and not (ancestor::footer) and not(ancestor::nav) and not(ancestor::head)]').getall()

        title = response.xpath('//title/text()').get()

        description = response.xpath('//meta[@name="description"]/@content').get()

        # remove leading and trailing whitespace and join
        page_text = ' '.join(text).strip()
        # spit into array and join
        clean_text = ' '.join(page_text.split())  
        filter_text = self.remove_words(clean_text, self.filters)
        get_text = ' '.join(filter_text.split())

        # Get additional metadata from the JSON entry
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
        word_limit = 450
        words = whole_text.split()
        if len(words) > word_limit:
            trim_text = ' '.join(words[:word_limit])
        else:
            trim_text = whole_text

        # Categorized and label from the original text
        categories = self.label_subject(trim_text, self.subjects, self.subjectsMerged, self.subjectsSingled)

        techStack = self.label_language(trim_text, self.languages, self.languagesMerged)

        certificate = self.check_certificate(trim_text, self.isCertificated)
        
        cost = self.check_cost(trim_text, self.costIndicator)

        materialType = self.label_type(trim_text, self.materialsFormat)

        # trim the text for LLM
        description_limit = 200
        text_words = whole_text.split()
        if len(text_words) > description_limit:
            trim_text = ' '.join(words[:description_limit])
        else:
            trim_text = whole_text
            
        # Yield the data
        yield {
            'url': response.url,
            'name': entry.get('name', ''),
            'raw_url': entry.get('raw_url', ''),
            "length": len(trim_text.split()),
            'category': categories,
            'techStack': techStack,
            'type': materialType,
            'hasCert': certificate,
            'cost' : cost,
            'trimmed_text': trim_text
        }
