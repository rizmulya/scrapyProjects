import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # # follow all countries //td/a
            # absolute url
            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url=absolute_url)
            # relative url
            yield response.follow(url=link, callback=self.parse_meter, meta={"country":country_name})
    
    def parse_meter(self, response):
        country = response.request.meta["country"]

        rows = response.xpath("(//table[contains(@class, 'table')] )[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield {
                "country": country,
                "year": year,
                "population": population,
            }
