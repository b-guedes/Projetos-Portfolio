# 🧠 Clínica Escola de Psicologia – Sistema Integrado de Gestão

Este projeto é uma solução tecnológica para gerenciamento de atendimentos clínicos em uma clínica-escola de psicologia. Ele integra **Google Forms**, **Google Sheets**, **Google Apps Script** e **MySQL**, permitindo o registro automatizado de pacientes, estudantes, coordenadores, atendimentos e consultas.

---

## 🛠 Tecnologias Utilizadas

- **Google Sheets & Forms** — Coleta de dados por meio de formulários
- **Google Apps Script** — Processamento automático, triggers e inserção no banco de dados
- **MySQL** — Armazenamento estruturado e relacional dos dados
- **Landing Page** — Interface pública para apresentação: [Acesse aqui](https://clinica-escola-landingpage.netlify.app/)

---

## 📁 Estrutura do Repositório

```plaintext
sistema-gestao-clinica-escola/

├── README.md
├── apps_script/
│   ├── criarLog.js
│   ├── obterConexao.js
│   ├── triggerAgendamentoConsultas.js
│   ├── triggerAssociacaoAtendimento.js
│   ├── triggerCadastroCoordenadores.js
│   ├── triggerCadastroEstudantes.js
│   ├── triggerCadastroPacientes.js
│   ├── utilitarios.js
│   └── README_APPS_SCRIPT.md
├── database/
│   └── schema.sql
├── sheets/
│   └── estrutura_colunas.md
├── forms/
│   └── modelos.md
├── web/
│   └── landingpage_link.md
└── LICENSE
```


---

## 🔧 Funcionalidades

- 📝 Cadastro automatizado de:
  - Pacientes
  - Estudantes
  - Coordenadores
- 📆 Agendamento de consultas com:
  - Registro de presença
  - Prontuário
  - Controle de faltas
- 🔗 Associação entre pacientes e estudantes com histórico de atendimentos
- 🗂️ Sistema de logging em arquivos no Google Drive
- 🔌 Integração com banco de dados relacional via JDBC
- 🧩 Modularização de scripts e funções auxiliares

---

## 🧰 Pré-requisitos

- Conta Google com acesso ao Drive, Forms e Sheets
- Banco de dados MySQL configurado
- Acesso ao Google Apps Script e permissões de execução

---

## ⚙️ Como Executar

1. **Configurar o Banco de Dados**  
   Execute o script [`schema.sql`](database/schema.sql) para criar as tabelas.

2. **Configurar Google Apps Script**  
   - Crie um projeto de Apps Script vinculado ao seu Google Sheets.
   - Importe os scripts da pasta [`apps_script/`](apps_script/).
   - Configure os triggers `onFormSubmit` para cada formulário.
   - Adicione o ID da pasta do Drive ao script [`criarLog.js`](apps_script/criarLog.js).

3. **Testar os fluxos de cadastro e atendimento**  
   Use os formulários para simular o preenchimento de dados.

---

## 🛡️ Licença

Este projeto está sob os termos da **Licença MIT**. Consulte o arquivo [`LICENSE`](LICENSE) para mais informações.  
![MIT License Badge](https://img.shields.io/badge/license-MIT-green)

---

## 💬 Contato

Em caso de dúvidas, sugestões ou contribuições, sinta-se à vontade para abrir uma issue ou enviar uma mensagem.

---

## 🌟 Melhorias Futuras

- Dashboard interativo com gráficos de atendimento
