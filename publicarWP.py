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

def user_inputFAST():
    urList = []
    while True:
        url = input('digite a url CORRETAMENTE\n0 para de enviar').strip()
        if url == '0':
            break
        urList.append(url)

    for i in urList:
        try:
            make_post(scrape(i))
        except:
            print(i,'\ndigitada errado')

def user_inputUpdate():
    ''' essa função coleta o input do usuario e chama todos os outros scripts necessarios
        e publica

    :return:
    '''
    class entradas:
        def __init__(self):
            self.url = None
            self.categorias= '0'
            self.tags = '0'
            self.date = None
            self.conteudo = None

    listaEntradas =[]

    while True:
        entrada = entradas()
        #recebendo a url
        url = input('insira a url (digite 0 se nao tiver mais links para enviar)\n').strip()

        if url == '0':
            break
        entrada.url = url
        #recebendo as categorias
        categorias = input('insira as categoras (separadas por ",")\npara nenhuma categoria digite 0 ').split(',')

        #consultando se elas estao no banco de dados do script dicionario.py
        if categorias[0] != '0':
            categoriasCorretas = []
            for index, i in enumerate(categorias):
                match = False
                while match == False:
                    match = categoryComplete(i)
                    if match == False:
                        i = input('Categoria "{}" nao encontrada, digite novamente: '.format(i))
                        if i== '0':
                            break
                    if match != False:
                        categoriasCorretas.append(match)

                entrada.categorias = categoriasCorretas
        #varivael entrada recebe as categorias verificadas



        print('\n')
        entrada.tags = ( input('insira as tags (separadas por ",")\npara nenhuma tag digite 0 ').split(',') )
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
        #entrada recebe a data formatada corretamente
        entrada.date = data

        #lista de entradas recebe a entrada fornecida nesse loop
        listaEntradas.append(entrada)


        clearConsole()


    #analizar todas as urls recebidas
    fail = []
    failIndex =[]
    clearConsole()
    print('Postando.... Aguarde!')
    #vai tentar analizar todas as urls
    #se nao for possivel, a url é invalida
    #se a url for invalida, a entrada correspondente vai pra lista fail
    #e posteriormente é retirada da listaEntradas
    for index, i in enumerate(listaEntradas):
        try:
            listaEntradas[index].conteudo = scrape(i.url)
        except:
            failIndex.append(index)
            fail.append(i)
    for index, i in enumerate(failIndex):
        listaEntradas.pop(i-index)

    #aqui vai repetir ate uma url valida for digitada ou '0' para cancelar
    while len(fail) > 0:
        for index, i in enumerate (fail):
            print(i.url)
            failInput = input('url invalida, digite novamente ').strip()
            if failInput == '0':
                fail.pop(index)
            else:
                try:
                    fail[index].conteudo = scrape(failInput)
                except:
                    fail[index].url = failInput
                else:
                    fail[index].url = failInput
                    listaEntradas.append(fail[index])
                    fail.pop(index)



    #publicar o conteúdo recebido
    for i in listaEntradas:
        make_post(i.conteudo,i.categorias,i.tags,i.date)


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
        #user_input()
        #user_inputFAST()
        user_inputUpdate()
        print('\n\n')

