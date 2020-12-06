# Author : Max Widjaja
# Description : Guitar Center HTML Scraper
# Date : 28 Nov 2020

# Imports Beautiful Soup as well as url request module
from bs4 import BeautifulSoup
from urllib.request import urlopen

# function that obtains the price of the item
def priceFinder(inputA):
    priceString = str(inputA.find_all("span","topAlignedPrice")[0])
    priceList = list(priceString)
    priceDigits = ""
    for i in priceList:
        if i.isdigit() == True:
            priceDigits = priceDigits + i
    priceFinal = priceDigits[0:-2]+"."+priceDigits[-2 :-1]+"9"

    return priceFinal

def savingsFinder(inputA):
    savingsString = str(inputA.find_all("div","product-discount-details")[0])
    savingsList = list(savingsString)
    savingsDigits = ""
    for i in savingsList:
        if i.isdigit() == True:
            savingsDigits = savingsDigits + i
    savingsFinal = savingsDigits[0:-2]+"."+savingsDigits[-2]+savingsDigits[-1]

    return savingsFinal

# The function that takes the user input and converts the URL into an html object.
def onSale(soupObject):
    # print(soupObject)
    # print(soupObject.find_all('section',"product-data-wrap clearfix"))


    if soupObject.find_all('section',"product-data-wrap clearfix") != []:
        if soupObject.find_all('div', "product-discount-details") != []:
            print("This product is on sale.")
            return True
        else:
            print("This product is not on sale.")
            return False
    else:
        print("You have not inputted a product page.")
        return False

def main():
    # greeting message
    print("==================================================")
    print("Guitar Center HTML Scraper Beta v1.2")
    print("Created by Max Widjaja")
    print("==================================================")

    userResponse = ""
    while True:
        print("Would you like to see your saved items or check for more sales? (enter in saved or new): ")
        userResponse = input().lower()
        if userResponse == 'saved' or userResponse == 'new':
            break

    if userResponse == 'new':
        x = True
        while x:
           print("Input the URL of the product you're interesting in knowing about: ")
           inputtedURL = input()
           '''
           inputtedURL = None
           if rawInputtedURL[-1] != "c":
               print("This is not a Guitar Center webpage.")
               exit()
           else:
               rawInputtedURL = inputtedURL
        
        '''
           # opens the URL using urlopen() from urllib.request module
           page = urlopen(inputtedURL)

           # Reads the HTML from the user inputted URL and assigns it the html variable
           htmlObject = page.read().decode("utf-8")

           # Creates Beautiful Soup object
           # the string "html.parser" tells the object which parser to use behind the scenes

           userGivenURL = BeautifulSoup(htmlObject, "html.parser")

           if onSale(userGivenURL) == True:
               print("The discounted price is: $", priceFinder(userGivenURL), sep="")
               print("You save: $", (savingsFinder(userGivenURL)), sep="")
           else:
               print("The price is: $", priceFinder(userGivenURL), sep="")
    else:
        savedItems = open('saved_items.txt')
        print("")
        print(savedItems)



'''
===============================================================================
NOTES:
------------------
28 Nov 2020 
Build v1.2
Program is hardcoded to print prices that are specifically 6 characters long. 
Need to implement a system to detect numbers and print them. 
Use list and or str concatenation. 

Build v1.3
Implemented number detection system, and used string concatination and indexing 
to return the price with a decimal, which would have otherwise been omitted. 
Might be hardcode reliant on the ones place of price being '9'. 
Refer to line 26

30 Nov 2020
Build v1.3
Confirmed the problem on line 26. No idea on potential solution, however. 




===============================================================================
'''


main()




