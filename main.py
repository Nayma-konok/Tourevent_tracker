import requests
import selectorlib
import smtplib, ssl
import os
from dotenv import load_dotenv 
import time

load_dotenv()

URL= "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    """scrape the page source from the URL"""
    response=requests.get(url, headers= HEADERS)
    source=response.text
    return source

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = os.getenv("SENDER") 
    password = os.getenv("PASSWORD")

    receiver = os.getenv("RECIEVER") 
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent!")

def extract(source):
    extractor=selectorlib.Extractor.from_yaml_file("extract.yaml")
    value=extractor.extract(source)["tours"]
    return value

def read_file():
    """Read data.txt and return list of existing events"""
    try:
        with open("data.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

if __name__=="__main__":
    while True:
        scraped=scrape(URL)
        extracted=extract(scraped)
        print(extracted)

        existing_events = read_file()
        if extracted not in existing_events:
            with open("data.txt", "a") as file:
                file.write(extracted + "\n") 
                send_email(message="New event was found")  
            time.sleep(2)