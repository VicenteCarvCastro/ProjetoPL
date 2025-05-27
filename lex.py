import re
import ply.lex as lex

# -------------------------
# LISTA DE TOKENS
# -------------------------
tokens = [
    'PROGRAM', 'FUNCTION', 'VAR', 'ARRAY', 'OF',
    'BEGIN', 'END', 'READLN', 'READ', 'WRITELN', 'WRITE',
    'IF', 'THEN', 'ELSE', 'WHILE', 'DOWNTO', 'FOR', 'TO',
    'DO', 'TRUE', 'FALSE', 'DIV', 'MOD',
    'NOT', 'AND', 'OR', 'ID', 'NUMBER', 'STRING_LITERAL', 'ASSIGN',
    'EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'LESS_THAN_OR_EQUAL_TO',
    'GREATER_THAN', 'GREATER_THAN_OR_EQUAL_TO', 'RANGE',
    'STRING', 'CHAR', 'BOOLEAN', 'REAL', 'INTEGER'
]

# -------------------------
# LITERAIS
# -------------------------
literals = [';', ',', '(', ')', '.', ':', '[', ']', '+', '-', '*', '/']


# Palavras reservadas

def t_PROGRAM(t):
    r'program'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_VAR(t):
    r'var'
    return t

def t_INTEGER(t):
    r'integer'
    return t

def t_REAL(t):
    r'real'
    return t

def t_BOOLEAN(t):
    r'boolean'
    return t

def t_CHAR(t):
    r'char'
    return t

def t_STRING(t):
    r'string'
    return t

def t_ARRAY(t):
    r'array'
    return t

def t_OF(t):
    r'of'
    return t

def t_BEGIN(t):
    r'begin'
    return t

def t_END(t):
    r'end'
    return t

def t_READLN(t):
    r'readln'
    return t

def t_READ(t):
    r'read'
    return t

def t_WRITELN(t):
    r'writeln'
    return t

def t_WRITE(t):
    r'write'
    return t

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DOWNTO(t):
    r'downto'
    return t

def t_DO(t):
    r'do'
    return t

def t_FOR(t):
    r'for'
    return t

def t_TO(t):
    r'to'
    return t

def t_TRUE(t):
    r'true'
    t.value = True
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t

def t_DIV(t):
    r'div'
    return t

def t_MOD(t):
    r'mod'
    return t

def t_NOT(t):
    r'not'
    return t

def t_AND(t):
    r'and'
    return t

def t_OR(t):
    r'or'
    return t

# -------------------------
# EXPRESSÕES REGULARES DOS TOKENS
# -------------------------
t_ignore = ' \t'

def t_ASSIGN(t):
    r':='
    return t

def t_EQUALS(t):
    r'='
    return t

def t_NOT_EQUALS(t):
    r'<>|!='
    return t

def t_LESS_THAN_OR_EQUAL_TO(t):
    r'<='
    return t

def t_GREATER_THAN_OR_EQUAL_TO(t):
    r'>='
    return t

def t_LESS_THAN(t):
    r'<'
    return t

def t_GREATER_THAN(t):
    r'>'
    return t

def t_RANGE(t):
    r'\.\.'
    return t

def t_STRING_LITERAL(t):
    r"'[^']*?'"
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_COMMENT(t):
    r'\{[^}]*\}'
    pass  # ignora comentários

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    t.lexer.skip(1)

# -------------------------
# CONSTRUIR O LEXER
# -------------------------
lexer = lex.lex(reflags=re.IGNORECASE)


