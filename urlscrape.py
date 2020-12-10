import requests
import os
from newspaper import Article
from blogpost import make_post
from urllib.parse import urlparse
import re
from unidecode import unidecode
import random

def scrape(url):
    '''

    :param url: url valida do site a ser analizado
    :return: dicionario com o conteudo do site
    '''
    #primeiro a funcao vai descobrir qual o site que foi mandado
    host = urlparse(url).hostname

    #se existir algum codigo especifico pro site, ele sera chamado
    #se nao tiver especifico sera chamado o geral (biblioteca newspaper)

    if host == 'tribunadoceara.uol.com.br' :
        return tribuna_scrape(url)

    elif host == 'diariodonordeste.verdesmares.com.br':
        print ('fazer codigo diario')
        return newspaperScrape(url)

    elif host == 'www.opovo.com.br':
        return opovo_scrape(url)
    #fazer as devidas funçoes de ajuste

    else:
        return newspaperScrape(url)




def newspaperScrape(url):
    '''

    :param url: recebe a url a ser examinada
    :return: utiliza a biblioteca Newspaper, que é mais geral para examinar o artigo
    '''
    #criando dicionario que vai ser usado na funcao makepost
    content = dict()

    #gerando artigo da biblioteca Newspaper
    article = Article(url, language='pt')
    article.download()
    article.parse()


    #print(article.title) #como pode ver ele ja AUTOMATICAMENTE separa tudo

    #colocando as informacoes no dicionario
    content['title'] = article.title
    content['body'] = article.text + '\n\nFonte: ' + url

    #pegando a imagem ""principal""
    #print(article.top_image)
    # For Image We Will Save Our Image Path In To Our Dictionary
    # Lets Download And Save The Image
    # Using Requests To Download And Save The Image File In Our Local Directory
    resp = requests.get(article.top_image)
    hash = random.getrandbits(128)
    hash = str(hash)
    with open( hash + '.jpg', 'wb+') as imagefile:
        imagefile.write(resp.content)
    content['image'] = hash + '.jpg'
    return content

def opovo_scrape(url):
    #aqui só é necessario tirar o link para o podcast no fim de algumas noticias

    conteudo = newspaperScrape(url)
    #print(conteudo['body'])

    listen = re.search(r'Listen to ', conteudo['body'])

    if listen != None:
        if listen.start() >= (len(conteudo['body'])) / 2:

            conteudo['body'] = conteudo['body'][:listen.start()] + '\n\nFonte: ' + url
            #print(conteudo['body'])
    return conteudo

def tribuna_scrape(url):
    conteudo = newspaperScrape(url)
    # Procura pela "marca d'agua da tribuna"

    listen = re.search(r'Por Tribuna do Ceará', conteudo['body'])
    if listen == None:
        listen = re.search(r'Por TV Jangadeiro', conteudo['body'])
    if listen == None:
        listen = re.search(r'por jangadeiro', conteudo['body'].lower())
    if listen == None:
        listen = re.search(r'por futeboles', conteudo['body'].lower())
    if listen == None:
        return conteudo

    startError = listen.start()

    # procura pelo fim (onde sempre vao ter duas quebras de linha)
    listen = re.search(r'\n\n', conteudo['body'][startError:])

    # registra o fim
    endError = listen.end() + startError

    #checa se o recorte foi correto
    if all(['por' in conteudo['body'][startError:endError].lower() , 'de' in conteudo['body'][startError:endError].lower()]):
        # se foi correto executa o recorte do texto
        conteudo['body'] = conteudo['body'][:startError] + conteudo['body'][endError:]

    #checa se o começo do texto ta igual ao título

    if unidecode( conteudo['title'].lower().strip() )== unidecode ( conteudo['body'][:len(conteudo['title'])].lower().strip() ):
        conteudo['body'] = conteudo['body'][len(conteudo['title']):]

    return conteudo

if __name__ == '__main__':
    url = input('entre com a url (teste do script urlscrape)').strip()
    data = scrape(url)
    print('Title')
    print(data['title'])
    print('\nBody')
    print(data['body'])
    print('\nImage')
    print(data['image'])
