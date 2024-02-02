#importanto os pacotes que serão utilizados no projeto
from requests import get
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

import time
import re
import datetime


url = 'https://www.cobasi.com.br/c/gatos/racao/racao-seca?terms=/gatos/racao/racao-seca/7%40dot%405%20kg/Adulto/Super%20Premium%20Natural?map=c,c,c,specificationFilter_291,specificationFilter_297,specificationFilter_470&page=1'
response = get(url)

# usando os parâmetros do Beautifulsoup para transformar a página em um objeto
soup = BeautifulSoup(response.text, 'html.parser')

# criando objetos individuais para cada objeto (ração), para que possam ser analisadas em um lastro de repetição.
racao_containers= soup.find_all(class_= 'bNtpHK')


# criando listas para cada valor que buscamos para montar a tabela final
racao_loja = []
racao_nome = []
racao_marca = []
racao_nota = []
racao_preco = []
racao_peso = []
data_acesso = []

#criando um lastro for para pegar cada informação de cada objeto e colocar nas listas criadas anteriormente
for item in range(len(racao_containers)):
    racao_loja.append(re.findall('www.(.*).com', url))
    racao_nome.append(racao_containers[item].find(class_ = 'dPsqyZ').get_text())
    racao_marca.append(racao_containers[item].find(class_ = 'bNiXcY').get_text())
    racao_nota.append(racao_containers[item].find(class_= 'kISiHB').get_text())
    if racao_containers[item].find(class_ = 'card-price') is not None: #linha para coletar itens que possam estar indisponíveis no site
       racao_preco.append(racao_containers[item].find(class_ = 'card-price').get_text()[3:].replace(',', '.'))
    else:
       racao_preco.append('na')
    if racao_containers[item].find(class_ = 'bOmFEM') is not None: #linha para coletar itens que possam estar indisponíveis no site
       racao_peso.append(racao_containers[item].find(class_= 'bOmFEM').get_text())
    else:
       racao_peso.append('na')
    data_acesso.append(datetime.date.today().strftime('%Y-%m-%d'))
time.sleep(2) # tempo para carregar cada vez e não sobrecarregar o server


#criando a tabela no Pandas
racao_gatos = pd.DataFrame({
    'racao_loja': racao_loja,
    'racao_nome': racao_nome,
    'racao_marca': racao_marca,
    'racao_nota': racao_nota,
    'racao_preco': racao_preco,
    'racao_peso': racao_peso,
    'data_acesso': data_acesso
})

#vendo o resultado final
racao_gatos.head()


#criando arquivo csv do resultado
racao_gatos.to_csv('racao_gatos.csv', index=False)
