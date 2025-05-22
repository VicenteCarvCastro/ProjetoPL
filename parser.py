import ply.yacc as yacc
from lex import tokens
from simbolos import TabelaSimbolos

tabela = TabelaSimbolos()
codigo_assembly = []
proximo_endereco = 0
proximo_endereco_local = 0
label_count = 0
parametros_em_espera = []  # usado para passar os parâmetros para o bloco_funcao


def gen(instr):
    codigo_assembly.append(instr)


def nova_label(prefix="label"):
    global label_count
    label = f"{prefix}{label_count}"  # sem underscore!
    label_count += 1
    return label

def gen_label(nome):
    gen(f"LABEL: {nome}")


# -------------------------
# GRAMÁTICA PRINCIPAL
# -------------------------
def p_gramatica(p):
    "gramatica : programa '.'"
    p[0] = p[1]

def p_programa(p):
    "programa : cabecalho corpo"

    global proximo_endereco
    proximo_endereco = 0
    _,titulo, funcoes, variaveis_globais = p[1]

    # Inserir variáveis globais na tabela de símbolos (alteraçao para pascal7)
    for declaracao in variaveis_globais:
        _, nomes, tipo = declaracao
        for nome in nomes:
            try:
                tabela.adicionar(nome, tipo, endereco=proximo_endereco)
                proximo_endereco += 1
            except ValueError as e:
                print(f"Erro semântico: {e}")

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
    for func in p[2]:
        nome_funcao = func[0]
        tipo_funcao = func[1]
        try:
            tabela.adicionar(nome_funcao, tipo_funcao, categoria="funcao")
        except ValueError as e:
            print(f"Erro semântico: {e}")





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
    global parametros_em_espera
    nome_funcao = p[1]
    tipo_funcao = p[6]
    parametros_em_espera = p[3]  # ← Guarda os parâmetros para o bloco

    bloco = p[8]  # vai chamar entrar_funcao e usar os parâmetros
    p[0] = (nome_funcao, tipo_funcao, p[3], bloco)





def p_bloco_funcao(p):
    "bloco_funcao : declaracoes_variaveis corpo"
    global parametros_em_espera, proximo_endereco_local
    proximo_endereco_local = 0

    tabela.entrar_funcao()

    for nome_param, tipo_param in parametros_em_espera:
        tabela.adicionar(nome_param, tipo_param, categoria="parametro", endereco=proximo_endereco_local)
        proximo_endereco_local += 1

    vars = p[1]
    corpo = p[2]

    # Adiciona as variáveis locais à tabela de símbolos (alteraçao para pascal7)
    for declaracao in vars:
        _, nomes, tipo = declaracao
        for nome in nomes:
            try:
                tabela.adicionar(nome, tipo, endereco=proximo_endereco_local)
                proximo_endereco_local += 1
            except ValueError as e:
                print(f"Erro semântico: {e}")


    tabela.sair_funcao()

    p[0] = (vars, corpo)




# -------------------------
# PARÂMETROS DE FUNÇÃO
# -------------------------
def p_parametros(p):
    "parametros : lista_id ':' tipo"
    p[0] = [ (nome, p[3]) for nome in p[1] ]  # apenas devolve os pares (nome, tipo)


def p_parametros_varias(p):
    "parametros : lista_id ':' tipo ';' parametros"
    atuais = [ (nome, p[3]) for nome in p[1] ]
    p[0] = atuais + p[5]


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
    p[0] = p[1].lower()

def p_tipo_real(p):
    "tipo : REAL"
    p[0] = p[1].lower()


def p_tipo_boolean(p):
    "tipo : BOOLEAN"
    p[0] = p[1].lower()

def p_tipo_char(p):
    "tipo : CHAR"
    p[0] = p[1].lower()

def p_tipo_string(p):
    "tipo : STRING"
    p[0] = p[1].lower()

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

def inferir_tipo(expr):
    if isinstance(expr, int):
        return "integer"
    if isinstance(expr, float):
        return "real"
    if isinstance(expr, bool):
        return "boolean"
    if isinstance(expr, str):
        if expr.startswith('"') or expr.startswith("'"):
            return "string"
        if tabela.existe(expr):
            return tabela.obter(expr)["tipo"]
        return "desconhecido"
    if isinstance(expr, tuple):
        if expr[0] == '+':
            t1 = inferir_tipo(expr[1])
            t2 = inferir_tipo(expr[2])
            if t1 == "real" or t2 == "real":
                return "real"
            return "integer"
        if expr[0] == 'relop':
            return "boolean"
    return "desconhecido"


def gerar_expressao(expr):
    if isinstance(expr, int):
        gen(f"PUSHI {expr}")
    elif isinstance(expr, float):
        gen(f"PUSHF {expr}")
    elif isinstance(expr, bool):
        gen("PUSHI 1" if expr else "PUSHI 0")
    elif isinstance(expr, str):
        if tabela.existe(expr):
            endereco = tabela.obter(expr)["endereco"]
            gen(f"PUSHG {endereco}")
        else:
            item_fmt = expr.replace('"', '\\"')
            gen(f'PUSHS "{item_fmt}"')
    elif isinstance(expr, tuple):
        if expr[0] == '+':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("ADD")
        elif expr[0] == '-':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("SUB")
        elif expr[0] == '*':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("MUL")
        elif expr[0] == 'div':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("DIV")
        elif expr[0] == 'mod':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("MOD")
        elif expr[0] == 'relop':
            gerar_expressao(expr[2])
            gerar_expressao(expr[3])
            op = expr[1]
            if op == '>':
                gen("SUP")
            elif op == '<':
                gen("INF")
            elif op == '=':
                gen("EQUAL")
            elif op == '<>':
                gen("EQUAL")
                gen("NOT")
            elif op == '>=':
                gen("SUPEQ")
            elif op == '<=':
                gen("INFEQ")
        elif expr[0] == 'and':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("AND")
        elif expr[0] == 'or':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("OR")
        elif expr[0] == 'not':
            gerar_expressao(expr[1])
            gen("NOT")
        elif expr[0] == 'call' and expr[1] == 'length':
            var = expr[2]
            endereco = tabela.obter(var)["endereco"]
            gen(f"PUSHG {endereco}")
            gen("STRLEN")
        elif expr[0] == 'array_acesso':
            nome_array = expr[1]
            indice_expr = expr[2]
            endereco = tabela.obter(nome_array)["endereco"]
            gen(f"PUSHG {endereco}")
            gerar_expressao(indice_expr)
            gen("PUSHI 1")
            gen("SUB")                     # índice zero-based = i - 1
            gen("ADD")
            gen("LOADN")




def p_atribuicao(p):
    "atribuicao : ID ASSIGN expressao"
    p[0] = ("atribuicao", p[1], p[3])


def p_atribuicao_array(p):
    "atribuicao : ID '[' expressao ']' ASSIGN expressao"
    p[0] = ("atribuicao_array", p[1], p[3], p[6])



# -------------------------
# Leitura
# -------------------------

# funcao auxiliar
def emitir_uma_expressao_para_input(item):
    info = tabela.obter(item)

    if info:
        # É uma variável declarada
        endereco = info.get("endereco")
        tipo = info.get("tipo")

        if endereco is None:
            print(f"Erro semântico: variável '{item}' não tem endereço atribuído.")
            return

        gen("READ")  # lê string do input

        # Conversão dependendo do tipo esperado
        if tipo == "integer":
            gen("ATOI")
        elif tipo == "real":
            gen("ATOF")
        # string não precisa de conversão

        gen(f"STOREG {endereco}")

    else:
        print(f"Erro semântico: não é possível fazer readln para '{item}' — não é uma variável declarada.")


def p_leitura_read(p):
    "leitura : READ '(' expressao ')'"
    p[0] = ("read", p[3])

def p_leitura_readln(p):
    "leitura : READLN '(' expressao ')'"
    #emitir_uma_expressao_para_input(p[3])
    p[0] = ("readln", p[3])

# -------------------------
# Escrita
# -------------------------

# Funcao auxiliar
def emitir_uma_expressao_para_output(item):
    info = tabela.obter(item)

    if info:
        # É uma variável declarada
        endereco = info.get("endereco")
        tipo = info.get("tipo")

        if endereco is None:
            print(f"Erro semântico: variável '{item}' não tem endereço atribuído.")
            return

        gen(f'PUSHG {endereco}')

        if tipo == "integer":
            gen("WRITEI")
        elif tipo == "real":
            gen("WRITEF")
        else:
            gen("WRITES")

    else:
        # Não está na tabela: assume que é literal
        if isinstance(item, str):
            # Remove aspas simples se existirem
            if item.startswith("'") and item.endswith("'"):
                item = item[1:-1]
            # Escapa aspas duplas internas
            item_fmt = item.replace('"', '\\"')
            gen(f'PUSHS "{item_fmt}"')
            gen("WRITES")
        else:
            # Se for um número literal direto
            gen(f'PUSHI {item}')
            gen("WRITEI")



def p_escrita_write(p):
    "escrita : WRITE '(' lista_expressao ')'"
    p[0] = ("write", p[3])



def p_escrita_writeln(p):
    "escrita : WRITELN '(' lista_expressao ')'"
    p[0] = ("writeln", p[3])


# -------------------------
# IF, WHILE, FOR
# -------------------------

# funcao auxiliar
def gerar_instrucao(instr):
    print(">>> gerar_instrucao:", instr)  # debug
    if instr is None:
        return

    if instr[0] == "corpo":
        for i in instr[1]:
            gerar_instrucao(i)

    elif instr[0] == "writeln":
        for item in instr[1]:
            emitir_uma_expressao_para_output(item)
        gen("WRITELN")

    elif instr[0] == "write":
        for item in instr[1]:
            emitir_uma_expressao_para_output(item)

    elif instr[0] == "atribuicao":
        destino, valor = instr[1], instr[2]
        gerar_expressao(valor)

        if isinstance(destino, tuple) and destino[0] == "array_acesso":
            nome = destino[1]
            indice = destino[2]
            endereco = tabela.obter(nome)["endereco"]
            gen(f"PUSHG {endereco}")   # endereço base do array
            gerar_expressao(indice)    # índice i (1..5)
            gen("PUSHI 1")
            gen("SUB")                 # índice zero-based = i - 1
            gen("STOREN")              # armazenar no endereço base + (i-1)
        else:
        
            endereco = tabela.obter(destino)["endereco"]
            gen(f"STOREG {endereco}")

    elif instr[0] == "readln":
        var = instr[1]

        if isinstance(var, tuple) and var[0] == "array_acesso":
            nome = var[1]
            indice = var[2]
            endereco = tabela.obter(nome)["endereco"]
            gen("READ")
            gen("ATOI")
            gen(f"PUSHG {endereco}")
            gerar_expressao(indice)
            gen("PUSHI 1")
            gen("SUB")                 # índice zero-based = i - 1
            gen("STOREN")
        else:
            emitir_uma_expressao_para_input(var)

    elif instr[0] == "atribuicao_array":
        nome_array = instr[1]
        indice_expr = instr[2]
        valor_expr = instr[3]
        endereco = tabela.obter(nome_array)["endereco"]
        gen(f"PUSHG {endereco}")
        gerar_expressao(indice_expr)
        gen("PUSHI 1")
        gen("SUB")                     # índice zero-based = i - 1
        gerar_expressao(valor_expr)
        gen("STOREN")

    elif instr[0] == "if":
        gerar_codigo_if_else(instr[1], instr[2])

    elif instr[0] == "if-else":
        gerar_codigo_if_else(instr[1], instr[2], instr[3])

    elif instr[0] == "while":
        cond = instr[1]
        corpo = instr[2]
        label_inicio = nova_label("while_inicio")
        label_fim = nova_label("while_fim")
        gen_label(label_inicio)
        gerar_expressao(cond)
        gen(f"JZ {label_fim}")
        gerar_instrucao(corpo)
        gen(f"JUMP {label_inicio}")
        gen_label(label_fim)

    elif instr[0] == "bloco":
        for i in instr[1]:
            gerar_instrucao(i)

    elif instr[0] == "for-to":
        var, inicio, fim, corpo = instr[1], instr[2], instr[3], instr[4]
        endereco = tabela.obter(var)["endereco"]
        gerar_expressao(inicio)
        gen(f"STOREG {endereco}")
        label_inicio = nova_label("for_inicio")
        label_fim = nova_label("for_fim")
        gen_label(label_inicio)
        gen(f"PUSHG {endereco}")
        gerar_expressao(fim)
        gen("INFEQ")
        gen(f"JZ {label_fim}")
        gerar_instrucao(corpo)
        gen(f"PUSHG {endereco}")
        gen("PUSHI 1")
        gen("ADD")
        gen(f"STOREG {endereco}")
        gen(f"JUMP {label_inicio}")
        gen_label(label_fim)

    elif instr[0] == "for-downto":
        var, inicio, fim, corpo = instr[1], instr[2], instr[3], instr[4]
        endereco = tabela.obter(var)["endereco"]
        gerar_expressao(inicio)
        gen(f"STOREG {endereco}")
        label_inicio = nova_label("for_inicio")
        label_fim = nova_label("for_fim")
        gen_label(label_inicio)
        gen(f"PUSHG {endereco}")
        gerar_expressao(fim)
        gen("SUPEQ")
        gen(f"JZ {label_fim}")
        gerar_instrucao(corpo)
        gen(f"PUSHG {endereco}")
        gen("PUSHI 1")
        gen("SUB")
        gen(f"STOREG {endereco}")
        gen(f"JUMP {label_inicio}")
        gen_label(label_fim)



# Funcao auxiliar
def gerar_codigo_if_else(cond, then_instr, else_instr=None):
    label_else = nova_label("else")
    label_fim = nova_label("fim")

    gerar_expressao(cond)       # expr → empilha resultado
    gen(f"JZ {label_else}")     # se falso → salta para else

    gerar_instrucao(then_instr) # ← aqui estava o problema: pode não ter sido chamado

    gen(f"JUMP {label_fim}")    # salta para o fim

    gen_label(label_else)

    if else_instr:
        gerar_instrucao(else_instr)  # ← este também precisa ser chamado

    gen_label(label_fim)


def p_if_statement_else(p):
    "if_statement : IF expressao THEN instrucao ELSE instrucao"
    #gerar_codigo_if_else(p[2], p[4], p[6])
    p[0] = ("if-else", p[2], p[4], p[6])

def p_if_statement(p):
    "if_statement : IF expressao THEN instrucao"
    #gerar_codigo_if_else(p[2], p[4])
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

def gerar_alocacoes_arrays(cabecalho):
    print(">>> ENTROU EM gerar_alocacoes_arrays")

    if not isinstance(cabecalho, tuple):
        return

    if len(cabecalho) < 3:
        return  # Não há declarações de variáveis

    declaracoes_variaveis = cabecalho[3]

    if not isinstance(declaracoes_variaveis, list):
        return

    for decl in declaracoes_variaveis:
        if isinstance(decl, tuple) and decl[0] == "declaracao":
            nomes = decl[1]
            tipo = decl[2]

            if isinstance(tipo, tuple) and tipo[0] == "array":
                # tipo = ('array', limite_inferior, limite_superior, tipo_elemento)
                limite_inf = tipo[1]
                limite_sup = tipo[2]
                tamanho = limite_sup - limite_inf + 1

                for nome in nomes:
                    info = tabela.obter(nome)
                    if not info:
                        print(f"Erro: variável '{nome}' não encontrada na tabela de símbolos.")
                        continue

                    endereco = info.get("endereco")
                    if endereco is None:
                        print(f"Erro: variável '{nome}' não tem endereço definido.")
                        continue

                    # Geração de código assembly para alocação do array
                    gen(f"PUSHI {tamanho}")
                    gen("ALLOC")
                    gen(f"STOREG {endereco}")




# funcao auxiliar
def gerar_codigo(ast):
    if ast[0] == "programa":
        cabecalho = ast[1]
        corpo = ast[2]
        
        print("DEBUG cabecalho:", cabecalho)

        #  1. Inicializar arrays no segmento global
        gerar_alocacoes_arrays(cabecalho)

        #  2. Gerar o corpo do programa
        gerar_instrucao(corpo)


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

if __name__ == "__main__":
    import sys
    texto = sys.stdin.read()

    parser.success = True
    codigo_assembly.clear()


    ast = parser.parse(texto)

    if parser.success:
        print("Frase válida.")
        print(ast)

        gen("START")
        gerar_codigo(ast)
        gen("STOP")


        # Escrever assembly no ficheiro
        with open("saida.asm", "w", encoding="ascii", errors="ignore", newline="\n") as f:
            for instr in codigo_assembly:
                f.write(instr + "\n")

        # Opcional: imprimir também no terminal
        print("\nCódigo Assembly gerado:")
        for instr in codigo_assembly:
            print(instr)


