import re

from src.app.library.libparser import HtmlParser
# from src.app.service.requester import Requester
from src.app.utility.utility import Utilities
from src.app.utility.summarize import Summarize
from typing import *

class CleverScrapper:
    def __init__(self) -> None:
        
        self.parser = HtmlParser()
        # self.req = Requester()
        self.next = False
    
    def iNewsLL(self, **kwargs):
        '''
        Gets the URLs from the HTML response and 
        returns a list containing values in the form of article URLs.

        Arguments :
          - :mod:`html` (str): response content decoded to string
        '''
        RAW_DATA = kwargs.get("html")

        DIV = self.parser.pyq_parser(
            html=RAW_DATA,
            selector='div[class="col-lg-9 col-md-12 col-sm-12 col-xs-9"]'
        )

        URLlIST = [
            url.attr("href")
            for url in self.parser.pyq_parser(
                html=DIV, selector='div[class="news-feed"] ul[id="news-list"]'
            ).find('li[class="padding-10px-all"] a').items()
        ]

        NEXT_PAGE = self.parser.pyq_parser(html=DIV, selector='div[class="paging"] a').eq(1).attr("href")
        if NEXT_PAGE: NEXT_PAGE = re.search(pattern=r'/(\d+)$', string=NEXT_PAGE).group(1)

        return URLlIST, NEXT_PAGE
    
    def kompasLL(self, **kwargs):
        '''
        '''
        RAW_DATA = kwargs.get("html")

        # with open("result.html", "w") as file:
        #     file.write(RAW_DATA)
        DIV = self.parser.pyq_parser(
            html=RAW_DATA,
            selector='div[class="row mt2 col-offset-fluid clearfix"] div[class="col-bs10-7"] div[class="sectionBox"]'
        )

        TEST = self.parser.pyq_parser(
            html=DIV,
            selector='div[class="articleList -list"] div[class="articleItem"]'
        )

        # URLIST = [
        #     url.attr("href")
        #     for url in self.parser.pyq_parser(
        #         html=RAW_DATA, selector='div[class="articleList -list"]'
        #     ).find('div[class="articleItem"] a[class="article-link"]').items()
        # ]

        return TEST

    def iNewsCS(self, **kwargs):
        '''
        Take the necessary data.

        Arguments :
            - :mod:`html` (str): response content decoded to string
        '''
        data = dict()
        RAW_DATA = kwargs.get("html")
        URL = kwargs.get("url")

        ID = Utilities.hashTomd5(string=URL)
        SOURCE = Utilities.webName(string=URL)

        DIV = self.parser.pyq_parser(html=RAW_DATA, selector='div[class="col-lg-9 col-md-8 col-sm-7 col-xs-9"] div[class="row"]')

        JUDUL = self.parser.pyq_parser(html=DIV, selector='div[class="col-lg-12 col-md-12 col-sm-12 col-xs-12"] h1').text()
        AUTHOR_NAME = self.parser.pyq_parser(html=DIV, selector='div[class="author"] a[class="author-profile"] img[class="lazy"]').attr("title")
        AUTHOR_LINK = self.parser.pyq_parser(html=DIV, selector='div[class="author"] a[class="author-profile"]').attr("href")
        PUBLISH_DATE = self.parser.pyq_parser(html=DIV, selector='div[class="col-lg-12 col-md-12 col-sm-12 col-xs-12"] div[class="author"] a[class="author-profile"] time').attr("datetime")
        THUMBNAIL = self.parser.pyq_parser(html=DIV, selector='div[class="width-100 height-100 object-fit-cover"] img').attr("src")
        if not THUMBNAIL: THUMBNAIL = self.parser.pyq_parser(html=DIV, selector='div[class="col-lg-12 col-md-12 col-sm-12 col-xs-12"] div[class="gallery"] img').attr("src")
        THUMBNAIL_CAPTION = self.parser.pyq_parser(html=DIV, selector='div[class="col-lg-12 col-md-12 col-sm-12 col-xs-12"] div[class="caption-news justify-text"] span[class="img-clearx"]').text()
        if not THUMBNAIL_CAPTION: THUMBNAIL_CAPTION = self.parser.pyq_parser(html=DIV, selector='div[class="col-lg-12 col-md-12 col-sm-12 col-xs-12"] div[class="gallery"] div[class="caption-photos"] p').text()
        BODY_TEXT = self.parser.pyq_parser(html=DIV, selector='div[class="body-text-news"] div[itemprop="articleBody"]')
        if not BODY_TEXT: BODY_TEXT = self.parser.pyq_parser(html=DIV, selector='div[class="col-lg-10 col-md-10 col-sm-10 col-xs-10"] div[class="gallery"] div[class="body-text-photo"] div[class="text-photo justify-text"]')
        EDITOR = re.search(pattern=r'<b>Editor\s:\s(.*?)</b>', string=str(BODY_TEXT))
        if EDITOR: EDITOR = EDITOR.group(1)
        TAGS = [
            tag.text()
            for tag in self.parser.pyq_parser(
                html=DIV, selector='div[class="body-text-news"] div[itemprop="articleBody"] div[class="tag"]'
            ).find('a').items()
        ]
        if not TAGS: TAGS = [
            tag.text()
            for tag in self.parser.pyq_parser(
                html=DIV, selector='div[class="body-text-photo"] div[class="text-photo"] div[class="tag"]'
            ).find('a').items()
        ]
        SUMMARY = ""
        RAW_CONTENT = BODY_TEXT.eq(0).find("p").text()
        CONTENT = re.search(r'[A-Z]+[,]*\siNews.id\s-\s(.*?)\sEditor.+[Google News]*', string=RAW_CONTENT)
        if CONTENT:
            CONTENT = CONTENT.group(1)
            SUMMARY = Summarize.summarize(text=CONTENT)
        try:
            DESC = CONTENT[:100] + "..."
        except TypeError:
            DESC = ""

        data.update({
            "id": ID,
            "link": URL,
            "source": SOURCE,
            "title": JUDUL,
            "author_name": AUTHOR_NAME,
            "author_link": AUTHOR_LINK,
            "publish_date": PUBLISH_DATE,
            "thumbnail": THUMBNAIL,
            "thumbnail_caption": THUMBNAIL_CAPTION,
            "content": CONTENT,
            "summary": SUMMARY,
            "description": DESC,
            "editor": EDITOR,
            "tags": TAGS
        })
        return data

    def tribunNewsLL(self, **kwargs):
        '''
        '''
        RAW_DATA = kwargs.get("html")
        
        DIV = self.parser.pyq_parser(
            html=RAW_DATA,
            selector='div[class="main"] div[class="content"] div[class="fl w677"] div[class="bsh ovh"] div[class="p2030"]'
        )

        URLIST = [
            url.attr("href")
            for url in self.parser.pyq_parser(
                html=DIV, selector='div[class="pt10 pb10"] ul[class="lsi"]'
            ).find('li[class="ptb15"] h3[class="f16 fbo"] a').items()
        ]
        return URLIST
    
    def tribunNewsCS(self, **kwargs):
        '''
        '''
        data = dict()
        RAW_DATA = kwargs.get("html")
        URL = kwargs.get("url")

        ID = Utilities.hashTomd5(string=URL)
        SOURCE = Utilities.webName(string=URL)

        DIV = self.parser.pyq_parser(
            html=RAW_DATA,
            selector='div[class="main"] div[class="content"] div[class="fl w677"] div[class="bsh mb20"] div[id="article"]'
        )

        JUDUL = self.parser.pyq_parser(html=DIV, selector='h1[id="arttitle"]').text()
        PUBLISH_DATE = self.parser.pyq_parser(html=DIV, selector='div[class="mt10"] time').text()
        return JUDUL, PUBLISH_DATE