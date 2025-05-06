import ply.yacc as yacc
from lex import tokens

# -------------------------
# PRECEDÊNCIA (para if-else)
# -------------------------
precedence = (
    ('nonassoc', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', '+', '-'),
    ('left', '*', '/', 'DIV', 'MOD'),
    #('right', 'UMINUS'),
    ('left', '(', ')', '[' ,']')  # chamadas e indexações
)

# -------------------------
# GRAMÁTICA PRINCIPAL
# -------------------------
def p_gramatica(p):
    "gramatica : programa '.'"
    p[0] = p[1]

def p_programa(p):
    "programa : cabecalho corpo"
    p[0] = ("programa", p[1], p[2])



# -------------------------
# CABEÇALHO
# -------------------------
def p_cabecalho(p):
    "cabecalho : titulo declaracao_funcoes declaracoes_variaveis"
    p[0] = ("cabecalho", p[1], p[2], p[3])


def p_titulo(p):
    "titulo : PROGRAM ID ';'"
    p[0] = ("titulo", p[2])

# -------------------------
# DECLARAÇÕES DE FUNÇÕES
# -------------------------
def p_declaracao_funcoes(p):
    "declaracao_funcoes : FUNCTION funcoes"
    p[0] = p[2]

def p_declaracao_funcoes_vazio(p):
    "declaracao_funcoes :"
    p[0] = []

def p_funcoes_funcao(p):
    "funcoes : funcao"
    p[0] = [p[1]]

def p_funcoes(p):
    "funcoes : funcao funcoes"
    p[0] = [p[1]] + p[2]

def p_funcao(p):
    "funcao : ID '(' parametros ')' ':' tipo ';' bloco_funcao ';'"
    p[0] = ("funcao", p[1], p[3], p[6], p[8], p[9])

def p_bloco_funcao(p):
    "bloco_funcao : declaracoes_variaveis corpo"
    p[0] = ("bloco_funcao", p[1], p[2])



# -------------------------
# PARÂMETROS DE FUNÇÃO
# -------------------------
def p_parametros_uma(p):
    "parametros : lista_id ':' tipo"
    p[0] = [("param", p[1], p[3])]

def p_parametros_varias(p):
    "parametros : lista_id ':' tipo ';' parametros"
    p[0] = [("param", p[1], p[3])] + p[5]


# -------------------------
# DECLARAÇÕES DE VARIÁVEIS
# -------------------------
def p_declaracoes_variaveis(p):
    "declaracoes_variaveis : VAR declaracoes"
    p[0] = p[2]

def p_declaracoes_variaveis_vazio(p):
    "declaracoes_variaveis :"
    p[0] = []

def p_declaracoes_uma(p):
    "declaracoes : declaracao"
    p[0] = [p[1]]

def p_declaracoes_varias(p):
    "declaracoes : declaracao declaracoes"
    p[0] = [p[1]] + p[2]

def p_declaracao(p):
    "declaracao : lista_id ':' tipo ';'"
    p[0] = ("declaracao", p[1], p[3])

def p_lista_id_uma(p):
    "lista_id : ID"
    p[0] = [p[1]]

def p_lista_id_varias(p):
    "lista_id : lista_id ',' ID"
    p[0] = p[1] + [p[3]]

# -------------------------
# TIPOS
# -------------------------
def p_tipo_inteiro(p):
    "tipo : INTEGER"
    p[0] = "integer"

def p_tipo_real(p):
    "tipo : REAL"
    p[0] = "real"

def p_tipo_boolean(p):
    "tipo : BOOLEAN"
    p[0] = "boolean"

def p_tipo_char(p):
    "tipo : CHAR"
    p[0] = "char"

def p_tipo_string(p):
    "tipo : STRING"
    p[0] = "string"

def p_tipo_array(p):
    "tipo : ARRAY '[' NUMBER RANGE NUMBER ']' OF tipo"
    p[0] = ("array", p[3], p[5], p[8])

# -------------------------
# CORPO
# -------------------------
def p_corpo(p):
    "corpo : BEGIN lista_instrucoes END"
    p[0] = ("corpo", p[2])

# -------------------------
# LISTA DE INSTRUÇÕES
# -------------------------
def p_lista_instrucoes_uma(p):
    "lista_instrucoes : instrucao"
    p[0] = [p[1]]

def p_lista_instrucoes_varias(p):
    "lista_instrucoes : lista_instrucoes ';' instrucao"
    p[0] = p[1] + [p[3]]

# -------------------------
# INSTRUÇÕES
# -------------------------
def p_instrucao_atribuicao(p):
    "instrucao : atribuicao"
    p[0] = p[1]

def p_instrucao_leitura(p):
    "instrucao : leitura"
    p[0] = p[1]

def p_instrucao_escrita(p):
    "instrucao : escrita"
    p[0] = p[1]

def p_instrucao_if(p):
    "instrucao : if_statement"
    p[0] = p[1]

def p_instrucao_while(p):
    "instrucao : while_statement"
    p[0] = p[1]

def p_instrucao_for(p):
    "instrucao : for_statement"
    p[0] = p[1]

def p_instrucao_bloco(p):
    "instrucao : bloco"
    p[0] = p[1]

def p_instrucao_vazia(p):
    "instrucao :"
    p[0] = ("vazio",)



# -------------------------
# Atribuição
# -------------------------
def p_atribuicao_variavel(p):
    "atribuicao : ID ASSIGN expressao"
    p[0] = ("atribuicao", p[1], p[3])

def p_atribuicao_array(p):
    "atribuicao : ID '[' expressao ']' ASSIGN expressao"
    p[0] = ("atribuicao_array", p[1], p[3], p[6])




# -------------------------
# Leitura
# -------------------------
def p_leitura_read(p):
    "leitura : READ '(' expressao ')'"
    p[0] = ("read", p[3])

def p_leitura_readln(p):
    "leitura : READLN '(' expressao ')'"
    p[0] = ("readln", p[3])

# -------------------------
# Escrita
# -------------------------
def p_escrita_write(p):
    "escrita : WRITE '(' lista_expressao ')'"
    p[0] = ("write", p[3])

def p_escrita_writeln(p):
    "escrita : WRITELN '(' lista_expressao ')'"
    p[0] = ("writeln", p[3])

# -------------------------
# IF, WHILE, FOR
# -------------------------
def p_if_statement_else(p):
    "if_statement : IF expressao THEN instrucao ELSE instrucao"
    p[0] = ("if-else", p[2], p[4], p[6])

def p_if_statement(p):
    "if_statement : IF expressao THEN instrucao"
    p[0] = ("if", p[2], p[4])

def p_while_statement(p):
    "while_statement : WHILE expressao DO instrucao"
    p[0] = ("while", p[2], p[4])

def p_for_statement_to(p):
    "for_statement : FOR ID ASSIGN expressao TO expressao DO instrucao"
    p[0] = ("for-to", p[2], p[4], p[6], p[8])

def p_for_statement_downto(p):
    "for_statement : FOR ID ASSIGN expressao DOWNTO expressao DO instrucao"
    p[0] = ("for-downto", p[2], p[4], p[6], p[8])

def p_bloco(p):
    "bloco : BEGIN lista_instrucoes END"
    p[0] = ("bloco", p[2])

# Lista_expressao
def p_lista_expressao_uma(p):
    "lista_expressao : expressao"
    p[0] = [p[1]]

def p_lista_expressao_varias(p):
    "lista_expressao : lista_expressao ',' expressao"
    p[0] = p[1] + [p[3]]

# -------------------------
# EXPRESSÕES
# -------------------------

# Expressão aritmética
def p_expressao(p):
    "expressao : expressao_logica"
    p[0] = p[1]

def p_expressao_logica_OR(p):
    "expressao_logica : expressao_logica OR expressao_relacional"
    p[0] = ("or", p[1], p[3])

def p_expressao_logica_AND(p):
    "expressao_logica : expressao_logica AND expressao_relacional"
    p[0] = ("and", p[1], p[3])

def p_expressao_logica_relacional(p):
    "expressao_logica : expressao_relacional"
    p[0] = p[1]

# Expressão relacional
def p_expressao_relacional_composta(p):
    "expressao_relacional : expressao_aritmetica operador_relacional expressao_aritmetica"
    p[0] = ("relop", p[2], p[1], p[3])

def p_expressao_relacional_simples(p):
    "expressao_relacional : expressao_aritmetica"
    p[0] = p[1]


# -------------------------
# OPERADORES RELACIONAIS
# -------------------------

def p_operador_relacional_igual(p):
    "operador_relacional : EQUALS"
    p[0] = p[1]

def p_operador_relacional_diferente(p):
    "operador_relacional : NOT_EQUALS"
    p[0] = p[1]

def p_operador_relacional_menor(p):
    "operador_relacional : LESS_THAN"
    p[0] = p[1]

def p_operador_relacional_menor_igual(p):
    "operador_relacional : LESS_THAN_OR_EQUAL_TO"
    p[0] = p[1]

def p_operador_relacional_maior(p):
    "operador_relacional : GREATER_THAN"
    p[0] = p[1]

def p_operador_relacional_maior_igual(p):
    "operador_relacional : GREATER_THAN_OR_EQUAL_TO"
    p[0] = p[1]


def p_expressao_aritmetica_soma(p):
    "expressao_aritmetica : expressao_aritmetica '+' termo"
    p[0] = ('+', p[1], p[3])

def p_expressao_aritmetica_sub(p):
    "expressao_aritmetica : expressao_aritmetica '-' termo"
    p[0] = ('-', p[1], p[3])

def p_expressao_aritmetica_termo(p):
    "expressao_aritmetica : termo"
    p[0] = p[1]

# Termos
def p_termo_multiplicacao(p):
    "termo : termo '*' fator"
    p[0] = ('*', p[1], p[3])

def p_termo_divisao(p):
    "termo : termo '/' fator"
    p[0] = ('/', p[1], p[3])

def p_termo_div(p):
    "termo : termo DIV fator"
    p[0] = ('div', p[1], p[3])

def p_termo_mod(p):
    "termo : termo MOD fator"
    p[0] = ('mod', p[1], p[3])

def p_termo_fator(p):
    "termo : fator"
    p[0] = p[1]

# Fatores
#def p_fator_unario_negativo(p):
    #"fator : '-' fator %prec UMINUS"
    #p[0] = ('neg', p[2])

def p_fator_numero(p):
    "fator : NUMBER"
    p[0] = p[1]

def p_fator_string(p):
    "fator : STRING_LITERAL"
    p[0] = p[1]

def p_fator_id(p):
    "fator : ID"
    p[0] = p[1]

def p_fator_array_index(p):
    "fator : ID '[' expressao ']'"
    p[0] = ("array_acesso", p[1], p[3])


def p_fator_chamada_funcao(p):
    "fator : ID '(' expressao ')'"
    p[0] = ("call", p[1], p[3])

def p_fator_true(p):
    "fator : TRUE"
    p[0] = True

def p_fator_false(p):
    "fator : FALSE"
    p[0] = False

def p_fator_parenteses(p):
    "fator : '(' expressao ')'"
    p[0] = p[2]

def p_fator_not(p):
    "fator : NOT fator"
    p[0] = ('not', p[2])

def p_fator_menos(p):
    "fator : '-' fator"
    p[0] = ('menos', p[2])


# -------------------------
# ERROS
# -------------------------
def p_error(p):
    if p:
        print(f"Erro sintático: Token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("Erro sintático: Fim inesperado do arquivo.")
    parser.success = False

# -------------------------
# PARSER
# -------------------------
parser = yacc.yacc(debug=True)

if __name__ == '__main__':
    import sys
    texto = sys.stdin.read().strip()
    parser.success = True
    result = parser.parse(texto)

    if parser.success:
        print("Frase válida.")
        print(result)
    else:
        print("Frase inválida.")