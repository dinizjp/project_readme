# tools.py

import os
import re

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
