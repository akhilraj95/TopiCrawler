import urllib2
from bs4 import BeautifulSoup
from bs4 import Comment
import string

def fetch_source(url):
    "fetches the page content(html) from the given url"
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    return page


def extract_hyperlink(soup):
    "returns the list of hyperlinks from bs4 soup"
    links = soup.find_all('a')
    linklist = []
    for tag in links:
        link = tag.get('href',None)
        if link is not None:
            linklist.append(link)
    linklist = list(set(linklist))
    return linklist

def visible(element):
    "filter for extracting page's main content"
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif isinstance(element,Comment):
        return False
    return True

def extract_content(soup):
    "returns the main content visible in the page"
    texts = soup.find_all(text = True)
    visible_texts = filter(visible, texts)
    visible_texts = " ".join(visible_texts)
    visible_texts = visible_texts.encode("UTF-8")
    visible_texts = visible_texts.replace('\n','')
    visible_texts = ''.join(ch for ch in visible_texts if ch.isalnum() or ch == ' ')
    return visible_texts

def scrape(url):
    source = fetch_source(url)
    soup = BeautifulSoup(source,"html.parser")
    hyperlinks = extract_hyperlink(soup)
    content = extract_content(soup)
    return content
