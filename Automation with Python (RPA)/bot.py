import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from botcity.maestro import *
from botcity.web import WebBot, Browser, By
from config import vars_map
from Utils import *

# Carrega variáveis de ambiente
load_dotenv(override=True)

# Verifica conexão com Maestro
IS_MAESTRO_CONNECTED = vars_map['IS_MAESTRO_CONNECTED']
ACTIVITY_LABEL = vars_map['ACTIVITY_LABEL']
BotMaestroSDK.RAISE_NOT_CONNECTED = not IS_MAESTRO_CONNECTED


def main():
    # Inicializa objetos padrão
    maestro = vars_map['DEFAULT_MAESTRO']
    execution = vars_map['DEFAULT_EXECUTION']
    bot = vars_map['DEFAULT_BOT']
    
    logger = IntegratedLogger(
        maestro=maestro,
        filepath=vars_map['BASE_LOG_PATH'],
        activity_label=ACTIVITY_LABEL
    )

    try:
        logger.info("=" * 50)
        logger.info("🏁 Início do Processo: RPA VALOR COTAÇÃO")
        logger.info("=" * 50)
        
        # 1. Leitura de entrada
        input_path = os.path.join(vars_map['DEFAULT_PROCESSAR_PATH'], 'Planilha de Entrada Grupos.xlsx')
        df = open_excel_file_to_dataframe(input_path, logger)
        df_output = create_output_dataframe(df, logger)

        # 2. Processamento via API
        api_data, df_output = api_data_lookup(df_output, logger)
        api_data = make_column_endereco(api_data, logger)
        df_output, df_correios, df_jadlog = make_jadlog_correios_dataframes(df_output, api_data, logger)

        # 3. Interações Web
        rpa_challenge(df=api_data, logger=logger)
        df_output = buscar_cotacoes_correios(df_filtered=df_correios, df_output=df_output, bot=bot, logger=logger)
        df_output = obter_cotacoes_jadlog(bot=bot, maestro=maestro, df_filtered=df_jadlog, df_output=df_output, logger=logger)

        # 4. Salvamento e Comparações
        output_file = save_df_output_to_excel(vars_map['DEFAULT_PROCESSADOS_PATH'], df_output, logger)
        compare_quotation(df_output, output_file, logger)

        # 5. Envio de resultado por e-mail
        executar_envio_email(
            caminho_arquivo_anexo=output_file,
            nome_processo="RPA VALOR COTAÇÃO",
            logger=logger
        )

    except Exception as erro:
        logger.error(f"Erro durante a execução do processo principal: {erro}", exc_info=True)

        if IS_MAESTRO_CONNECTED:
            maestro.finish_task(
                task_id=execution.task_id,
                status=AutomationTaskFinishStatus.FAILED,
                message="Task finalizada com falhas.",
                total_items=0,
                processed_items=0,
                failed_items=0
            )

        # Envia e-mail de erro com anexo opcional de print
        executar_envio_email_erro(
            remetente=vars_map['EMAIL_USERNAME'],
            senha_app=vars_map['EMAIL_PASSWORD'],
            destinatarios=ler_emails_da_planilha(vars_map['DEFAULT_EMAILS_FILE']),
            processo="RPA VALOR COTAÇÃO",
            mensagem_erro=str(erro),
            caminho_screenshot=None,  # Você pode adicionar o caminho de print aqui, se desejar
            logger=logger
        )

    else:
        total_tasks, total_success, total_failed = calc_finish_task(df_output)

        if IS_MAESTRO_CONNECTED:
            maestro.post_artifact(
                task_id=execution.task_id,
                artifact_name=os.path.basename(output_file),
                filepath=output_file
            )

            maestro.finish_task(
                task_id=execution.task_id,
                status=AutomationTaskFinishStatus.SUCCESS,
                message="Task finalizada com sucesso.",
                total_items=total_tasks,
                processed_items=total_success,
                failed_items=total_failed
            )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()