import asyncio, csv
from time import sleep
from pyppeteer import launch
from bs4 import BeautifulSoup

from pyjsparser import parse

import requests
import os
from PIL import Image
from io import BytesIO
import pickle
import re
    
PATH = r'C:\Users\lukez\PycharmProjects\CMSC499\Models\Images'
PATH1 = r'C:\Users\lukez\PycharmProjects\CMSC499\Models'


#Scrape data for the current subject's address
async def scrapeLinks(product, num_pages):
    """
    Due to amazon being an ass this code may break often.
    One of the main ways to fix it is to check if the 'class_ = ' string is still correct. 
    This can change based of the product you are searching for as well so have fun.
    Also you do at time need too or more version of it as sometime for different pages or products the block have different 'class_ = ' strings.
    """
    ProductURL_list = []
    search_name = product.replace(' ', '+')
    base_url = 'http://www.amazon.com/s?k={0}'.format(search_name)

    for i in range(1, num_pages + 1):
        ProductURL_list_test = []
        print('Processing {0}...'.format(base_url + '&page={0}'.format(i))) 
    #print(url)
        url = base_url + '&page={0}'.format(i)
        source = requests.get("http://localhost:8050/render.html", params={'url': url, 'wait': 2}).text
        soup = BeautifulSoup(source,"html.parser")
        
        with open('test.html', 'w', encoding = "utf-8") as f:
            f.write(soup.prettify())   

        
        #For Chair                                      
        for productBlock in soup.find_all('div', class_ = 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20'):
            productURL = productBlock.find('a')['href']
            ProductURL_list.append(productURL)
            ProductURL_list_test.append(productURL)

        #for Mouse
        for productBlock in soup.find_all('div', class_ = 'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'):
            productURL = productBlock.find('a')['href']
            ProductURL_list.append(productURL)
            ProductURL_list_test.append(productURL)
        
        #for couch
        for productBlock in soup.find_all('div', class_ = 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'):
            productURL = productBlock.find('a')['href']
            ProductURL_list.append(productURL)
            ProductURL_list_test.append(productURL)
        
            
        await asyncio.sleep(5)
        print(ProductURL_list_test)

    """#Launching CHromium and focusing on the input field
    chrome = await launch(headless=False, ignoreHTTPSErrors = True)
    page = await chrome.newPage()
    await page.goto("https://www.amazon.com/")

    await asyncio.sleep(10)
    
    await page.waitForSelector(".nav-search-field input")
    await page.focus(".nav-search-field input")
    await asyncio.sleep(3)

    
    #Enter the address and search
    await page.keyboard.type(product)
    await asyncio.sleep(0.75)
    await page.keyboard.press("Enter")

    #Grab contents and close the browser
    await asyncio.sleep(3)
    contents = await page.content()
    await chrome.close()"""

    
    return ProductURL_list

async def scrape360Image(productURL, prodcut):
    """
    Same issue as the scrapeLinks() were you have to check to make sure all the diffent html string are still correct.
    There are a few places in the code where I have commented out sections that print out the html or a section of it to a file
    which I used to check if the string were still the same.
    """

    if 'bestsellers' in productURL:
        return False
    else:
        url = "http://www.amazon.com/" + productURL
        print(url)
        source = requests.get("http://localhost:8050/render.html", params={'url': url, 'wait': 2}).text
        

        """
        chrome = await launch(headless=False, ignoreHTTPSErrors = True)
        page = await chrome.newPage()
        await page.goto("https://www.amazon.com/" + productURL)

        await asyncio.sleep(2)

        await page.waitForSelector(".nav-search-field input")
        await page.focus(".nav-search-field input")
        await asyncio.sleep(3)

        await page.keyboard.type("FU")
        await asyncio.sleep(0.75)
        await page.waitForSelector('input.a-button-inner' , timeout=600)
        #await page.waitForSelector('.a-button-inner input[aria-labelledby="a-autoid-10-announce"' , timeout=600)
        await page.click('input.a-button-inner')
        
        #Grab contents and close the browser
        await asyncio.sleep(3)
        contents = await page.content()
        await chrome.close()
        """

        """try:"""

        soup = BeautifulSoup(source,"lxml")
        with open('full1.html', 'w', encoding = "utf-8") as f:
            f.write(soup.prettify())

        #print(soup.find('html')['class'][0])
        if soup.find('html')['class'][0] == "a-no-js": 
            chrome = await launch(headless=False, ignoreHTTPSErrors = True)
            page = await chrome.newPage()
            await page.goto("https://www.amazon.com/" + productURL)

            await asyncio.sleep(2)

            await page.waitForSelector(".nav-search-field input")
            await page.focus(".nav-search-field input")
            await asyncio.sleep(3)

            await page.keyboard.type("FU I can still parse your shit")
            await asyncio.sleep(0.75)
            
            #Grab contents and close the browser
            await asyncio.sleep(3)
            contents = await page.content()
            await chrome.close()
            soup = BeautifulSoup(contents,"lxml")

        try:
            productName1 = soup.find('div', id = 'titleSection')
            productName2 = productName1.find('span', id = "productTitle")
            ProductName3 = (productName2.text).strip()
            ProductName = re.sub('[^A-Za-z0-9 ]+', '', ProductName3)
            print('Name Gotten')

            path = PATH + '\\' + prodcut + '\\' + ProductName
            #print(path)
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)

            image360 = True
            image360d1 = soup.find('div', id = 'dp')
            image360d2 = image360d1.find('div', id = 'dp-container')
            image360d3 = image360d2.find('div', id = 'ppd')
            image360d4 = image360d3.find('div', id = 'leftCol')
            image360d5 = image360d4.find('div', id = 'spin360_feature_div')
            try:
                image360 = image360d5.find('script').text
                #with open('readme2.html', 'w', encoding = "utf-8") as f:
                #    f.write(image3605.prettify())
                test = parse(image360)
            except:
                """with open(ProductName + '.html', 'w', encoding = "utf-8") as f:
                    f.write(url + '\n')
                    f.write(image360d4.prettify())"""
                print('360 fail')
                image360 = False
                #return False

            productPrice1 = soup.find('div', id = 'ppd')
            productPrice2 = productPrice1.find('span', class_ = "a-offscreen")
            ProductPrice = productPrice2.text
            print('Price Gotten')


            try:
                productBrand0 = soup.find('div', id = 'ppd')
                productBrand1 = productBrand0.find('div', class_ = 'a-section a-spacing-small a-spacing-top-small')
                """with open('readme12.html', 'w', encoding = "utf-8") as f:
                    f.write(productBrand1.prettify())"""
                try:
                    productBrand2 = productBrand1.find('tr', class_ ="a-spacing-small po-brand")
                    productBrand3 = productBrand2.find('td', class_="a-span9")
                except:
                    productBrand2 = productBrand1.find('tr', class_ ="a-spacing-none a-spacing-top-small po-brand")
                    productBrand3 = productBrand2.find('td', class_="a-span6")
                productBrand4 = productBrand3.find('span')
                productBrand = productBrand4.text
                print('Brand Gotten')
            except:
                productBrand = ''
                print('Brand Not Gotten')
                
            
            if(image360):
                test1 = test['body'][0]['expression']
                test2 = test1['arguments']
                test3 = test2[0]['body']['body']
                test4 = test3[0]['expression']
                test5 = test4['arguments']
                test6 = test5[0]['body']
                test7 = test6['body']
                test8 = test7[0]['expression']
                test9 = test8['arguments']
                test10 = test9[0]['properties']

                test11 = test10[3]['value']['properties']
                #print(test11[1])
                x = 0
                for key in test11:
                    #print(key)
                    try:
                        key1 = key['value']['value']
                        print(x, ' ', key1)
                        
                        x = x + 1
                        
                        img_data = requests.get(key1)
                        #print(img_data.status_code)
                        img_content = img_data.content
                        imag = Image.open(BytesIO(img_content))

                        image = imag.save(f"{path}/image{x}.png")
                    except:
                        print(' failed')
                    """
                    with open(path + '\image_' + str(x) + '.jpg', 'wb') as handler:
                        handler.write(img_data)

                    """

            image1 = soup.find('div', class_ = 'a-dynamic-image-container')
            image2 = image1.find('span', class_ = 'a-declarative')
            image3 = image2.find('div').find('img')['src']
            img_data = requests.get(image3).content
            imag = Image.open(BytesIO(img_data))

            image = imag.save(f"{path}/image.png")
            print('Image Gotten')


            productDerct =  {"Name": ProductName, "Brand": productBrand, "Price": ProductPrice, "imagePath": path}
            return productDerct
        except:
            return False

        """with open(f"{PATH1}/ProductData.txt", 'w', encoding = "utf-8") as f:
            f.write(str(productDerct))
            f.write('\n')"""
    
    
    
    """except:
        return False"""

    
    


    
    """
    for image in image360.find_all('img'):
        #image1 = productBlock.find['src']
        print(image['src'])
    """
def getProdcutURL(product, num_pages):
    products = asyncio.get_event_loop().run_until_complete(scrapeLinks(product, num_pages))
    #print(products)
    with open('Productlist_' + product, 'wb') as fp:
        pickle.dump(products, fp)
        fp.close

def getData(product, start_position, end):
    products = []
    with open ('Productlist_' + product, 'rb') as fp:
        products = pickle.load(fp)
    #print(products)

    #with open(f"{PATH1}/ProductData_" + product + ".txt", 'a', encoding = "utf-8") as amazon:
    position = start_position
    start = position
    for product1 in products[start:end]:
        print()
        print(position)
        testfunction(product1, product)
        position = position + 1

def testfunction(product1, product):
    info = asyncio.get_event_loop().run_until_complete(scrape360Image(product1.strip('\''), product))
    print(info)
    with open(f"{PATH1}/ProductData_" + product + ".txt", 'a', encoding = "utf-8") as amazon:
        if(info):
            amazon.write(str(info))
        amazon.write('\n')
        amazon.close

def main():
    """
    First run the 'getProductURL(product, 10)' code to get a file filled with product URL's (name format is  ['Productlist_' + product]). 
    Then after running that run the 'getData(product)' code which requires the file from the previus code.
    If you have the file alread you do not need to run the 'getProductURL(product, 10)' agian.

    Do note the '10' in 'getProductURL(product, 10)' is the number of pages you will search.
    """
    product = 'couch'
    """url = 'Razer-DeathAdder-Gaming-Mouse-Programmable/dp/B082G5SPR5/ref=sr_1_11?crid=JEX79HYJ4SMJ&keywords=mouse&qid=1669989015&sprefix=mouse%2Caps%2C87&sr=8-11&th=1'
    info = asyncio.get_event_loop().run_until_complete(scrape360Image(url, product))
    print(info)"""
    getProdcutURL(product, 10)
    getData(product, 0, -1)



if __name__ == "__main__":
    main()