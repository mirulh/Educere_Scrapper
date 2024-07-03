import uuid
import re
from openai import OpenAI
import openai
import tiktoken
from transformers import pipeline


# Set your OpenAI API key here
api_key = ""

# Initialize OpenAI client with your API key
client = openai.OpenAI(api_key=api_key)

# print(f"WHERE is THIS {client}")

# FUNCTIONS TOOLS ---------------------------------------------------
def remove_words(text, miscellaneous):
    pattern = re.compile('|'.join(re.escape(word) for word in miscellaneous), re.IGNORECASE)
    return pattern.sub('', text)

# FUNCTIONS URLS ---------------------------------------------------

# SLUG
def generate_slug(name):
        unique_string = f"{name.lower()}-{uuid.uuid1().hex}"
        return unique_string

# IMAGE
def generate_placeholder(name):
    letter = name[0].upper()
    image = f"/images/letters_placeholder/default_{letter}.png"
    return image

# CATEGORIES/SUBJECTS
def label_subject(trim_text, subjects, subjectsMerged, subjectsSingled):
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

# LANGUAGES/TECH STACK
def label_language(trim_text, languages, languagesMerged):
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
    
# TYPE
def label_type(trim_text, materialsFormat):
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
    
# COST
def check_cost(trim_text, costIndicator):
    text = trim_text.replace(',','').lower()
    for cost, costItems in costIndicator.items():
        if any(word in text for word in costItems):
            return cost
        
    return "Free/Paid"

# CERTIFICATE
def check_certificate(trim_text, isCertificated):
    text = trim_text.replace(',', '').lower()
    for cert in isCertificated:
        if cert in text:
            return True
        else:
            return False


# DESCRIPTION OPENAI


def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    list = encoding.encode(string)
    wordLength = len(string.split())
    return(f"Token count:{num_tokens}\nToken list : {list}\nWord Length: {wordLength}")


def summarize_text_OpenAI(text):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Summarize the web-scraped text into a readable description. If the text does not contain enough information, return 'Description not available.\nText:\n\n{text}\n\n",
        max_tokens=150,
        temperature=0
    )
    summary = response.choices[0].text.strip()
    return summary

# DESCRIPTION TRANSFORMER 5 / T-5
summarizer = pipeline("summarization", model="t5-small")

def summarize_text_T5(text, instruction):
    # input_text = f"{instruction}\n\n{text}"
    input_text = text
    summary = summarizer(input_text, max_length=150, min_length=100, do_sample=False)
    return summary[0]['summary_text']


""" 

        prompt=f"Summarize this text into a readable description. If the text has not enough information, then return 'Description not available.\nText:\n\n{text}\n\n",
 """