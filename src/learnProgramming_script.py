import praw
import re
import json
from urllib.parse import urlparse

# Replace with your own credentials
CLIENT_ID = 'qAm-iWW7J81dDoUlZWha8w'
CLIENT_SECRET = '9pKs6GitwyB935Hu7y2GxQZtxyngvQ'
USER_AGENT = 'a url scrapper for Educere'

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

setLimit = 130
posts = reddit.subreddit('learnprogramming').top(time_filter='all', limit=setLimit)

urls = []

# Exclude URLs from certain domains
def exclude_urls(url):
    excluded_domains = ['youtube.com', 'reddit.com', 'github.com', 'notion.so', 'amazon.com', 'amzn', 'medium.com', 'twitter.com', 'instagram.com', 'zdnet.com', "discord"]
    for domain in excluded_domains:
        if domain in url:
            return True
    return False

# Remove parenthesis and other irrelevant characters from url
def clean_url(url):
    cleaned_url = url.split(")")[0]
    return cleaned_url

def extract_domain(url):
    # Remove protocol
    if "://" in url:
        url = url.split("://")[1]
    # Remove www if present
    if url.startswith("www."):
        url = url[4:]
    # Extract domain name
    domain = url.split("/")[0]
    # Remove any subdomains and extensions
    parts = domain.split('.')
    if len(parts) > 2:
        domain = parts[-2]  # Extract the second-level domain
    else:
        domain = parts[0]  # If no subdomains, take the first part
    # Capitalize first letter of domain
    domain = domain.capitalize()

    return domain

# Function to extract domain name from URL
def extract_sdl(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.scheme + "://" + parsed_url.netloc
        return domain
    except ValueError:
        # Ignore the error and proceed with the next URL
        return None


for post in posts:
    # Extract URLs from post body
    post_urls = re.findall(r'(https?://[^\s]+)', post.selftext)
    for url in post_urls:
        if not exclude_urls(url):

            cleanUrl = clean_url(url)
            # Extract domain and sdl
            domain = extract_domain(cleanUrl)
            sdl = extract_sdl(cleanUrl)
            
            # Check if the domain is already present in urls
            if not any(u['name'] == domain for u in urls):
                # If not present, append it to urls
                urls.append({
                    # "post_title": post.title,
                    "raw_url": cleanUrl,
                    "name": domain,
                    "url": sdl
                })

# Save to JSON
with open('learnProgramming_urls.json', 'w') as f:
    json.dump(urls, f, indent=4)


with open('learnProgramming_urls.json', 'r') as f:
    data = json.load(f)

length = len(data)

print("Limit of the posts:", setLimit)
print("Number of URLs:", length)


keywordsTool = [
# Lowercase
# Programming Languages
"Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin", "Go", "Rust", "TypeScript", "Perl", "Scala", "Haskell", "Objective-C", "Lua", "HTML/CSS", "SQL", "Shell Scripting", "Assembly", "CSS", "HTML", 
# Frameworks 
"Django", "Spring", "React", "Angular", "Vue.js", "Ruby on Rails", "Laravel", "Express.js", "Express", "ExpressJS", "Flask", "Node.js", "NodeJS", ".NET", "TensorFlow", "PyTorch", "Bootstrap", "jQuery", "Symfony", "ASP.NET", "CakePHP", "CodeIgniter", "Ember.js", "Meteor", "Sails.js", "Struts", "Play", "Hibernate", "Flask", "Dropwizard", "Quarkus", "Spring Boot", "Vue.js", "Next.js", "NestJS", "FastAPI", "Jupyter", "Unity", "Unreal Engine", "Xamarin", "Electron", "Flutter", "NativeScript", "Ionic", "React Native", "Cordova", "PhoneGap", "Adobe AIR", "Qt", "Tkinter", "PyQt", "wxPython", "Jinja2", "Smarty", "Blade", "Thymeleaf", "JSF", "Gatsby", "Nuxt.js", "Svelte", "Quasar", "Tailwind CSS", "Bulma", "Foundation", "Materialize", "Semantic UI", "Ant Design", "Chakra UI", "UIKit", "Flutter UI", "Jetpack Compose", "Android SDK", "iOS SDK", "Unity UI", "Unreal UI"
# Add more as needed
]