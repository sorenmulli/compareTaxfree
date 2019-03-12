const cheerio = require('cheerio');
const axios = require('axios');
const fs = require('fs'); 

var borderPrices 	= JSON.parse(fs.readFileSync( "/Users/Moesen/Git/compareTaxfree/PriceGetter/AllPricesBordersShop.json" ));
const danishPrices 	= JSON.parse(fs.readFileSync("/Users/Moesen/Git/compareTaxfree/PriceGetter/pricerunner_prices.json"));

for(let i = 0; i < 4; i++){

	//console.log(borderPrices[i].idItems[1]['items'])

	let allItems = borderPrices[i].idItems[1]['items']


	for(let j = 0; j < allItems.length; j++){
		//console.log(allItems[j]['displayName'])

		var name = allItems[j]['displayName']



	}

}

function findDanishPrice(__borderString, danish){



}

function binarySearch(string, danish_list){

}