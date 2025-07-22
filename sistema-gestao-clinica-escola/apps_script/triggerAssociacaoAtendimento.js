/**
 * Trigger executado ao enviar o formulário de associação de atendimento.
 * Realiza inserção na tabela Atendimento, vinculando paciente e estudante.
 */
function onFormSubmitAssociacaoAtendimento(e) {
  var dados = e.values;

  // Mapeamento dos campos da planilha
  var nomePaciente = dados[1];
  var nomeEstudante = dados[2];
  var dataInicio = dados[3];
  var dataFim = dados[4]; // pode estar vazio

  try {
    var conexao = obterConexao();
    registrarLog('INFO', `Conexão estabelecida para associação: ${nomePaciente} ↔ ${nomeEstudante}`);

    // Buscar IDs relacionados
    var idPaciente = buscarIdPacientePorNome(conexao, nomePaciente);
    var idEstudante = buscarIdEstudantePorNome(conexao, nomeEstudante);

    // Validação da existência dos IDs
    if (!idPaciente || !idEstudante) {
      registrarLog('WARNING', `IDs não encontrados para associação: Paciente=${nomePaciente}, Estudante=${nomeEstudante}`);
      conexao.close();
      return;
    }

    // Inserir atendimento
    var stmt = conexao.prepareStatement(
      'INSERT INTO Atendimento (idPaciente, idEstudante, dataInicio, dataFim) VALUES (?, ?, ?, ?)'
    );
    stmt.setInt(1, idPaciente);
    stmt.setInt(2, idEstudante);
    stmt.setDate(3, Jdbc.newDate(new Date(dataInicio)));

    if (dataFim && dataFim.trim() !== '') {
      stmt.setDate(4, Jdbc.newDate(new Date(dataFim)));
    } else {
      stmt.setNull(4, Jdbc.Types.DATE);
    }

    stmt.execute();
    stmt.close();
    registrarLog('INFO', `Associação inserida com sucesso: ${nomePaciente} ↔ ${nomeEstudante}`);

    // Fechar a conexão com o BD
    conexao.close();
  } catch (erro) {
    registrarLog('ERROR', `Erro ao associar atendimento: ${nomePaciente} ↔ ${nomeEstudante}: ${erro}`);
  }
}
