import os 

def list_projects(root_path: str) -> list:
    """
    Retorna uma lista de pastas de projetos no diretório root_path

    """
    return [

        name for name in os.listdir(root_path)
        if os.path.isdir(os.path.join(root_path, name))      
    ]


def read_project_files(project_path: str) -> dict:
    """ 
    Lê os arquivos .py, .md, requirements.txt de um projeto
     e retorna um dicionário {nome_arquivo: conteúdo}
    """

    files = {}

    for dirpath, _, filenames in os.walk(project_path):
        for fn in filenames:
            if fn.endswith(('.py', '.md', '.txt', '.json')):
                full = os.path.join(dirpath, fn)
                with open(full, encoding='utf-8') as f:
                    rel = os.path.relpath(full, project_path)
                    files[rel] = f.read()
    return files     
    
