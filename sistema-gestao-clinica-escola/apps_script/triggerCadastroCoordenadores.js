/**
 * Trigger executado ao enviar o formulário de cadastro de coordenadores.
 * Realiza inserção na tabela Coordenador, vinculando ao núcleo correspondente.
 */
function onFormSubmitCadastroCoordenadores(e) {
  var dados = e.values;

  // Mapeamento dos campos da planilha
  var nome = dados[1];
  var email = dados[2];
  var telefone = dados[3];
  var nomeNucleo = dados[4];

  try {
    var conexao = obterConexao();
    registrarLog('INFO', `Conexão estabelecida para cadastro de coordenador: ${nome}`);

    // Buscar ID do núcleo
    var idNucleo = buscarIdNucleoPorNome(conexao, nomeNucleo);

    // Validação da existência do núcleo
    if (!idNucleo) {
      registrarLog('WARNING', `Núcleo não encontrado para coordenador ${nome}: ${nomeNucleo}`);
      conexao.close();
      return;
    }

    // Inserir coordenador
    var stmt = conexao.prepareStatement(
      'INSERT INTO Coordenador (nome, email, telefone, idNucleo) VALUES (?, ?, ?, ?)'
    );
    stmt.setString(1, nome);
    stmt.setString(2, email);
    stmt.setString(3, telefone);
    stmt.setInt(4, idNucleo);
    stmt.execute();
    stmt.close();
    registrarLog('INFO', `Coordenador inserido com sucesso: ${nome}`);
    
    //Fecha conexão com o BD
    conexao.close();
  } catch (erro) {
    registrarLog('ERROR', `Erro ao cadastrar coordenador ${nome}: ${erro}`);
  }
}
