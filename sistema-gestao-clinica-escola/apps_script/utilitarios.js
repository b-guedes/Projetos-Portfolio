/**
 * Executa uma consulta SQL para buscar um ID com base no nome e na tabela/coluna fornecidos.
 * Essa é uma função genérica para utilizar em outras consultas.
 * 
 * @param {Object} conexao - Conexão com o banco de dados.
 * @param {string} tabela - Nome da tabela a ser consultada.
 * @param {string} colunaNome - Nome da coluna que contém o nome.
 * @param {string} colunaId - Nome da coluna que contém o ID.
 * @param {string} nome - Nome exato a ser buscado.
 * @returns {number|null} - ID encontrado ou null se não houver correspondência.
 */
function buscarIdPorNome(conexao, tabela, colunaNome, colunaId, nome) {
  var id = null;
  var query = `SELECT ${colunaId} FROM ${tabela} WHERE ${colunaNome} = ?`;
  var stmt = null;
  var rs = null;

  try {
    Logger.log(`Executando consulta: ${query} com nome = ${nome}`);
    stmt = conexao.prepareStatement(query);
    stmt.setString(1, nome);
    rs = stmt.executeQuery();

    if (rs.next()) {
      id = rs.getInt(colunaId);
      Logger.log(`ID encontrado: ${id}`);
    } else {
      Logger.log(`Nenhum resultado encontrado para nome: ${nome}`);
    }
  } catch (e) {
    Logger.log(`Erro ao buscar ID na tabela ${tabela}: ${e.message}`);
  } finally {
    // Garantir que recursos sejam liberados mesmo em caso de erro
    try {
      if (rs) rs.close();
      if (stmt) stmt.close();
    } catch (fe) {
      Logger.log(`Erro ao fechar recursos: ${fe.message}`);
    }
  }

  return id;
}


//Busca o ID de um paciente pelo nome exato.
function buscarIdPacientePorNome(conexao, nomePaciente) {
  return buscarIdPorNome(conexao, 'Paciente', 'nome', 'idPaciente', nomePaciente);
}


//Busca o ID de um estudante pelo nome exato.
function buscarIdEstudantePorNome(conexao, nomeEstudante) {
  return buscarIdPorNome(conexao, 'Estudante', 'nome', 'idEstudante', nomeEstudante);
}


// Busca o ID de um coordenador pelo nome exato.
function buscarIdCoordenadorPorNome(conexao, nomeCoordenador) {
  return buscarIdPorNome(conexao, 'Coordenador', 'nome', 'idCoordenador', nomeCoordenador);
}


//Busca o ID de um núcleo pelo nome da especialidade.
function buscarIdNucleoPorNome(conexao, nomeNucleo) {
  return buscarIdPorNome(conexao, 'Nucleo', 'nomeEspecialidade', 'idNucleo', nomeNucleo);
}
