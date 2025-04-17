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

    # Prompt principal em português e mais restrito
    base_prompt = (
        f"Você é um gerador profissional de README.md. Use **apenas** as informações abaixo—"
        f"não invente nada que não esteja nestes dados.\n"
        f"Gere um README claro, conciso e completo para o projeto **{proj_name}**.\n\n"
        "O README deve conter as seguintes seções:\n"
        "1. **Título**: use o nome do projeto\n"
        "2. **Descrição**: visão geral baseada só nos arquivos fornecidos\n"
        "3. **Sumário**: links para cada seção\n"
        "4. **Instalação**: instruções a partir de requirements.txt ou setup.py\n"
        "5. **Uso**: exemplos de execução dos principais scripts\n"
        "6. **Estrutura de Pastas**: apenas os arquivos listados — sem dependências externas\n"
        "7. **Contato**: como reportar problemas\n\n"
    )

    # Monta bloco único com todo o código/texto
    file_sections = []
    for name, text in arquivos.items():
        file_sections.append(
            f"---\n### Arquivo: {name}\n```\n{text}\n```\n"
        )
    full_prompt = base_prompt + "\n".join(file_sections)

    messages = [
        {
            "role": "system",
            "content": (
                "Você é um gerador profissional de README.md para GitHub. "
                "Responda **somente** com o conteúdo do README—"
                "não inclua comentários ou markup extra."
                "Tome cuidado extra e revise sempre o texto para não haver trechos repetidos"
            )
        },
        {
            "role": "user",
            "content": full_prompt
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=messages
    )
    readme_text = response.choices[0].message.content

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
        help="Trata cada caminho como um projeto único."
    )
    parser.add_argument(
        "paths", nargs="+",
        help="Caminhos para pastas de projetos ou containers."
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
