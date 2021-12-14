"""
Site endpoint definition main file
- Using Flask to create rest-api endpoints to track bot status and update timestamps
- Running cronjobs on the deployed site
"""

from flask import Flask, jsonify, request
from src import CheckStock

# app definition
app = Flask(__name__)

# home endpoint
@app.route('/')
def home_page():
    return 'Home page...'

# adding product stock state as an api endpoint
@app.route('/api/stock/<product_url>')
def product_stock(product_url):
    return f'URL:{product_url}'

# test call bby_scraper
@app.route('/api/stock/bby')
def bby_stock():
    url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-ti-12gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6462956.p?skuId=6462956'
    BbyStock = CheckStock(url)
    stock_status = BbyStock.status_object()
    return stock_status


if __name__ == '__main__':
    app.run(debug=True)