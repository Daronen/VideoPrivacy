import os
import sys
import shutil

import numpy as np
import matplotlib.pyplot as plt
from random import randint
import pandas as pd
import pickle
import json

PATH = r'C:\Users\lukez\PycharmProjects\CMSC499\Models\Images'
PATH1 = r'C:\Users\lukez\PycharmProjects\CMSC499\Models'

def loadProductData(file):
    finalDict = {}
    with open(file, "r") as ProductDataFull:
        lines = ProductDataFull.readlines()
        for line in lines:
            if(len(line) > 1):
                print(line)
                line = line.replace('\'', '\"')
                lineDict = json.loads(str(line))
                finalDict[lineDict['Name']] = lineDict
    
    return finalDict

def loadImagesFolders(product, maxProducts):
    path = PATH
    path = path + '\\' + product
    productImages = []
    number_products = 0

    os.chdir(path)


    folders = os.listdir(path)
    if((maxProducts > len(folders)) or maxProducts == -1):
        maxProducts = len(folders)
    for folder in range(maxProducts):
        number_products = number_products + 1
    
        productImages.append(folders[folder])
        
        
    return productImages, number_products

def main():
    path1 = PATH1
    os.chdir(path1)
    product = 'couch'
    ProductsDict = (loadProductData('ProductData_' + product + '.txt'))

    productImages, number_products = loadImagesFolders(product, -1)
    #print(productImages)
    emptyProduct = []
    x = True
    for prod in productImages:
        if(prod in ProductsDict):
            #print(True)
            x=x
        else:
            emptyProduct.append(prod)
    
    print(len(productImages))
    print()
    print(len(ProductsDict))
    #path2 = r"C:\Users\lukez\PycharmProjects\CMSC499\Image Scrape\Images" 
    #path2 = path2 + '\\' + product + '\\' + emptyProduct[0]

    #print(path2)
    

    #os.rmdir(path2)
    
    for emptyProductX in emptyProduct:
        path2 = PATH 
        path2 = path2 + '\\' + product + '\\' + emptyProductX

        try:
            shutil.rmtree(path2)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
    



if __name__ == "__main__":
    main()