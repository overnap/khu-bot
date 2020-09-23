# Let us process asynchronously
import asyncio
import functools
# For some simple text processing
import re
# Import crawling libraries
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# On this code, only the timeout exception is handled
from selenium.common.exceptions import TimeoutException
# For headless Firefox
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("--headless")

# Post data
class Post:

    def __init__(self, title, date, link):
        self.title = title
        self.date = date
        self.link = link
    
    def __eq__(self, other):
        return self.title == other.title and self.date == other.date

async def khu_undergraduate_crawl():

    data = []

    try:
        loop = asyncio.get_event_loop()

        # Timeout after 8 seconds of no load
        req = functools.partial(requests.get, "https://www.khu.ac.kr/kor/notice/list.do?category=UNDERGRADUATE&page=1", timeout=8)
        web = await loop.run_in_executor(None, req)
        soup = BeautifulSoup(web.content, "lxml")
        raw_data = soup.find("table", {"class": "board01"}).find("tbody").find_all("td", {"class": "col02"})
        for content in raw_data:
            # Ignore the Seoul campus mark
            if content.a.span.text == "서울":
                continue
            title = content.a.p.text.strip()
            link = "https://www.khu.ac.kr/kor/notice/" + content.a.attrs["href"]
            content = content.find_next_sibling("td", {"class": "col04"})
            date = int(content.text.replace('-', ''))
            data.append(Post(title, date, link))

    except requests.exceptions.Timeout:
        print("[Timeout] KHUS crawling timeout")
    except Exception as error:
        print("[ERROR] KHUS unknown error")
        print("Error :", error)
    finally:
        return data

async def sw_business_crawl():

    data = []

    try:
        loop = asyncio.get_event_loop()

        # Timeout after 8 seconds of no load
        req = functools.partial(requests.get, "http://swedu.khu.ac.kr/board5/bbs/board.php?bo_table=06_01", timeout=8)
        web = await loop.run_in_executor(None, req)
        soup = BeautifulSoup(web.content, "lxml")
        raw_data = soup.find_all("td", {"class": "td_num2"})
        regex1 = re.compile("종료")
        regex2 = re.compile("마감")

        for content in raw_data:
            # TODO: Notice mark identification, not used but can be used
            # notice = True if content.text.strip() == "공지" else False
            content = content.find_next_sibling("td", {"class": "td_subject"})
            # skip if there is an [END] mark
            if regex1.search(content.a.text.strip()) != None:
                continue
            elif regex2.search(content.a.text.strip()) != None:
                continue
            title = content.a.text.strip()
            link = content.a.attrs["href"]
            content = content.find_next_sibling("td", {"class": "td_datetime"})
            date = int(content.text.replace('-', ''))
            data.append(Post(title, date, link))

    except requests.exceptions.Timeout:
        print("[Timeout] SWB crawling timeout")
    except Exception as error:
        print("[ERROR] SWB unknown error")
        print("Error :", error)
    finally:
        return data

async def sw_college_crawl():

    data = []

    try:
        loop = asyncio.get_event_loop()

        # Timeout after 8 seconds of no load
        req = functools.partial(requests.get, "http://software.khu.ac.kr/board5/bbs/board.php?bo_table=05_01", timeout=8)
        web = await loop.run_in_executor(None, req)
        soup = BeautifulSoup(web.content, "lxml")
        raw_data = soup.find_all("td", {"class": "td_subject"})
        
        for content in raw_data:
            # TODO: Important mark identification, not used but can be used
            # important = True if content.text.strip() == "중요" else False
            title = content.a.text.strip()
            link = content.a.attrs["href"]
            content = content.find_next_sibling("td", {"class": "td_datetime"})
            date = int(content.text.replace('-', ''))
            data.append(Post(title, date, link))

    except requests.exceptions.Timeout:
        print("[Timeout] SWC crawling timeout")
    except Exception as error:
        print("[ERROR] SWC unknown error")
        print("ERROR :", error)
    finally:
        return data

async def j_dormitory_crawl():

    data = []

    try:
        loop = asyncio.get_event_loop()
        drv = functools.partial(webdriver.Firefox, options=options)
        driver = await loop.run_in_executor(None, drv)
    except Exception as error:
        print("[ERROR] J_DORMIT selenium firefox driver error")
        print("ERROR :", error)
        return data

    try:
        # Timeout after 90 seconds of no load
        driver.set_page_load_timeout(90)
        await loop.run_in_executor(None, driver.get, "https://dorm2.khu.ac.kr/dorm2/00/0000.kmc")

        # Waiting for web load to avoid errors
        await asyncio.sleep(2)

        soup = BeautifulSoup(driver.page_source, "lxml")
        raw_data = soup.find("ul", {"id": "board_notice"}).find_all("li")

        for content in raw_data:
            title = content.a.text.strip()
            link = "https://dorm2.khu.ac.kr/dorm2/bbs/getBbsWriteView.kmc?bbs_locgbn=K1&bbs_id=notice&seq="
            link += content.a.attrs["onclick"][8:13]
            date = int(content.span.text.replace('.', ''))
            post = Post(title, date, link)
            data.append(post)

    except TimeoutException:
        print("[Timeout] J_DORMIT crawling timeout")
    except Exception as error:
        print("[ERROR] J_DORMIT unknown error")
        print("ERROR :", error)
    finally:
        driver.quit()
        return data

async def j_meal_crawl():

    data = []
    
    try:
        loop = asyncio.get_event_loop()
        drv = functools.partial(webdriver.Firefox, options=options)
        driver = await loop.run_in_executor(None, drv)
    except Exception as error:
        print("[ERROR] J_MEAL selenium firefox driver error")
        print("ERROR :", error)
        return data
    
    try:
        # Timeout after 90 seconds of no load
        driver.set_page_load_timeout(90)
        await loop.run_in_executor(None, driver.get, "https://dorm2.khu.ac.kr/dorm2/40/4050.kmc")

        # Waiting for web load to avoid errors
        await asyncio.sleep(2)

        soup = BeautifulSoup(driver.page_source, "lxml")
        raw_data = soup.find("li", {"style": "display: list-item;"}).table.find_all("td", {"class": "bb te_left pl15"})

        for content in raw_data:
            data.append(content.text)

    except TimeoutException:
        print("[Timeout] J_MEAL crawling timeout")
    except Exception as error:
        print("[ERROR] J_MEAL unknown error")
        print("ERROR :", error)
    finally:
        driver.quit()
        return data