# Scrapy settings for erudite project

SPIDER_MODULES = ['erudite.spiders']
NEWSPIDER_MODULE = 'erudite.spiders'
DEFAULT_ITEM_CLASS = 'erudite.items.LearningResource'
ITEM_PIPELINES = {'erudite.pipelines.FilterWordsPipeline': 1}
