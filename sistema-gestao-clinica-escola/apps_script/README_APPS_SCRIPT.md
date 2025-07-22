# Google Apps Script – Integração com Google Sheets e MySQL

Este diretório contém os scripts utilizados para integrar os formulários e planilhas do Google com o banco de dados MySQL da clínica-escola de psicologia. A automação garante que os dados sejam processados em tempo real por meio de triggers do Apps Script.

---

## Configuração Inicial

1. **Crie um projeto de Apps Script** associado a cada planilha (Google Sheets).
2. Importe os arquivos correspondentes deste diretório.
3. Crie uma pasta no Google Drive para armazenar os logs e obtenha o `ID da pasta`.
4. Configure o ID da pasta no script `criarLog.js`.
5. Configure os triggers do tipo `onFormSubmit` para cada formulário.

---

## Scripts

| Arquivo                          | Finalidade                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `criarLog.js`                    | Cria arquivos de log detalhado em uma pasta no Drive                       |
| `obterConexao.js`               | Estabelece conexão com banco MySQL via JDBC                                |
| `utilitarios.js`                | Funções auxiliares de busca por nome para obter IDs de entidades           |
| `triggerCadastroPacientes.js`   | Processa o cadastro de pacientes e endereço via formulário                 |
| `triggerCadastroEstudantes.js`  | Insere estudantes com vínculo a coordenadores e núcleos                    |
| `triggerCadastroCoordenadores.js`| Insere coordenadores vinculados ao núcleo correspondente                   |
| `triggerAssociacaoAtendimento.js`| Registra associação entre paciente e estudante                             |
| `triggerAgendamentoConsultas.js`| Registra consultas, faltas e prontuários clínicos                          |

---

## Permissões Necessárias

O projeto requer as seguintes permissões para funcionar corretamente:

- Acesso ao **Google Drive** (para salvar logs)
- Acesso ao **Google Sheets** (triggers)
- Acesso ao **JDBC / Banco de Dados Externo**

---

##  Boas Práticas

- Utilize `PropertiesService` para armazenar credenciais como usuário e senha do banco.
- Documente as planilhas com mapeamento de colunas para facilitar manutenção.
- Faça testes com entradas simuladas antes de ativar em produção.
- Revise os logs regularmente para identificar possíveis falhas ou inconsistências.

---

## Suporte

Para dúvidas sobre integração com Apps Script, consulte a [documentação oficial](https://developers.google.com/apps-script/guides/jdbc) ou envie uma issue neste repositório.
