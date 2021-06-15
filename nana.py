import requests
import lxml.html
import codecs
import re

def get_sound_info(url):
    response = requests.get(url)
    html = lxml.html.fromstring(response.content.decode('utf-8'))

    page_info = {}
    page_info["image"] = html.cssselect('meta[property="og:image"]')[0].get('content')
    page_info["user_name"] = html.xpath("//div[@class='post-user-name']")[0].text_content().strip()
    page_info["icon_url"] = html.xpath("//div[@class='user-thumb']/img")[0].attrib["src"]
    page_info["user_url"] = "https://nana-music.com"+html.xpath("//div[@class='user-latest-posts__heading']")[0][0].attrib["href"]
    sound_url_base = html.xpath("/html/body/script[1]")[0].text_content().strip()
    m = re.search(r"sound_url=\"(.*?\.m4a)\"", sound_url_base)
    page_info["sound_url"] = codecs.decode(m.groups()[0], 'unicode-escape')
    
    page_info["artist_name"] = html.xpath("//div[@class='post-artist']")[0][0].text_content().strip()
    page_info["title"] = html.xpath("//div[@class='post-title']")[0][0].text_content().strip()
    page_info["play_counts"] = int(html.xpath("//li[@class='count__list-play']")[0].text_content().strip())
    page_info["applause_counts"] = int(html.xpath("//li[@class='count__list-applause']")[0].text_content().strip())
    page_info["comment_counts"] = int(html.xpath("//li[@class='count__list-comment']")[0].text_content().strip())

    return page_info

if __name__ == '__main__':
    url = "https://nana-music.com/sounds/053a0a3f"
    page_info = get_sound_info(url)
    print(page_info)

