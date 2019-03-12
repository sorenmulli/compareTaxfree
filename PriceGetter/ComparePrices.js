const cheerio = require('cheerio');
const axios = require('axios');
const fs = require('fs'); 

const borderPrices = JSON.parse(fs.readFileSync( "/Users/Moesen/Git/NodeScraber/BorderAPIGetter/AllPricesBordersShop.json" ));
