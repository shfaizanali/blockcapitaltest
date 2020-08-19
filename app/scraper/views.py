import scrapy
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
import json

from .models import BingSearch

class BingSpider(scrapy.Spider):
    name = "bing"

    def start_requests(self):
        print(self.keyword)
        print(self.ob_id)
        urls = [
            'https://api.cognitive.microsoft.com/bing/v7.0/search?q={}'.format(self.keyword),
        ]
        headers = {
            'Ocp-Apim-Subscription-Key': '73125de7982949b49d2704d8290313e1'
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        data = json.loads(response.text)

        if not BingSearch.exists():
            BingSearch.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

        bing_search = BingSearch()
        bing_search.id = 'None'
        bing_search.type = data.get('_type', 'None')
        bing_search.query_context = data.get('queryContext', 'None')
        bing_search.instrumentation = data.get('instrumentation', 'None')
        bing_search.web_pages = data.get('webPages', 'None')
        bing_search.entities = data.get('entities', 'None')
        bing_search.images = data.get('images', 'None')
        bing_search.news = data.get('news', 'None')
        bing_search.related_searches = data.get('relatedSearches', 'None')
        bing_search.videos = data.get('videos', 'None')
        bing_search.save()

@csrf_exempt
def bing_scraper(request):
    keyword = request.GET.get('keyword', False)

    if keyword:
        try:

            n = random.randint(0, 999)
            runner = CrawlerRunner()
            d = runner.crawl(BingSpider, keyword=keyword, ob_id=n)
            d.addBoth(lambda _: reactor.stop())
            reactor.run()

            bing_search = BingSearch.scan(rate_limit=15)

            list = []
            for data in bing_search:
                list.append(data.convert())

            json_data = json.dumps(list)
            return JsonResponse({'error': False, 'data': json_data})

        except Exception as e:
            return JsonResponse({'error': True, 'message': str(e)})
    else:
        return JsonResponse({'error': False, 'message': 'Keyword param is missing.'})
