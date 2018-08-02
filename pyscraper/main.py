from bs4 import BeautifulSoup
from selenium import webdriver



def getHtml(pageLink):


    #Henter siden
    browser = webdriver.Chrome()
    #driver.implicitly_wait(30)
    browser.get(pageLink)

    parseHtml(browser)
    pass

def removeHtmlTagsFromString(string):
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

def parseHtml(browser):
    #products = driver.find_elements_by_class_name("product-tile")
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.close()

    #Skærer alt andet end produktrækkerne væk
    productList = soup.find_all("product-tile", class_="ng-scope ng-isolate-scope")

    productDict = {}

    for product in productList:

        prodNameTag = product.find("h2", class_="product-tile__title ng-binding")
        prodName = removeHtmlTagsFromString(prodNameTag)

        prodPriceTag = product.find("span", class_= "__price ng-binding")
        prodPrice = removeHtmlTagsFromString(prodPriceTag)

        productDict[str(prodName)]=str(prodPrice)

    print(productDict)
    pass

#getHtml('https://www.bordershop.com/dk/ol-cider/dansk-ol')
print(removeHtmlTagsFromString('<h2 class="product-tile__title ng-binding">Tuborg Grøn Pilsner Øl 4,6%</h2>'))

