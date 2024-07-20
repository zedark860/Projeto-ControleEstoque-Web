# Projeto-ControleEstoque-Web

Projeto de controle de estoque para a WebCertificados.

## Descrição

Este projeto é uma aplicação web desenvolvida para gerenciar o controle de estoque de produtos. Ele permite cadastrar, atualizar, visualizar e deletar itens do estoque, fornecendo uma interface amigável para os usuários.

## Tecnologias Utilizadas

- **Linguagem:** Python
- **Frameworks e Bibliotecas Principais:**
  - `cachetools==5.3.3`
  - `certifi==2024.7.4`
  - `charset-normalizer==3.3.2`
  - `google-api-core==2.19.1`
  - `google-api-python-client==2.137.0`
  - `google-auth==2.32.0`
  - `google-auth-httplib2==0.2.0`
  - `google-auth-oauthlib==1.2.1`
  - `googleapis-common-protos==1.63.2`
  - `httplib2==0.22.0`
  - `idna==3.7`
  - `oauthlib==3.2.2`
  - `pillow==10.4.0`
  - `proto-plus==1.24.0`
  - `protobuf==5.27.2`
  - `pyasn1==0.6.0`
  - `pyasn1_modules==0.4.0`
  - `pygsheets==2.0.6`
  - `pyparsing==3.1.2`
  - `requests==2.32.3`
  - `requests-oauthlib==2.0.0`
  - `rsa==4.9`
  - `ttkbootstrap==1.10.1`
  - `uritemplate==4.1.1`
  - `urllib3==2.2.2`

## Instalação

Para executar o projeto localmente, siga os passos abaixo:

1. Clone o repositório:
    ```bash
    git clone https://github.com/zedark860/Projeto-ControleEstoque-Web.git
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd Projeto-ControleEstoque-Web
    ```

3. Crie um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate   # Para Linux/Mac
    venv\Scripts\activate      # Para Windows
    ```

4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

5. Execute a aplicação:
    ```bash
    python app.py
    ```

## Funcionalidades

- **Cadastro de Produtos:** Adicione novos produtos ao estoque.
- **Atualização de Produtos:** Atualize informações de produtos existentes.
- **Visualização de Produtos:** Veja a lista completa de produtos no estoque.
- **Remoção de Produtos:** Delete produtos que não são mais necessários.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
