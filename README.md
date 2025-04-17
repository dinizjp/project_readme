# Project Readme

Este projeto, chamado **project_readme**, é uma ferramenta para gerar documentação em formato Markdown para projetos. Ele utiliza uma abordagem automatizada para analisar códigos e gerar um README.md detalhado.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)

## Sumário

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Exemplos de Uso](#exemplos-de-uso)
- [Estrutura de Pastas](#estrutura-de-pastas)

## Requisitos

- Python 3.12 ou superior
- Bibliotecas: `httpx`, `typing_extensions`, `pytest`

## Instalação

Para instalar este projeto, basta clonar o repositório e instalar as dependências necessárias com o comando:

```bash
git clone https://github.com/username/project_readme.git
cd project_readme
pip install -r requirements.txt
```

## Exemplos de Uso

Para gerar o README.md do seu projeto, execute o seguinte comando no terminal:

```bash
python agent.py --single /caminho/para/seu/projeto
```

Isso irá gerar um arquivo README.md na raiz do seu projeto com base na análise dos arquivos do projeto.

## Estrutura de Pastas

A estrutura de pastas do projeto é a seguinte:

```
project_readme/
├── agent.py
├── tools.py
├── venv/
│   ├── lib/
│   │   └── python3.12/site-packages/
│   │       ├── typing_extensions.py
│   │       ├── httpx/
│   │       └── ...
├── README.md (gerado automaticamente)
└── requirements.txt
```

Os arquivos principais do projeto são:

- `agent.py`: O script principal que realiza a geração do README.md.
- `tools.py`: Contém funções auxiliares utilizadas pelo agente.
- `venv/`: Virtual environment contendo as dependências do projeto.

---

Este projeto fornece uma maneira eficiente de gerar documentação para projetos Python, ajudando desenvolvedores a manter suas documentações sempre atualizadas.

