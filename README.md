# project_readme

## Descrição
Este projeto automatiza a geração de documentação README.md para projetos Python. Utiliza inteligência artificial (GPT-4) para criar um README claro, conciso e completo, a partir de arquivos do projeto. O processo envolve leitura de arquivos relevantes, filtragem de pastas e arquivos, e consulta ao GPT para elaborar a documentação seguindo uma estrutura padronizada, que inclui título, descrição, sumário, dependências, instalação, uso e estrutura de pastas.

## Sumário
- [Dependências](#dependências)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura de Pastas](#estrutura-de-pastas)

## Dependências
- openai
- python-dotenv

## Instalação
```bash
pip install -r requirements.txt
```

## Uso
Para gerar README.md para um ou mais projetos, utilize o script `agent.py`. Exemplos:

Para tratar cada caminho como um projeto único:
```bash
python agent.py --single caminho/do/projeto
```

Para analisar múltiplos projetos dentro de uma pasta:
```bash
python agent.py caminho/para/pasta
```

Se desejar processar diferentes pastas:
```bash
python agent.py pasta1 pasta2
```

O script irá detectar automaticamente os projetos dentro dos caminhos fornecidos, solicitando ao GPT a elaboração dos READMEs.

## Estrutura de Pastas
```
project_readme/
│
├── agent.py
├── requirements.txt
└── tools.py
```