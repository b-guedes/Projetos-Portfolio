import os
import logging
import sys
import traceback
from datetime import datetime
from PIL import ImageGrab
from botcity import maestro
from botcity.web import WebBot  # Opcional, dependendo do seu uso externo
from .functions_email import send_error_email

class IntegratedLogger:
    """
    Logger customizado que integra logs locais (cliente e desenvolvedor),
    comunicação com o BotCity Maestro e envio de notificações por e-mail.

    Gera logs diários com separação entre informações relevantes para clientes e dados técnicos,
    além de capturar prints de tela e enviar alertas em casos de erro.
    """

    def __init__(self, maestro: maestro.BotMaestroSDK, filepath: os.PathLike, activity_label: str):
        self.maestro = maestro
        self.filepath = filepath
        self.image_filepath = filepath
        self.activity_label = activity_label
        self.dev_logger = logging.getLogger("dev_logger")
        self.client_logger = logging.getLogger("client_logger")
        self.datetime_format = "%d-%m-%Y %H:%M:%S"
        self.datetime_file_format = "%d-%m-%Y_%H-%M-%S"
        self.__initial_configs()

    def __initial_configs(self):
        """
        Configura os diretórios e arquivos de log. Cria pastas separadas para logs e imagens.
        """
        data_path = datetime.now().strftime("%d-%m-%Y")
        self.filepath = os.path.join(self.filepath, data_path, "Files")
        self.image_filepath = os.path.join(self.filepath.replace("Files", ""), "Errors")

        os.makedirs(self.filepath, exist_ok=True)
        os.makedirs(self.image_filepath, exist_ok=True)

        # Configura logger de desenvolvedor
        self.dev_logger.setLevel(logging.DEBUG)
        handler_dev = logging.FileHandler(
            filename=os.path.join(self.filepath, f"devlog_{datetime.now().strftime(self.datetime_file_format)}.log"),
            mode="a", encoding="utf-8"
        )
        handler_dev.setFormatter(logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt=self.datetime_format))
        self.dev_logger.addHandler(handler_dev)

        # Adiciona saída no terminal (útil para debug local)
        stream_dev = logging.StreamHandler()
        stream_dev.setFormatter(logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt=self.datetime_format))
        self.dev_logger.addHandler(stream_dev)

        # Configura logger de cliente
        self.client_logger.setLevel(logging.INFO)
        handler_client = logging.FileHandler(
            filename=os.path.join(self.filepath, f"log_{datetime.now().strftime(self.datetime_file_format)}.log"),
            mode="a", encoding="utf-8"
        )
        handler_client.setFormatter(logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt=self.datetime_format))
        self.client_logger.addHandler(handler_client)

        self.dev_logger.info(f"Logs salvos em: {self.filepath}")
        self.dev_logger.info(f"Capturas de erro em: {self.image_filepath}")

    def info(self, msg: str):
        """
        Registra uma mensagem de informação no log (nível INFO).

        Parâmetros:
            msg (str): Mensagem a ser registrada.
        """
        for line in msg.splitlines():
            self.dev_logger.info(line)
            self.client_logger.info(line)

        if self.maestro:
            self.maestro.new_log_entry(
                activity_label=self.activity_label,
                values={
                    "Datetime": datetime.now().strftime(self.datetime_format),
                    "Level": "INFO",
                    "Message": msg.splitlines()[-1]
                }
            )

    def debug(self, msg: str):
        """
        Registra uma mensagem de depuração no log (nível DEBUG).

        Parâmetros:
            msg (str): Mensagem a ser registrada.
        """
        for line in msg.splitlines():
            self.dev_logger.debug(line)

        if self.maestro:
            self.maestro.new_log_entry(
                activity_label=self.activity_label,
                values={
                    "Datetime": datetime.now().strftime(self.datetime_format),
                    "Level": "DEBUG",
                    "Message": msg.splitlines()[-1]
                }
            )

    def warning(self, process_name: str):
        """
        Registra um aviso no log com captura de tela e envio de e-mail.

        Parâmetros:
            process_name (str): Nome da etapa/processo em que o aviso ocorreu.
        """
        msg_list = traceback.format_exc().splitlines()
        etype, value, _ = sys.exc_info()
        msg_reduced = "".join(traceback.format_exception_only(etype, value)).strip()

        for msg in msg_list:
            self.dev_logger.warning(msg)
        self.client_logger.warning(msg_reduced)

        screenshot_path = os.path.join(
            self.image_filepath,
            f"{datetime.now().strftime(self.datetime_file_format)}_RPA_{process_name}.jpg"
        )

        try:
            ImageGrab.grab().save(screenshot_path)
        except Exception as e:
            screenshot_path = None
            self.dev_logger.warning(f"Falha ao capturar screenshot: {e}")

        send_error_email(process_name, msg_reduced, screenshot_path)

        if self.maestro:
            self.maestro.new_log_entry(
                activity_label=self.activity_label,
                values={
                    "Datetime": datetime.now().strftime(self.datetime_format),
                    "Level": "WARNING",
                    "Message": msg_reduced
                }
            )
            self.maestro.error(
                task_id=self.maestro.get_execution().task_id,
                exception=Exception(msg_reduced),
                screenshot=screenshot_path
            )

    def error(self, process_name: str):
        """
        Registra um erro no log com captura de tela e envio de notificação por e-mail.

        Parâmetros:
            process_name (str): Nome da etapa/processo em que o erro ocorreu.
        """
        msg_list = traceback.format_exc().splitlines()
        etype, value, _ = sys.exc_info()
        msg_reduced = "".join(traceback.format_exception_only(etype, value)).strip()

        for msg in msg_list:
            self.dev_logger.error(msg)
        self.client_logger.error(msg_reduced)

        screenshot_path = os.path.join(
            self.image_filepath,
            f"{datetime.now().strftime(self.datetime_file_format)}_RPA_{process_name}.jpg"
        )

        try:
            ImageGrab.grab().save(screenshot_path)
        except Exception as e:
            screenshot_path = None
            self.dev_logger.warning(f"Falha ao capturar screenshot: {e}")

        send_error_email(process_name, msg_reduced, screenshot_path)

        if self.maestro:
            self.maestro.new_log_entry(
                activity_label=self.activity_label,
                values={
                    "Datetime": datetime.now().strftime(self.datetime_format),
                    "Level": "ERROR",
                    "Message": msg_reduced
                }
            )
            self.maestro.error(
                task_id=self.maestro.get_execution().task_id,
                exception=Exception(msg_reduced),
                screenshot=screenshot_path
            )
