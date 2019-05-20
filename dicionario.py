from datetime import datetime,time,date

#para converter palavras acentuadas em sem acentos
#pip install unidecode
from unidecode import unidecode

#CATEGORIAS DO SITE

categorias =['Ceará','Fortaleza','Região Metropolitana','Esportes','Policial','Politica']



def convertData(data,stdrHora=8):
    '''

    :param data: qualquer data ou hora no formato dd/mm/aaaa , hh:mm:ss
    stdrHora vai ser a hora pra publicacao ser postade se nao for fornecido horario
    :return: vai retornar uma instancia de datetime.datetime() ou False se o input estiver errado
    '''
    if data == '0':
        return None
    conversao = []
    cont = 0
    separadores = [')' , ']','}', ',', ';']
    separadoresData = ['/' , '\\','-','_']
    separadoresHora = [':']

    #Esse loop vai converter a entrada data para a lista conversão formatada do jeito necessario
    for i in data:
        erro = False
        #VAI TESTAR SE A POSIÇÃO É INT
        try:
            x = int(i)
        except:
            erro = True
            if len(conversao) > 0:
                if any([i in separadores,i in separadoresHora, i in separadoresData]):
                    conversao.append(i)
                   # print(conversao[cont])
                    try:
                        conversao[cont]=int(conversao[cont])
                    except:
                        pass
                    cont +=1
        #Se a posição acima não for inteira e for \,/,: vai virar a proxima posiçao da lista
        #abaixo vai registrar os numeros inteiros recebidos
        if not erro:
            try:
                int(conversao[cont])
            except ValueError:
                cont+=1
            except IndexError:
                pass
            try:
                conversao[cont] = conversao[cont] + i
            except:
                conversao.append(i)
    try:
        conversao[cont] = int(conversao[cont])
    except:
        pass
    #a lista conversao está formada como data

    #agora fazendo a separação de dia e hora
    dia = False
    for i in separadores:
        if i in conversao:
            dia = conversao[:conversao.index(i)]
            hora = conversao[conversao.index(i) + 1:]
            for i in hora:
                if i in separadores:
                    hora.pop(hora.index(i))
            break
    #se a variavel dia continuar falsa quer dizer que não existe nenhum separador ( ','  ';' e tal )
    if not dia:
        hora = False
        for i in separadoresData:
            if i in conversao:
                dia = conversao
                break
        for i in separadoresHora:
            if i in conversao:
                hora = conversao
                break
    if all([not hora,not dia]):
        dia = conversao

    #separação entre dia e hora completa
    horaconv =[]
    diaconv = []
    if hora:
        cont = 0
        index = 0
        for j, i in enumerate (hora):
            if i in separadoresHora:
                index = j
                if isinstance(hora[index-1],int):
                    horaconv.append(hora[index-1])
                cont+=1
        if index != 0:
            try:

                if isinstance(hora[index+1],int):
                    horaconv.append(hora[index+1])
            except IndexError: pass

            if cont != len(hora) - len(horaconv):
                print('WRONG DATA INPUT')
                return False
        else: #NESSE CASO SÓ FOI FORNECIDO A HORA (NÃO FOI ENCOTRADO SEPARADORES DE HORA COM MINUTOS)
            horaconv.append(hora[index])

    if len(horaconv)==0: #Se nao for fornecido horario, vai ser postado no horario standart definido na entrada
        horaconv.append(stdrHora)
    while len(horaconv) < 4:
        horaconv.append(0)

    try:
        x = time(horaconv[0],horaconv[1],horaconv[2],horaconv[3])
    except:
        print('WRONG DATA INPUT')
        return False

    #no codigo acima a hora já ficou formatada de maneira que cada numero ocupa
    #cada numero da hora ocupa um espaço da lista horaconv
    #se a hora estiver escrito errada, irá retornar False

    if dia:
        cont = 0
        index = 0
        for j, i in enumerate(dia):
            if i in separadoresData:
                index = j
                if isinstance(dia[index - 1], int):
                    diaconv.append(dia[index - 1])
                cont += 1
        if index != 0:
            try:
                if isinstance(dia[index + 1], int):
                    diaconv.append(dia[index + 1])
            except IndexError: pass

            if cont != len(dia) - len(diaconv):
                print('WRONG DATA INPUT')
                return False
        else:  # NESSE CASO SÓ FOI FORNECIDO O DIA (NÃO FOI ENCOTRADO SEPARADORES DE DIA)
            diaconv.append(dia[index])

        if len(diaconv) == 2:
            diaconv.append(datetime.today().year)
        if len(diaconv) == 1:
            diaconv.append(datetime.today().month)
            diaconv.append(datetime.today().year)
        if len(diaconv) > 3:
            print('WRONG DATA INPUT')
            return False
        if diaconv[2] <100:
            diaconv[2]+=2000
        try:
            x = date(diaconv[2],diaconv[1],diaconv[0])
        except:
            print('WRONG DATA INPUT')
            return False

    if len(diaconv) == 0:
        diaconv.append(datetime.today().day)
        diaconv.append(datetime.today().month)
        diaconv.append(datetime.today().year)

    #formatacao completa da data
    return datetime(diaconv[2],diaconv[1],diaconv[0],horaconv[0],horaconv[1],horaconv[2],horaconv[3])


def categoryComplete(nome,categorias=categorias):
    '''

    :param nome: recebe um nome e se ele estiver nas categorias previamente estabelecidas, retorna ela, se nao renorna None
    :param categorias: opcional, lista de categorias
    :return: categoria correspondente
    '''
    nome = nome.strip()
    try:
        index = next(i for i, v in enumerate(categorias) if unidecode(v[:len(nome)].lower())== unidecode(nome.lower()))
    except StopIteration:
        return False
    return categorias[index]

if __name__ == '__main__':
    print('categoryComplete: ',categoryComplete('regiao       '))
    print ('convertData ',convertData('10:30'))
