import scrapy

class OtoEnbacSpider(scrapy.Spider):
    name = "enbac_car"
    allowed_domains = ["oto.enbac.com"]
    start_urls = ["https://oto.enbac.com/Da-Nang/c331/Xe-hoi"]

    def parse(self, response):
        items = response.css("li._JS_EB_ITEM")

        if not items:
            self.crawler.engine.close_spider(self)
            return

        for item in items:
            yield {
                "car_name": item.css("h3.ititle a span::text").get().strip() if item.css("h3.ititle a span::text").get() else None,
                "price": item.css(".price_r span::text").get(),
                "link": item.css(".ititle a::attr(href)").get(),
                "image": item.css(".ithumb a.photolarger::attr(href)").get(),
                "seller": item.css(".iuser a.iuavatar::attr(title)").get(),
                "place_of_sale": item.css(".icity span[title='Nơi đăng']::text").get(),
                "upload_time": item.css(".icity span[title='Thời gian up tin']::text").get(),
                "view": item.css("div.iview *::text").getall()[-1].strip() if item.css("div.iview *::text").getall() else None
            }

        next_page = response.css(".paging_next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
