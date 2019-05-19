import requests
import os
from newspaper import Article
from blogpost import make_post
#biblioteca para descobrir o hostname dos sites
from urllib.parse import urlparse

url =input()

def scrape(url):
    host = urlparse(url).hostname

    '''if host == 'tribunadoceara.uol.com.br' :
        chamar o scrape desse site e assim vai
    '''

def article_content(url):
    #criando dicionario que vai ser usado na funcao makepost
    content = dict()

    #gerando artigo da biblioteca Newspaper
    article = Article(url, language='pt')
    article.download()
    article.parse()


    print(article.title) #como pode ver ele ja AUTOMATICAMENTE separa tudo

    #colocando as informacoes no dicionario
    content['title'] = article.title
    content['body'] = article.text + '\n\nFonte: ' + url

    #pegando a imagem ""principal""
    print(article.top_image)
    # For Image We Will Save Our Image Path In To Our Dictionary
    # Lets Download And Save The Image
    # Using Requests To Download And Save The Image File In Our Local Directory
    resp = requests.get(article.top_image)
    with open('1.jpg', 'wb') as imagefile:
        imagefile.write(resp.content)
    content['image'] = '1.jpg'
    return content

make_post(article_content(url[:-1]),['Fortaleza' ,'News'],['autopost'])
