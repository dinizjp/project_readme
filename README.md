# project_readme

## Descrição
Este projeto automatiza a geração de arquivos README.md para projetos Python. Ele identifica as pastas de projetos em um diretório principal, lê os arquivos relevantes de cada projeto e utiliza inteligência artificial (ChatGPT) para criar uma documentação estruturada. A geração do README inclui seções como título, descrição, sumário, dependências, instalação, uso e estrutura de pastas, tudo com base nas informações extraídas dos arquivos do projeto.

## Sumário
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura de Pastas](#estrutura-de-pastas)

## Instalação
Após obter os arquivos do projeto, execute:

```sh
pip install -r requirements.txt
```

Certifique-se de configurar a variável de ambiente `OPENAI_API_KEY` com sua chave da API do OpenAI.

## Uso
Para gerar README.md para projetos específicos ou detectar múltiplos projetos em um diretório, utilize o script `agent.py`.

- Para tratar um caminho como projeto individual:

```sh
python agent.py --single caminho/do/projeto
```

- Para detectar projetos em um diretório e gerar README para cada um:

```sh
python agent.py caminho/do/diretorio
```

- Para detectar múltiplos projetos em vários caminhos e gerar seus READMEs:

```sh
python agent.py caminho1 caminho2 --single
```

O script identifica automaticamente repositórios Git ou pastas com arquivos de configuração Python, lê os arquivos relevantes e gera o README em cada projeto.

## Estrutura de Pastas
```
project_readme/
├── agent.py
├── tools.py
└── requirements.txt
```