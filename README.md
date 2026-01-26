# py-drive
Um Projeto em Python para gerenciar e instalar/enviar pastas e arquivos para o Google Drive

## 🏗 Estrutura e Arquitetura do Projeto

O projeto segue o padrão `src-layout` para garantir isolamento do código fonte e facilitar o empacotamento. A lógica é dividida em módulos desacoplados para facilitar a manutenção e testes.

### 📂 Raiz do Projeto
* **`.env`**: Arquivo de configuração local (não versionado). Armazena variáveis de ambiente sensíveis, como o ID da pasta raiz do Google Drive e caminhos locais absolutos.
* **`credentials.json`**: Credenciais de cliente OAuth 2.0 baixadas do Google Cloud Console. Define a identidade da aplicação (Client ID/Secret).
* **`token.json`**: Armazena o token de acesso e refresh token da sessão do usuário. Gerado automaticamente após o primeiro login bem-sucedido.
* **`requirements.txt`**: Lista de dependências do projeto (ex: `google-api-python-client`, `google-auth-oauthlib`, `python-dotenv`).

### 🐍 Módulo `src/` (Código Fonte)

#### `src/main.py` (Entry Point)
Ponto de entrada da aplicação. Responsável por:
* Inicializar o logger.
* Carregar configurações.
* Orquestrar a lógica de sincronização, chamando os métodos dos módulos `core` para comparar o estado local vs. remoto e decidir quais ações (upload/download) executar.

#### `src/config.py`
Gerenciador de configurações centralizado.
* Carrega as variáveis do arquivo `.env`.
* Valida se as variáveis obrigatórias (ex: `GDRIVE_ROOT_ID`) estão presentes antes da execução iniciar, falhando graciosamente caso contrário.

### ⚙️ Módulo `src/core/` (Lógica de Negócio)

#### `src/core/auth.py`
Gerencia o ciclo de vida da autenticação OAuth 2.0.
* Implementa o fluxo de "Authorisation Code".
* Verifica a validade do token atual.
* Realiza o refresh automático do token expirado sem intervenção do usuário, garantindo execução contínua em background (ex: cron jobs).

#### `src/core/drive.py` (API Wrapper)
Camada de abstração (Facade) para a API do Google Drive v3.
* Isola a complexidade da biblioteca `google-api-python-client`.
* Contém métodos de alto nível como `list_files()`, `upload_file()`, `download_file()`.
* Implementa **Exponential Backoff** para lidar com *Rate Limits* e erros de rede (códigos 429/500).

#### `src/core/local.py`
Manipulador do Sistema de Arquivos Local (OS).
* Responsável por varrer diretórios recursivamente.
* **Integridade de Dados:** Calcula checksums (MD5) dos arquivos locais para comparação eficiente com os metadados do Google Drive, evitando uploads desnecessários de arquivos inalterados.

### 🛠 Módulo `src/utils/`

#### `src/utils/logger.py`
Configuração centralizada de logs.
* Define formatos de saída e níveis de log (DEBUG, INFO, ERROR).
* Garante que logs de erro sejam persistidos em arquivo (`sync.log`) para auditoria futura, enquanto logs informativos podem ser exibidos no stdout.


## Referências
- Documentação PyDoc da API do Google Drive: https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html
- Como criar um programa de lista de tarefas de linha de comando com Python: https://realpython.com/python-typer-cli/