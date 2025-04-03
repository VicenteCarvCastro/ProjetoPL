import ply.yacc as yacc
from lex import tokens

def p_Gramatica(p):
    "S : Programa '.'"

def p_Programa(p): 
    "Programa : Head Body"


def p_Head(p):
    "Head : Titulo Variaveis"

def p_Titulo(p):
    "Titulo : PROGRAM nome"

def p_Titulo_geral(p):
    "Variaveis : VAR vars"

def p_Titulo_empty(p):
    "Variaveis : "

def p_vars_ListaInstrucoes(p):
    "vars : varsDecl ';' vars"

def p_vars_decl(p):
    "vars : varsDecl"

def p_Body(p):
    "Body : BEGIN ListaInstrucoes END"


def p_ListaInstrucoes_geral(p):
    "ListaInstrucoes : ListaInstrucoes ';' Instrucao"

def p_ListaInstrucoes_empty(p):
    "ListaInstrucoes : Instrucao"


def p_Instrucao_codigo(p):
    "Instrucao : codigo ';'"

def p_Instrucao_imprime(p):
    "Instrucao : Print ';'"

def p_Print(p):
    "Print : IMPRIME conteudoP"
    p[0] = p[2][1:-1]
    print(">> ", p[0])


# Função de erro detalhada
def p_error(p):
    if p:
        print(f"Erro sintático: Token inesperado '{p}' na linha {p.lineno}")
    else:
        print("Erro sintático: Fim inesperado do arquivo. Verifique se falta um ponto no final.")  
    parser.success = False

# Construir o parser
parser = yacc.yacc(debug=True)

# Ler entrada e processar
import sys
texto = sys.stdin.read().strip()  # Remove espaços extras no final da entrada
parser.success = True
parser.parse(texto)

if parser.success:
    print("Frase válida: ", texto)
else:
    print("Frase inválida.. Corrija e tente novamente")
