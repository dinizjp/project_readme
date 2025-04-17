# project_readme

## Descrição
O projeto automatiza a geração de arquivos README.md para projetos Python, utilizando inteligência artificial. Ele identifica as pastas de projetos em um diretório raiz, lê os arquivos relevantes, e cria uma documentação estruturada com seções específicas. A geração do README é feita por um agente que utiliza o OpenAI GPT-4, baseado nas informações extraídas dos arquivos do projeto.

## Sumário
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura de Pastas](#estrutura-de-pastas)

## Instalação
Após clonar ou obter os arquivos do projeto, execute:

```sh
pip install -r requirements.txt
```

Certifique-se de que a variável de ambiente `OPENAI_API_KEY` está configurada com sua chave da API do OpenAI.

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

O script irá identificar automaticamente repositórios Git ou pastas com arquivos de configuração Python, lendo os arquivos relevantes e gerando o README em cada projeto.

## Estrutura de Pastas
```
project_readme/
├── agent.py
├── tools.py
└── requirements.txt
```