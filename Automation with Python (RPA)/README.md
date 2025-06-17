# 📨 Automação de Cotações - Correios e Jadlog

Este projeto automatiza a simulação de cotações de frete nos sites dos **Correios** e da **Jadlog**, permitindo comparar preços e selecionar a melhor opção para envio de mercadorias. O sistema gera relatórios Excel, envia notificações por e-mail e se integra ao BotCity Maestro para rastreamento e controle centralizado de tarefas.

---

## 🚀 Funcionalidades

- 🔍 Coleta automática de dados de cotação nos sites dos Correios e Jadlog
- 🧮 Comparação dos valores e destaque do menor no Excel
- 📤 Envio de planilha de resultados por e-mail
- 📬 Notificações automáticas com anexos em caso de erro
- 🪵 Geração de logs organizados por data e contexto (cliente e desenvolvedor)
- 🤖 Integração com BotCity Maestro para acompanhamento e gestão da automação

---

## 📁 Estrutura do Projeto

```
📦 Projeto
├── main.py                         # Script principal de execução da automação
├── config.py                       # Mapeamento centralizado de variáveis
├── .env                            # Variáveis de ambiente sensíveis
├── requirements.txt                # Lista de dependências do projeto
└── Utils/
    ├── helper_functions.py         # Validações e transformações
    ├── IntegratedLogger.py         # Logger inteligente com integração Maestro + email
    ├── email_functions.py          # Envio de e-mails e orquestradores
    ├── interact_correios.py        # Acesso e preenchimento do simulador dos Correios
    ├── interact_jadlog.py          # Acesso e preenchimento do simulador da Jadlog
    ├── interactions_dataframe_correios.py  # Cotação via loop para os Correios
```

---

## 🧾 Instalação

Certifique-se de ter o Python 3.10+ instalado e execute:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Execução

Para iniciar a automação:

```bash
python main.py
```

A planilha de entrada e demais caminhos devem estar configurados no arquivo `.env` ou dentro de `vars_map` no `config.py`.

---

## 📦 Entrada Esperada

O robô espera uma planilha `.xlsx` contendo, para cada CNPJ/grupo de envio:

- CEP de destino
- Peso do produto
- Dimensões do pacote (altura x largura x comprimento)
- Tipo de serviço desejado (Correios e/ou Jadlog)

---

## 📈 Resultados

- A planilha gerada contém colunas com os valores de cotação e status por transportadora.
- A célula com o menor valor entre as opções é destacada em verde.
- O arquivo é salvo na pasta de processados e enviado por e-mail automaticamente.

---

## 🧠 Logs e Erros

- Logs são salvos em dois níveis:
  - `log_*.log`: informações resumidas (nível cliente)
  - `devlog_*.log`: detalhes técnicos (nível desenvolvedor)
- Em caso de erro, é capturada uma imagem da tela e enviada por e-mail automaticamente.

---

## ☁️ Integração com BotCity Maestro

Se configurado, o robô reporta ao Maestro:

- Status de execução
- Logs detalhados
- Arquivo final como artefato
- Notificações de erro centralizadas

---

## 📬 Notificações por E-mail

- Envio de e-mails ao fim da execução (com ou sem erro)
- E-mails retirados automaticamente de uma planilha `.xlsx`
- Envio seguro via SMTP com anexo (resultado ou print de erro)

---

## 👨‍💻 Contribuição

O projeto está estruturado para expansão. Sugestões de melhoria, novas integrações (transportadoras ou APIs) ou adaptações para outros fluxos logísticos são bem-vindas.

---
