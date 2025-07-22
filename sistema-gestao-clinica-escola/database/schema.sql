CREATE DATABASE clinicaEscola_psicologia;
USE clinicaEscola_psicologia;

-- Tabela de Endereços
CREATE TABLE Endereco (
    idEndereco INT AUTO_INCREMENT PRIMARY KEY,
    rua VARCHAR(100),
    numero VARCHAR(10),
    bairro VARCHAR(50),
    cidade VARCHAR(50),
    estado VARCHAR(2),
    cep VARCHAR(10)
);

-- Tabela de Pacientes
CREATE TABLE Paciente (
    idPaciente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    dataNascimento DATE,
    sexo ENUM('Masculino', 'Feminino', 'Outro'),
    telefone VARCHAR(15),
    email VARCHAR(100),
    idEndereco INT,
    FOREIGN KEY (idEndereco) REFERENCES Endereco(idEndereco)
);

-- Tabela de Coordenadores
CREATE TABLE Coordenador (
    idCoordenador INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(15),
    idNucleo INT,
    FOREIGN KEY (idNucleo) REFERENCES nucleo(idNucleo)
);

-- Tabela de estudantes
CREATE TABLE Estudante (
    idEstudante INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(15),
    idCoordenador INT,
    idNucleo INT,
    FOREIGN KEY (idCoordenador) REFERENCES coordenador(idCoordenador),
    FOREIGN KEY (idNucleo) REFERENCES nucleo(idNucleo)
);

-- Associação N:N entre Paciente e Estudante
CREATE TABLE Atendimento (
    idPaciente INT,
    idEstudante INT,
    dataInicio DATE,
    dataFim DATE,
    PRIMARY KEY (idPaciente, idEstudante),
    FOREIGN KEY (idPaciente) REFERENCES Paciente(idPaciente),
    FOREIGN KEY (idEstudante) REFERENCES Estudante(idEstudante)
);

-- Tabela de Consultas
CREATE TABLE Consulta (
    idConsulta INT AUTO_INCREMENT PRIMARY KEY,
    idPaciente INT,
    idEstudante INT,
    dataConsulta DATETIME,
    status ENUM('Agendada', 'Realizada', 'Cancelada'),
    compareceu BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (idPaciente) REFERENCES Paciente(idPaciente),
    FOREIGN KEY (idEstudante) REFERENCES Estudante(idEstudante)
);

-- Tabela de Prontuários
CREATE TABLE Prontuario (
    idProntuario INT AUTO_INCREMENT PRIMARY KEY,
    idConsulta INT,
    resumo TEXT,
    observacoes TEXT,
    encaminhamentos TEXT,
    caminhoArquivo TEXT,
    FOREIGN KEY (idConsulta) REFERENCES Consulta(idConsulta)
);

-- Tabela de Faltas
CREATE TABLE Falta (
    idFalta INT AUTO_INCREMENT PRIMARY KEY,
    idConsulta INT,
    dataFalta DATE,
    justificativa TEXT,
    documentoAnexo VARCHAR(255), -- opcional, se quiser armazenar caminho de arquivo
    FOREIGN KEY (idConsulta) REFERENCES Consulta(idConsulta)
);

-- Tabela com os Núcleos da Clínica-Escola
CREATE TABLE Nucleo (
    idNucleo INT AUTO_INCREMENT PRIMARY KEY,
    nomeEspecialidade VARCHAR(100)
);
