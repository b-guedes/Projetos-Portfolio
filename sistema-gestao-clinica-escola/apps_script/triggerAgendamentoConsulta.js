/**
 * Trigger executado ao enviar o formulário de agendamento de consultas.
 * Realiza inserções no banco de dados conforme os dados recebidos.
 */
function onFormSubmitAgendamentoConsultas(e) {
  var dados = e.values;

  // Mapeamento dos campos da planilha
  var nomePaciente = dados[1];
  var nomeEstudante = dados[2];
  var dataConsulta = dados[3];
  var horarioConsulta = dados[4];
  var statusConsulta = dados[5];
  var compareceu = dados[6].toLowerCase() === 'sim';
  var justificativa = dados[7];
  var documentoAnexo = dados[8];
  var resumo = dados[9];
  var observacoes = dados[10];
  var encaminhamentos = dados[11];
  var caminhoArquivo = dados[12];

  try {
    var conexao = obterConexao();
    registrarLog('INFO', `Conexão estabelecida para agendamento de consulta: ${nomePaciente} com ${nomeEstudante}`);

    // Buscar IDs relacionados
    var idPaciente = buscarIdPacientePorNome(conexao, nomePaciente);
    var idEstudante = buscarIdEstudantePorNome(conexao, nomeEstudante);

    // Validação da existência dos IDs
    if (!idPaciente || !idEstudante) {
      registrarLog('WARNING', `IDs não encontrados para consulta: Paciente=${nomePaciente}, Estudante=${nomeEstudante}`);
      conexao.close();
      return;
    }

    // Combinar data e hora da consulta
    var dataHoraConsulta = new Date(dataConsulta + ' ' + horarioConsulta);
    if (isNaN(dataHoraConsulta)) {
      registrarLog('ERROR', `Data/hora inválida: ${dataConsulta} ${horarioConsulta}`);
      conexao.close();
      return;
    }

    // Inserir consulta
    var stmtConsulta = conexao.prepareStatement(
      'INSERT INTO Consulta (idPaciente, idEstudante, dataConsulta, status, compareceu) VALUES (?, ?, ?, ?, ?)',
      Jdbc.Statement.RETURN_GENERATED_KEYS
    );
    stmtConsulta.setInt(1, idPaciente);
    stmtConsulta.setInt(2, idEstudante);
    stmtConsulta.setTimestamp(3, Jdbc.newTimestamp(dataHoraConsulta));
    stmtConsulta.setString(4, statusConsulta);
    stmtConsulta.setBoolean(5, compareceu);
    stmtConsulta.execute();

    // Captura ID da consulta gerada
    var rsConsulta = stmtConsulta.getGeneratedKeys();
    var idConsulta = null;
    if (rsConsulta.next()) {
      idConsulta = rsConsulta.getInt(1);
    } else {
      registrarLog('ERROR', `Falha ao obter ID da consulta inserida`);
    }
    rsConsulta.close();
    stmtConsulta.close();
    registrarLog('INFO', `Consulta registrada com sucesso: ${nomePaciente} com ${nomeEstudante}`);

    // Se não compareceu, registrar falta
    if (!compareceu) {
      var stmtFalta = conexao.prepareStatement(
        'INSERT INTO Falta (idConsulta, dataFalta, justificativa, documentoAnexo) VALUES (?, ?, ?, ?)'
      );
      stmtFalta.setInt(1, idConsulta);
      stmtFalta.setDate(2, Jdbc.newDate(new Date(dataConsulta)));
      stmtFalta.setString(3, justificativa);
      stmtFalta.setString(4, documentoAnexo);
      stmtFalta.execute();
      stmtFalta.close();
      registrarLog('INFO', `Falta registrada: ${nomePaciente} em ${dataConsulta}`);
    }

    // Se compareceu, registrar prontuário
    if (compareceu) {
      var stmtProntuario = conexao.prepareStatement(
        'INSERT INTO Prontuario (idConsulta, resumo, observacoes, encaminhamentos, caminhoArquivo) VALUES (?, ?, ?, ?, ?)'
      );
      stmtProntuario.setInt(1, idConsulta);
      stmtProntuario.setString(2, resumo);
      stmtProntuario.setString(3, observacoes);
      stmtProntuario.setString(4, encaminhamentos);
      stmtProntuario.setString(5, caminhoArquivo);
      stmtProntuario.execute();
      stmtProntuario.close();
      registrarLog('INFO', `Prontuário registrado: ${nomePaciente} em ${dataConsulta}`);
    }

    // Fechar conexão com o BD
    conexao.close();
  } catch (erro) {
    // Capturar erro
    registrarLog('ERROR', `Erro ao registrar consulta: ${nomePaciente} com ${nomeEstudante}: ${erro}`);
  }
}

