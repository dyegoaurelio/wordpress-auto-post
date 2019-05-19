import urllib.request as requests
import os
from blogpost import make_post
from dicionario import convertData
url = "https://www.poder360.com.br/opiniao/governo/sergio-moro-foi-noticia-duplamente-na-ultima-6a-feira/"




#gerando um conteudo teste para postar no site
def postar(url):
    content = dict()
    content['title'] = 'teste 2121'
    content['body'] = 'CORPO DO TEXTO'
    content['image'] = '10.jpeg'
    return content


#gerando categorias teste para postar no blog
categorias = ['Fortaleza' ,'News']
tags = ['autopost']


#make_post(postar(url),categorias,tags,convertData('15/12'))

