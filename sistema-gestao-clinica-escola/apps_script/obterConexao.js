/**
 * Registra logs em um arquivo de texto único por execução, armazenado em uma pasta específica.
 * O nome do arquivo é baseado na data e hora da execução.
 * 
 * @param {string} nivel - Nível do log: 'INFO', 'WARNING', 'ERROR'.
 * @param {string} mensagem - Mensagem a ser registrada.
 */
function registrarLog(nivel, mensagem) {
  var timestamp = new Date();
  var dataFormatada = Utilities.formatDate(timestamp, Session.getScriptTimeZone(), 'yyyy-MM-dd_HH-mm-ss');
  var nomeArquivo = `log_${dataFormatada}.txt`;

  var logFormatado = `[${timestamp.toISOString()}] [${nivel}] ${mensagem}\n`;

  // ID da pasta onde os logs serão armazenados (crie a pasta manualmente e pegue o ID)
  var idPastaLogs = 'ID_DA_PASTA';
  var pastaLogs = DriveApp.getFolderById(idPastaLogs);

  // Verifica se o arquivo já foi criado nesta execução
  var arquivos = pastaLogs.getFilesByName(nomeArquivo);
  var arquivo;

  if (arquivos.hasNext()) {
    arquivo = arquivos.next();
    var conteudoAtual = arquivo.getBlob().getDataAsString();
    arquivo.setContent(conteudoAtual + logFormatado);
  } else {
    // Cria novo arquivo com o primeiro log
    arquivo = pastaLogs.createFile(nomeArquivo, logFormatado, MimeType.PLAIN_TEXT);
  }

  // Também exibe no console do Apps Script
  Logger.log(logFormatado);
}
