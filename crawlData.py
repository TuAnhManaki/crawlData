import requests
from bs4 import BeautifulSoup, NavigableString
from bs4.element import Tag

import sys, json


# Set STDOUT Encoding to UTF-8
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

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
# Tải nội dung HTML từ URL chính để phân tích nội dung HTML bằng BeautifulSoup
def download_parse_html():
    # Kiểm tra xem đây là URL hay tệp cục bộ
    if url.startswith("http"):
        # Lấy nội dung HTML của trang web
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text

            # Phân tích nội dung HTML bằng BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            return soup
        else:
            print("Không thể lấy dữ liệu từ trang web.")        
    
# Hàm để crawl dữ liệu từ trang web và lưu vào file JSON
def crawl_and_save(output_file):
    #   
    soup = download_parse_html()
    if not soup:
        return
    # Trích xuất thông tin cần thiết từ trang web
    items = []
    for  index, item in enumerate(soup.find_all('article', class_='item-news')):
        if (index == 5):
            break
        title = item.find('h3').text.strip()
        link = item.find('a')['href']
        items.append({"title": title, "link": link})
    
    # Lưu thông tin vào một cấu trúc dữ liệu Python
    data = {"items": items}
    
    # Ghi cấu trúc dữ liệu Python vào file JSON
    with open(output_file, 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)
    print("Dữ liệu đã được lưu vào", output_file)
    
    for item in items:  
        soup = download_parse_html()
        print("Crawl data website: ", item["link"])
        print("Title: ", item["title"])
        crawl_Data(item)
        
        # Convert the BeautifulSoup object to a string
        html_content = soup.prettify()
        save_html_to_file(html_content, "raw_htmls/" + str(item["title"]) + ".html")
    
def crawl_Data(item):
    # Lấy nội dung HTML của trang web
    response = requests.get(
        item["link"],
        cookies=cookies,
        headers=headers,
    )
    if response.status_code == 200:
        # Phân tích nội dung HTML bằng BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print("Không thể lấy dữ liệu từ trang web.")  
        
    description = soup.find("p", {"class": "description"})
    content = soup.find("article", {"class": "fck_detail "})

    description = soup.find("p", {"class": "description"})
    content = soup.find("article", {"class": "fck_detail"})

    # print("content: ",description)  
    # print("content1: ",content)  
    # print("content: ",description)  

    crawlData = []
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
                    src_conment= child.find("p", {"class": "Image"}).text
                    src = child.find('img')['src']

                    # crawlData.append(str(class_name),'image', src_conment, src))
                    crawlData.append({
                        "className": class_name,
                        "tabName": 'image',
                        "content": src_conment,
                        "link": src
                    })
                else:
                    crawlData.append({
                        "className": class_name,
                        "tabName": child.name,
                        "content": child.text,
                    })

    # save data
    data_to_save = {
        'title': soup.title.string,
        'description': description.string,
        'content': crawlData
    }
    with open( "articles/" + str(item["title"]) + ".json", 'w', encoding="utf-8") as json_file:
        json.dump(data_to_save, json_file, indent=4)


# Hàm để lưu nội dung HTML vào một tệp HTML mới
def save_html_to_file(html_content, output_file_path):
    with open(output_file_path, 'w', encoding="utf-8") as file:
        file.write(html_content)


# URL của trang web bạn muốn crawl
url = 'https://vnexpress.net/'
# Tên của tệp JSON bạn muốn lưu dữ liệu vào
output_file = 'data.json'


# Gọi hàm crawl_and_save để crawl dữ liệu và lưu vào file JSON
crawl_and_save(output_file)