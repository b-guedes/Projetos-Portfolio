# Clínica Escola Psicologia – Sistema Integrado de Gestão

Este projeto é uma solução tecnológica para gerenciamento de atendimentos clínicos em uma clínica-escola de psicologia. Ele integra **Google Forms**, **Google Sheets**, **Google Apps Script** e **MySQL**, permitindo o registro automatizado de pacientes, estudantes, coordenadores, atendimentos e consultas.

---

##  Tecnologias Utilizadas

- **Google Sheets & Forms** — Coleta de dados por meio de formulários
- **Google Apps Script** — Processamento automático, triggers e inserção no banco de dados
- **MySQL** — Armazenamento estruturado e relacional dos dados
- **Landing Page** — Interface pública para apresentação: [Acesse aqui](https://clinica-escola-landingpage.netlify.app/)

---

## 📁 Estrutura do Repositório

clinica-escola-psicologia/
├── README.md
├── database/
│   └── schema.sql
├── forms/
│   └── modelos.md
├── sheets/
│   └── estrutura_colunas.md
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
├── web/
│   └── landingpage_link.md
└── LICENSE


---

## Funcionalidades

- Cadastro automatizado de:
  - Pacientes
  - Estudantes
  - Coordenadores
- Agendamento de consultas com registro de presença, prontuário e faltas
- Associação entre pacientes e estudantes com histórico de atendimentos
- Sistema de logging em arquivos no Google Drive para rastreamento das execuções
- Integração com banco de dados relacional por JDBC
- Modularização de scripts e funções auxiliares

---

## Como Executar

1. **Configurar o Banco de Dados**  
   Execute `schema.sql` para criar as tabelas.

2. **Configurar Google Apps Script**  
   - Crie um projeto de Apps Script vinculado ao seu Google Sheets.
   - Importe os scripts da pasta `apps_script/`.
   - Configure os triggers `onFormSubmit` para cada formulário.
   - Crie uma pasta no Google Drive e adicione seu ID ao `criarLog.js`.

3. **Testar os fluxos de cadastro e atendimento**  
   Use os formulários para simular o preenchimento de dados.

---

## Licença

Este projeto está licenciado sob os termos da **Licença MIT**. Consulte o arquivo [`LICENSE`](./LICENSE) para mais informações.

---

## Contato

Em caso de dúvidas, sugestões ou contribuições, sinta-se à vontade para abrir uma issue ou enviar uma mensagem.

---

