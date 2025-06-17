from dotenv import load_dotenv
import os
from botcity.web import WebBot, By, element_as_select
from botcity.maestro import BotMaestroSDK
import pandas as pd
from .helper_functions import *
from .integrated_logger import *
from config import vars_map


load_dotenv(override=True)

def obter_cotacoes_jadlog(bot: WebBot, maestro: BotMaestroSDK, df_filtered: pd.DataFrame,
    df_output: pd.DataFrame, logger: IntegratedLogger) -> pd.DataFrame:
    """
    Realiza automação no site da Jadlog para simular entregas com base nos dados fornecidos e preenche o DataFrame de saída.

    Para cada registro no DataFrame filtrado, essa função acessa o formulário da Jadlog, preenche os campos
    obrigatórios com os dados de entrada e extrai o valor da cotação. Em caso de falha por CNPJ, atualiza o
    campo STATUS e continua o processamento.

    Parâmetros:
        bot (WebBot): Instância do navegador automatizado da BotCity.
        maestro (BotMaestroSDK): Instância do maestro para possível gerenciamento remoto (não usado diretamente aqui).
        df_filtered (pd.DataFrame): DataFrame contendo apenas os dados prontos para simulação.
        df_output (pd.DataFrame): DataFrame de saída que será atualizado com os resultados de cotação.
        logger (IntegratedLogger): Instância de logger para rastrear eventos e falhas.

    Retorna:
        pd.DataFrame: O mesmo DataFrame de saída fornecido, agora com a coluna 'VALOR COTAÇÃO JADLOG'
        preenchida para os CNPJs processados e, em caso de falha, a coluna 'STATUS'.

    Raises:
        Exception: Qualquer exceção geral que ocorra fora do escopo do loop principal (ex: falha de carregamento do site).
    """
    try:
        # Constantes de configuração
        DEFAULT_URL_JADLOG = vars_map['DEFAULT_URL_JADLOG']
        PICKUP_VALUE = vars_map['PICKUP_VALUE']
        ORIGIN_CEP = vars_map['ORIGIN_CEP']

        logger.info(" Início - obter_cotacoes_jadlog ")

        # Acessa o site de simulação da Jadlog
        logger.info("Abrindo o site da Jadlog para simulação")
        bot.browse(DEFAULT_URL_JADLOG)

        # Verifica se o campo de origem está disponível (validação mínima)
        if not bot.find_element('#origem'):
            raise Exception("O site da Jadlog não carregou corretamente.")

        # Mantém apenas as colunas relevantes para evitar erros em colunas ausentes
        colunas_necessarias = [
            "CNPJ",
            "TIPO DE SERVIÇO JADLOG",
            "DIMENSÕES CAIXA (altura x largura x comprimento cm)",
            "PESO DO PRODUTO",
            "CEP",
            "VALOR DO PEDIDO"
        ]
        df_filtered = df_filtered[colunas_necessarias]

        total = len(df_filtered)

        for index, row in df_filtered.iterrows():
            cnpj = row["CNPJ"]
            logger.info(f"[{index + 1}/{total}] Processando cotação para CNPJ {cnpj}")

            try:
                # Define o tipo de serviço (ex: '030' para EXPRES)
                jadlog_service_select = element_as_select(bot.find_element('#modalidade'))
                service_value = get_jadlog_value(row['TIPO DE SERVIÇO JADLOG'])
                jadlog_service_select.select_by_value(service_value)

                # Separa as dimensões (altura x largura x comprimento)
                height, width, length = row['DIMENSÕES CAIXA (altura x largura x comprimento cm)'].split(" x ")

                # Preenche as dimensões
                bot.find_element('#valLargura').clear()
                bot.find_element('#valLargura').send_keys(width)

                bot.find_element('#valAltura').clear()
                bot.find_element('#valAltura').send_keys(height)

                bot.find_element('#valComprimento').clear()
                bot.find_element('#valComprimento').send_keys(length)

                # Preenche o peso
                bot.find_element('#peso').clear()
                bot.find_element('#peso').send_keys(row['PESO DO PRODUTO'])

                # Preenche os CEPs de origem e destino
                bot.find_element('#destino').clear()
                bot.find_element('#destino').send_keys(row['CEP'])

                bot.find_element('#origem').clear()
                bot.find_element('#origem').send_keys(ORIGIN_CEP)

                # Preenche valor de coleta e valor do pedido
                bot.find_element('#valor_coleta').clear()
                bot.find_element('#valor_coleta').send_keys(PICKUP_VALUE)

                bot.find_element('#valor_mercadoria').clear()
                bot.find_element('#valor_mercadoria').send_keys(row['VALOR DO PEDIDO'])

                # Clica no botão "Simular"
                bot.find_element('//input[@value="Simular"]', By.XPATH).click()

                # Aguarda o carregamento do valor da nova cotação (evita pegar valor anterior)
                bot.wait(1000)

                # Captura o valor da cotação
                raw_quote = bot.find_element('//span[contains(text(),"R$")]', By.XPATH).get_attribute('innerText')
                formatted_quote = raw_quote.replace("R$ ", "").replace(".", ",")

                # Atualiza o DataFrame de saída
                df_output.loc[df_output["CNPJ"] == cnpj, "VALOR COTAÇÃO JADLOG"] = f"R$ {formatted_quote}"
                logger.info(f"Cotação Jadlog registrada com sucesso para CNPJ {cnpj}")

            except Exception as err:
                logger.error(f"Erro ao processar cotação para CNPJ {cnpj}: {err}")
                df_output.loc[df_output["CNPJ"] == cnpj, "STATUS"] = "Falha cotação Jadlog"
                continue

        bot.stop_browser()

    except Exception as erro_geral:
        logger.error(f"Erro geral na execução de obter_cotacoes_jadlog: {erro_geral}")
    finally:
        return df_output
