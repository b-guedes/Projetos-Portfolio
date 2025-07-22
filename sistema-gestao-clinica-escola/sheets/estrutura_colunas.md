# 📋 Projeto de Gestão de Atendimento Clínico

Este documento apresenta a estrutura de dados utilizada em um sistema de gerenciamento de atendimentos clínicos, incluindo cadastro de pacientes, agendamentos, associações, estudantes e coordenadores envolvidos.

---

## 🧍 Cadastro de Pacientes

**Colunas:**
- Carimbo de data/hora
- Nome completo
- Data de Nascimento
- Sexo
- Telefone (xx) xxx-xxx-xxx
- E-mail
- Rua
- Número
- Bairro
- Cidade
- Estado
- CEP

---

## 🔄 Associação Paciente-Atendimento

**Colunas:**
- Carimbo de data/hora
- Nome do Paciente
- Nome do Estudante
- Data de INÍCIO do atendimento
- Data de FIM do atendimento (caso já encerrado)

---

## 📅 Agendamento de Consultas

**Colunas:**
- Carimbo de data/hora
- Nome do paciente
- Nome do Estudante
- Data da consulta
- Horário da consulta
- Status da consulta
- Compareceu?
- Justificativa
- Link para documento/anexo (se houver)
- Registros da consulta (resumo)
- Observações clínicas
- Encaminhamentos necessários
- Link para arquivo digitalizado (se houver)

---

## 🎓 Cadastro de Estudantes

**Colunas:**
- Carimbo de data/hora
- Número de matrícula
- Nome completo
- E-mail
- Telefone (xx) xxx-xxx-xxx
- Coordenador responsável (nome)
- Núcleo

---

## 🧑‍🏫 Cadastro de Coordenadores

**Colunas:**
- Carimbo de data/hora
- Nome completo
- E-mail
- Telefone (xx) xxx-xxx-xxx
- Núcleo
