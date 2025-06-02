import ply.yacc as yacc
from lex import tokens
from simbolos import TabelaSimbolos

from semantica import (
    inferir_tipo,
    verificar_variavel_existe,
    verificar_atribuicao,
    verificar_array_acesso,
    verificar_funcao,
    verificar_parametros,
    declarar_variaveis,
    declarar_array,
    declarar_funcao,
    verificar_instrucao,
    verificar_programa
)

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
    label = f"{prefix}{label_count}".upper().replace("_", "")  # usa LABEL0, FORINICIO1, etc.
    label_count += 1
    return label

def gen_label(nome):
    gen(f"{nome}:    // Label {nome}")


# -------------------------
# GRAMÁTICA PRINCIPAL
# -------------------------
def p_gramatica(p):
    "gramatica : programa '.'"
    p[0] = p[1]

def p_programa(p):
    "programa : cabecalho corpo"

    cabecalho = p[1]
    corpo = p[2]

    titulo = cabecalho[1]
    funcoes = cabecalho[2]
    variaveis_globais = cabecalho[3]

    global proximo_endereco
    proximo_endereco = 0


    # for func in funcoes:
    #     nome_funcao = func[0]
    #     tipo_funcao = func[1]
    #     try:
    #         tabela.adicionar(nome_funcao, tipo_funcao, categoria="funcao", endereco=proximo_endereco)
    #         proximo_endereco += 1
    #     except ValueError as e:
    #         print(f"Erro semântico: {e}")

    for declaracao in variaveis_globais:
        _, nomes, tipo = declaracao
        for nome in nomes:
            if isinstance(tipo, tuple) and tipo[0] == "array":
                # Chama declarar_array (importa-a no topo do ficheiro)
                try:
                    tabela.adicionar(nome, tipo, endereco=proximo_endereco)
                    proximo_endereco += 1
                    #declarar_array(tabela, nome, tipo)
                except ValueError as e:
                    print(f"Erro semântico: {e}")
            else:
                try:
                    tabela.adicionar(nome, tipo, endereco=proximo_endereco)
                    proximo_endereco += 1
                except ValueError as e:
                    print(f"Erro semântico: {e}")

    p[0] = ("programa", cabecalho, corpo)




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
    global parametros_em_espera
    nome_funcao = p[1]
    tipo_funcao = p[6]
    parametros_em_espera = p[3]  # ← Guarda os parâmetros para o bloco

    bloco = p[8]  # vai chamar entrar_funcao e usar os parâmetros
    p[0] = (nome_funcao, tipo_funcao, p[3], bloco)

def p_bloco_funcao(p):
    "bloco_funcao : declaracoes_variaveis corpo"
    p[0] = (p[1], p[2])

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

def p_parametros_vazio(p):
    "parametros :"
    p[0] = []

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



def gerar_expressao(expr):
    if isinstance(expr, bool):
        gen("PUSHI 1     // Push True" if expr else "PUSHI 0     // Push False")
    elif isinstance(expr, int):
        gen(f"PUSHI {expr}     // Push valor {expr}") 
    elif isinstance(expr, float):
        gen(f"PUSHF {expr}     // Push valor {expr}")
    elif isinstance(expr, str):
        if tabela.existe(expr):
            info = tabela.obter(expr)
            endereco = info["endereco"]
            tipo = info["tipo"]
            
            # Se é um array, empilha o endereço base
            if isinstance(tipo, tuple) and tipo[0] == "array":
                gen(f"PUSHG {endereco}     // Push Array Base Address")
            else:
                gen(f"PUSHG {endereco}     // Empilha endreço de {expr}")
        else:
            # String literal
            if expr.startswith("'") and expr.endswith("'"):
                expr = expr[1:-1]  # Remove aspas simples
            item_fmt = expr.replace('"', '\\"')
            if len(item_fmt) == 1:
                converte_to_ascii = ord(item_fmt[0])
                gen(f'PUSHI {converte_to_ascii}     // Push Char Ascii Value')
            else:
                gen(f'PUSHS "{item_fmt}"     // Push String Literal')
    elif isinstance(expr, tuple):
        if expr[0] == '+':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("FADD     // Soma de dois valores")
        # subtração float
        elif expr[0] == '-':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("FSUB     // Subtração de dois valores")
        # multiplicação float
        elif expr[0] == '*':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("FMUL     // Multiplicação de dois valores")

        # divisão inteira (div)
        elif expr[0] == 'div':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("DIV     // Divisão inteira de dois valores")

        # divisão real (/)
        elif expr[0] == '/':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("FDIV     // Divisão real de dois valores")

        # módulo inteiro (mod)
        elif expr[0] == 'mod':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("MOD     // Módulo inteiro de dois valores")
        elif expr[0] == 'relop':
            gerar_expressao(expr[2])
            gerar_expressao(expr[3])
            op = expr[1]
            if op == '>':
                gen("FSUP     // Maior")
            elif op == '<':
                gen("FINF     // Menor")
            elif op == '=':
                gen("EQUAL     // Igual")
            elif op == '<>':
                gen("EQUAL     // Diferente")
                gen("NOT     // Diferente")
            elif op == '>=':
                gen("FSUPEQ     // Maior ou Igual")
            elif op == '<=':
                gen("FINFEQ     // Menor ou Igual")
        elif expr[0] == 'and':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("AND     // E lógico")
        elif expr[0] == 'or':
            gerar_expressao(expr[1])
            gerar_expressao(expr[2])
            gen("OR     // Ou lógico")
        elif expr[0] == 'not':
            gerar_expressao(expr[1])
            gen("NOT     // Não lógico")
        elif expr[0] == 'call' and expr[1] == 'length':
            
            var = expr[2]
            endereco = tabela.obter(var)["endereco"]
            gen(f"PUSHG {endereco}     // Empilha endereço da string")
            gen("STRLEN     // Calcula o tamanho da string")

        elif expr[0] == 'call':
            nome_funcao = expr[1]
            argumento = expr[2]
            
            gerar_expressao(argumento)  # Empilha argumento
            gen(f"PUSHA {nome_funcao}     // Empilha endereço da função {nome_funcao}")
            gen(f"CALL    // Invoca Função")  # Chama a função

        elif expr[0] == 'array_acesso':
            nome_array = expr[1]
            indice_expr = expr[2]
            info = tabela.obter(nome_array)
            endereco = info["endereco"]
            tipo = info["tipo"] 

            if tipo == "string":
                # Empilha endereço base do array
                gen(f"PUSHG {endereco}     // Empilha  endreço de {nome_array}")
                
                # Gera código para o índice
                gerar_expressao(indice_expr)
    
                gen("PUSHI 1     // Offset")  # Para o offset
                gen("FSUB     // Offset")  # Adiciona o offset ao endereço base

                # Carrega o valor do array
                gen("CHARAT     // Valor Asccii do caractere")
            else:
            
                # Empilha endereço base do array
                gen(f"PUSHG {endereco}     // Empilha endereço base do array {nome_array}")

                # Gera código para o índice
                gerar_expressao(indice_expr)

                gen("PUSHI 1     // Offset")  # Para o offset
                gen("FSUB     // Offset")  # Adiciona o offset ao endereço base


                # Carrega o valor do array
                gen("LOADN     // Carrega valor do array")
        elif expr[0] == 'menos':
            gen("PUSHI 0     // Push zero")
            gerar_expressao(expr[1])
            gen("FSUB     // Subtração para negativo")



def p_atribuicao(p):
    "atribuicao : ID ASSIGN expressao"
    p[0] = ("atribuicao", p[1], p[3])

def p_atribuicao_array(p):
    "atribuicao : ID '[' expressao ']' ASSIGN expressao"
    p[0] = ("atribuicao_array", p[1], p[3], p[6])



# -------------------------
# Leitura
# -------------------------

def emitir_uma_expressao_para_input(item):
    """Função auxiliar para gerar código de leitura"""
    if isinstance(item, str):
        # Variável simples
        if tabela.existe(item):
            info = tabela.obter(item)
            endereco = info.get("endereco")
            tipo = info.get("tipo")

            if endereco is None:
                print(f"Erro semântico: variável '{item}' não tem endereço atribuído.")
                return

            gen("READ  // Le string do input")  # lê string do input

            # Conversão dependendo do tipo esperado
            if isinstance(tipo, tuple) and tipo[0] == "array":
                # Para arrays, assume que o tipo base é integer por padrão
                gen("ATOI      // Converte string para inteiro")
            elif tipo == "integer":
                gen("ATOI     // Converte string para inteiro")
            elif tipo == "real":
                gen("ATOF     // Converte string para float")
            # string não precisa de conversão
            
            
            gen(f"STOREG {endereco}     // Armazena {item} no endereço {endereco}")
        else:
            print(f"Erro semântico: variável '{item}' não declarada.")
    
    elif isinstance(item, tuple) and item[0] == "array_acesso":
        # Acesso a array: item = ("array_acesso", nome_array, indice_expr)
        nome_array = item[1]
        indice_expr = item[2]
        
        
        if isinstance(item, tuple) and item[0] == "array_acesso":
            nome_array = item[1]
            indice_expr = item[2]



            if tabela.existe(nome_array):
                info = tabela.obter(nome_array)
                endereco = info["endereco"]
                tipo = info["tipo"]

                gen(f"PUSHG {endereco}     // Empilha endereço base do array {nome_array}")

                gerar_expressao(indice_expr)

                gen("PUSHI 1     // Offset")  # Para o offset
                gen("FSUB     // Offset")  # Adiciona o offset ao endereço base
                

                gen("READ     // lê string do input")
                gen("ATOI     // Converte string para inteiro")  # assume input is integer


                
                gen("STOREN     // Armazena o valor lido no array")
        else:
            print(f"Erro semântico: array '{nome_array}' não declarado.")

def p_leitura_read(p):
    "leitura : READ '(' expressao ')'"
    p[0] = ("read", p[3])

def p_leitura_readln(p):
    "leitura : READLN '(' expressao ')'"
    p[0] = ("readln", p[3])

# -------------------------
# Escrita
# -------------------------

def emitir_uma_expressao_para_output(item):
    """Função auxiliar para gerar código de escrita"""

    if isinstance(item, str):
        if tabela.existe(item):
            # É uma variável declarada
            info = tabela.obter(item)
            endereco = info.get("endereco")
            tipo = info.get("tipo")

            if endereco is None:
                print(f"Erro semântico: variável '{item}' não tem endereço atribuído.")
                return

            gen(f'PUSHG {endereco}    // Empilha endereço de {item}')

            if isinstance(tipo, tuple) and tipo[0] == "array":
                # Para arrays, não sabemos como imprimir diretamente
                gen("WRITEI")  # Assume que vai imprimir o endereço por agora
            elif tipo == "integer":
                gen("WRITEI     // Imprime inteiro")
            elif tipo == "real":
                gen("WRITEF     // Imprime float")
            else:
                gen("WRITES     // Imprime string")
        else:
            # String literal
            if item.startswith("'") and item.endswith("'"):
                item = item[1:-1]  # Remove aspas simples
            item_fmt = item.replace('"', '\\"')
            gen(f'PUSHS "{item_fmt}"     // Push String')
            gen("WRITES     // Imprime string")
    elif isinstance(item, tuple) and item[0] == "array_acesso":
        # Acesso a elemento de array
        gerar_expressao(item)
        
        # Determina o tipo do elemento para escolher a instrução de escrita
        nome_array = item[1]
        if tabela.existe(nome_array):
            info = tabela.obter(nome_array)
            tipo = info["tipo"]
            if isinstance(tipo, tuple) and tipo[0] == "array":
                tipo_elemento = tipo[3]
                if tipo_elemento == "integer":
                    gen("WRITEI     // Imprime inteiro")
                elif tipo_elemento == "real":
                    gen("WRITEF     // Imprime float")
                else:
                    gen("WRITES     // Imprime string")
            else:
                gen("WRITEI     // Imprime inteiro")  # padrão
        else:
            gen("WRITEI     // Imprime inteiro")  # padrão
    elif isinstance(item, int):
        gen(f'PUSHI {item}     // Push {item}')
        gen("WRITEI     // Imprime inteiro")
    elif isinstance(item, float):
        gen(f'PUSHF {item}     // Push {item}')
        gen("WRITEF     // Imprime float")
    else:
        # Expressão complexa
        gerar_expressao(item)
        tipo_expr = inferir_tipo(tabela, item)
        if tipo_expr == "integer":
            gen("WRITEI     // Imprime inteiro")
        elif tipo_expr == "real":
            gen("WRITEF     // Imprime float")
        else:
            gen("WRITES     // Imprime string")

def p_escrita_writeln_vazio(p):
    "escrita : WRITELN"
    p[0] = ("writeln", [])          # aceita somente writeln;

def p_escrita_writeln(p):
    "escrita : WRITELN '(' lista_expressao ')'"
    p[0] = ("writeln", p[3])        # writeln(lista)

def p_escrita_write(p):
    "escrita : WRITE '(' lista_expressao ')'"
    p[0] = ("write", p[3])

# -------------------------
# IF, WHILE, FOR
# -------------------------

def gerar_instrucao(instr):
    """Função principal para gerar código das instruções"""
    if instr is None or (isinstance(instr, tuple) and instr[0] == "vazio"):
        return

    if instr[0] == "corpo":
        for i in instr[1]:
            gerar_instrucao(i)

    elif instr[0] == "writeln":
        for item in instr[1]:
            emitir_uma_expressao_para_output(item)
        gen("WRITELN     // Imprime nova linha")

    elif instr[0] == "write":
        for item in instr[1]:
            emitir_uma_expressao_para_output(item)

    elif instr[0] == "atribuicao":
        destino, valor = instr[1], instr[2]
        gerar_expressao(valor)
        
        if tabela.existe(destino):
            endereco = tabela.obter(destino)["endereco"]
            if endereco is None:
                print(f"Erro semântico: variável '{destino}' não tem endereço atribuído.")
                return
            gen(f"STOREG {endereco}     // Armazena {destino} no endereço {endereco}")
        else:
            print(f"Erro semântico: variável '{destino}' não declarada.")

    elif instr[0] == "retorno_funcao":
        nome_funcao = instr[1]
        expr = instr[2]

        gerar_expressao(expr)

        if tabela.existe(nome_funcao):
            endereco = tabela.obter(nome_funcao)["endereco"]
            gen(f"STOREG {endereco}     // Armazena {nome_funcao} no endereço da função")
        else:
            print(f"Erro: função '{nome_funcao}' não tem endereço atribuído.")

        gen("RETURN     // Retorna da função")

    elif instr[0] == "atribuicao_array":
        nome_array = instr[1]
        indice_expr = instr[2]
        valor_expr = instr[3]
        endereco = tabela.obter(nome_array)["endereco"]
        gen(f"PUSHG {endereco}     // Empilha endereço base do array {nome_array}")
        gerar_expressao(indice_expr)
        gen("PUSHI 1     // Offset")  # Para o offset
        gen("FSUB     // Offset")                     # índice zero-based = i - 1
        gerar_expressao(valor_expr)
        gen("STOREN     // Armazena valor no array")
        


    elif instr[0] == "readln":
        emitir_uma_expressao_para_input(instr[1])

    elif instr[0] == "read":
        emitir_uma_expressao_para_input(instr[1])

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
        gen(f"JZ {label_fim}     // Se condição for falsa, salta para o fim do loop")
        gerar_instrucao(corpo)
        gen(f"JUMP {label_inicio}     // Jump para {label_inicio}")
        gen_label(label_fim)

    elif instr[0] == "bloco":
        for i in instr[1]:
            gerar_instrucao(i)

    elif instr[0] == "for-to":
        var, inicio, fim, corpo = instr[1], instr[2], instr[3], instr[4]
        
        if tabela.existe(var):
            endereco = tabela.obter(var)["endereco"]
            
            # Inicializa a variável
            gerar_expressao(inicio)
            if endereco is None:
                print(f"Erro semântico: variável '{var}' não tem endereço atribuído.")
            
            gen(f"STOREG {endereco}  // 2Armazena {var} no endereço {endereco}")
            
            # Labels para o loop
            label_inicio = nova_label("forinicio")
            label_fim = nova_label("forfim")
            
            gen_label(label_inicio)
            
            # Testa condição (var <= fim)
            gen(f"PUSHG {endereco}    // Empilha indice")
            gerar_expressao(fim)
            gen("FSUP    // Verifica se o indice é maior que o limite superior")  # var >= fim ? (invertido porque queremos var <= fim)
            gen("NOT   // Negação")    # NOT(var >= fim) = (var < fim)
            gen(f"JZ {label_fim}   // Se condição for falsa, salta para o fim do loop")
            
            # Executa corpo
            gerar_instrucao(corpo)
            
            # Incrementa variável
            gen(f"PUSHG {endereco} // Empilha indice")
            gen("PUSHI 1   // Empilha 1")
            gen("FADD  // Incrementa indice")
            gen(f"STOREG {endereco}  // Armazena novo valor na variável")
            
            gen(f"JUMP {label_inicio}   // Salta para o início do loop")
            gen_label(label_fim)
        else:
            print(f"Erro semântico: variável de controle '{var}' não declarada.")

    elif instr[0] == "for-downto":
        var, inicio, fim, corpo = instr[1], instr[2], instr[3], instr[4]
        
        if tabela.existe(var):
            endereco = tabela.obter(var)["endereco"]
            
            gerar_expressao(inicio)
            gen(f"STOREG {endereco}   // Armazena valor inicial na variável")
            
            label_inicio = nova_label("for_inicio")
            label_fim = nova_label("for_fim")
            
            gen_label(label_inicio)
            gen(f"PUSHG {endereco}   // Empilha indice")
            gerar_expressao(fim)
            gen("FINF  // Verifica se é inferior")  # var <= fim ? (invertido porque queremos var >= fim)
            gen("NOT // Negação")    # NOT(var <= fim) = (var > fim)
            gen(f"JZ {label_fim}   // Se condição for falsa, salta para o fim do loop")
            
            gerar_instrucao(corpo)
            
            gen(f"PUSHG {endereco}  // Empilha indice")
            gen("PUSHI 1  // Empilha 1")
            gen("FSUB  // Decrementa indice")  # Decrementa a variável de controle
            gen(f"STOREG {endereco}  // Armazena novo valor na variável")
            
            gen(f"JUMP {label_inicio}  // Salta para o início do loop")
            gen_label(label_fim)
        else:
            print(f"Erro semântico: variável de controle '{var}' não declarada.")

def gerar_codigo_if_else(cond, then_instr, else_instr=None):
    """Função auxiliar para gerar código de if-else"""
    label_else = nova_label("else")
    label_fim = nova_label("fim")

    gerar_expressao(cond)       # expr → empilha resultado
    gen(f"JZ {label_else}  // Salta para a label de else ")     # se falso → salta para else

    gerar_instrucao(then_instr) # executa then

    gen(f"JUMP {label_fim}  // Salta para o final da Label")    # salta para o fim

    gen_label(label_else)

    if else_instr:
        gerar_instrucao(else_instr)  # executa else

    gen_label(label_fim)

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

def p_fator_real_numero(p):
    "fator : REAL_NUMBER"
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
                    gen(F"ALLOC {tamanho} // Aloca espaço para o array {nome} com tamanho {tamanho}")
                    gen(f"STOREG {endereco} // Armazena o o array {nome} no endereço {endereco}")




# funcao auxiliar
def gerar_codigo(ast):
    if ast[0] == "programa":
        cabecalho = ast[1]
        corpo = ast[2]


        # 1. Alocar arrays globais
        gerar_alocacoes_arrays(cabecalho)
        gen("JUMP MAIN  // Salta para o início do programa")

        # 2. Gerar código para funções
        funcoes = cabecalho[2]
        for func in funcoes:
            nome_funcao, tipo_funcao, parametros, bloco = func

            # Entra no escopo da função novamente
            tabela.entrar_funcao()

            # Redefinir endereçamento local
            global proximo_endereco_local
            proximo_endereco_local = 0

            # Parâmetros
            for nome_param, tipo_param in parametros:
                tabela.adicionar(nome_param, tipo_param, categoria="parametro", endereco=proximo_endereco_local)
                proximo_endereco_local += 1

            # Variáveis locais
            declaracoes, corpo_funcao = bloco
            for declaracao in declaracoes:
                _, nomes, tipo = declaracao
                for nome in nomes:
                    try:
                        tabela.adicionar(nome, tipo, endereco=proximo_endereco_local)
                        proximo_endereco_local += 1
                    except ValueError as e:
                        print(f"Erro semântico: {e}")

            gen_label(nome_funcao)
            gerar_instrucao(corpo_funcao)
            gen("RETURN")

            tabela.sair_funcao()  # sair do escopo da função

        # 3. Gerar código principal
        gen ("MAIN:")
        gen("START   // Início do programa")
        gerar_instrucao(corpo)
        gen("STOP   // Fim do programa")

        print("\n Tabela de símbolos final:")
        print(tabela)

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


def executar_parser(codigo_fonte):
    import lex
    from simbolos import TabelaSimbolos
    from semantica import verificar_programa

    # Reset da tabela de símbolos e do código
    if hasattr(tabela, "global_scope"):
        tabela.global_scope.clear()
        tabela.local_scope = None
        tabela.escopo_atual = tabela.global_scope
    codigo_assembly.clear()

    parser.success = True
    ast = parser.parse(codigo_fonte, lexer=lex.lexer)

    if parser.success:
        verificar_programa(tabela, ast)
        gerar_codigo(ast)

        print("\nCódigo Assembly gerado:")
        for instr in codigo_assembly:
            print(instr)
    else:
        print(" Erro de parsing.")



if __name__ == "__main__":
    import sys
    texto = sys.stdin.read()

    parser.success = True
    codigo_assembly.clear()


    ast = parser.parse(texto)

    if parser.success:
        print("Frase válida.")
        print(ast)

        verificar_programa(tabela, ast)


        gerar_codigo(ast)



        # Escrever assembly no ficheiro
        with open("saida.asm", "w", encoding="utf-8", newline="\n") as f:
            for instr in codigo_assembly:
                # Remove espaços e quebras estranhas
                linha = instr.strip().replace('\r', '')
                f.write(linha + "\n")

        ## Opcional: imprimir também no terminal
        #print("\nCódigo Assembly gerado:")
        #for instr in codigo_assembly:
        #    print(instr)