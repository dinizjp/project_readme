#!/usr/bin/env python3
# tools.py

import os
import re

# ------------------------------------------------------------------------------
# CONFIGURAÇÃO DE FILTROS
# ------------------------------------------------------------------------------
EXCLUDE_DIRS = {".git", "data", "tests", "build", "__pycache__", "venv", ".venv", "env", "site-packages"}
EXTS = (
    ".py", ".md", ".txt", "requirements.txt",
    "setup.py", "pyproject.toml"
)
MAX_FILES = 25              # até 25 arquivos por projeto
MAX_CHARS_PER_FILE = 10_000 # até 10.000 caracteres por arquivo
MAX_NAME_LENGTH = 64        # nome do 'message.name' ≤ 64 chars

def read_project_files(project_path: str) -> dict:
    """
    Lê até MAX_FILES arquivos de interesse em project_path,
    pula pastas de venv e dependências, filtra por EXTS e trunca a MAX_CHARS_PER_FILE.
    Retorna {safe_name: conteúdo}.
    """
    files = {}
    count = 0
    for dirpath, dirnames, filenames in os.walk(project_path):
        # exclui pastas irrelevantes
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if not fn.endswith(EXTS):
                continue

            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, project_path)

            # sanitiza nome
            safe_name = re.sub(r"[\\/ <>\|]", "_", rel)
            if len(safe_name) > MAX_NAME_LENGTH:
                safe_name = safe_name[:MAX_NAME_LENGTH]

            # lê e trunca conteúdo
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
    Retorna apenas subpastas de primeiro nível de root_dir
    que contenham .git ou arquivos de configuração Python.
    """
    markers = {".git", "requirements.txt", "pyproject.toml", "setup.py"}
    projetos = []
    for name in os.listdir(root_dir):
        path = os.path.join(root_dir, name)
        if not os.path.isdir(path):
            continue

        # repositório Git?
        if os.path.isdir(os.path.join(path, ".git")):
            projetos.append(path)
            continue

        # arquivo marcador?
        for m in markers - {".git"}:
            if os.path.isfile(os.path.join(path, m)):
                projetos.append(path)
                break

    return projetos
