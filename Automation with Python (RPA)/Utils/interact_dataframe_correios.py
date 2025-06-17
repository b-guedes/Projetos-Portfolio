from pandas import DataFrame
from botcity.web import WebBot
from Utils.helper_functions import check_variables
from Utils.interact_correios import interact_correios
from Utils.integrated_logger import IntegratedLogger

def buscar_cotacoes_correios(df_output: DataFrame, df_filtered: DataFrame,
    bot: WebBot, logger: IntegratedLogger) -> DataFrame:
    """ 
    Realiza a iteração sobre um DataFrame filtrado, executa consultas no site dos Correios
    e preenche o DataFrame de saída com o prazo e o valor da cotação.

    Essa função combina automação web com manipulação de dados em larga escala. Para cada
    linha do DataFrame filtrado, valida as variáveis com `check_variables` e utiliza o 
    `interact_correios` para extrair informações do site. Em caso de erro, o status
    é atualizado para facilitar o rastreamento posterior.

    Parâmetros:
        df_output (DataFrame): DataFrame completo com todos os registros (inclusive os que não serão processados).
        df_filtered (DataFrame): Subconjunto contendo apenas os CNPJs válidos para consulta.
        bot (WebBot): Instância do navegador controlado pela BotCity Web para automação no site dos Correios.
        logger (IntegratedLogger): Logger personalizado para registrar o progresso e os erros da execução.

    Retorna:
        DataFrame: DataFrame atualizado com as colunas 'PRAZO DE ENTREGA CORREIOS', 
        'VALOR COTAÇÃO CORREIOS' e 'STATUS' preenchidas para os CNPJs processados.

    Raises:
        Exception: Qualquer erro interno não tratado (geralmente interceptado por try/except internos para continuidade do loop).
    """

    total = len(df_filtered)

    for index, row in df_filtered.iterrows():
        cnpj = row.get("CNPJ", "")
        logger.info(f"[{index + 1}/{total}] Iniciando processamento para CNPJ {cnpj}")

        try:
            # Valida e extrai as variáveis obrigatórias para consulta no site dos Correios.
            # A função check_variables retorna: dimensões, peso, tipo de serviço e CEP de destino.
            dimensions, weight, service, cep_destiny = check_variables(row)
            logger.debug(f"Variáveis validadas para CNPJ {cnpj}")
        
        except Exception as err:
            # Caso as variáveis estejam incompletas ou com formato incorreto, marca como erro no STATUS.
            logger.warning(f"Erro nas variáveis do CNPJ {cnpj}: {err}")
            df_output.loc[df_output["CNPJ"] == cnpj, "STATUS"] = str(err)
            continue  # Segue para o próximo CNPJ

        try:
            # Realiza a automação no site dos Correios utilizando os dados validados.
            # A função interact_correios retorna prazo estimado e valor da entrega.
            prazo, preco = interact_correios(
                bot=bot,
                service_type=service,
                cep_destiny=cep_destiny,
                weight=weight,
                dimensions=dimensions,
            )

            # Preenche os resultados no DataFrame de saída.
            df_output.loc[df_output["CNPJ"] == cnpj, "PRAZO DE ENTREGA CORREIOS"] = prazo
            df_output.loc[df_output["CNPJ"] == cnpj, "VALOR COTAÇÃO CORREIOS"] = preco

            logger.info(f"Consulta Correios finalizada com sucesso para CNPJ {cnpj}")

        except Exception as err:
            # Em caso de falha durante a automação (como erro de carregamento da página), registra no STATUS.
            logger.error(f"Erro ao consultar CNPJ {cnpj} nos Correios: {err}")
            df_output.loc[df_output["CNPJ"] == cnpj, "STATUS"] = str(err)
            continue  # Continua para o próximo registro

    return df_output