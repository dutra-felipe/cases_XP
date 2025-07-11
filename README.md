# Cases Práticos - Plataforma de Gestão

Uma plataforma web completa para gerenciar e exibir estudos de caso práticos. A aplicação conta com um painel público para visualização e uma área administrativa segura para gerenciamento de conteúdo (CRUD).

## ✨ Funcionalidades

* **Painel Público:** Exibição dos cases para os clientes com paginação e busca em tempo real.
* **Detalhes do Case:** Página dedicada para cada case, exibindo todas as informações formatadas.
* **Painel Administrativo:** Interface segura para criar, editar e excluir cases.
* **Autenticação Segura:** Sistema de login para o administrador com senha hasheada no banco de dados.
* **API RESTful:** Back-end robusto que serve os dados para o front-end de forma eficiente.
* **Design Responsivo:** Interface moderna e adaptável a diferentes tamanhos de tela.

## 🚀 Tecnologias Utilizadas

* **Backend:**
    * Python 3
    * Flask
    * SQLAlchemy
    * Flask-Login (Autenticação)
    * Gunicorn (Servidor de Produção)
* **Frontend:**
    * HTML5 / CSS3
    * Bootstrap 5
    * JavaScript
* **Banco de Dados:**
    * PostgreSQL
* **Ambiente e Deploy:**
    * Docker & Docker Compose
    * Projetado para deploy em plataformas PaaS (ex: Render, Railway)

## ⚙️ Como Executar Localmente

Siga os passos abaixo para rodar a aplicação no seu ambiente de desenvolvimento.

### Pré-requisitos

* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```

2.  **Crie o arquivo de ambiente:**
    Navegue até a pasta `backend` e crie um arquivo chamado `.env`. Você pode copiar o exemplo abaixo.
    ```bash
    cd backend
    touch .env
    ```

3.  **Configure as variáveis de ambiente:**
    Abra o arquivo `backend/.env` e preencha com suas credenciais. Este arquivo é ignorado pelo Git para sua segurança.

    ```ini
    # Chave secreta para segurança do Flask
    SECRET_KEY='UMA_CHAVE_SECRETA_MUITO_FORTE_E_ALEATORIA'

    # Credenciais para o PRIMEIRO login do admin. Após o primeiro login,
    # as credenciais serão gerenciadas pelo banco de dados.
    ADMIN_USERNAME='admin'
    ADMIN_PASSWORD='senha_forte_para_o_admin'

    # Credenciais do Banco de Dados PostgreSQL (usado pelo Docker Compose)
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=cases_db
    DB_HOST=db
    DB_PORT=5432
    ```

4.  **Suba os containers com Docker Compose:**
    Volte para a pasta raiz do projeto e execute o comando:
    ```bash
    docker-compose up --build
    ```
    O comando `--build` garante que a imagem Docker será construída na primeira vez.

5.  **Acesse a aplicação:**
    Abra seu navegador e acesse `http://localhost:5000`. A aplicação estará funcionando.

## 🚢 Deploy

A aplicação foi projetada para ser implantada facilmente em qualquer plataforma PaaS que suporte Docker, como Render ou Railway. O deploy requer a configuração das mesmas variáveis de ambiente listadas acima no painel da plataforma de hospedagem e o uso de um `Procfile` para iniciar o servidor Gunicorn.

## <caption> API Endpoints

A aplicação expõe os seguintes endpoints de API:

| Método | Endpoint | Descrição | Requer Autenticação? |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/cases` | Retorna todos os cases em ordem alfabética.| Não |
| `GET` | `/api/cases/<id>` | Retorna os detalhes de um case específico. | Não |
| `POST` | `/api/cases` | Cria um novo case. | **Sim** |
| `PUT` | `/api/cases/<id>` | Atualiza um case existente. | **Sim** |
| `DELETE`| `/api/cases/<id>` | Deleta um case. | **Sim** |
| `POST` | `/api/login` | Autentica o usuário administrador. | Não |
| `POST` | `/api/logout` | Desconecta o usuário logado. | **Sim** |
| `GET` | `/api/check-auth` | Verifica se a sessão atual está autenticada. | Não |