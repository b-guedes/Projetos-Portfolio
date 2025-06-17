import pandas as pd
from pandas import Series

def check_variables_correios(row: Series) -> tuple[dict, str, str, str]:
    """
    Valida e extrai as variáveis necessárias para simulação de envio nos Correios.

    A função garante que os dados fornecidos por linha estejam completos e sigam os critérios
    exigidos pelo site dos Correios, incluindo dimensões mínimas/máximas e campos obrigatórios.

    Parâmetros:
        row (Series): Linha de um DataFrame contendo os dados de entrada.

    Retorna:
        tuple[dict, str, str, str]: Uma tupla contendo:
            - dicionário com as dimensões da embalagem (height, width, length)
            - peso estimado do produto (str)
            - tipo de serviço escolhido (str)
            - CEP de destino (str)

    Raises:
        ValueError: Se algum dos campos estiver ausente ou inválido.
    """

    # Define a chave para o campo de dimensões
    campo_dimensoes = "DIMENSÕES CAIXA (altura x largura x comprimento cm)"

    try:
        # Extrai os dados da linha
        dim_string = row[campo_dimensoes]
        peso = row["PESO DO PRODUTO"]
        servico = row["TIPO DE SERVIÇO CORREIOS"]
        cep_destino = str(row["CEP"]).strip()

        # Verifica campos obrigatórios
        if pd.isna(peso):
            raise ValueError("Peso do produto ausente.")
        if pd.isna(dim_string):
            raise ValueError("Dimensões da embalagem ausentes.")
        if pd.isna(servico):
            raise ValueError("Tipo de serviço dos Correios ausente.")
        if pd.isna(cep_destino) or not cep_destino.isdigit():
            raise ValueError("CEP de destino inválido.")

        # Valida e formata as dimensões
        partes = dim_string.strip().split(" x ")
        if len(partes) != 3:
            raise ValueError("Formato inválido nas dimensões da embalagem.")

        chaves = ["height", "width", "length"]
        dimensoes = dict(zip(chaves, partes))

        if not are_package_dimensions_valid(**dimensoes):
            raise ValueError("Dimensões da embalagem fora dos critérios dos Correios.")

        return dimensoes, str(peso), servico.strip(), cep_destino

    except Exception as erro:
        raise ValueError(f"Falha ao validar linha da planilha: {erro}")


def are_package_dimensions_valid(height: str, width: str, length: str) -> bool:
    """
    Verifica se as dimensões da embalagem estão dentro dos critérios definidos pelos Correios.

    As restrições oficiais (para envio via Correios) são:
        - Altura: mínimo 0.4 cm e máximo 100 cm
        - Largura: mínimo 8 cm e máximo 100 cm
        - Comprimento: mínimo 13 cm e máximo 100 cm
        - Soma das três dimensões: mínimo 21.4 cm e máximo 200 cm

    Parâmetros:
        height (str): Altura da embalagem, como string numérica (ex: "10").
        width (str): Largura da embalagem, como string numérica (ex: "15").
        length (str): Comprimento da embalagem, como string numérica (ex: "30").

    Retorna:
        bool: Retorna True se todas as restrições forem atendidas, ou False se alguma for violada.

    Raises:
        ValueError: Se as entradas não forem valores numéricos convertíveis em float.
    """
    try:
        # Converte os valores recebidos para float
        altura = float(height)
        largura = float(width)
        comprimento = float(length)

        soma_total = altura + largura + comprimento

        # Lista de restrições estabelecidas pelos Correios
        restricoes = [
            0.4 <= altura <= 100,
            8 <= largura <= 100,
            13 <= comprimento <= 100,
            21.4 <= soma_total <= 200
        ]

        return all(restricoes)

    except ValueError as e:
        # Retorna falso se não for possível converter os valores para número
        return False



def get_jadlog_value(jadlog_service: str) -> str:
    """
    Retorna o código correspondente ao tipo de serviço Jadlog informado.

    Parâmetros:
        jadlog_service (str): Nome do serviço Jadlog (ex: "JADLOG Expresso").

    Retorna:
        str: Código interno correspondente ao serviço Jadlog.

    Raises:
        KeyError: Se o tipo de serviço informado não existir no dicionário.
    """
    JADLOG_DICT = {
        "JADLOG Expresso": "0",
        "JADLOG Econômico": "5",
        "JADLOG Doc": "6",
        "JADLOG Cargo": "12",
        "JADLOG Rodo": "4",
        "JADLOG Package": "3",
        "JADLOG .Com": "9",
    }

    try:
        return JADLOG_DICT[jadlog_service]
    except KeyError:
        raise KeyError(f"Serviço Jadlog não reconhecido: {jadlog_service}")


def calc_finish_task(df_output: pd.DataFrame) -> tuple[int, int, int]:
    """
    Calcula as estatísticas de execução para reportar no Maestro.

    Considera como 'finalizado' qualquer linha com pelo menos uma cotação preenchida.
    Linhas completamente vazias em ambos os campos de cotação são consideradas erro.

    Parâmetros:
        df_output (pd.DataFrame): DataFrame com colunas de cotação dos Correios e Jadlog.

    Retorna:
        tuple[int, int, int]: Uma tupla contendo:
            - total_tasks (int): Total de registros processados.
            - total_finished (int): Total com pelo menos uma cotação preenchida.
            - total_errors (int): Total de registros falhos (ambos vazios).
    """
    colunas = ["VALOR COTAÇÃO JADLOG", "VALOR COTAÇÃO CORREIOS"]
    df_check = df_output[colunas] if all(col in df_output.columns for col in colunas) else df_output

    total_tasks = len(df_check)
    total_finished = len(df_check.dropna(how='all'))
    total_errors = total_tasks - total_finished

    return total_tasks, total_finished, total_errors
