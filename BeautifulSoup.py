import requests
from bs4 import BeautifulSoup, NavigableString
from bs4.element import Tag
import sys, json


# Set STDOUT Encoding to UTF-8
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

# print("α")

class TestDat():
    def __init__(self="", className="", tabName="", content="", link=""):
        self.className = className
        self.tabName = tabName
        self.content = content
        self.link = link

cookies = {
    'login_system': '1',
    'fosp_uid': 'zf4kztmiz7c8a6yn.1658049966.des',
    'fosp_aid': 'zf4kztmiz7c8a6yn.1658049966.des',
    'orig_aid': 'zf4kztmiz7c8a6yn.1658049966.des',
    'sw_version': '1',
    'readed_news': '%5B4647016%5D',
    'AB_1000000': 'A',
    'podcast_playnext': '1',
    'gocnhin_reader_list': '[4666336,4661448,4654640,4649074,4652113,4651516,4650251,4647779,4645743,4568052]',
    'device_env': '4',
    'device_env_real': '4',
    'vne_vote_39106': '138481',
    '_gtm_ps_track': '1',
    '_efr': '1699782720000',
    'fosp_loc': '19141-0-NL',
    '_ps_track_zf4kztmiz7c8a6yn.1658049966.des': '1',
}

headers = {
    'authority': 'vnexpress.net',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'login_system=1; fosp_uid=zf4kztmiz7c8a6yn.1658049966.des; fosp_aid=zf4kztmiz7c8a6yn.1658049966.des; orig_aid=zf4kztmiz7c8a6yn.1658049966.des; sw_version=1; readed_news=%5B4647016%5D; AB_1000000=A; podcast_playnext=1; gocnhin_reader_list=[4666336,4661448,4654640,4649074,4652113,4651516,4650251,4647779,4645743,4568052]; device_env=4; device_env_real=4; vne_vote_39106=138481; _gtm_ps_track=1; _efr=1699782720000; fosp_loc=19141-0-NL; _ps_track_zf4kztmiz7c8a6yn.1658049966.des=1',
    'dnt': '1',
    'referer': 'https://vnexpress.net/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://vnexpress.net/gan-5-000-ty-dong-mo-rong-nha-ga-quoc-te-t2-noi-bai-4747952.html',
    cookies=cookies,
    headers=headers,
)


soup = BeautifulSoup(response.text, 'html.parser')



description = soup.find("p", {"class": "description"})
content = soup.find("article", {"class": "fck_detail"})

TestArray = []


# Lặp qua từng phần tử div 
for child in content.children: 
    # Kiểm tra xem div có thuộc tính class không
    if isinstance(child, Tag) :
        # print("-", child)
        if isinstance(child, NavigableString):
            continue
        if ( child.has_attr('class')) :
            class_name = child.get('class')
            if (class_name == ['tplCaption']):
                src_conment= soup.find("p", {"class": "Image"}).text
                src = str(soup.find('img').get('src'))
            
                TestArray.append(TestDat(str(class_name),'image', src_conment, src))
            else:
                TestArray.append(TestDat(class_name,child.name,child.text))


# save data
data_to_save = {
    'title': soup.title.string,
    'description': description.string,
    'content': 'TestArray'
}
# with open('data.json', 'w') as json_file:
#     json.dump(data_to_save, json_file, indent=4)

print("crawl data")
print("Title: ",soup.title.string)
print("Description: ", soup.title.string)
print("Content:")
for x in range(len(TestArray)):
    print("object "+str(x))
    print(TestArray[x].className)
    print(TestArray[x].tabName)
    print(TestArray[x].content)
    if (TestArray[x].link):
        print(TestArray[x].link)
        
   

