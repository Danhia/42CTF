from django import template
from django.core.files.storage import default_storage

register = template.Library()

@register.simple_tag
def get_news_by_lang(news, lang):
	filepath = "home/templates/news/"+ lang + "/" + news.slug + ".html"
	try:
		with open(filepath) as fp:
			return fp.read()
	except:
		return news.content_en