import requests
import selectorlib
import time
import sqlite3
import send_email

URL = "https://programmer100.pythonanywhere.com/tours/"

class Event:
    def scrape(self, url):
        response = requests.get(url)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value

class Database:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    def store_data(self, data):
        with open("data.txt", "a") as file:
            file.write(f"{data}\n")

    def read_db(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows

    def store_data_in_db(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()
        print("Successfully stored data")

if __name__ == '__main__':
    email = send_email.Email()

    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted.lower() != "no upcoming tours":
            database = Database("data.db")
            # Store data using local database
            content = database.read_db(extracted)
            if not content:
                database.store_data_in_db(extracted)
                email.send(extracted)

            # Store data using local file
            # with open("data.txt") as data:
            #     if f"{extracted}\n" not in data:
            #         store_data(extracted)
            #         send_email(extracted)
        time.sleep(1)
