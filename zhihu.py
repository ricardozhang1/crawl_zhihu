#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import parse
import scrapy
import re
from articlespider.items import JobboleArticleItem
from scrapy.http import Request
from utils.common import get_md5


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Host": "www.zhihu.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }

    answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    def start_requests(self):
        return [scrapy.Request(url=self.start_urls[0],headers=self.headers,cookies=get_loggin())]


    def parse(self, response):
        """提取出html页面中的所有url 并跟踪这些url进行一步爬取
            如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数"""
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # 使用lambda函数对于每一个url进行过滤，如果是true放回列表，返回false去除。
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)


    def parse_question(self,response):
        quesition_messagr = response.css('.QuestionPage meta::attr(content)').extract()
        question_name = quesition_messagr[0]
        question_url = quesition_messagr[1]
        quesition_fullid = re.match('.*?(\d+).*',question_url)
        quesition_id = int(quesition_fullid.group(1))
        keywords = quesition_messagr[2]
        answerCount = quesition_messagr[3]
        commentCount = quesition_messagr[4]
        dateCreated = quesition_messagr[5]
        dateModified = quesition_messagr[6]

        follow_visit = response.css('.NumberBoard-itemValue::attr(title)').extract()
        followerCount = follow_visit[0]
        visitorCount = follow_visit[1]

        question_item = ZhihuQuesitionItem()
        # 实例化item 对象
        question_item['question_name'] = question_name
        question_item['question_url'] = question_url

        question_item['keywords'] = keywords
        question_item['answerCount'] = answerCount
        question_item['commentCount'] = commentCount
        question_item['dateCreated'] = dateCreated
        question_item['dateModified'] = dateModified
        question_item['followerCount'] = followerCount
        question_item['visitorCount'] = visitorCount

        yield scrapy.Request(self.answer_url.format(quesition_id,20,0),headers=self.headers,callback=self.parse_answer)
        yield question_item



    def parse_answer(self,reponse):
        ans_json = json.loads(reponse.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()

            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)