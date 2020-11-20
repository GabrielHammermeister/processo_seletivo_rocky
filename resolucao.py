import json

# ASCII values:
#   a/æ 145
#   c/¢ 189
#   o/ø 155
#   b/ß 225

'''

a) Uma função que imprime a lista com todos os nomes dos produtos, ordenados
primeiro por categoria em ordem alfabética e ordenados por id em ordem
crescente. Obs: é apenas uma saída, ordenada pelos dois fatores citados acima.

'''

def displayProducts(jsonFile):

    with open(jsonFile) as brokenFile:
        data = json.load(brokenFile)
        brokenFile.close()

    print( sorted(data, key=lambda x: x["category"]))
    print( sorted(data, key=lambda x: x["id"]))

'''

b) Uma função que calcula qual é o valor total do estoque por categoria, ou seja,
a soma do valor de todos os produtos em estoque de cada categoria,
considerando a quantidade de cada produto.

'''

def displayTotalByCat(jsonFile):

    with open(jsonFile) as brokenFile:
        data = json.load(brokenFile)
        brokenFile.close()

    # Inicializando um dicionario vazio para catalogar todas as Categories
    categoryDict = {}

    for dict in data:
        category = ""
        quant = 0
        price = 0
        for key, value in dict.items():
            if key == "category":
                if value not in categoryDict:
                    categoryDict[value] = 0
                category = value
            elif key == "quantity":
                quant = value
            elif key == "price":
                price = value
        categoryDict[category] += quant*price

    # Mostrando os valores por categoria
    for key, value in categoryDict.items():
        print(f"{key}: R$ {value:.2f};")

def fixNames(dict):

    '''
    Python nao permite editar um caractere de uma String.
    exemplo: py = "python"
             py[1] = 'i'
    Portanto tomei a abordagem de listar todos o caracteres do
    atributo em uma lista, sendo assim, posso indexa-los e troca-los
    mais facilmente.

    :param dict:
    :return:
    '''


    cont = 0
    aux = dict["name"]

    # Listando todos os caracteres
    name = list(aux)

    # Localizando e trocando caracteres corrompidos.
    for letter in name:
        if letter == 'æ':
            name[cont] = 'a'
        elif letter == '¢':
            name[cont] = 'c'
        elif letter == 'ø':
            name[cont] = 'o'
        elif letter == 'ß':
            name[cont] = 'b'
        else:
            name[cont] = letter
        cont += 1

    # Reunindo o caracteres em uma String
    newName = ''.join(name)

    dict["name"] = newName

def fixPrices(dict):

    # Usando um simples casting na String ja e o suficiente
    dict["price"] = float(dict["price"])

def fixQuantity(dict):

    # Caso nao houver o atributo "quantity" no dicionario,
    # criar o atributo e atribuir 0 a ele
    if "quantity" not in dict.keys():
        dict["quantity"] = 0

def exportJson(fixedFile, destination):

    '''

    essa funcao executa a gravacao do broken-database em um arquivo .json novo,
    caso esqueca de colocar "ensure_ascii = False" o json.dump() vai converter o caracteres especiais
    para sua forma Unicode

    :param fixedFile:
    :param destination:
    :return:

    '''

    with open(destination, 'w') as jsonFile:
        json.dump(fixedFile, jsonFile, indent=2, ensure_ascii=False)
        jsonFile.close()

def fixObjects(data):

    '''

    essa funcao foi criada para aumentar a modularizacao do projeto
    e facilitar na leitura e possiveis manutencoes no codigo.

    :param data:
    :return:

    '''
    for dict in data:
        fixNames(dict)
        fixPrices(dict)
        fixQuantity(dict)


def loadJson(file):

    # Abrindo o arquivo .json, em utf-8
    # Sem especificar o encoding do arquivo,
    # nao eh possivel decodificar
    # devido aos caracteres especiais
    with open(file , encoding="utf-8") as brokenFile:
        # Descerializando o arquivo e convertendo em um Dictionary
        data = json.load(brokenFile)
        brokenFile.close()

    return data

if __name__ == '__main__':

    oldDB = "broken-database.json"
    newDB = "saida.json"

    # Extraindo os dados do broken-database.json
    data = loadJson(oldDB)

    # Concertando todos os Atributos relatados com falhas
    fixObjects(data)

    # Exportando os dados limpos para a fixed-database.json
    exportJson(data, newDB)

    # Display
    displayProducts(newDB)
    displayTotalByCat(newDB)
