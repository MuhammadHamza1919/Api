from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize Firebase credentials
cred = credentials.Certificate('C:/Users/MuhammadHamza/Desktop/Scrap/shoescanner-26aa5-firebase-adminsdk-kvsjl-3c0c6319f8.json')
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()

# Create Flask app instance
app = Flask(__name__)
print('headless started')
# Create Firefox webdriver instance
# Define the route for scraping

@app.route('/', methods=['GET'])

# Define the route for scraping
def scrape():
    urls = [
        'https://www.nike.com/w/mens-shoes-nik1zy7ok',
        'https://www.nike.com/w/womens-shoes-5e1x6zy7ok',
        'https://www.nike.com/w/kids-shoes-v4dhzy7ok',
    ]
    
    for i in urls:
        # Set options for Firefox
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
        data = {"shoes": []}
        count = 0
        Gender = ''
        Company = 'Nike'
        Type = ''
        Sp_filter = ''
        Seller = '01'
        ProductID = ''
        
        if i == 'https://www.nike.com/w/mens-shoes-nik1zy7ok':
            Gender = 'Men'
            Sp_filter = 'Men'
        elif i == 'https://www.nike.com/w/womens-shoes-5e1x6zy7ok':
            Gender = 'Women'
            Sp_filter = 'Women'
        elif i == 'https://www.nike.com/w/kids-shoes-v4dhzy7ok':
            Gender = 'Kid'
            Sp_filter = 'Kid'
        driver.get(i)
        print('URL Fetched')

        # Define the dictionary to hold the scraped data

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
                            'Image': image, 'Color': color, 'Full_prices': full_price, 'Seller':Seller, 'ProductID':ProductID}
                    data["shoes"].append(item)
                    print(item)
                    if (count >= 1):
                        break
                if (count >= 1):
                        break
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
                        item["Description"] = 'We apologize for any inconvenience. Unfortunately, we were unable to fetch the description at this time. Please click on the button below and visit the website for more information. We are currently working on the issue and hope to have it resolved soon. Thank you for your understanding.'
                    # Print the dictionary for the current shoe item with its added description
                    print(item)
            else: item["Description"] = 'We apologize for any inconvenience. Unfortunately, we were unable to fetch the description at this time. Please click on the button below and visit the website for more information. We are currently working on the issue and hope to have it resolved soon. Thank you for your understanding.'
        for item in data["shoes"]:
            query = db.collection(u'Products Data').where(u'Link', u'==', item['Link']).limit(1)
            docs = list(query.stream())
            if len(docs) > 0:
                # Update the existing document with the new data
                doc = docs[0]
                doc_ref = db.collection(u'Products Data').document(doc.id)
                update_dict = {"Description": item["Description"], "Name": item["Name"], "Gender": item["Gender"],"Company": item["Company"],"Type": item["Type"],"Sp_filter": item["Sp_filter"],
                                "Image": item["Image"], "Color": item["Color"], "Full_prices": item["Full_prices"]}
                doc_ref.update(update_dict)
            else:
                db.collection(u'Products Data').add(item)
        # Close the browser
    driver.quit()

if __name__ == '__main__':
    app.run(port=5000)