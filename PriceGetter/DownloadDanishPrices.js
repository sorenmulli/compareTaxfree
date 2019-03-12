const cheerio = require('cheerio');
const axios = require('axios');
const fs = require('fs'); 

const filePath = "/Users/Moesen/Git/NodeScraber/BorderAPIGetter/";
const filename = "AllPricesBordersShop.json";
const hyperlink= 'https://www.pricerunner.dk/results?q=';

const prices = JSON.parse(fs.readFileSync(filePath + filename, 'utf8'));

for(let i = 0; i < 1; i++){

	let displayName = prices[i]['displayName'];

	let searchString = displayName.replace('/[0-9]/g', '');
	searchString = searchString.replace(/\s/g, "%20");

	axios.get(hyperlink + searchString).then((response) => {
		const $ = cheerio.load(response.data);
		const items = $('._1NKXYqawid');

		if(items.length > 0){
			const prices = $(items.find('._3SSjCz1vsV'));

			if(prices.length > 0){
				console.log(items.children())
			}
		}


	})
}

