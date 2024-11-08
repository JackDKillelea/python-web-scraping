import requests
import selectorlib
import time
import sqlite3
from send_email import email

URL = "https://programmer100.pythonanywhere.com/tours/"
connection = sqlite3.connect("data.db")

def scrape(url):
    response = requests.get(url)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def store_data(data):
    with open("data.txt", "a") as file:
        file.write(f"{data}\n")

def read_db(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows

def store_data_in_db(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()
    print("Successfully stored data")

if __name__ == '__main__':
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted.lower() != "no upcoming tours":
            # Store data using local database
            content = read_db(extracted)
            if not content:
                store_data_in_db(extracted)
                email(extracted, "utf-8")

            # Store data using local file
            # with open("data.txt") as data:
            #     if f"{extracted}\n" not in data:
            #         store_data(extracted)
            #         send_email(extracted)
        time.sleep(1)