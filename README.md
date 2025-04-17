# project_readme

Este projeto, **project_readme**, é uma ferramenta poderosa para gerar automaticamente documentação em formato Markdown (README.md) para seus projetos Python. Ele analisa a estrutura do projeto e gera um README completo e formatado, seguindo as melhores práticas.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-yellow)

## Sumário

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Exemplos de Uso](#exemplos-de-uso)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Contribuindo](#contribuindo)

## Requisitos

- Python 3.12 ou superior.
- Dependências: `httpx`, `typing_extensions`, e outras que podem ser instaladas via `pip`.

## Instalação

Para instalar o **project_readme**, siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone https://github.com/username/project_readme.git
   cd project_readme
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Exemplos de Uso

Para gerar um README.md para seu projeto, execute o seguinte comando no terminal:

```bash
python agent.py --single /caminho/para/seu/projeto
```

Você pode personalizar as opções de geração de README utilizando os parâmetros adicionais disponíveis:

- `--project_name`: Para especificar um nome para o projeto.
- `--author`: Para adicionar o nome do autor no README.
- `--output`: Para especificar o arquivo de saída do README.md.

## Estrutura de Pastas

A estrutura de pastas do projeto é a seguinte:

```
project_readme/
├── agent.py               # Script principal para gerar README.md
├── tools.py               # Funções auxiliares
├── venv/                  # Ambiente virtual
│   ├── bin/               # Dependências do projeto
│   ├── include/
│   └── lib/
├── README.md              # Instruções do projeto
├── requirements.txt       # Dependências

```

### Principais Arquivos

- `agent.py`: O script principal que realiza a geração do README.md.
- `tools.py`: Contém funções auxiliares para operação do agente.
- `venv/`: Ambiente virtual contendo as dependências do projeto.

## Contribuindo

Contribuições são bem-vindas! Se você encontrar um bug ou quiser adicionar uma nova funcionalidade, sinta-se à vontade para abrir uma issue ou um pull request.

1. Faça um fork do repositório.
2. Crie uma nova branch (`git checkout -b feature/nova-funcionalidade`).
3. Faça suas alterações e commit (`git commit -m 'Adiciona nova funcionalidade'`).
4. Envie para o seu fork (`git push origin feature/nova-funcionalidade`).
5. Abra um pull request.

---

Estamos sempre procurando formas de melhorar e otimizar o **project_readme**. Se você tiver sugestões, não hesite em nos avisar!