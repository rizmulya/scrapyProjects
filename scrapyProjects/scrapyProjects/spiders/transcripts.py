import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies_letter-Z"]
    # start_urls = ["https://subslikescript.com/movies"] 
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

    rules = (
        # follow all movies //ul/a
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='scripts-list']/a"), callback="parse_item", follow=True),
        # pagination (follow next button)
        Rule(LinkExtractor(restrict_xpaths="( //a[@rel='next'] )[1]"),follow=True)
    )

    def start_requests(self):
        headers = {"User-Agent": self.user_agent}
        yield scrapy.Request(url="https://subslikescript.com/movies_letter-Z", headers=headers)
        # yield scrapy.Request(url="https://subslikescript.com/movies", headers=headers)

    def parse_item(self, response):
        article = response.xpath("//article[@class='main-article']")
        transcript_list = article.xpath("./div[@class='full-script']/text()").getall()
        transcript_str = " ".join(transcript_list)
        yield {
            "title": article.xpath("./h1/text()").get(),
            "plot": article.xpath("./p/text()").get(),
            "transcript": transcript_str,
            "url": response.url
        }