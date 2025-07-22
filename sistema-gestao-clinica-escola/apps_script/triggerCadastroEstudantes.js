/**
 * Trigger executado ao enviar o formulário de cadastro de estudantes.
 * Realiza inserção na tabela Estudante, vinculando ao coordenador e núcleo correspondentes.
 */
function onFormSubmitCadastroEstudantes(e) {
  var dados = e.values;

  // Mapeamento dos campos da planilha
  var matricula = dados[1];
  var nome = dados[2];
  var email = dados[3];
  var telefone = dados[4];
  var nomeCoordenador = dados[5];
  var nomeNucleo = dados[6];

  try {
    var conexao = obterConexao();
    registrarLog('INFO', `Conexão estabelecida para cadastro de estudante: ${nome}`);

    // Validar matrícula como número
    var idEstudante = parseInt(matricula);
    if (isNaN(idEstudante)) {
      registrarLog('ERROR', `Matrícula inválida para estudante ${nome}: ${matricula}`);
      conexao.close();
      return;
    }

    // Buscar IDs relacionados
    var idCoordenador = buscarIdCoordenadorPorNome(conexao, nomeCoordenador);
    var idNucleo = buscarIdNucleoPorNome(conexao, nomeNucleo);

    // Validação da existência dos IDs
    if (!idCoordenador || !idNucleo) {
      registrarLog('WARNING', `IDs não encontrados para estudante ${nome}: Coordenador=${nomeCoordenador}, Núcleo=${nomeNucleo}`);
      conexao.close();
      return;
    }

    // Inserir estudante
    var stmt = conexao.prepareStatement(
      'INSERT INTO Estudante (idEstudante, nome, email, telefone, idCoordenador, idNucleo) VALUES (?, ?, ?, ?, ?, ?)'
    );
    stmt.setInt(1, idEstudante);
    stmt.setString(2, nome);
    stmt.setString(3, email);
    stmt.setString(4, telefone);
    stmt.setInt(5, idCoordenador);
    stmt.setInt(6, idNucleo);
    stmt.execute();
    stmt.close();
    registrarLog('INFO', `Estudante inserido com sucesso: ${nome} (Matrícula: ${idEstudante})`);

    // Fecha a conexão com o BD
    conexao.close();
  } catch (erro) {
    registrarLog('ERROR', `Erro ao cadastrar estudante ${nome} (Matrícula: ${matricula}): ${erro}`);
  }
}
