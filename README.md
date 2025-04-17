# project_readme

## Descrição

Este projeto consiste em um agente que automatiza a geração de arquivos README.md para projetos de software. Ele analisa o conteúdo dos arquivos do projeto e utiliza o modelo GPT-4 para criar uma documentação clara, concisa e completa, de acordo com as diretrizes fornecidas.

## Sumário

- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Contato](#contato)

## Instalação

Execute os seguintes comandos para instalar as dependências necessárias:

```bash
pip install -r requirements.txt
```

ou

```bash
python setup.py install
```

## Uso

Para gerar README.md de um projeto específico:

```bash
python agent.py --single /caminho/para/o/projeto
```

Para escanear um diretório e gerar README.md para cada projeto detectado automaticamente:

```bash
python agent.py /caminho/para/diretorio
```

Se desejar tratar vários caminhos como projetos únicos:

```bash
python agent.py --single /caminho/1 /caminho/2
```

Certifique-se de que a variável de ambiente `OPENAI_API_KEY` esteja configurada com sua chave da API da OpenAI.

## Estrutura de Pastas

- agent.py
- tools.py

## Contato

Problemas ou dúvidas? Reporte-os abrindo uma issue neste repositório ou entrando em contato pelo canal de suporte disponível.