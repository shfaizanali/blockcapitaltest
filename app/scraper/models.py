from pynamodb.models import Model
from pynamodb.attributes import JSONAttribute, UnicodeAttribute
from django.conf import settings


class BingSearch(Model):
    class Meta:
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        table_name = "dynamodb-bingsearch"

    id = UnicodeAttribute(hash_key=True, null=True)
    type = JSONAttribute(range_key=True, null=True)
    query_context = JSONAttribute(null=True)
    instrumentation = JSONAttribute(null=True)
    web_pages = JSONAttribute(null=True)
    entities = JSONAttribute(null=True)
    images = JSONAttribute(null=True)
    news = JSONAttribute(null=True)
    related_searches = JSONAttribute(null=True)
    videos = JSONAttribute(null=True)

    def save(self):
        if not BingSearch.exists():
            BingSearch.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
        else:
            print('already created')

        super(BingSearch, self).save()

    def convert(self):
        data = {
            'id': self.id,
            'type': self.type,
            'query_context': self.query_context,
            'instrumentation': self.instrumentation,
            'web_pages': self.web_pages,
            'entities': self.entities,
            'images': self.images,
            'news': self.news,
            'related_searches': self.related_searches,
            'videos': self.videos
        }
        return data
