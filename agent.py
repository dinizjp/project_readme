#!/usr/bin/env python3
# agent.py

import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

from tools import read_project_files, discover_projects

def generate_readme_for_project(proj_path: str, client: OpenAI):
    """
    Gera e salva README.md em proj_path usando o ChatGPT.
    """
    proj_name = os.path.basename(proj_path)
    arquivos = read_project_files(proj_path)
    if not arquivos:
        print(f"⚠️ Nenhum arquivo relevante em {proj_name}, pulando.")
        return

    # Seu prompt original, sem alterações
    prompt = (
        f"Crie um **README.md** completo para o projeto **{proj_name}**, "
        f"cuja lista de arquivos é: {list(arquivos.keys())}.\n\n"
        "O README deve conter:\n"
        "- **Título** e breve descrição do projeto\n"
        "- **Sumário** com links para cada seção\n"
        "- **Requisitos** e instruções de instalação\n"
        "- **Exemplos de uso** e como rodar/testar\n"
        "- **Estrutura de pastas** e principais arquivos\n"
    )

    messages = [
        {
            "role": "system",
            "content": (
                "Você é um gerador de README.md de alta qualidade para projetos GitHub. "
                "Siga as melhores práticas de documentação: clareza, hierarquia de títulos, "
                "e navegação por sumário."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    # Anexa cada arquivo como contexto
    for name, text in arquivos.items():
        messages.append({
            "role": "assistant",
            "name": name,
            "content": text
        })

    # Chama o ChatGPT sem 'functions' (garante sempre content)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    readme_text = response.choices[0].message.content

    # Salva o README.md
    target = os.path.join(proj_path, "README.md")
    with open(target, "w", encoding="utf-8") as f:
        f.write(readme_text)
    print(f"✅ README gerado em: {target}")

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

        if args.single:
            targets = [root]
        else:
            targets = discover_projects(root)
            print(f"🔍 Em {root}, projetos detectados:", targets)

        for proj in targets:
            generate_readme_for_project(proj, client)

if __name__ == "__main__":
    main()
