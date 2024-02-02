#importando as bibliotecas que serão usadas
import requests
import pandas as pd
import numpy as np


#baixando o arquivo da base de dados da Prefeitura de Porto Alegre
url = 'https://dadosabertos.poa.br/dataset/abafb264-4418-4423-b6c8-62d146ca8462/resource/8bf09aa3-15bb-4eaa-9f3e-5b0364ece6a7/download/alvaras_ativos.csv'

with requests.get(url, stream = True) as r:
  with open('alvaras_ativos', mode='wb') as arquivo:
    for chunk in r.iter_content(chunk_size = 10*1024):
        arquivo.write(chunk)
print(f'arquivo baixado')


#transformando o arquivo CSV em DataFrame no pacote Pandas
df = pd.read_csv('alvaras_ativos', sep= ';',encoding='utf-8')


#removendo as colunas sobressalentes
df_limpando = df.drop(['data_extracao',
                  'codigo_logradouro',
                  'predio',
                  'data_deferimento',
                  'codigo_atividade',
                  'horario',
                  'area',
                  'data_vencimento',
                  'ano_processo',
                  'numero_processo',
                  'processo_sei',
                  'processo_baixa_sei',
                  'data_emissao_seg_via',
                  'alvara_anterior',
                  'data_baixa',
                  'baixado',
                  'motivo',
                  'numero_boletim',
                  'mes_vencimento'], axis= 1)


#adequando algumas colunas pelos tipos de dado
df_transformando = df_limpando.astype({'alvara': 'object',
                                       'mei':'bool',
                                       'data_inicio_atividade': 'datetime64[M]',
                                       'data_emissao_alvara': 'datetime64[M]'})


#modificando e acrescentando colunas e dados
df_transformando['ponto_referencia'] = df_limpando['ponto_referencia'].map({2: 0, 3: 1}).astype('bool')
df_transformando['inicio_ano'] = df_transformando['data_inicio_atividade'].dt.year.astype('object')
df_transformando['inicio_mes'] = df_transformando['data_inicio_atividade'].dt.month.astype('object')
df_transformando['emissao_ano'] = df_transformando['data_emissao_alvara'].dt.year.astype('object')
df_transformando['emissao_mes'] = df_transformando['data_emissao_alvara'].dt.month.astype('object')


#renomeando e reordenando as colunas
df_transformando.rename(columns={'alvara': 'ID_alvara',
                                 'ponto_referencia': 'ambulante'}, inplace = True)
df_transformando= df_transformando.reindex(['ID_alvara',
                                            'atividade',
                                            'bairro',
                                            'logradouro',
                                            'mei',
                                            'ambulante',
                                            'equipamento',
                                            'data_inicio_atividade',
                                            'inicio_mes',
                                            'inicio_ano',
                                            'data_emissao_alvara',
                                            'emissao_mes',
                                            'emissao_ano'], axis=1 )


#observando como ficaram os dados limpos e transformados no dataframe final
df_final = df_transformando
df_final.head(5)


#salvando o DataFrame em CSV para ser utilizado em outras plataformas
df_final.to_csv('alvaras_ativos_PoA.csv', index=False)
print('arquivo salvo')
