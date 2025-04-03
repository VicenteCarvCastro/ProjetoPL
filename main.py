import sys
import lex
import parser

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_pascal>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            pascal_code = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        sys.exit(1)

    pascal_lexer = lex.PascalLex().build()
    pascal_parser = parser.PascalParser(pascal_lexer)
    result = pascal_parser.parse(pascal_code)

    if result:
        print("Análise sintática bem-sucedida!")
        # Aqui você pode processar a AST (result)
        print(result)
    else:
        print("Análise sintática falhou.")