from bs4 import BeautifulSoup
from selenium import webdriver
import json



def getHtml(pageLink):


    #Åbner browseren vha. selenium
    browser = webdriver.Chrome()

    #Går ind på siden
    browser.get(pageLink)

    #Igangsætter læsning af siden
    return browser


def removeHtmlTagsFromString(string):

    #Gør den til string
    string = str(string)

    # Finder åbnende Html-tags slutning og gemmer dens index
    for x in range(len(string)):
        if string[x] == ">":
            startIdx = x
            break

    #Finder lukkende Html-tags begyndelse og gemmer dens index
    for x in range(startIdx, len(string)):
        if string[x] =="<":
            endIdx = x
            break

    #Cutter strengen det rigtige sted
    cleanedString = string[startIdx + 1:endIdx]

    return cleanedString

def findDiscount(product):

    #Finder mængdeprisen og fjerner html
    discountPriceTag = product.find("span", class_="__price ng-binding")
    discountPrice = removeHtmlTagsFromString(discountPriceTag)

    #Finder tekststykket med den enkelte pris i og fjerner html
    productPriceTextTag = product.find("span", class_="block ng-binding")
    productPriceText = removeHtmlTagsFromString(productPriceTextTag)

    #Fjerner alt teksten og bibeholder prisen
    for x in range(len(productPriceText)):
        if productPriceText[x] == ":":
            startIdx = x
            break

    for x in range(startIdx, len(productPriceText)):
        if productPriceText[x] ==",":
            endIdx = x
            break

    #Cutter stringen for den unødvendige tekst
    productPrice = productPriceText[startIdx+2:endIdx]

    return productPrice, discountPrice

def parseHtml(browser):

    #Åbner siden i bs4, der læser html'en
    soup = BeautifulSoup(browser.page_source, 'lxml')

    #Lukker browservinduet
    browser.close()

    #Skærer alt andet end produktruderne væk ved at søge på deres klasse
    productList = soup.find_all("product-tile", class_="ng-scope ng-isolate-scope")

    #Fjerner duplikanter
    productList = list(set(productList))

    #Tomme lister til de færdige produkt-strings
    normalProducts, discountProducts = [], []

    #Loop, der skal undersøge hver produktrude og udtrække pris, navn og detaljer om discount
    for product in productList:

        #Udtrækker navnet og fjerner Html-kode
        prodNameTag = product.find("h2", class_="product-tile__title ng-binding")
        prodName = removeHtmlTagsFromString(prodNameTag)

        #Undersøger, om der er kode, der afslører, at det er et produkt på tilbud
        discountAmountTag = product.find("span", class_="__deal ng-binding ng-scope")


        if discountAmountTag == None:

            #Hvis det ikke er på tilbud findes standardprisen nemt og udtrækkes og rengøres for html
            prodPriceTag = product.find("span", class_= "__price ng-binding")
            prodPrice = removeHtmlTagsFromString(prodPriceTag)

            #Navn og pris tilføjes listen
            normalProducts.append([prodName,prodPrice])

        else:
            #Gælder produkter, der ER på tilbud
            #Tryller alt andet end tal væk fra tagget med mængden af tilbd
            discountAmount = ''.join(filter(lambda x: x.isdigit(), removeHtmlTagsFromString(discountAmountTag)))

            #Produktets pris og den samlede pris for mængdetilbuddet findes og udtrækkes
            prodPrice, discountPrice  = findDiscount(product)

            #navn, standardpris, tilbudsmængde og mængdepris tilføjes listen
            discountProducts.append([prodName, prodPrice, discountAmount, discountPrice])



    print(normalProducts)
    print(discountProducts)

    return normalProducts, discountProducts


def jsonify(normalProducts, discountProducts, boozeType):

    productsList = []

    for product in normalProducts:
        productInfoDict = {}
        productInfoDict["title"]=product[0]
        productInfoDict["price"]=product[1]
        productsList.append(productInfoDict)

    for product in discountProducts:
        productInfoDict = {}
        productInfoDict["title"]=product[0]
        productInfoDict["price"]=product[1]
        productInfoDict["discountAmount"]=product[2]
        productInfoDict["discountPrice"]=product[3]

        productsList.append(productInfoDict)




    mainDict = {
        boozeType: productsList
    }

    with open('data.txt', 'w') as f:
        json.dump(mainDict, f, ensure_ascii=False, indent=4, sort_keys=True)

    return None

def getPrices(pageLink, boozeType):

    #Browseren sættes op og åbnes
    browser = getHtml(pageLink)

    #Fra browseren trækkes html'en og derefter priserne ud
    normalProducts, discountProducts = parseHtml(browser)

    #Produkternes information skrives til JSON
    jsonify(normalProducts, discountProducts, boozeType)
    pass


getPrices('https://www.bordershop.com/dk/ol-cider/dansk-ol', "beer")

