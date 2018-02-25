# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader


class PicturespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ZhihuQuesitionItem(scrapy.Item):
    question_name = scrapy.Field()
    question_url = scrapy.Field()
    keywords = scrapy.Field()
    answerCount = scrapy.Field()
    commentCount = scrapy.Field()
    dateCreated = scrapy.Field()
    dateModified = scrapy.Field()
    followerCount = scrapy.Field()
    visitorCount = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
                    insert into text_06(question_name,question_url,keywords,answerCount,commentCount,dateCreated,dateModified,followerCount,visitorCount) VALUES (%s, %s, %s, %s,%s, %s, %s,%s,%s)
                """

        params = (self['question_name'],self['question_url'],self['keywords'],self['answerCount'],self['commentCount'],self['dateCreated'],self['dateModified'],self['followerCount'],self['visitorCount'])
        return insert_sql,params


class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                            insert into text_07(zhihu_id,url,question_id,author_id,parise_num,comments_num,create_time,update_time) VALUES (%s, %s, %s, %s,%s, %s, %s,%s)
                        """

        params = (self['zhihu_id'],self['url'],self['question_id'],self['author_id'],self['parise_num'],self['comments_num'],self['create_time'],self['update_time'])
        return insert_sql,params