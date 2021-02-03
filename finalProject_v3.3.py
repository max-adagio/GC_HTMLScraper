# Author : Max Widjaja
# Description : Guitar Center HTML Scraper
# Date : 11 Dec 2020
##################################################################################################
##################################################################################################

# Imports Beautiful Soup as well as url request module
from bs4 import BeautifulSoup
from urllib.request import urlopen

##################################################################################################
# function that returns the price of the item
def priceFinder(inputtedURL):
    # this variable is the string of an HTML object that contains the price
    # of the item, regardless of if it's on sale or not.
    priceString = str(inputtedURL.find_all("span","topAlignedPrice")[0])
    # turns the string into a list
    priceList = list(priceString)
    # creates empty string which will hold the digits of the price.
    priceDigits = ""
    # this for loop iterates over each character in the list, and checks if each one is
    # a digit. If it is, it concatenates the digit to the empty list 'priceDigits'
    for i in priceList:
        if i.isdigit() == True:
            priceDigits = priceDigits + i
    # the string of digits is then indexed with a proper decimal point to denote dollars and cents.
    # this final string is returned.
    priceFinal = priceDigits[0:-2]+"."+priceDigits[-2]+priceDigits[-1]
    return priceFinal


##################################################################################################
# function that returns the amount saved on an item.
# This function functions identically to priceFinder.
def savingsFinder(inputtedURL):
    # this variable is the string of an HTML object that contains how much is discounted
    # off of the normal price of the item.
    savingsString = str(inputtedURL.find_all("dd","price-display-value")[0])
    # turns the string into a list
    savingsList = list(savingsString)
    # creates empty string which will hold the digits of the price.
    savingsDigits = ""
    # this for loop iterates over each character in the list, and checks if each one is
    # a digit. If it is, it concatenates the digit to the empty list 'savingsDigits'
    for i in savingsList:
        if i.isdigit() == True:
            savingsDigits = savingsDigits + i
    # the string of digits is then indexed with a proper decimal point to denote dollars and cents.
    # this final string is returned.
    savingsFinal = savingsDigits[0:-2] + "." + savingsDigits[-2] + savingsDigits[-1]
    return savingsFinal

##################################################################################################
def onSale(soupObject):
    # this if statement checks for a string of HTML that codes for an object that is only
    # present on product pages that are on sale. The function prints a corresponding statement,
    # and returns a boolean depending on if it is on sale or not.
    if soupObject.find_all('section',"product-data-wrap clearfix") != []:
        if soupObject.find_all('dl', "price-display-wrapper savings") != []:
            print("This product is on sale.")
            return True
        else:
            print("This product is not on sale.")
            return False
    else:
        print("You have not inputted a product page.")
        return False

##################################################################################################
# this function is the meat of the program. It takes the string of the URL as input, processes it,
# prints corresponding statements and prices for the item, and returns a boolean determined by if
# the input is empty or not.
def urlChecker(inputtedURL):
    if inputtedURL == "" or inputtedURL == [] or inputtedURL == None:
        return False
    else:
        # opens the URL using urlopen() from urllib.request module
        page = urlopen(inputtedURL)

        # Reads the HTML from the user inputted URL and assigns it the html variable
        htmlObject = page.read().decode("utf-8")

        # Creates Beautiful Soup object
        # the string "html.parser" tells the object which parser to use behind the scenes

        userGivenURL = BeautifulSoup(htmlObject, "html.parser")

        # This if statement evaluates a function, which still evokes it. The function in question
        # either messages the user the product is on sale, or it is not on sale.
        if onSale(userGivenURL) == True:
            print("The discounted price is: $", priceFinder(userGivenURL), sep="")
            print("You save: $", (savingsFinder(userGivenURL)),sep="")
        else:
            print("The price is: $", priceFinder(userGivenURL), sep="")
        return True

##################################################################################################
#                                   MAIN  MAIN  MAIN  MAIN                                       #
##################################################################################################
def main():
    # greeting message
    print("==================================================")
    print("Guitar Center HTML Scraper Beta v3.3")
    print("Created by Max Widjaja")
    print("==================================================")

    # this while loop will continually prompt user for a valid input
    # until it is received.
    while True:
        print("Would you like to see your saved items or check URLs for sales? (input in saved or new): ")
        userResponse = input().lower()
        if userResponse == 'saved' or userResponse == 'new':
            break

#################################################################
# This section of main is if the user wishes to check new URLs
    # if the user inputted 'new,' then this will run.
    if userResponse.lower() == 'new':
        # this while loop handles each item one by one.
        # it ask for input, uses the urlChecker function
        # to print the item info,
        # then asks if the user wants to save the item
        # which if yes, format the URL so it can be parsed for
        # reading, and then writes it to the
        # accompanying text document.
        while True:
            # prompting user for input
            print("Input the URL of the product you're interesting in knowing about: (input quit to quit) ")
            userInput = input()

            # first two if statements handle exceptions and quitting the program.
            if userInput.lower() == "quit":
                print("Goodbye!")
                break
            # a really simple solution I found. All Guitar Center pages end with '.gc'.
            # so this if statement checks if the URL ends in 'c'. If it doesn't,
            # the program stops.
            elif userInput[-1] != "c":
                print("This is not a Guitar Center product page.")
                break
            # The main section of the while loop.
            else:
                # this will execute the urlChecker function, which utilizes Beautiful Soup
                # to scrape the URL's HTML document for info
                urlChecker(userInput)
                saveOrNot = input("Would you like to save this to your saved items? (y/n): ")
                if saveOrNot == 'y':
                    print("Saving...")
                    savedItems = open('saved_items.txt', 'a')

                    # the variable savedURL concatenates two '||' in order to seperate URLs from each other.
                    savedURL = userInput + " ||"
                    savedItems.write(savedURL)
                    print("Saved.")

#################################################################
# This section of main is if the user wishes to check saved URLs
    # the program is hardcoded to read a text document named 'saved_items.txt'
    # this section of the program essentially parses the document into a list of
    # all the URLs, which have been formatted to be seperated by "||"'s.
    elif userResponse.lower() == 'saved':
        savedItemsRaw = open('saved_items.txt','r')
        savedItemsString = ""
        # this for loop adds each line together into a big string.
        for i in savedItemsRaw:
            savedItemsString += i
        # this variable splits the big string by the seperators.
        # it is called in the later for loop for processing.
        savedItemsList = savedItemsString.split("||")

    # this for loop iterates over the amount of URLs in the list of saved URLs.
        for placeInList in range(0,len(savedItemsList)):
            # the program will ask each time to proceed to the next item.
            # if the user inputs anything other than 'y', the program will
            # terminate.
            continueCheck = input("See next item? (y/n): ")
            if continueCheck != "y":
                print("Goodbye!")
                break
            # this variable is the string of whatever URL is being counted by the for loop into.
            # So, if we were to print this, it would print the actual URL that the for loop is
            # iterating over.
            URL_from_txt = savedItemsList[placeInList]

            # if the URL is blank, that means the list has ended.
            # there is an accompanying message and a break for the loop.
            if URL_from_txt == "":
                print("You have reached the end of the list.")
                print("Goodbye!")
                break
            # this final block handles each saved URL.
            # NOTE: Only the URL is saved into the text document, and
            # the information of each item is assessed each time the
            # saved URLs are viewed. Yes, this means they could change.
            # This is intentional.
            else:
                print("========================================")
                print("Item #", placeInList + 1, sep="")
                print("URL:", URL_from_txt, sep="")
                print("loading...")
                urlChecker(URL_from_txt)


main()

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

7 Dec 2020
Build v1.4
Implemented fix for line 26. 

10 Dec 2020
Build v3.1
Moved a lot of the URLchecker functionality to it's own function, so it can 
also be called when the user wants to view saved items. 

11 Dec 2020
Build v3.2
Completed implementation of saved URL text document functionality. 

11 Dec 2020
Build v3.3 
Commenting done for final submission. 
===============================================================================
'''