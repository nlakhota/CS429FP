from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlingSpider(CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["toscrape.com"]
    start_urls = ["http://books.toscrape.com"]
    max_pages_input = int(input("How many pages would like to crawl?: "))
    max_pages = max_pages_input  # Maximum number of pages to crawl
    crawled_pages = 0  # Variable to keep track of crawled pages

    rules = (
        Rule(LinkExtractor(allow="catalogue/category")),
        Rule(LinkExtractor(allow="catalogue", deny="category"), callback="parse_item")
    )

    def parse_item(self, response):
        # Check if the maximum pages limit has been reached
        if self.crawled_pages >= self.max_pages:
            self.logger.info("Maximum pages limit reached. Crawling stopped.")
            return

        # Extracting data from the page
        yield {
            "upc": response.css(".table-striped td::text")[0].get(),
            "title": response.css(".product_main h1::text").get(),
            "price": response.css(".price_color::text").get(),
            "availability": response.css(".availability::text")[1].get().replace("\n", "").replace(" ", "").replace("In", "").replace("stock","").replace("available","").replace("(","").replace(")",""),
            "product description": response.css(".product_page p::text")[10].get().replace(" ...more", "")
        }
        # Increment the count of crawled pages
        self.crawled_pages += 1

    # Override the parse method to handle the maximum depth
    def _parse_response(self, response, callback, cb_kwargs, follow=True):
        depth = response.meta.get('depth', 1)
        if depth > 2:  # Maximum depth limit
            self.logger.info("Maximum depth limit reached. Skipping further links.")
            return

        return super()._parse_response(response, callback, cb_kwargs, follow)
