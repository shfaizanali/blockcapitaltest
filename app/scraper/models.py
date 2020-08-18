from pynamodb.models import Model
from pynamodb.attributes import JSONAttribute
from django.conf import settings

class BingSearch(Model):
    class Meta:
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        table_name = "dynamodb-bingsearch"

    id = JSONAttribute(hash_key=True, null=True)
    type = JSONAttribute(range_key=True, null=True)
    query_context = JSONAttribute(null=True)
    instrumentation = JSONAttribute(null=True)
    web_pages = JSONAttribute(null=True)
    entities = JSONAttribute(null=True)
    images = JSONAttribute(null=True)
    news = JSONAttribute(null=True)
    related_searches = JSONAttribute(null=True)
    videos = JSONAttribute(null=True)
