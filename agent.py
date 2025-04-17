#!/usr/bin/env python3
# agent.py

import os
import re
import sys
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI

# ------------------------------------------------------------------------------
# CONFIGURAÇÃO DE FILTROS
# ------------------------------------------------------------------------------
EXCLUDE_DIRS = {".git", "data", "tests", "build", "__pycache__"}
EXTS = (
    ".py", ".md", ".txt", "requirements.txt",
    "setup.py", "pyproject.toml"
)
MAX_FILES = 25              # até 25 arquivos por projeto
MAX_CHARS_PER_FILE = 10_000 # até 10k caracteres por arquivo
MAX_NAME_LENGTH = 64        # nome do 'message.name' ≤ 64 chars

# ------------------------------------------------------------------------------
# FERRAMENTAS (tools)
# ------------------------------------------------------------------------------

def read_project_files(project_path: str) -> dict:
    """
    Lê até MAX_FILES arquivos de interesse em project_path,
    pula EXCLUDE_DIRS, filtra por EXTS e trunca a MAX_CHARS_PER_FILE.
    Retorna {safe_name: conteúdo}.
    """
    files = {}
    count = 0
    for dirpath, dirnames, filenames in os.walk(project_path):
        # Remove pastas que não queremos descer em
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for fn in filenames:
            if not fn.endswith(EXTS):
                continue

            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, project_path)

            # Sanitiza nome (remove barras e caracteres proibidos)
            safe_name = re.sub(r"[\\/ <>\|]", "_", rel)
            # Trunca para não ultrapassar 64 caracteres
            if len(safe_name) > MAX_NAME_LENGTH:
                safe_name = safe_name[:MAX_NAME_LENGTH]

            # Lê o arquivo, trunca o conteúdo
            try:
                with open(full, encoding="utf-8", errors="ignore") as f:
                    text = f.read(MAX_CHARS_PER_FILE)
            except Exception as e:
                print(f"⚠️ Falha ao ler {full}: {e}")
                continue

            if len(text) >= MAX_CHARS_PER_FILE:
                text += f"\n\n... (arquivo truncado em {MAX_CHARS_PER_FILE} caracteres)"

            files[safe_name] = text
            count += 1
            if count >= MAX_FILES:
                return files

    return files

def discover_projects(root_dir: str) -> list:
    """
    Retorna apenas as subpastas de primeiro nível de root_dir
    que contenham .git ou arquivos de configuração Python.
    """
    markers = {".git", "requirements.txt", "pyproject.toml", "setup.py"}
    projetos = []
    for name in os.listdir(root_dir):
        path = os.path.join(root_dir, name)
        if not os.path.isdir(path):
            continue

        # Repositório Git?
        if os.path.isdir(os.path.join(path, ".git")):
            projetos.append(path)
            continue

        # Possui arquivo marcador?
        for m in markers - {".git"}:
            if os.path.isfile(os.path.join(path, m)):
                projetos.append(path)
                break

    return projetos

# ------------------------------------------------------------------------------
# GERAÇÃO DO README
# ------------------------------------------------------------------------------

# Schema da tool que expomos ao ChatGPT
FUNCTIONS = [
    {
        "name": "read_project_files",
        "description": "Lê os arquivos de código/texto de um projeto e retorna {nome: conteúdo}.",
        "parameters": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Caminho absoluto da pasta do projeto"
                }
            },
            "required": ["project_path"]
        }
    }
]

def generate_readme_for_project(proj_path: str, client: OpenAI):
    """
    Gera e salva README.md em proj_path usando o ChatGPT.
    """
    proj_name = os.path.basename(proj_path)
    arquivos = read_project_files(proj_path)
    if not arquivos:
        print(f"⚠️ Nenhum arquivo relevante em {proj_name}, pulando.")
        return

    # Cria o prompt
    prompt = (
        f"Crie um **README.md** completo para o projeto **{proj_name}**, "
        f"cuja lista de arquivos é: {list(arquivos.keys())}.\n\n"
        "O README deve conter:\n"
        "- **Título** e breve descrição do projeto\n"
        "- **Badges** (build, versão, licença)\n"
        "- **Sumário** com links para cada seção\n"
        "- **Requisitos** e instruções de instalação\n"
        "- **Exemplos de uso** e como rodar/testar\n"
        "- **Estrutura de pastas** e principais arquivos\n"
    )

    # Mensagens para o ChatGPT
    messages = [
        {
            "role": "system",
            "content": (
                "Você é um gerador de README.md de alta qualidade para projetos GitHub. "
                "Siga as melhores práticas de documentação: clareza, hierarquia de títulos, "
                "badges informativos e navegação por sumário."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    # Anexa cada arquivo (contexto para o modelo)
    for name, text in arquivos.items():
        messages.append({
            "role": "assistant",
            "name": name,
            "content": text
        })

    # Chamada ao ChatGPT (API v1.x style)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=FUNCTIONS,
        function_call="auto"
    )
    readme_text = response.choices[0].message.content

    # Salva o README.md
    target = os.path.join(proj_path, "README.md")
    with open(target, "w", encoding="utf-8") as f:
        f.write(readme_text)
    print(f"✅ README gerado em: {target}")

# ------------------------------------------------------------------------------
# MAIN: parsing de argumentos e controle de modos
# ------------------------------------------------------------------------------

def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    parser = argparse.ArgumentParser(
        description="Agent para gerar README.md via ChatGPT"
    )
    parser.add_argument(
        "--single", "-s",
        action="store_true",
        help="Trata cada caminho como um projeto único (não lista subpastas)."
    )
    parser.add_argument(
        "paths", nargs="+",
        help="Caminhos para pastas de projetos ou containers de projetos."
    )
    args = parser.parse_args()

    for root in args.paths:
        if not os.path.exists(root):
            print(f"❌ Caminho não existe: {root}")
            continue

        # Escolhe o modo baseado no flag
        if args.single:
            targets = [root]
        else:
            targets = discover_projects(root)
            print(f"🔍 Em {root}, projetos detectados:", targets)

        for proj in targets:
            generate_readme_for_project(proj, client)

if __name__ == "__main__":
    main()
