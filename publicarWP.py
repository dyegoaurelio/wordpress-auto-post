import urllib.request as requests
from os import system, name
from blogpost import make_post
from dicionario import convertData,categoryComplete
from urlscrape import scrape
url = "https://www.opovo.com.br/esportes/futebol/times/ceara/"


def user_input():
    ''' essa função coleta o input do usuario e chama todos os outros scripts necessarios
        e publica

    :return:
    '''
    #recebendo a url
    url = input('insira a url ').strip()
    match = False
    while not match:
        try:
            conteudo = scrape(url)
        except:
            url = input('url invalida, digite novamente ').strip()
        else:
            match = True
    clearConsole()
    print(conteudo['title'])
    #recebendo as categorias
    categorias = input('insira as categoras (separadas por ",")\npara nenhuma categoria digite 0 ').split(',')

    #consultando se elas estao no banco de dados do script dicionario.py
    if categorias[0] != '0':
        for index, i in enumerate(categorias):
            match = False
            while match == False:
                match = categoryComplete(i)
                if match == False:
                    i = input('Categoria "{}" nao encontrada, digite novamente: '.format(i))
            categorias[index] = match
    print('\n')
    tags = input('insira as tags (separadas por ",")\npara nenhuma tag digite 0 ').split(',')
    print('\n')
    #convertendo a data recebida
    data = input('insira a data de publicacao do post (0 para publicar agora) ')
    match = False
    while match == False:
        match = convertData(data)
        if data == '0':
            data == None
            break
        if match == False:
            data = input('Data escrito errado, digite novamente: ')
    data = match

    #enviando a publicacao
    #atraves da funcao make_post do script blogpost



    make_post(conteudo,categorias,tags,data)


#gerando um conteudo teste para postar no site
def postarTESTE():
    content = dict()
    content['title'] = 'teste 28121'
    content['body'] = 'CORPO DO TEXTO'
    content['image'] = '10.jpeg'
    return content

def clearConsole():
    '''

    :return: quando chamada limpa o console
    '''
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


if __name__ == '__main__':
    #gerando categorias teste para postar no blog
    categoriasTESTE = ['Fortaleza' ,'ceará','teste']
    tagsTESTE = ['autopost']
    while True:
        user_input()
        print('\n\n')

