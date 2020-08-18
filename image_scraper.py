from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import os
 
# Basic info
max_page = 2# ページ数（20枚/ページ）
dst_path = './IZONE/'
os.makedirs(dst_path, exist_ok=True)
 
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
}

# Func to download
def download(word, num_page, folder):
    
    cnt = 1
    for i in range(num_page):
        cnt += 20
        url = 'https://search.yahoo.co.jp/image/search?p={}&ei=UTF-8&b={}'.format(urllib.parse.quote(word), num_page)
    
        # Get request
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        soup = BeautifulSoup(res, features="lxml")
    
        # Scrape images in each page
        div = soup.find('div', id='gridlist')
        imgs = div.find_all('img')
    
        # Save images
        for j in range(len(imgs)):
            img = imgs[j]['src']
            tmp = urllib.request.urlopen(img)
            data = tmp.read()

            os.makedirs(dst_path+word, exist_ok=True)

            file_name = dst_path+word +'/' + 'pic_' + str(i*20+j) + '.jpg'
    
            with open(file_name, 'wb') as save_img:
                save_img.write(data)

    # Show it's done for each member
    print("{} done".format(word))


if __name__ == "__main__":
    
    words_list = ["Kwon Eunbi IZONE", "Sakura Miyawaki IZONE", "Hyewon Kang IZONE", "Yena Choi IZONE", "Cheyeon Lee IZONE", "Chewon Kim IZONE", "Minju Kim IZONE", "Nako Yabuki IZONE", "Hitomi Honda IZONE", "Yuri Choi IZONE", "Yujin Ahn IZONE", "Wonyoung Chang IZONE"]

    for word in words_list:
        download(word, max_page, dst_path+word)
