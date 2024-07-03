import json
import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html

# Load the JSON file with URLs

with open('urls_test.json', 'r') as file:
    urls = json.load(file)


# Get HTML content from URL
def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML
            tree = html.fromstring(response.content)

            # Get the text content of the <p> element
            p_element = tree.xpath('//p')[0]
            text_content = p_element.text_content()
            return text_content
        else:
            return ''
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ''


def categorize_content(content):
    categories = []
    content = content.lower()

    # category keywords
    keywordCategories = {
        'Web Development': ['web development', 'frontend', 'backend', 'html', 'css', 'javascript'],
        'Fullstack Development': ['fullstack', 'mern', 'mean', 'django', 'ruby', 'ruby on rails', 'lamp', 'lemp'],
        'Software Engineering': ['software engineering', 'software development', 'software design', 'agile methodology'],
        'Data Science': ['data science', 'data analysis', 'data visualization', 'machine learning', 'statistics'],
        'Cybersecurity': ['cybersecurity', 'network security', 'information security', 'penetration testing', 'encryption'],
        'Computer Science': ['computer science', 'algorithms', 'data structures', 'operating systems', 'computer architecture'],
        'Network Engineering': ['network engineering', 'network protocols', 'routing', 'switching', 'network administration'],
        'Database Administration': ['database administration', 'sql', 'database management', 'relational databases', 'nosql'],
        'Artificial Intelligence': ['artificial intelligence', 'machine learning', 'deep learning', 'natural language processing', 'computer vision'],
        'Machine Learning': ['machine learning', 'supervised learning', 'unsupervised learning', 'reinforcement learning', 'neural networks', 'llm'],
        'Data Analytics': ['data analytics', 'business intelligence', 'big data', 'data mining', 'predictive analytics'],
        # 'General Areas': ['programming', 'coding', 'technology', 'development methodologies', 'software tools']
        # 'Multidisciplinary': ['web development' | 'fullstack development', 'software engineering', 'data science', 'cybersecurity', 'computer science', 'network engineering', 'database'],
    }

    for category, tools in keywordCategories.items():
        if any (word in content for word in tools):
            categories.append(category)
            print(category)

    return categories if categories else ('Other')


def tool_content(content):
    techTools = []
    # content = content.lower()

    keywordTools = [
        # Main Programming Languages
        "JavaScript", "Python", "Java", "C++", "C#", "Ruby", "Go", "Swift", "Kotlin", "Rust", 
        # Web Programming Languages 
        "HTML", "CSS", "PHP", "php",
        # Web Development Frameworks 
        "React", "Angular", "Vue.js", "Vue", "Django", "Flask", "Spring Boot", "Express", "Express.js", "ExpressJS", "NodeJS", "Node.js", "Laravel", "Ruby on Rails", "jQuery",
        # Databases 
        "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Microsoft SQL Server", "Oracle", "GraphQL",
        # Mobile Development Languages and Frameworks 
        "React Native", "Flutter", "Xamarin", "NativeScript", "Ionic", "Swift", "Kotlin",
        # Others
        "CI/CD"
    ]

    for tool in keywordTools:
        if tool in content:
            techTools.append(tool)
    
    return techTools if techTools else ('Other')


for item in urls:
    url = item['url']
    content = get_page_content(url)
    item['content'] = content
    # item['category'] = categorize_content(content)
    # item['techStack'] = tool_content(content)


# print(f"{urls}")

with open('urls_test.json', 'w') as file:
    json.dump(urls, file, indent=2)

print("Finished compiling")