from bs4 import BeautifulSoup
from selenium import webdriver



def getHtml(pageLink):


    #Henter siden
    browser = webdriver.Chrome()
    browser.get(pageLink)

    parseHtml(browser)
    pass

def removeHtmlTagsFromString(string):

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
    discountPriceTag = product.find("span", class_="__price ng-binding")
    discountPrice = removeHtmlTagsFromString(discountPriceTag)

    productPriceTextTag = product.find("span", class_="block ng-binding")
    productPriceText = removeHtmlTagsFromString(prodPriceTag)

    for x in range(len(productPriceText)):
        if productPriceText[x] == ":":
            startIdx = x
            break

    #Finder lukkende Html-tags begyndelse og gemmer dens index
    for x in range(startIdx, len(productPriceText)):
        if productPriceText[x] ==",":
            endIdx = x
            break


    pass productPrice, discountPrice

def parseHtml(browser):
    #products = driver.find_elements_by_class_name("product-tile")
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.close()

    #Skærer alt andet end produktrækkerne væk
    productList = soup.find_all("product-tile", class_="ng-scope ng-isolate-scope")

    normalProducts, discountProducts = [], []

    for product in productList:
        prodNameTag = product.find("h2", class_="product-tile__title ng-binding")
        prodName = removeHtmlTagsFromString(prodNameTag)
        discountAmountTag = product.find("span", class_="__deal ng-binding ng-scope")

        if discountAmountTag == None:

            prodPriceTag = product.find("span", class_= "__price ng-binding")
            prodPrice = removeHtmlTagsFromString(prodPriceTag)

            normalProducts.append([prodName,prodPrice])

        else:
            #Tryller alt andet end tal væk fra tagget med mængden af tilbd
            discountAmount = int(''.join(filter(lambda x: x.isdigit(), removeHtmlTagsFromString(discountAmountTag))))

            prodPrice, discountPrice  = findDiscount(product)

            discountProducts.append([prodName, prodPrice, discountAmount, discountPrice])


    print(normalProductDict)
    pass

getHtml('https://www.bordershop.com/dk/ol-cider/dansk-ol')

#removeHtmlTagsFromString('<h2 class="product-tile__title ng-binding">Tuborg Grøn Pilsner Øl 4,6%</h2>')
