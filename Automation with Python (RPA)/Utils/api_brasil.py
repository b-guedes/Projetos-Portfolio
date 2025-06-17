import pandas as pd
import requests
import os
from Utils.integrated_logger import IntegratedLogger
from Utils.functions_excel import open_excel_file_to_dataframe
from config import vars_map
from time import sleep


def query_brasilapi(cnpj: str, logger: IntegratedLogger) -> tuple:
    """
    Consulta a API BrasilAPI utilizando o CNPJ informado e retorna os dados da empresa.

    Parâmetros:
        cnpj (str): Número do CNPJ a ser consultado.
        logger (IntegratedLogger): Instância do logger para registrar logs da execução.

    Retorna:
        tuple: (dict ou None, str)
            - Dados retornados pela API (ou None em caso de falha)
            - Status da consulta: "Sucesso", "falha" ou "inválido"

    Raises:
        Exception: Para qualquer erro inesperado que ocorra durante a consulta.
    """
    try:
        # Validação básica do CNPJ
        if not cnpj.isdigit() or len(cnpj) != 14:
            logger.warning(f"CNPJ inválido informado: {cnpj}")
            return None, "inválido"

        url = f"{vars_map['DEFAULT_BRASILAPI_URL']}{cnpj}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.91"
            )
        }

        logger.info(f"Iniciando consulta à BrasilAPI com CNPJ: {cnpj}")
        response = requests.get(url=url, headers=headers, timeout=10)
        response.raise_for_status()  # Lança erro se a resposta tiver status de falha HTTP

        logger.info(f"Consulta bem-sucedida para o CNPJ: {cnpj}")
        return response.json(), "Sucesso"

    except requests.exceptions.Timeout:
        logger.warning(f"Timeout ao consultar o CNPJ {cnpj}")
        return None, "falha"

    except requests.exceptions.ConnectionError:
        logger.warning(f"Erro de conexão ao consultar o CNPJ {cnpj}")
        return None, "falha"

    except requests.exceptions.HTTPError as erro_http:
        logger.warning(f"Erro HTTP ao consultar o CNPJ {cnpj}: {erro_http}")
        return None, "falha"

    except requests.exceptions.RequestException as erro_requisicao:
        logger.warning(f"Falha na requisição para o CNPJ {cnpj}: {erro_requisicao}")
        return None, "falha"

    except Exception as erro:
        logger.error(f"Erro inesperado ao consultar o CNPJ {cnpj}: {erro}")
        raise


def create_companies_dataframe(companies_data: list, logger: IntegratedLogger) -> pd.DataFrame:
    """
    Cria um DataFrame Pandas contendo os dados formatados das empresas consultadas na API.

    Parâmetros:
        companies_data (list): Lista de dicionários com os dados da API para cada CNPJ.
        logger (IntegratedLogger): Instância do logger para registrar logs da execução.

    Retorna:
        pd.DataFrame: DataFrame com os dados estruturados e colunas normalizadas.
    
    Raises:
        Exception: Para qualquer erro inesperado durante o processamento dos dados.
    """
    try:
        logger.info("Iniciando a criação do DataFrame com dados da API.")

        # Filtra apenas os dados válidos com status e conteúdo
        dados_empresa = [
            {**item["data"], "status": item.get("status", "desconhecido")}
            for item in companies_data if item.get("data")
        ]

        logger.debug(f"Dados recebidos da API: {dados_empresa}")

        # Define as colunas desejadas
        colunas_desejadas = [
            "cnpj", "razao_social", "nome_fantasia", "situacao_cadastral",
            "logradouro", "numero", "municipio", "cep",
            "descricao_identificador_matriz_filial", "ddd_telefone_1",
            "email", "status"
        ]

        # Cria DataFrame aplicando todas as transformações em cadeia
        df = (
            pd.DataFrame(dados_empresa, dtype=str)
              .filter(items=colunas_desejadas)
              .dropna(subset=["cnpj"])
              .fillna("N/A")
              .replace("", "N/A")
              .reset_index(drop=True)
        )

        # Mapeia os códigos de situação cadastral (se possível)
        status_map = {
            1: "Nula",
            2: "Ativa",
            3: "Suspensa",
            4: "Inapta",
            5: "Ativa Não Regular",
            8: "Baixada"
        }
        try:
            df["situacao_cadastral"] = (
                df["situacao_cadastral"]
                  .astype(float)  # Para suportar valores como "2.0"
                  .map(status_map, na_action='ignore')
            )
        except Exception as mapeamento_erro:
            logger.warning(f"Erro ao mapear a situação cadastral: {mapeamento_erro}")

        # Renomeia as colunas para os nomes finais
        df.rename(columns={
            "cnpj": "CNPJ",
            "razao_social": "RAZÃO SOCIAL",
            "nome_fantasia": "NOME FANTASIA",
            "situacao_cadastral": "SITUAÇÃO CADASTRAL",
            "logradouro": "LOGRADOURO",
            "numero": "NÚMERO",
            "municipio": "MUNICÍPIO",
            "cep": "CEP",
            "descricao_identificador_matriz_filial": "DESCRIÇÃO MATRIZ FILIAL",
            "ddd_telefone_1": "TELEFONE + DDD",
            "email": "E-MAIL",
            "status": "STATUS"
        }, inplace=True)

        logger.info("DataFrame de empresas criado com sucesso.")
        return df

    except Exception as erro:
        logger.error(f"Erro ao criar o DataFrame de empresas: {erro}")
        raise

#? Talvez essa função possa ser uma linha de código dentro da função api_data_lookup - não parece ser utilizada em outro momento
def save_dataframe_to_csv(df: pd.DataFrame, csv_file_path: str, logger: IntegratedLogger):
    """
    Salva um DataFrame em formato CSV no caminho especificado.

    Parâmetros:
        df (pd.DataFrame): DataFrame que será salvo.
        csv_file_path (str): Caminho completo onde o arquivo CSV será gerado.
        logger (IntegratedLogger): Instância do logger para registrar logs da execução.

    Raises:
        Exception: Para qualquer erro durante o processo de salvamento.
    """
    try:
        logger.info(f"Iniciando salvamento do DataFrame em CSV: {csv_file_path}")

        # Exporta o DataFrame para um arquivo CSV
        df.to_csv(csv_file_path, index=False, encoding="utf-8-sig")
        logger.info(f"Arquivo CSV salvo com sucesso em: {csv_file_path}")

    except Exception as erro:
        logger.error(f"Erro ao salvar o arquivo CSV em {csv_file_path}: {erro}")
        raise


def join_and_transform(excel_df: pd.DataFrame, api_df: pd.DataFrame, logger: IntegratedLogger) -> pd.DataFrame:
    """
    Mescla os dados do DataFrame original do Excel com os dados adicionais obtidos da API,
    atualizando os campos correspondentes.

    Parâmetros:
        excel_df (pd.DataFrame): Dados originais lidos do Excel.
        api_df (pd.DataFrame): Dados obtidos via API com informações complementares.
        logger (IntegratedLogger): Instância do logger para registrar o progresso da operação.

    Retorna:
        pd.DataFrame: DataFrame resultante da mesclagem com os dados atualizados.
    
    Raises:
        Exception: Se ocorrer algum erro durante o processo de mesclagem.
    """
    try:
        logger.info("Iniciando processo de mesclagem e transformação dos dados.")

        # Converte ambos os DataFrames para 'object' para preservar formatações (como zeros à esquerda)
        excel_df = excel_df.astype("object")
        api_df = api_df.astype("object")

        # Valida se ambos os DataFrames possuem a coluna 'CNPJ'
        if "CNPJ" not in excel_df.columns or "CNPJ" not in api_df.columns:
            logger.error("Coluna 'CNPJ' ausente em um ou ambos os DataFrames.")
            raise ValueError("Coluna 'CNPJ' ausente para mesclagem.")

        # Se o DataFrame da API possui as colunas de endereço, utiliza a função make_column_endereco
        endereco_cols = ["LOGRADOURO", "NÚMERO", "MUNICÍPIO"]
        if all(col in api_df.columns for col in endereco_cols):
            logger.info("Utilizando função make_column_endereco para criar a coluna 'ENDEREÇO'.")
            from functions_excel import make_column_endereco
            api_df = make_column_endereco(api_df, logger)

        # Realiza um único merge entre os DataFrames com sufixo para colunas presentes na API
        logger.info("Realizando merge único entre Excel e API.")
        df_merged = excel_df.merge(api_df, on="CNPJ", how="left", suffixes=("", "_novo"))

        # Para cada coluna presente tanto no Excel quanto na API (exceto 'CNPJ'),
        # atualiza os valores utilizando os dados novos da API quando disponíveis
        for col in api_df.columns:
            if col != "CNPJ" and col in excel_df.columns:
                novo_col = f"{col}_novo"
                if novo_col in df_merged.columns:
                    logger.debug(f"Atualizando coluna: {col}")
                    df_merged[col] = df_merged[novo_col].combine_first(df_merged[col])
                    df_merged.drop(columns=[novo_col], inplace=True)

        # Preenche quaisquer valores faltantes com "N/A"
        df_merged.fillna("N/A", inplace=True)

        logger.info("Mesclagem dos dados concluída com sucesso.")
        return df_merged

    except Exception as erro:
        logger.error(f"Erro durante a mesclagem dos dados: {erro}")
        raise


def api_data_lookup(df_output: pd.DataFrame, logger: IntegratedLogger) -> tuple:
    """
    Função principal do programa que realiza a consulta de dados na BrasilAPI e atualiza o DataFrame de saída.

    Parâmetros:
        df_output (pd.DataFrame): DataFrame contendo os dados originais lidos do Excel.
        logger (IntegratedLogger): Instância do logger para registrar o progresso das operações.

    Retorna:
        tuple: (companies_df, df_output)
            - companies_df (pd.DataFrame): DataFrame com os dados consultados na API e processados.
            - df_output (pd.DataFrame): DataFrame original atualizado, sinalizando CNPJs sem retorno da API.
    
    Raises:
        Exception: Se ocorrer algum erro durante as etapas do processo.
    """
    try:
        logger.info("Iniciando busca de dados na BrasilAPI.")

        # Define o caminho do arquivo Excel, utilizando a variável de configuração
        excel_file_path = os.path.join(vars_map['DEFAULT_PROCESSAR_PATH'], 'Planilha de Entrada Grupos.xlsx')
        logger.info(f"Arquivo Excel encontrado em: {excel_file_path}")

        # Lê o Excel e recebe um DataFrame com os dados de entrada
        df_input = open_excel_file_to_dataframe(excel_file_path, logger)

        # Extrai a coluna 'CNPJ' em formato de texto, garantindo 14 dígitos (zeros à esquerda se necessário)
        cnpj_list = df_input["CNPJ"].apply(lambda x: str(x).strip().zfill(14)).tolist()
        logger.info(f"{len(cnpj_list)} CNPJs extraídos do Excel.")

        companies_data = []
        missing_cnpjs = []

        # Para cada CNPJ, realiza a consulta à API e armazena o retorno com o status correspondente
        for cnpj in cnpj_list:
            company_data, status = query_brasilapi(cnpj, logger)
            companies_data.append({'data': company_data, 'status': status})
            # Se a consulta falhar, registra o CNPJ como ausente
            if status == 'falha':
                missing_cnpjs.append(cnpj)

        # Processa os dados obtidos da API e cria um DataFrame com as informações das empresas
        companies_df = create_companies_dataframe(companies_data, logger)

        if companies_df is not None:
            logger.info("Identificando CNPJs ausentes na resposta da API.")
            # Identifica quais CNPJs não foram consultados com sucesso usando uma operação vetorizada
            df_output.loc[df_output['CNPJ'].isin(missing_cnpjs), 'STATUS'] = 'Sem retorno da API'
            logger.info(f"CNPJs sem retorno na API: {missing_cnpjs}")

            # Aqui poderíamos, se desejado, salvar o DataFrame de empresas em CSV de forma embutida
            # Exemplo: df.to_csv(caminho_arquivo_csv, index=False)
            
        logger.info("Busca de dados concluída com sucesso.")
        return companies_df, df_output

    except Exception as erro:
        logger.error(f"Erro em api_data_lookup: {erro}")
        raise


if __name__ == "__main__":
    api_data_lookup()