from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

url = 'https://www.youtube.com/c/AlexTheAnalyst/videos'
video_urls = []


def get_video_urls(url):
    # initializing selenium driver
    print('Process started...\n')
    path = '/Users/donatusprince/Development/chromedriver'
    driver = webdriver.Chrome(executable_path=path)
    driver.get(url)

    # scrolling to the bottom of the page
    for item in range(50):
        page = driver.find_element_by_tag_name('html')
        page.send_keys(Keys.END)

    # extracting data from page
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'html.parser')
    print('Extracting video urls...\n')

    # extracting and printing youtube video url from channel
    for url in soup.findAll('a', id='video-title'):
        video_urls.append('https://www.youtube.com' + url.get('href'))
    print('Printing results...\n')
    print(f'This youtube channel has {len(video_urls)} videos published')

    # close browser
    driver.quit()

if __name__ == '__main__':
    get_video_urls(url)