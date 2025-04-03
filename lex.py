import ply.lex as lex
import re


# Definir literais (exceto '.')

literals = [';', '(', ')', ',', '.']



# Definir os tokens

tokens = ['PROGRAM', 'BEGIN', 'END', 'VAR', 'nome', 'codigo', 'varsDecl', 
          'IMPRIME', 'conteudoP']




# Palavras reservadas

def t_PROGRAM(t):
    r'program'
    return t


def t_BEGIN(t):
    r'begin'
    return t


def t_END(t):
    r'end'
    return t


def t_VAR(t):
    r'var'
    return t


def t_IMPRIME(t):
    r'writeln'
    return t

def t_conteudoP(t):
    r'\([^)]*\)'
    return t


# VOU MUDAR ISTO
def t_varsDecl(t):

    r'[A-Za-z]\w*(\s*,\s*[A-Za-z]\w*)*\s*:\s*[A-Za-z]\w*\s*'

    match = re.match(r'([A-Za-z]\w*(?:\s*,\s*[A-Za-z]\w*)*)\s*:\s*([A-Za-z]\w*)\s*', t.value)

    if match:
        variaveis = match.group(1).split(",")
        tipo = match.group(2)
        variaveis = [var.strip() for var in variaveis]
        t.value = {"variaveis": variaveis, "tipo": tipo}

    return t



# Captura código genérico

def t_codigo(t):
    r'[a-zA-Z_][^\n;]*;'
    return t

def t_nome(t):
    r'[A-Za-z]+'
    return t


# Ignorar espaços e novas linhas

t_ignore = " \n"


# Tratamento de erros

def t_error(t):

    print(f'Caracter ilegal: {t.value[0]}')

    t.lexer.skip(1)


# Construir o lexer
lexer = lex.lex()


