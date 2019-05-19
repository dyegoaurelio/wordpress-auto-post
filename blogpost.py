from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

from datetime import datetime


def make_post(content, categorys, tags, date = False):
    '''
    :param content: dict() formatado corretamente
    :param categorys: lista com as categorias do post
    :param tags: lista com as tags do post
    :param date: data para o post ser publicado ( formato datetime.datetime())
    :return:
    '''
    #URL DO SITE, USUARIO , SENHA !!!
    wp = Client('https://estanislau2.000webhostapp.com/xmlrpc.php',
                'admin', 'admin')
    post = WordPressPost()
    post.title = content['title']
    post.content = content['body']
    post.terms_names = {
        'post_tag': tags,
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
    post.post_status = 'publish'

    # marcando p/ o post ser postado na data desejada
    if date != False:
        post.date = date
    post.id = wp.call(posts.NewPost(post))
    # Set Default Status For Post .i.e Publish Default Is Draft

    # We Are Done With This Part :) Lets Try To Run It
    print("Sucessfully Posted To Our Blog !")
