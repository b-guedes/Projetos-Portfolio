/**
 * Trigger executado ao enviar o formulário de cadastro de pacientes.
 * Realiza inserções nas tabelas Endereco e Paciente, vinculando os dados corretamente.
 */
function onFormSubmitCadastroPacientes(e) {
  var dados = e.values;

  // Mapeamento dos campos da planilha
  var idPacienteStr = dados[1]; // matrícula como ID
  var nome = dados[2];
  var dataNascimento = dados[3];
  var sexo = dados[4];
  var telefone = dados[5];
  var email = dados[6];
  var rua = dados[7];
  var numero = dados[8];
  var bairro = dados[9];
  var cidade = dados[10];
  var estado = dados[11];
  var cep = dados[12];

  try {
    var conexao = obterConexao();
    registrarLog('INFO', `Conexão estabelecida para cadastro de paciente: ${nome}`);

    // Validar ID do paciente
    var idPaciente = parseInt(idPacienteStr);
    if (isNaN(idPaciente)) {
      registrarLog('ERROR', `ID inválido para paciente ${nome}: ${idPacienteStr}`);
      conexao.close();
      return;
    }

    // Inserir endereço
    var stmtEndereco = conexao.prepareStatement(
      'INSERT INTO Endereco (rua, numero, bairro, cidade, estado, cep) VALUES (?, ?, ?, ?, ?, ?)',
      Jdbc.Statement.RETURN_GENERATED_KEYS
    );
    stmtEndereco.setString(1, rua);
    stmtEndereco.setString(2, numero);
    stmtEndereco.setString(3, bairro);
    stmtEndereco.setString(4, cidade);
    stmtEndereco.setString(5, estado);
    stmtEndereco.setString(6, cep);
    stmtEndereco.execute();

    var rsEndereco = stmtEndereco.getGeneratedKeys();
    var idEndereco = null;
    if (rsEndereco.next()) {
      idEndereco = rsEndereco.getInt(1);
    } else {
      registrarLog('ERROR', `Falha ao obter ID do endereço inserido para paciente ${nome}`);
      stmtEndereco.close();
      conexao.close();
      return;
    }
    rsEndereco.close();
    stmtEndereco.close();
    registrarLog('INFO', `Endereço inserido com sucesso para paciente: ${nome}`);

    // Inserir paciente 
    var stmtPaciente = conexao.prepareStatement(
      'INSERT INTO Paciente (idPaciente, nome, dataNascimento, sexo, telefone, email, idEndereco) VALUES (?, ?, ?, ?, ?, ?, ?)'
    );
    stmtPaciente.setInt(1, idPaciente);
    stmtPaciente.setString(2, nome);
    stmtPaciente.setDate(3, dataNascimento);
    stmtPaciente.setString(4, sexo);
    stmtPaciente.setString(5, telefone);
    stmtPaciente.setString(6, email);
    stmtPaciente.setInt(7, idEndereco);
    stmtPaciente.execute();
    stmtPaciente.close();

    registrarLog('INFO', `Paciente inserido com sucesso: ${nome} (ID: ${idPaciente})`);
    conexao.close();
  } catch (erro) {
    registrarLog('ERROR', `Erro ao cadastrar paciente ${nome} (ID: ${idPacienteStr}): ${erro}`);
  }
}
