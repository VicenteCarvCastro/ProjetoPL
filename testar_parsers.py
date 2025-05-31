import os
import importlib.util

# Caminho para a pasta com os testes
PASTA_TESTES = "pascal"
PASTA_TESTES_ERROS = "pascal_erros"


# Caminhos para os dois parsers
CAMINHO_PARSER1 = "parser.py"
CAMINHO_PARSER2 = "parser2.py"

# Função para importar dinamicamente um módulo .py
def importar_parser(caminho, nome_modulo):
    spec = importlib.util.spec_from_file_location(nome_modulo, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

# Importar os dois parsers
parser1 = importar_parser(CAMINHO_PARSER1, "parser1")
parser2 = importar_parser(CAMINHO_PARSER2, "parser2")

def testar_parsers_em_ficheiros():
    for nome_ficheiro in sorted(os.listdir(PASTA_TESTES_ERROS)):
        if nome_ficheiro.endswith(".pas"):
            caminho = os.path.join(PASTA_TESTES_ERROS, nome_ficheiro)

            with open(caminho, "r", encoding="utf-8") as f:
                codigo = f.read()

            print("=" * 60)
            print(f"🧪 Ficheiro: {nome_ficheiro}")
            print("-" * 60)
            
            print("🔹 Parser 1:")
            try:
                parser1.executar_parser(codigo)
            except Exception as e:
                print(f"Erro: {e}")

            print("\n🔹 Parser 2:")
            try:
                parser2.executar_parser(codigo)
            except Exception as e:
                print(f"Erro: {e}")
            print("=" * 60 + "\n")

if __name__ == "__main__":
    testar_parsers_em_ficheiros()
