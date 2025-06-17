import os
import openpyxl
from typing import List
import smtplib
from email.message import EmailMessage
from datetime import datetime
from botcity.maestro import *
from config import vars_map


# Global settings
EMAIL = vars_map['EMAIL_USERNAME']
PROCESS_NAME = "E-mail de finalização da execução"
EXCEL_FILE_PATH = vars_map['DEFAULT_EMAILS_FILE']

def obter_data_e_hora_formatadas() -> tuple[str, str]:
    """
    Retorna a data e a hora atuais no formato personalizado para uso em e-mails, log ou nome de arquivos.

    Retorna:
        tuple[str, str]: Uma tupla contendo:
            - A data atual formatada como 'ddmmaaaa'.
            - A hora atual formatada como 'HHMM'.

    Exemplo:
        Se a data e hora forem 17/06/2025 às 18:42, o retorno será:
        ('17062025', '1842')
    """
    # Obtém o momento atual do sistema
    agora = datetime.now()

    # Formata a data e a hora separadamente
    data_formatada = agora.strftime("%d%m%Y")
    hora_formatada = agora.strftime("%H%M")

    return data_formatada, hora_formatada



def ler_emails_da_planilha(caminho_arquivo: str) -> List[str]:
    """
    Lê os endereços de e-mail a partir de uma planilha Excel e retorna uma lista com os dados.

    A função assume que os e-mails estão na primeira coluna da aba ativa e ignora células vazias.
    É possível utilizar qualquer planilha `.xlsx` desde que contenha os e-mails na primeira coluna.

    Parâmetros:
        caminho_arquivo (str): Caminho absoluto ou relativo para o arquivo Excel contendo os e-mails.

    Retorna:
        list[str]: Lista com os endereços de e-mail encontrados na planilha.

    Raises:
        FileNotFoundError: Se o caminho especificado não levar a um arquivo existente.
        Exception: Para qualquer erro ao abrir ou processar a planilha.
    """
    try:
        # Verifica se o arquivo existe no caminho informado
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

        # Abre o arquivo Excel
        workbook = openpyxl.load_workbook(caminho_arquivo, data_only=True)
        sheet = workbook.active

        emails = []

        # Itera sobre a primeira coluna da aba ativa
        for row in sheet.iter_rows(min_row=1, min_col=1, max_col=1):
            for cell in row:
                if cell.value:
                    emails.append(str(cell.value).strip())

        return emails

    except FileNotFoundError as e:
        raise e  # Deixa o erro subir para tratamento externo se necessário

    except Exception as erro:
        raise Exception(f"Erro ao ler a planilha de e-mails: {erro}")


def enviar_email_com_anexo(caminho_arquivo_anexo: str, assunto: str, corpo: str,
    remetente: str, senha_app: str, destinatarios: list[str],
    logger=None) -> None:
    """
    Envia um e-mail com anexo do tipo Excel para uma lista de destinatários utilizando SMTP seguro (SSL).

    Parâmetros:
        caminho_arquivo_anexo (str): Caminho do arquivo a ser anexado (.xlsx).
        assunto (str): Título do e-mail (campo "Subject").
        corpo (str): Mensagem de texto que será o conteúdo do e-mail.
        remetente (str): Endereço de e-mail que enviará a mensagem.
        senha_app (str): Senha do aplicativo para autenticação do SMTP.
        destinatarios (list[str]): Lista de e-mails que irão receber a mensagem.
        logger (opcional): Instância de logger para registrar eventos e falhas.

    Retorna:
        None

    Raises:
        FileNotFoundError: Se o arquivo de anexo não for localizado.
        smtplib.SMTPException: Para qualquer erro durante o envio via servidor SMTP.
    """
    try:
        # Verifica se o anexo existe
        if not os.path.exists(caminho_arquivo_anexo):
            raise FileNotFoundError(f"Arquivo anexo não encontrado: {caminho_arquivo_anexo}")

        # Lê o conteúdo do anexo
        with open(caminho_arquivo_anexo, "rb") as arquivo:
            anexo_bytes = arquivo.read()

        # Configura e envia e-mail para cada destinatário
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remetente, senha_app)

            for destinatario in destinatarios:
                msg = EmailMessage()
                msg["Subject"] = assunto
                msg["From"] = remetente
                msg["To"] = destinatario
                msg.set_content(corpo)
                msg.add_attachment(
                    anexo_bytes,
                    maintype="application",
                    subtype="xlsx",
                    filename=os.path.basename(caminho_arquivo_anexo)
                )

                smtp.send_message(msg)
                if logger:
                    logger.info(f"E-mail enviado com sucesso para: {destinatario}")

    except FileNotFoundError as e:
        if logger:
            logger.error(f"Arquivo anexo não localizado: {e}")
        raise

    except smtplib.SMTPException as e:
        if logger:
            logger.error(f"Erro ao enviar e-mail: {e}")
        raise

    except Exception as e:
        if logger:
            logger.error(f"Erro inesperado durante envio de e-mails: {e}")
        raise


def enviar_email_de_erro(remetente: str, senha_app: str, destinatarios: list[str],
    processo: str, mensagem_erro: str, caminho_screenshot: str = None,
    logger=None) -> None:
    """
    Envia uma notificação por e-mail para informar que um erro ocorreu durante a execução do RPA.

    O corpo do e-mail contém o nome do processo afetado, a data, a hora e uma descrição resumida do erro.
    Um screenshot pode ser anexado, caso o caminho da imagem seja fornecido.

    Parâmetros:
        remetente (str): Endereço de e-mail que enviará a notificação.
        senha_app (str): Senha do aplicativo configurada para o envio via SMTP.
        destinatarios (list[str]): Lista de e-mails que irão receber a notificação.
        processo (str): Nome do processo RPA em que o erro ocorreu.
        mensagem_erro (str): Descrição detalhada do erro ocorrido.
        caminho_screenshot (str, opcional): Caminho de um arquivo .png com print de tela. Padrão: None.
        logger (opcional): Instância de logger para registrar eventos e erros.

    Retorna:
        None

    Raises:
        Exception: Caso ocorra falha ao enviar o e-mail.
    """
    try:
        data = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M")

        assunto = f"Erro - RPA [{processo}] {data} ⏰ {hora}"
        corpo = (
            f"O processo RPA '{processo}' encontrou um erro em {data} às {hora}.\n\n"
            f"Detalhes do erro:\n{mensagem_erro}"
        )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha_app)

            for destinatario in destinatarios:
                msg = EmailMessage()
                msg['Subject'] = assunto
                msg['From'] = remetente
                msg['To'] = destinatario
                msg.set_content(corpo)

                # Anexa o screenshot, se houver
                if caminho_screenshot and os.path.exists(caminho_screenshot):
                    with open(caminho_screenshot, "rb") as img:
                        msg.add_attachment(
                            img.read(),
                            maintype='image',
                            subtype='png',
                            filename=os.path.basename(caminho_screenshot)
                        )

                smtp.send_message(msg)
                if logger:
                    logger.info(f"Notificação de erro enviada para: {destinatario}")

    except Exception as erro:
        if logger:
            logger.error(f"Erro ao enviar e-mail de notificação: {erro}")
        raise Exception(f"Erro ao enviar e-mail de notificação: {erro}")


def executar_envio_email(
    caminho_arquivo_anexo: str,
    nome_processo: str,
    logger=None
) -> None:
    """
    Função orquestradora que realiza o envio do e-mail de conclusão do RPA com planilha em anexo.

    Parâmetros:
        caminho_arquivo_anexo (str): Caminho completo da planilha gerada pelo processo.
        nome_processo (str): Nome do processo RPA (para aparecer no assunto e corpo do e-mail).
        logger (opcional): Instância do logger integrado para registrar eventos.

    Retorna:
        None
    """
    try:
        from config import vars_map
        # from .envio_email_base import (
        #     obter_data_e_hora_formatadas,
        #     ler_emails_da_planilha,
        #     enviar_email_com_anexo
        # )

        data, hora = obter_data_e_hora_formatadas()
        remetente = vars_map["EMAIL_USERNAME"]
        senha_app = vars_map["EMAIL_PASSWORD"]
        caminho_planilha_emails = vars_map["DEFAULT_EMAILS_FILE"]

        assunto = f"RPA {nome_processo} - {data} - {hora}"
        corpo = (
            f"O processo RPA '{nome_processo}' foi executado com sucesso em {data}, às {hora}.\n\n"
            "A planilha de resultados está anexada neste e-mail."
        )

        destinatarios = ler_emails_da_planilha(caminho_planilha_emails)

        enviar_email_com_anexo(
            caminho_arquivo_anexo=caminho_arquivo_anexo,
            assunto=assunto,
            corpo=corpo,
            remetente=remetente,
            senha_app=senha_app,
            destinatarios=destinatarios,
            logger=logger
        )

    except Exception as erro:
        if logger:
            logger.error(f"Erro na função de envio de e-mail de conclusão: {erro}")
        raise


def executar_envio_email_erro(
    remetente: str,
    senha_app: str,
    destinatarios: list[str],
    processo: str,
    mensagem_erro: str,
    caminho_screenshot: str = None,
    logger=None
) -> None:
    """
    Função orquestradora para envio de um e-mail de notificação de erro com informações da falha.

    Utiliza as funções refatoradas para gerar timestamp, formatar mensagem de erro
    e acionar o envio seguro via SMTP com ou sem anexo (print).

    Parâmetros:
        remetente (str): Endereço do remetente autenticado para o envio.
        senha_app (str): Senha do aplicativo associada à conta de e-mail.
        destinatarios (list[str]): Lista de e-mails para envio da notificação.
        processo (str): Nome do processo RPA que encontrou uma falha.
        mensagem_erro (str): Descrição técnica ou resumida do erro ocorrido.
        caminho_screenshot (str, opcional): Caminho completo de um print de tela relevante. Default: None.
        logger (opcional): Logger para registrar sucesso ou falha do envio.

    Retorna:
        None

    Raises:
        Exception: Se a tentativa de envio do e-mail falhar por erro interno.
    """
    try:

        enviar_email_de_erro(
            remetente=remetente,
            senha_app=senha_app,
            destinatarios=destinatarios,
            processo=processo,
            mensagem_erro=mensagem_erro,
            caminho_screenshot=caminho_screenshot,
            logger=logger
        )

    except Exception as erro:
        if logger:
            logger.error(f"Falha ao executar envio de e-mail de erro: {erro}")
        raise
