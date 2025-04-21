import ply.lex as lex

# -------------------------
# PALAVRAS RESERVADAS
# -------------------------
reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'integer': 'INTEGER',
    'real': 'REAL',
    'boolean': 'BOOLEAN',
    'char': 'CHAR',
    'array': 'ARRAY',
    'of': 'OF',
    'begin': 'BEGIN',
    'end': 'END',
    'readln': 'READLN',
    'writeln': 'WRITELN',
    'write': 'WRITE',
    'read': 'READ',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'for': 'FOR',
    'to': 'TO',
    'downto': 'DOWNTO',
    'true': 'TRUE',
    'false': 'FALSE'
}

# -------------------------
# LISTA DE TOKENS
# -------------------------
tokens = [
    'ID', 'NUMBER', 'STRING_LITERAL', 'ASSIGN', 'RANGE',
    'EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'LESS_THAN_OR_EQUAL_TO',
    'GREATER_THAN', 'GREATER_THAN_OR_EQUAL_TO'
] + list(reserved.values())

# -------------------------
# LITERAIS
# -------------------------
literals = [';', ',', '(', ')', '.', ':', '[', ']']

# -------------------------
# EXPRESSÕES REGULARES DOS TOKENS
# -------------------------
t_ignore = ' \t'

t_ASSIGN = r':='
t_RANGE = r'\.\.'
t_EQUALS = r'='
t_NOT_EQUALS = r'<>'
t_LESS_THAN = r'<'
t_LESS_THAN_OR_EQUAL_TO = r'<='
t_GREATER_THAN = r'>'
t_GREATER_THAN_OR_EQUAL_TO = r'>='

def t_STRING_LITERAL(t):
    r'\'(.*?)\''
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
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

lexer = lex.lex()



