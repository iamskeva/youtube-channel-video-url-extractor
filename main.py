from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

url = 'https://www.youtube.com/c/AlexTheAnalyst/videos'
path = '/Users/donatusprince/Development/chromedriver'
video_urls = []


def get_video_urls(url):
    # initializing selenium driver
    print('Process started...\n')
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
    for link in soup.findAll('a', id='video-title'):
        video_urls.append('https://www.youtube.com' + link.get('href'))
    print('Printing results...\n')
    print(f'This youtube channel has {len(video_urls)} videos published')

    # close browser
    driver.quit()


def extract_info(url):
    get_video_urls(url)
    print('\nNow extracting video information...', '\n')

    for link in video_urls:
        # initializing selenium driver
        driver = webdriver.Chrome(executable_path=path)
        driver.get(link)
        # scrolling to the bottom of the page
        time.sleep(5)
        driver.find_element_by_tag_name('html').send_keys(Keys.PAGE_DOWN)

        # extracting video information
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'html.parser')
        video_url = link
        youtube_name = soup.find('a', class_='yt-simple-endpoint style-scope yt-formatted-string').text
        subscribers = soup.find('yt-formatted-string', id='owner-sub-count').text
        published = driver.find_element_by_xpath('//*[@id="info-strings"]/yt-formatted-string').text
        title = soup.find('yt-formatted-string', class_='style-scope ytd-video-primary-info-renderer').text
        views = soup.find('span', class_='view-count style-scope ytd-video-view-count-renderer').text
        likes = soup.findAll('yt-formatted-string', class_='style-scope ytd-toggle-button-renderer style-text')[0].text
        dislikes = soup.findAll('yt-formatted-string', class_='style-scope ytd-toggle-button-renderer style-text')[
            1].text
        comment = driver.find_element_by_xpath("//*[@id='count']/yt-formatted-string/span[1]").text

        driver.quit()
        with open('videos.txt', 'a') as f:
            f.write(
                f'{youtube_name} > {subscribers} > {published} > {title} > {views} > {likes} > {dislikes} > {comment} > {video_url}\n')

    print('All video information has being extracted successfully')


if __name__ == '__main__':
    get_video_urls(url)