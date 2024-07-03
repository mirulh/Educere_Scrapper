### Educere Srapper

The two main functionalities of Educere Scrapper is for web scraping URLs for texts and conduct data labeling and text summarization using OpenAI API on the texts

Tools: Scrapy, OpenAI API, Transformer T5

## Webscraping Texts

## 1. Problem Statement

- How to structure the data with this information in a JSON format?

![Alt text](pics/ProblemStatement.png)

## 2. Methodologies

- We employed two strategies to get the output desired

  ![Alt text](pics/Methods.png)

## 3. Webscraping texts

![Alt text](pics/Step1.png)

## 4. Data labeling

- Label the url with data that describes its contents (subjects, types, technologies, cost, and certificate)

![Alt text](pics/Step2.png)

## 5. Text Summarization

- Creating a readable description from the raw text using T5 LLM and OpenAI API
- In this picture we compare the quality of the description produce between T5 and OpenAI text summarization. We can conclude that OpenAI produce more accurate output description than T5

![Alt text](pics/Step3.png)

## 6. Displaying the final output

![Alt text](pics/FinalOutput.png)

## 7. Apply the same step to the rest of URLs

![Alt text](pics/FinalStep.png)
