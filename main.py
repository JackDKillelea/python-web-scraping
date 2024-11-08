import requests
import selectorlib
from send_email import email

URL = "https://programmer100.pythonanywhere.com/tours/"

def scrape(url):
    response = requests.get(url)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_email(extracted):
    email(extracted, "utf-8")

def store_data(data):
    with open("data.txt", "a") as file:
        file.write(f"{data}\n")

if __name__ == '__main__':
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    if extracted.lower() != "no upcoming tours":
        with open("data.txt") as data:
            if f"{extracted}\n" not in data:
                store_data(extracted)
                send_email(extracted)
