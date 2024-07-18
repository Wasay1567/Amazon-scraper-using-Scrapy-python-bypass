import scrapy



class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    start_urls = ["https://www.amazon.com/s?i=specialty-aps&srs=17900676011&rh=n%3A17900676011&fs=true&ref=lp_17900676011_sar"]


    def start_requests(self):
        keyword_list = ['ipad']
        for keyword in keyword_list:
            amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
            yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls)



    def discover_product_urls(self, response):
        products = response.css('div.s-result-item[data-component-type=s-search-result]')
        for product in products:
            relative_url = product.css('h2>a::attr(href)').get()
            product_url = "https://www.amazon.com/" + relative_url
            yield scrapy.Request(url=product_url, callback=self.parse_product_data)

    def parse_product_data(self, response):
        product_title = response.css('#productTitle::text').get()
        product_price = response.css('#corePrice_desktop span::text').get()
        product_reviews = response.css('#acrCustomerReviewText::text').get()
        stars = response.css('#acrPopover .a-color-base ::text').get()
        image_link = response.css('span[data-action="main-image-click"] img::attr(href)')
        yield {
            'name' : product_title,
            'price' : product_price,
            'stars' : stars,
            'reviews' : product_reviews,
            'image_url' : image_link
        }


