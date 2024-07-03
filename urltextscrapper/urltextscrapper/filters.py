user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A5341f Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36"
    ]



miscellaneous = [

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
    'UI Design': ['ui','ux/ui', 'ui/ux', 'wireframing', 'wireframe', 'mockup', 'prototype', 'material design'],
    'UX Design': ['ux','ux/ui', 'ui/ux']
}

languages = [
    # programming languages
    'javascript', 'python', 'java', 'c++', 'cpp', 'c#', 'ruby', 'php', 'swift', 'go', 'typescript', 
    'kotlin', 'rust', 'r', 'scala', 'objective-c', 'perl', 'haskell', 'elixir', 'dart', 'lua', 
    'matlab', 'groovy', 'visual basic', 'assembly', 'sql', 'sass', 'mongodb', 'rest api', 'graphql',
    
    # frameworks
    "flutter", 'django', 'flask', 'spring', 'laravel', 'rails', 'asp.net', 'symfony', 'phoenix', 'ember', 'svelte', 'gatsby', 'meteor', 'aurelia', 'pyramid', 'bottle', 'tornado', 'fastapi', 'nestjs', 'redux', 'mobx', 'apollo', 'relay', 'vuex', 'tailwind', 'bootstrap', 'foundation', 'semantic ui', 'bulma', 'materialize', 'material-ui', 'chakra ui', 'quasar', 'primefaces', 'ant design', 'element ui'
]

languagesMerged = {
        'React.js' : ['react', 'react.js', 'reactjs'],
        'Vue.js' : ['vue', 'vue.js', 'vuejs'],
        'Next.js' : ['nextjs', 'next.js'],
        'Angular.js': ['angualr', 'angular.js'],
        'Express.js': ['express','expressjs', 'express.js'],
        'Node.js': ['node', 'nodejs', 'node.js'],
        'Nuxt.js': ['nuxt', 'nuxtjs', 'nuxt.js'],
        'Backbone.js': ['backbone', 'backbonejs','backbone.js'],
        'Less.js': ['lessjs', 'less.js'],
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
        "Bootcamps": ['bootcamp', 'bootcamps'],
        "Coding Game": ['game', 'play', 'games']
    }

isCertificated = [
        'certificate', 'certificates', 'certificated', 'certification', 'certifications', 'certified', 'degree', 'degrees'
    ]

costIndicator = {
        'Paid': ['paid', 'payment', 'pay', 'subscription', 'subscriptions'],
        'Free' : ['free'],
    }