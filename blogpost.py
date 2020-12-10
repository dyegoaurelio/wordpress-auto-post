from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from os import remove

from datetime import datetime

import json
with open('auth.json') as f:
  authData = json.load(f)

def make_post(content, categorys='0', tags='0', date = None):
    '''
    :param content: dict() formatado corretamente
    :param categorys: lista com as categorias do post
    :param tags: lista com as tags do post
    :param date: data para o post ser publicado ( formato datetime.datetime())
    :return:
    '''
    #URL DO SITE, USUARIO , SENHA !!!
    wp = Client( authData['url'] + '/xmlrpc.php',
	authData['adminUsername'], authData['adminPassword'])
    post = WordPressPost()
    post.title = content['title']
    post.content = content['body']

    if tags[0] != '0':

        post.terms_names = {
            'post_tag': tags
        }
    try:
        categorys[0] == 0
    except IndexError:
        pass
    else:
        if categorys[0] != '0':
            post.terms_names = {
                'category': categorys
            }

    # Lets Now Check How To Upload Media Files
    filename = content['image']
    data = {
        'name': content['title']+ '.jpeg',
        'type': 'image/jpeg'  # Media Type
    }
    # Now We Have To Read Image From Our Local Directory !
    with open(filename, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
        response = wp.call(media.UploadFile(data))
    attachment_id = response['id']

    # Above Code Just Uploads The Image To Our Gallery
    # For Adding It In Our Main Post We Need To Save Attachment ID
    post.thumbnail = attachment_id

    #deletando do pc a imagem
    remove(filename)

    #setando para o post ser publicado (nao ficar de rascunho)
    post.post_status = 'publish'

    # marcando p/ o post ser postado na data desejada
    if date != None:
        post.date = date
    post.id = wp.call(posts.NewPost(post))
    # Set Default Status For Post .i.e Publish Default Is Draft

    # We Are Done With This Part :) Lets Try To Run It
    if not date:
        print(post.title, " Postado com sucesso !")
    if date:
        print(post.title, " Vai ser postado em ",date,'!')
