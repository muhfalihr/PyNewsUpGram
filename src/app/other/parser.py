import re

from src.app.library.libparser import HtmlParser
from src.app.service.inews.service import iNews
from src.app.utility import Utilities
from typing import *

class CleverScrapper:
    def __init__(self) -> None:
        
        self.parser = HtmlParser()
        self.inews = iNews()
        self.next = False
    
    def iNewsLL(self, **kwargs):
        '''
        Gets the URLs from the HTML response and 
        returns a list containing values in the form of article URLs.

        Arguments :
          - :mod:`html` (str): response content decoded to string
        '''
        raw_data = kwargs.get("html")

        DIV = self.parser.pyq_parser(
            html=raw_data,
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

    def iNewsCS(self, **kwargs):
        '''
        Take the necessary data.

        Arguments :
            - :mod:`html` (str): response content decoded to string
        '''
        URLlIST, NEXT_PAGE = self.iNewsLL(**kwargs)

        datas = []
        
        for url in URLlIST:
            if "/multimedia/video/" in url: continue
            
            data = dict()

            ID = Utilities.hashTomd5(string=url)
            SOURCE = Utilities.webName(string=url)

            RESP = self.inews.requester(method="GET", url=url, timeout=120)
            RAW_DATA: str = Utilities.raw(content=RESP.content, html=True)

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
            RAW_CONTENT = BODY_TEXT.eq(0).find("p").text()
            CONTENT = re.search(r'[A-Z]+[,]*\siNews.id\s-\s(.*?)\sEditor.+[Google News]*', string=RAW_CONTENT)
            if CONTENT: CONTENT = CONTENT.group(1)
            try:
                DESC = CONTENT[:100] + "..."
            except TypeError:
                DESC = ""

            data.update({
                "id": ID,
                "link": url,
                "source": SOURCE,
                "title": JUDUL,
                "author_name": AUTHOR_NAME,
                "author_link": AUTHOR_LINK,
                "publish_date": PUBLISH_DATE,
                "thumbnail": THUMBNAIL,
                "thumbnail_caption": THUMBNAIL_CAPTION,
                "content": CONTENT,
                "description": DESC,
                "editor": EDITOR,
                "tags": TAGS
            })
            datas.append(data)
        
        fixdatas = {
            "datas": datas,
            "nextpage": NEXT_PAGE
        }

        return fixdatas