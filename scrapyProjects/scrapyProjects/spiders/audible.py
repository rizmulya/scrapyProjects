import scrapy


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/adblbestsellers?ref_pageloadid=not_applicable&ref=a_search_b1_desktop_footer_column_2_0&pf_rd_p=6a55a63d-48d3-4d5e-857f-ae6682380e4d&pf_rd_r=Z1ZAF1S6QSK94TGKKY6P&pageLoadId=lRMD5WIQBwoaTcf9&ref_plink=not_applicable&creativeId=2d835e86-1f10-4f6e-a4c6-33d2001684e6"] 
    # start_urls = ["https://www.audible.com/search"]

    def parse(self, response):
        productListItem = response.xpath("//div[@class='adbl-impression-container ']//li[contains(@class, 'productListItem')]")
        for product in productListItem:
            title = product.xpath(".//h3[contains(@class, 'bc-heading')]/a/text()").get()
            author = product.xpath(".//li[contains(@class, 'authorLabel')]/span/a/text()").get()
            length = product.xpath(".//li[contains(@class, 'runtimeLabel')]/span/text()").get()
            length = length.replace("Length: ", "")

            yield {
                "title": title,
                "author": author,
                "length": length
            }

        # multiple page
        pagination = response.xpath("//ul[contains(@class, 'pagingElements')]")
        next_page_url = pagination.xpath(".//span[contains(@class, 'nextButton')]/a/@href").get()
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse)
