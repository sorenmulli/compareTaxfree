/* Henter mine pakker ned
cheerio er til at sortere i data
puppeteer er til at hente html kode, der er blevet parced
fs er jeg ikke helt sikker på hvad gør */
const cheerio = require('cheerio');
const puppeteer = require('puppeteer');
const fs = require('fs');

/* Henter først html koden ned med puppetter */

let scrape = async() => {
  /* Åbner først browser og en page til at søge på */
  const broswer = await puppeteer.launch({headless: false});
  const page = await broser.newPage();


  /* Går nu ind på hjemmesiden, for at hente ned */
  await page.goto('https://www.bordershop.com/dk/ol-cider/dansk-ol');

  browser.close();
  return data;
};
