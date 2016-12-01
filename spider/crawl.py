# coding=utf-8
import urllib2
from bs4 import BeautifulSoup
from bs4 import Comment
import string
from urlparse import urlparse
from nltk.tokenize import PunktSentenceTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import networkx as nx
import re

def fetch_source(url):
    "fetches the page content(html) from the given url"
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(url, None, headers)
    try:
        response = urllib2.urlopen(req)
        page = response.read()
        response.close()
    except:
        page = ""
    return page


def extract_hyperlink(soup, url):
    "returns the list of hyperlinks from bs4 soup"
    links = soup.find_all('a')
    linklist = []
    for tag in links:
        link = tag.get('href', None)
        if link is not None:
            if link[0] != '#':
                if link[0] != '/':
                    linklist.append(link.encode("UTF-8"))
                else:
                    parsed_uri = urlparse(url)
                    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                    linklist.append(domain + link.encode("UTF-8"))
    linklist = list(set(linklist))
    linklist = "{}".join(linklist)
    return linklist


def visible(element):
    "filter for extracting page's main content"
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'a', 'h1', 'h2', 'h3', 'h4', 'h5',
                               'h6']:
        return False
    elif isinstance(element, Comment):
        return False
    return True


def extract_content(soup):
    "returns the main content visible in the page"
    texts = soup.find_all(text=True)
    # print texts
    visible_texts = filter(visible, texts)
    # print visible_texts
    visible_texts = " ".join(visible_texts)
    # print visible_texts
    visible_texts = visible_texts.encode("UTF-8")
    # print visible_texts
    # visible_texts = visible_texts.replace('\n','')
    visible_texts = ''.join(ch for ch in visible_texts if ch.isalnum() or ch == ' ' or ch == '.')
    #print visible_texts
    return visible_texts


def wordCount(s, keywords,flag):
    if flag==0:
        # s is the sentence
        words = s.split()
        lw = len(words)
        lk = len(keywords)
        s = 0
        for i in range(0, lk):
            for j in range(0, lw):
                if keywords[i].lower() == words[j].lower():
                    s += 1
        return s
    else:
        # s is the sentence
        words = s.split()
        lw = len(words)
        lk = len(keywords)
        s = []
        for i in range(0, lk):
            s.append(0)
        for i in range(0, lk):
            for j in range(0, lw):
                if keywords[i].lower() == words[j].lower():
                    s[i] += 1
        count = 0
        for i in range(0, lk):
            if s[i] != 0:
                count += 1
        return count


def score(content, keywords):
    """
        score the content by its relavance to the keywords
        content = HTML string after removing (style,javascript,head,title)
        keywords = [] , list of keywords(string)
    """
    document = content
    keyword_length = len(keywords)
    k_present = wordCount(document, keywords, 1)
    k_exist_factor = float(k_present)/keyword_length
    print('Count = ',keyword_length)
    print('Present = ', k_present)
    print("Exist factor =",k_exist_factor)

    document = ' '.join(document.strip().split('\n'))
    tokenizer = PunktSentenceTokenizer()
    sentences = tokenizer.tokenize(document)  # tokenizing i.e. splitting the page into sentences.
    # Finding the bag of words i.e. count of each word in each sentence.
    # The row of each matrix are the sentences, columns are the words
    vectorizer = CountVectorizer()
    bow_mat = vectorizer.fit_transform(sentences)

    # reweighing the sentence using tf-idf. Will diminish the effect of common words in each sentence
    normalized_matrix = TfidfTransformer().fit_transform(bow_mat)

    similarity = normalized_matrix * normalized_matrix.T
    # similarity matrix is a mirrored matrix where each row & column corresponds
    # to sentences and the elements describe how similar each sentence is wrt each other. 1=exactly same, 0=no overlap

    # now we use textRank on the graph similarity
    text_rank_graph = nx.from_scipy_sparse_matrix(similarity)
    scores = nx.pagerank(text_rank_graph)

    # sorting the sentences in the webpage according to textrank score
    # ranked[][0]= score, ranked[][1]= corresponding sentence
    ranked = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    t_rank_factor = 0
    lim = len(ranked)*0.40
    lim = int(lim)
    print('Total=', len(ranked))
    print('Limit=', lim)
    for i in range(0, lim):
        t_rank_factor += ranked[i][0]
    print('Text rank factor =', t_rank_factor)
    t_rank_freq = 0
    for i in range(0, lim):
        t_rank_freq+= wordCount(ranked[i][1],keywords,0)
    print('Text rank freq=', t_rank_freq)

    # EQUATION can be changed
    final_score = k_exist_factor * t_rank_factor * t_rank_freq
    print('Final score =', final_score)
    return final_score  # testing value


def scrape(url, keywords):
    source = fetch_source(url)
    if source != "":
        soup = BeautifulSoup(source, "html.parser")
        hyperlinks = extract_hyperlink(soup, url)
        content = extract_content(soup)
        relavance_score = score(content, keywords)
        data = hyperlinks + "||" + str(relavance_score) + "||" + content
    else:
        data = "Invalid"
    return data


scrape("http://www.rogerebert.com/reviews/scarface-1983", ['cuban','tony','al','pacino','cocaine','say','hello','to','my','little','friend'])