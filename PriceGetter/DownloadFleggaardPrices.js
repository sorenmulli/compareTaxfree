const cheerio = require('cheerio');
const axios = require('axios');
const fs = require('fs');

const url = "https://www.fleggaard.dk/Services/ProductService.asmx/Products??v=1.0&cId=54&locId=14916&langId=1&so=0&countryId=11&sizeId=4317&pIds=";

axios.get(url).then((response) => {

}).catch(function(err) {
	console.log(err)
})