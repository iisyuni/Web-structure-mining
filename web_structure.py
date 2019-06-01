import pandas as pd

import requests
from bs4 import BeautifulSoup

import networkx as nx
import matplotlib.pyplot as plt

def simplifiedURL(url):

    if "www." in url:
        ind = url.index("www.")+4
        url = "http://"+url[ind:]
   
    if url[-1] == "/":
        url = url[:-1]

    parts = url.split("/")
    url = ''
    for i in range(3):
        url += parts[i] + "/"
    return url

def crawl(url, max_deep,  show=False, deep=0, done=[]):

    global edgelist

    deep += 1

    url = simplifiedURL(url)

    if not url in done:

        links = getAllLinks(url)
        done.append(url)
        if show:
            if deep == 1:
                print(url)
            else:
                print("|", end="")
                for i in range(deep-1): print("--", end="")
                print("(%d)%s" %(len(links),url))
            
        for link in links:
            link = simplifiedURL(link)
            edge = (url,link)
            if not edge in edgelist:
                edgelist.append(edge)
            if (deep != max_deep):
                crawl(link, max_deep, show, deep, done)
			
def getAllLinks(src):

    try:

        page = requests.get(src)

        soup = BeautifulSoup(page.content, 'html.parser')

        tags = soup.findAll("a")

        links = []
        for tag in tags:
            try:
                link = tag['href']
                if not link in links and 'http' in link:
                    links.append(link)
            except KeyError:
                pass
        return links
    except:
        return list()


root = "http://vivacosmetic.com/id/"
nodelist = [root]
edgelist = []


crawl(root, 3, show=True)
edgelistFrame = pd.DataFrame(edgelist, None, ("From", "To"))


g = nx.from_pandas_edgelist(edgelistFrame, "From", "To", None, nx.DiGraph())

pos = nx.spring_layout(g)


damping = 0.85
max_iterr = 100
error_toleransi = 0.0001
pr = nx.pagerank(g, alpha = damping, max_iter=max_iterr, tol=error_toleransi)


print("keterangan node:")
nodelist = g.nodes
label= {}
data = []
for i, key in enumerate(nodelist):
    data.append((pr[key], key))
    label[key]=i


urut = data.copy()
for x in range(len(urut)):
    for y in range(len(urut)):
        if urut[x][0] > urut[y][0]:
            urut[x],urut[y] = urut[y],urut[x]
        

urut = pd.DataFrame(urut, None, ("PageRank", "Node"))
print(urut)

nx.draw(g, pos)
nx.draw_networkx_labels(g, pos, label, font_color="w")

plt.axis("off")
plt.show()
