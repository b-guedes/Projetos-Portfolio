import re
import time
from botcity.web import WebBot, By, element_as_select
from config import vars_map

URL_CORREIOS = vars_map["DEFAULT_CORREIOS_URL"]

def interact_correios(bot: WebBot, service_type: str, cep_destiny: str,
    weight: str, dimensions: dict, cep_origin: str = vars_map["ORIGIN_CEP"],
    shipping_date: str = None, package_format: str = "caixa",
    package_type: str = "Outra Embalagem",
) -> tuple[str, str]:
    """ 
    Acessa o site dos Correios, realiza o preenchimento do formulário de cotação e retorna os dados de entrega.

    Utiliza um navegador controlado pelo BotCity WebBot para simular o envio de uma encomenda. 
    Inclui uma camada de retry para garantir a abertura do site, caso falhe nas primeiras tentativas.

    Parâmetros:
        bot (WebBot): Instância da automação Web.
        service_type (str): Tipo de serviço a ser simulado (ex: "PAC", "SEDEX").
        cep_destiny (str): CEP de destino do envio.
        weight (str): Peso estimado da encomenda em quilos.
        dimensions (dict): Dicionário contendo altura, largura e comprimento da embalagem.
        cep_origin (str, opcional): CEP de origem. Valor padrão é carregado da configuração global.
        shipping_date (str, opcional): Data desejada de postagem (formato: ddmmaaaa). Valor padrão: data atual.
        package_format (str, opcional): Formato da embalagem. Valores possíveis: "caixa", "rolo" ou "envelope".
        package_type (str, opcional): Tipo de embalagem a ser selecionada no formulário ("Embalagem dos Correios" ou "Outra Embalagem").

    Retorna:
        tuple[str, str]: Uma tupla contendo:
            - Prazo de entrega estimado em dias úteis.
            - Valor total da cotação em reais (como string formatada, ex: "R$ 23,90").

    Raises:
        RuntimeError: Caso o site dos Correios não carregue após múltiplas tentativas.
        Exception: Para qualquer outro erro que ocorra durante o preenchimento ou extração dos dados.
    """

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            bot.browse(URL_CORREIOS)
            bot.wait(5000)  # Aguarda carregamento inicial (5 segundos)
            bot.find_element("//input[@name='cepDestino']", By.XPATH)
            break  # Página carregou, sai do loop
        except Exception as erro:
            if attempt < max_attempts:
                bot.stop_browser()
                time.sleep(3)  # Espera antes de tentar novamente
                bot.restart_browser()
            else:
                raise RuntimeError(f"Não foi possível carregar o site dos Correios após {max_attempts} tentativas: {erro}")

    if shipping_date:
        bot.find_element("input#data", By.CSS_SELECTOR).clear()
        bot.find_element("input#data", By.CSS_SELECTOR).click()
        bot.paste(shipping_date)

    bot.find_element("//input[@name='cepOrigem']", By.XPATH).click()
    bot.paste(cep_origin)

    bot.find_element("//input[@name='cepDestino']", By.XPATH).click()
    bot.paste(cep_destiny)

    element_as_select(
        bot.find_element("//select[@name='servico']", By.XPATH)
    ).select_by_visible_text(service_type)

    bot.find_element(f"img.{package_format}", By.CSS_SELECTOR).click()

    element_as_select(
        bot.find_element("//select[@name='embalagem1']", By.XPATH)
    ).select_by_visible_text(package_type)

    bot.find_element("//input[@name='Altura']", By.XPATH).click()
    bot.paste(dimensions["height"])
    bot.tab()
    bot.paste(dimensions["width"])
    bot.tab()
    bot.paste(dimensions["length"])

    bot.find_element("//select[@name='peso']", By.XPATH).send_keys(weight)
    bot.find_element("input.btn2", By.CSS_SELECTOR).click()

    tabs = bot.get_tabs()
    if len(tabs) > 1:
        bot.activate_tab(tabs[-1])

    raw_time = bot.find_element(
        "//tr[@class='destaque']/th[text()='Prazo de entrega ']/following-sibling::td",
        By.XPATH,
    ).text
    raw_price = bot.find_element(
        "//tr[@class='destaque']/th[text()='Valor total ']/following-sibling::td",
        By.XPATH,
    ).text

    bot.stop_browser()

    match = re.search(r"\+ (\d+)", raw_time)
    deliver_time = match.group(1) if match else "N/A"

    return deliver_time, raw_price
