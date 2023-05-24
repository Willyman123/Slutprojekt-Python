""" This program scrapes the website fnbr.co/shop and 
prints out the name and price of the items in the shop
Author: Victor Lora
Date: 2020-10-15
"""
from bs4 import BeautifulSoup
import requests

 
def webbscrape():
    # The url to the website
    url = "https://fnbr.co/shop" 
    # Gets the website
    req = requests.get(url) 
    # Parses the website 
    soup = BeautifulSoup(req.text, "html.parser")
    # Prints the title of the website
    print(soup.title)
    # List for names and prices
    name = []
    price = []
    # Finds the names and prices of the items and appends them to the lists
    for span in soup.find_all("h4", class_="item-name"):
        name = span.text
        name.append(name)
    # Finds the prices of the items and appends them to the list
    for span in soup.find_all("p", class_="item-price"):
        price = span.text
        price.append(price.strip("\n"))
    # Prints the names and prices of the items
    for i in range(len(name)):
        print("Name: ", name[i] + "   price: " + price[i], "vbucks")





    




