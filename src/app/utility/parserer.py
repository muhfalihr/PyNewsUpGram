import re

from src.app.library.libparser import HtmlParser
# from src.app.service.requester import Requester
from src.app.utility.utility import Utilities
from src.app.utility.summarize import Summarize

from typing import *
from datetime import datetime
from googletrans import Translator

class CleverScrapper:
    def __init__(self) -> None:
        
        self.parser = HtmlParser()
        self.translate = Translator()
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
        RAW_DATA, URL = kwargs.get("html"), kwargs.get("url")

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
            "editor_name": EDITOR,
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
            url.attr("href") + "?page=all"
            for url in self.parser.pyq_parser(
                html=DIV, selector='div[class="pt10 pb10"] ul[class="lsi"]'
            ).find('li[class="ptb15"] h3[class="f16 fbo"] a').items()
        ]
        return URLIST
    
    def tribunNewsCS(self, **kwargs):
        '''
        '''
        data = dict()
        RAW_DATA, URL = kwargs.get("html"), kwargs.get("url")

        ID = Utilities.hashTomd5(string=URL)
        SOURCE = Utilities.webName(string=URL)

        DIV = self.parser.pyq_parser(
            html=RAW_DATA,
            selector='div[class="main"] div[class="content"] div[class="fl w677"] div[class="bsh mb20"] div[id="article"]'
        )

        JUDUL = self.parser.pyq_parser(html=DIV, selector='h1[id="arttitle"]').text()
        RAW_PUB_DATE = self.parser.pyq_parser(html=DIV, selector='div[class="mt10"] time').text()
        AUTHOR_NAME = self.parser.pyq_parser(html=DIV, selector='div[class="mt10"] div[class="f20 credit mt10"] h6 div[id="penulis"] a').text()
        AUTHOR_LINK = self.parser.pyq_parser(html=DIV, selector='div[class="mt10"] div[class="f20 credit mt10"] h6 div[id="penulis"] a').attr("href")
        EDITOR = self.parser.pyq_parser(html=DIV, selector='div[class="mt10"] div[class="f20 credit mt10"] h6 div[id="editor"] a').text()
        EDITOR_LINK = self.parser.pyq_parser(html=DIV, selector='div[class="mt10"] div[class="f20 credit mt10"] h6 div[id="editor"] a').attr("href")
        THUMBNAIL = self.parser.pyq_parser(html=DIV, selector='div[id="article_con"] div[id="artimg"] div[class="pb20 ovh"] div[class="ovh imgfull_div"] a[class="glightbox"] img').attr("src")
        THUMBNAIL_CAPTION = self.parser.pyq_parser(html=DIV, selector='div[id="article_con"] div[id="artimg"] div[class="pb20 ovh"] div[class="arial f12 pt5 grey2"]').text()
        
        BODY_TEXT = self.parser.pyq_parser(html=DIV, selector='div[id="article_con"] div[class="side-article txt-article multi-fontsize"]')
        BODY_TEXT = re.sub(r'<p class="baca">.*?</p>', '', BODY_TEXT.__str__())
        RAW_DATA = self.parser.pyq_parser(html=BODY_TEXT, selector='p').text() if BODY_TEXT else ''
        CONTENT = re.sub(r'^(\b[A-Z]+[\.]*[A-Z]+[\s]*-[\s]*\b|\b[A-Z]+[\.]*[A-Z]+\b[,]*\s\b[A-Z]+[\s]*-[\s]*\b|Laporan\sWartawan\sTribunnews\.com[,]*\s.+\b[A-Z]+[\.]*[A-Z]+\b[,]*\s\b[A-Z]+[\s]*-[\s]*\b)', '', RAW_DATA)
        
        RAW_PUB_DATE = self.translate.translate(text=RAW_PUB_DATE, src="id").text if RAW_PUB_DATE else ""
        RAW_PUB_DATE = re.sub(r'\sWIB$', '', RAW_PUB_DATE)
        PUBLISH_DATE = datetime.strptime(RAW_PUB_DATE, "%A, %B %d, %Y %H:%M").strftime("%Y-%m-%d %H:%M:%S") if RAW_PUB_DATE else ""
        
        TAGS = [
            tag.text()
            for tag in self.parser.pyq_parser(
                html=DIV, selector='div[id="article_con"] div[class="side-article mb5"] div[class="mb10 f16 ln24 mb10 mt5"]'
            ).find('h5[class="tagcloud3"] a').items()
        ]
        if CONTENT:
            DESC = CONTENT[:100] + "..."
            SUMMARY = Summarize.summarize(text=CONTENT)
        else:
            DESC = ""
            SUMMARY = ""
        
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
            "editor_name": EDITOR,
            "editor_link": EDITOR_LINK,
            "tags": TAGS
        })
        return data