# 🧠 Clínica Escola de Psicologia – Sistema Integrado de Gestão

Este projeto foi desenvolvido para **uso interno e administrativo** de uma Clínica Escola em Psicologia, com o objetivo de digitalizar, organizar e centralizar os fluxos de atendimento, supervisão e registros institucionais. Ele substitui o uso de planilhas manuais por uma solução integrada entre **formulários**, **scripts automatizados** e **banco de dados relacional**, promovendo mais controle, segurança e eficiência. Ele integra **Google Forms**, **Google Sheets**, **Google Apps Script** e **MySQL**, permitindo o registro automatizado de pacientes, estudantes, coordenadores e atendimentos.

---

## 🛠 Tecnologias Utilizadas

- **Google Sheets & Google Forms** — Interfaces de coleta de dados.
- **Google Apps Script** — Automatização de cadastros, triggers e integração com o banco de dados.
- **MySQL** — Armazenamento relacional dos dados clínicos e acadêmicos.
- **Landing Page Institucional** — Interface para usuários internos: [Acesse aqui](https://clinica-escola-landingpage.netlify.app/)
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

- 📝 **Cadastro automatizado de**:
  - Pacientes
  - Estudantes
  - Coordenadores

- 📆 **Agendamento de consultas com**:
  - Registro de presença
  - Prontuário clínico-acadêmico
  - Controle de faltas

- 🔗 **Associação de atendimento**:
  - Vínculo entre estudante e paciente
  - Histórico clínico consolidado

- 🗂️ **Sistema de logging**:
  - Geração de arquivos no Google Drive para rastreabilidade e auditoria interna

- 🔌 **Integração via JDBC com MySQL**:
  - Envio automatizado de registros para banco relacional
  - Compatível com autenticação segura e estrutura escalável

- 🧩 **Scripts modulares**:
  - Separação por responsabilidade
  - Facilidade para manutenção e expansão do sistema

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
   - Adicione o ID da pasta do Drive ao script [`criarLog.js`](apps_script/criarLogs.js).

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

- Integração com dashboards interativos e relatórios analíticos (Looker Studio)
