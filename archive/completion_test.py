
import openai
import os
from openai import OpenAI
import tiktoken

# openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

# summary = client.models.list()
# encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

text = "TITLE: Learn X in Y Minutes: Scenic Programming Language Tours || DESCRIPTION: N/A || BODY: Learn X in Y minutes Highlight your language: en-us ar-ar be-by bg-bg ca-es cs-cz de-de el-gr es-es fa-ir fi-fi fr-fr he-he hi-in hu-hu id-id it-it ja-jp ko-kr lt-lt ms-my nl-nl no-nb pl-pl pt-br pt-pt ro-ro ru-ru sk-sk sl-si sv-se ta-in th-th tr-tr uk-ua vi-vn zh-cn zh-tw Select theme: light dark Take a whirlwind tour of your favorite language. Community-driven! Languages Translations Ada APL arturo asciidoc ca-es de-de es-es id-id it-it ja-jp pt-br sl-si zh-cn AssemblyScript ATS Ballerina bc de-de pt-br zh-cn bf cs-cz de-de es-es fa-ir fr-fr id-id it-it ko-kr nl-nl pl-pl pt-br pt-pt ro-ro ru-ru sv-se tr-tr zh-cn BQN C de-de es-es fr-fr pt-br ru-ru tr-tr uk-ua zh-cn C# de-de es-es fr-fr pt-br tr-tr zh-cn C++ de-de es-es fr-fr hi-in it-it pt-br ru-ru tr-tr zh-cn chapel es-es CHICKEN clojure de-de es-es fr-fr ko-kr ms-my pt-br pt-br ro-ro ru-ru tr-tr zh-cn clojure macros de-de ko-kr ms-my zh-cn COBOL zh-cn coffeescript de-de es-es fr-fr hu-hu id-id it-it ko-kr ms-my nl-nl pt-br ro-ro ru-ru sk-sk zh-cn coldfusion es-es Common Lisp es-es ko-kr ms-my pt-br ru-ru zh-cn Coq crystal de-de fr-fr ru-ru zh-cn css cs-cz de-de el-gr es-es"


def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    list = encoding.encode(string)
    wordLength = len(string.split())
    return(f"Token count:{num_tokens}\nToken list : {list}\nWord Length: {wordLength}")


def summarize_text(text):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Summarize this text into a readable description. If the text has not enough information, then return 'Description not available.\nText:\n\n{text}\n\n",
        max_tokens=150,
        temperature=0
    )
    summary = response.choices[0].text.strip()
    return summary
    # print(f"Summary: {summary}")
    # num_tokens_from_string(summary, "gpt-3.5-turbo")


# summary = response.choices[0].text.strip()
summary = summarize_text(text)
count = num_tokens_from_string(summary, "gpt-3.5-turbo")
print(f"Summary: \n\n{summary} \n\nCount: {count}")
