from flask import Flask, jsonify
import json
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import uuid

# Initialize Firebase credentials
cred = credentials.Certificate('C:/Users/MuhammadHamza/Desktop/Scrap/shoescanner-26aa5-firebase-adminsdk-kvsjl-3c0c6319f8.json')
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()
# Set options for Firefox
options = Options()
options.add_argument('-headless')
# Create Flask app instance
app = Flask(__name__)
print('headless started')
# Create Firefox webdriver instance
driver = webdriver.Firefox(options=options)
# Define the route for scraping

@app.route('/', methods=['GET'])

# Define the route for scraping
def scrape():
    url = ['https://www.nike.com/w/mens-shoes-nik1zy7ok',
       'https://www.nike.com/w/mens-lifestyle-shoes-13jrmznik1zy7ok',
       'https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok',
       'https://www.nike.com/w/mens-air-max-shoes-a6d8hznik1zy7ok',
       'https://www.nike.com/w/mens-air-force-1-shoes-5sj3yznik1zy7ok',
       'https://www.nike.com/w/mens-90aohz9gw3aznik1',
       'https://www.nike.com/w/womens-shoes-5e1x6zy7ok',
       'https://www.nike.com/w/womens-lifestyle-shoes-13jrmz5e1x6zy7ok',
       'https://www.nike.com/w/womens-jordan-shoes-37eefz5e1x6zy7ok',
       'https://www.nike.com/w/womens-air-max-shoes-5e1x6za6d8hzy7ok',
       'https://www.nike.com/w/womens-air-force-1-shoes-5e1x6z5sj3yzy7ok',
       'https://www.nike.com/w/womens-5e1x6z90aohz9gw3a',
       'https://www.nike.com/w/womens-100-and-under-shoes-3s37kz5e1x6zy7ok',
       'https://www.nike.com/w/kids-shoes-v4dhzy7ok',
       'https://www.nike.com/w/big-kids-shoes-agibjzv4dhzy7ok',
       'https://www.nike.com/w/little-kids-shoes-6dacezv4dhzy7ok',
       'https://www.nike.com/w/baby-toddler-kids-shoes-2j488zv4dhzy7ok',
       'https://www.nike.com/w/kids-lifestyle-shoes-13jrmzv4dhzy7ok',
       'https://www.nike.com/w/kids-jordan-shoes-37eefzv4dhzy7ok',
       'https://www.nike.com/w/kids-air-max-shoes-a6d8hzv4dhzy7ok',
       'https://www.nike.com/w/kids-air-force-1-lifestyle-shoes-13jrmz5sj3yzv4dhzy7ok',
       'https://www.nike.com/w/1onraz3aqegz90aohz9gw3a',
       'https://www.nike.com/w/kids-under-70-shoes-abelozv4dhzy7ok']
    # Navigate to the webpage
    for i in url:
        if (i=='https://www.nike.com/w/mens-shoes-nik1zy7ok'):         
            Gender = 'Men'
        elif(i=='https://www.nike.com/w/mens-lifestyle-shoes-13jrmznik1zy7ok'):
            Type = 'LifeStyle shoes'
            Gender = 'Men'
        elif(i=='https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok'):
            Type = 'Jordan Shoes'
            Gender = 'Men'
        elif(i=='https://www.nike.com/w/mens-air-max-shoes-a6d8hznik1zy7ok'):
            Type = 'Air Max Shoes'
            Gender = 'Men'
        elif(i=='https://www.nike.com/w/mens-air-force-1-shoes-5sj3yznik1zy7ok'):
            Type = 'Air Force 1 Shoes'
            Gender = 'Men'
        elif(i=='https://www.nike.com/w/mens-90aohz9gw3aznik1'):
            Sp_filter = 'Best'
            Gender = 'Men'
        elif (i=='https://www.nike.com/w/womens-shoes-5e1x6zy7ok'):         
            Gender = 'Women'
        elif(i=='https://www.nike.com/w/womens-lifestyle-shoes-13jrmz5e1x6zy7ok'):
            Type = 'LifeStyle shoes'
            Gender = 'Women'
        elif(i=='https://www.nike.com/w/womens-jordan-shoes-37eefz5e1x6zy7ok'):
            Type = 'Jordan Shoes'
            Gender = 'Women'
        elif(i=='https://www.nike.com/w/womens-air-max-shoes-5e1x6za6d8hzy7ok'):
            Type = 'Air Max Shoes'
            Gender = 'Women'
        elif(i=='https://www.nike.com/w/womens-air-force-1-shoes-5e1x6z5sj3yzy7ok'):
            Type = 'Air Force 1 Shoes'
            Gender = 'Women'
        elif(i=='https://www.nike.com/w/womens-5e1x6z90aohz9gw3a'):
            Sp_filter = 'Best'
            Gender = 'Women'
        elif(i=='https://www.nike.com/w/womens-100-and-under-shoes-3s37kz5e1x6zy7ok'):
            Sp_filter = 'sale under 100'
            Gender = 'Women'
        elif (i=='https://www.nike.com/w/kids-shoes-v4dhzy7ok'):         
            Gender = 'Kid'
        elif (i=='https://www.nike.com/w/big-kids-shoes-agibjzv4dhzy7ok'):         
            Gender = 'Big kid'
        elif (i=='https://www.nike.com/w/little-kids-shoes-6dacezv4dhzy7ok'):         
            Gender = 'Little kid'
        elif (i=='https://www.nike.com/w/baby-toddler-kids-shoes-2j488zv4dhzy7ok'):         
            Gender = 'Toddler kid'
        elif(i=='https://www.nike.com/w/kids-lifestyle-shoes-13jrmzv4dhzy7ok'):
            Type = 'LifeStyle shoes'
            Gender = 'Kid'
        elif(i=='https://www.nike.com/w/kids-jordan-shoes-37eefzv4dhzy7ok'):
            Type = 'Jordan Shoes'
            Gender = 'Kid'
        elif(i=='https://www.nike.com/w/kids-air-max-shoes-a6d8hzv4dhzy7ok'):
            Type = 'Air Max Shoes'
            Gender = 'Kid'
        elif(i=='https://www.nike.com/w/kids-air-force-1-lifestyle-shoes-13jrmz5sj3yzv4dhzy7ok'):
            Type = 'Air Force 1 Shoes'
            Gender = 'Kid'
        elif(i=='https://www.nike.com/w/1onraz3aqegz90aohz9gw3a'):
            Sp_filter = 'Best'
            Gender = 'Kid'
        elif(i=='https://www.nike.com/w/kids-under-70-shoes-abelozv4dhzy7ok'):
            Sp_filter = 'sale under 70'
            Gender = 'Kid'
        driver.get(url)
        print('URL Fetched')

        # Define the dictionary to hold the scraped data
        data = {"shoes": []}
        count = 0
        Gender = ''
        Company = 'Nike'
        Type = ''
        Sp_filter = ''

        # Loop until there are no more products to scrape
        while True:
                # Wait for the page to load and extract the HTML
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card__body")))
                html = driver.page_source

                print('Page Loaded')

                # Parse the HTML with BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                product_cards = soup.find_all('div', class_='product-card__body')

                for product in product_cards:
                    print('count=', count)
                    count = count + 1
                    link = product.find('a', class_='product-card__link-overlay').get('href')
                    image = product.find('img', class_='product-card__hero-image').get('src')
                    name = product.find('a', {'class': 'product-card__link-overlay'}).text
                    color = product.find('div', {'class': 'product-card__product-count font-override__body1'}).text
                    full_price = product.find('div', {'class': 'product-card__price'}).find('div', {'class': 'is--current-price'}).text
                    full_price = full_price.replace('$', '')
                    item = {'Type': 'Nike', 'Link': link, 'Name': name, 'Gender': Gender, 'Company': Company, 'Type': Type, 'Sp_filter': Sp_filter,
                            'Image': image, 'Color': color, 'Full_prices': full_price}
                    data["shoes"].append(item)
                    print(item)
                    if (count >= 1):
                        break
                if (count >= 1):
                        break
            # Scrape the description for each item
            # Scrape the description for each item
        for item in data["shoes"]:
            driver.get(item["Link"])
            print('In Second For Loop')
            soup = BeautifulSoup(driver.page_source, 'lxml')
            product_cards = soup.find_all('div', class_='description-preview body-2 css-1pbvugb')

            if driver.current_url == item["Link"]:
                for card in product_cards:
                    print('product_cards', card.find_all('p'))

                    # Try to retrieve the shoe item's description and append it to the dictionary
                    try:
                        description = card.find_all('p')[0].text
                        item["Description"] = description
                        print('desc',description)
                    except:
                        item["Description"] = 'Nothing'
                    # Print the dictionary for the current shoe item with its added description
                    print(item)
            else:
                print(f"Link visited ({driver.current_url}) does not match the unique ID ({item['ID']}) of the current shoe item.")
                print("Skipping description retrieval for this item.")
        for item in data["shoes"]:
            query = db.collection(u'Products Data').where(u'Link', u'==', item['Link']).limit(1)
            docs = list(query.stream())
            if len(docs) > 0:
                # Update the existing document with the new data
                doc = docs[0]
                doc_ref = db.collection(u'Nike Data').document(doc.id)
                update_dict = {"Description": item["Description"], "Name": item["Name"], "Gender": item["Gender"],"Company": item["Company"],"Type": item["Type"],"Sp_filter": item["Sp_filter"],
                                "Image": item["Image"], "Color": item["Color"], "Full_prices": item["Full_prices"]}
                doc_ref.update(update_dict)
            else:
                db.collection(u'Nike Data').add(item)
        # Close the browser
        driver.quit()
        return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000)