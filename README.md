# Normaliza Iniciativas

Repositório com os códigos [Python](www.python.org) para a normalização dos dados das Iniciativas Periféricas.

## Instalação

> Esse projeto utiliza  poetry para gerenciamento de dependências.

> Inicie o ambiente virtual antes de instalar as dependências, se necessário

Para instalar as dependências, execute o comando abaixo:

```bash
poetry install
```

Instalando as dependencias de desenvolvimento:

```bash
poetry install --dev
```

## Configuração

Para configurar o projeto, crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Token de acesso ao KoboToolbox
KOBO_API_KEY=chave
KOBO_USERNAME=usuario
KOBO_PASSWORD=senha
KOBO_FORM_ID=id do formulário
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Ou pode copiar o arquivo `.env.example` e renomear para `.env` e preencher as variáveis.

```bash
cp .env.example .env
```

Lembre-se sempre de reiniciar o jupyter notebook após alterar o arquivo `.env`.
