import os
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.chrome.service import Service  
from webdriver_manager.chrome import ChromeDriverManager  
from config import vars_map


def access_website(driver, url, logger):
    """
    Acessa o site especificado e espera que o elemento com classe 'btn-large' esteja visível.
    
    Parâmetros:
        driver: Instância do WebDriver.
        url (str): URL do site a ser acessado.
        logger: Instância do logger para registrar eventos.
    """
    logger.info(f"Acessando o site: {url}")
    driver.get(url)
    # Aguarda até o elemento com a classe 'btn-large' ficar visível (timeout de 40 seg)
    WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'btn-large'))
    )
    logger.info(f"Site {url} acessado com sucesso!")


def start_challenge(driver, logger):
    """
    Clica no botão para iniciar o desafio.
    
    Parâmetros:
        driver: Instância do WebDriver.
        logger: Instância do logger.
    """
    logger.info("Iniciando desafio")
    # Clica no botão identificado pelo XPATH (ajuste o XPATH se necessário)
    driver.find_element(
        By.XPATH, '/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button'
    ).click()
    logger.info("Desafio iniciado com sucesso!")


def capture_form_xpaths(logger):
    """
    Retorna um dicionário com os XPaths dos campos do formulário.
    
    Parâmetros:
        logger: Instância do logger.
        
    Retorna:
        dict: Dicionário com os XPaths dos elementos do formulário.
    """
    logger.info("Capturando XPaths dos campos do formulário")
    locators = {
        'first_name': '//input[@ng-reflect-name="labelFirstName"]',
        'last_name': '//input[@ng-reflect-name="labelLastName"]',
        'company_name': '//input[@ng-reflect-name="labelCompanyName"]',
        'role_in_company': '//input[@ng-reflect-name="labelRole"]',
        'address': '//input[@ng-reflect-name="labelAddress"]',
        'email': '//input[@ng-reflect-name="labelEmail"]',
        'phone_number': '//input[@ng-reflect-name="labelPhone"]',
        'submit': '//input[@value="Submit"]'
    }
    logger.debug(f"XPaths capturados: {locators}")
    return locators


def fill_form_data(driver, data, logger):
    """
    Preenche o formulário com os dados do DataFrame.
    
    Parâmetros:
        driver: Instância do WebDriver.
        data (DataFrame): Dados extraídos do arquivo Excel.
        logger: Instância do logger para registrar o progresso.
    """
    logger.info("Preenchendo formulário com os dados do arquivo Excel")
    locators = capture_form_xpaths(logger)
    for index, row in data.iterrows():
        try:
            driver.find_element(By.XPATH, locators['first_name']).send_keys(row['RAZÃO SOCIAL'])
            driver.find_element(By.XPATH, locators['last_name']).send_keys(row['SITUAÇÃO CADASTRAL'])
            driver.find_element(By.XPATH, locators['company_name']).send_keys(row['NOME FANTASIA'])
            driver.find_element(By.XPATH, locators['role_in_company']).send_keys(row['DESCRIÇÃO MATRIZ FILIAL'])
            driver.find_element(By.XPATH, locators['address']).send_keys(row['ENDEREÇO'])
            driver.find_element(By.XPATH, locators['email']).send_keys(row['E-MAIL'])
            driver.find_element(By.XPATH, locators['phone_number']).send_keys(row['TELEFONE + DDD'])
            driver.find_element(By.XPATH, locators['submit']).click()
            logger.info(f"Linha {index + 1} inserida com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao inserir dados da linha {index + 1}: {e}")
            # Em caso de erro, continua para a próxima linha
            continue


def capture_execution_time(driver, logger):
    """
    Captura o tempo de execução exibido no site.
    
    Parâmetros:
        driver: Instância do WebDriver.
        logger: Instância do logger.
        
    Retorna:
        str: Tempo de execução capturado.
    """
    logger.info("Capturando tempo de execução")
    message = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'message2'))
    )
    execution_time = message.text
    logger.info(f"Tempo de execução capturado: {execution_time}")
    return execution_time


def take_success_screenshot(driver, image_path, logger):
    """
    Tira um screenshot da página e salva no caminho especificado.
    
    Parâmetros:
        driver: Instância do WebDriver.
        image_path (str): Caminho onde o screenshot será salvo.
        logger: Instância do logger.
    """
    logger.info(f"Tirando screenshot da página e salvando em {image_path}")
    driver.save_screenshot(image_path)
    logger.info(f"Screenshot salvo com sucesso em {image_path}")


def initialize_browser(logger):
    """
    Inicializa o navegador Chrome utilizando webdriver_manager.
    
    Parâmetros:
        logger: Instância do logger.
        
    Retorna:
        WebDriver: Instância configurada do Chrome.
    """
    logger.info("Inicializando navegador Chrome")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    logger.info("Navegador Chrome inicializado com sucesso!")
    return driver


def close_browser(driver, logger):
    """
    Fecha o navegador.
    
    Parâmetros:
        driver: Instância do WebDriver a ser fechada.
        logger: Instância do logger.
    """
    logger.info("Fechando navegador Chrome")
    driver.quit()
    logger.info("Navegador Chrome fechado com sucesso!")


def rpa_challenge(logger, df):
    """
    Função principal para orquestrar a execução do script de automação.
    
    Parâmetros:
        logger: Instância do logger para registrar os eventos.
        df (DataFrame): Dados do arquivo Excel a serem usados no formulário.
        
    Observações:
        - O caminho para salvar o screenshot e a URL do desafio são obtidos de vars_map.
        - Ajuste as chamadas comentadas conforme a necessidade.
    """
    # Define o caminho para salvar o screenshot; se 'DEFAULT_IMAGE_PATH' não estiver configurado, utiliza um caminho vazio
    image_path = os.path.join(vars_map.get('DEFAULT_IMAGE_PATH', ''), "screenshot.png")
    
    try:
        data = df  # Espera que df já seja um DataFrame válido
        logger.info("Arquivo carregado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao carregar o arquivo Excel: {e}")
        return

    driver = initialize_browser(logger)
    try:
        access_website(driver, vars_map.get('DEFAUT_RPACHALLENGE_URL', ''), logger)
        # Caso seja necessário iniciar o desafio, descomente a linha abaixo:
        # start_challenge(driver, logger)
        fill_form_data(driver, data, logger)
        # Se necessário, capture o tempo de execução:
        # execution_time = capture_execution_time(driver, logger)
        # logger.info(f"Tempo de execução: {execution_time}")
        # Para salvar screenshot, descomente a linha abaixo:
        # take_success_screenshot(driver, image_path, logger)
        logger.info("Execução finalizada com sucesso!")
    except Exception as e:
        logger.error(f"Erro durante o processo rpa_challenge: {e}")
    finally:
        close_browser(driver, logger)


if __name__ == "__main__":
    # Configuração básica do logger para execução local
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("RPA_Challenge")

    # Exemplo de carregamento de dados (substitua pelo seu arquivo real)
    # df = pd.read_excel(r"C:\caminho\para\seu\arquivo.xlsx")
    # Para teste, criamos um DataFrame dummy:
    df = pd.DataFrame({
        "RAZÃO SOCIAL": ["Empresa A", "Empresa B"],
        "SITUAÇÃO CADASTRAL": ["Ativa", "Suspensa"],
        "NOME FANTASIA": ["Fantasia A", "Fantasia B"],
        "DESCRIÇÃO MATRIZ FILIAL": ["Matriz", "Filial"],
        "ENDEREÇO": ["Rua A, 123", "Rua B, 456"],
        "E-MAIL": ["a@empresa.com", "b@empresa.com"],
        "TELEFONE + DDD": ["(11) 1234-5678", "(11) 8765-4321"],
        "CNPJ": ["00000000000191", "00000000000272"]
    })
    rpa_challenge(logger, df)
