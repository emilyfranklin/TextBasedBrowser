import sys
import os
from os import path
import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

args = sys.argv
dir_name = args[1]
stack = []

if not path.exists(dir_name):
    os.makedirs(dir_name)


def is_valid(url):
    return "." in url


def save_to_file(text, file_name):
    file = open(dir_name + "/" + file_name, "w")
    file.write(text)
    file.close()


def file_exists(file):
    return path.exists(dir_name + "/" + file)


def make_file_name(url):
    i = url.find(".")
    if i != -1:
        url = url[0:i]
    if "https://" in url:
        url = url[8:]
    return url


def make_full_url(url):
    if "https://" not in url:
        return "https://" + url
    else:
        return url


def parse_html(text):
    text = BeautifulSoup(text, 'html.parser')
    parsed_text = ""
    for tag in text.find_all('p'):
        parsed_text += (tag.get_text() + "\n")
    return parsed_text


while True:
    url = input("Enter a URL, type 'back' to go back, or type 'exit' to quit: ")
    file_name = make_file_name(url)
    full_url = make_full_url(url)
    if url == "back":
        if len(stack) > 0:
            print(stack.pop(-2))
    elif url == "exit":
        break
    elif file_exists(file_name):
        file = open(dir_name + "/" + file_name, "r")
        contents = file.read()
        print(contents)
        stack.append(contents)
        file.close()
    elif is_valid(url):
        r = requests.get(full_url)
        parsed = parse_html(r.text)
        vader = SentimentIntensityAnalyzer()
        sentiment = vader.polarity_scores(parsed)['compound']
        if sentiment >= 0:
            print("The following has a compound sentiment score of " + str(sentiment) + "!")
            save_to_file(parsed, file_name)
            stack.append(parsed)
            print(parsed)
        else:
            print("To preserve your happiness, we've decided not to display the results.")
    else:
        print("Error: Invalid URL")

