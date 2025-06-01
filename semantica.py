def inferir_tipo(tabela, expr):
    if isinstance(expr, bool):
        return "boolean"
    if isinstance(expr, int):
        return "integer"
    if isinstance(expr, float):
        return "real"
    if isinstance(expr, str):
        # Se é uma variável declarada
        if tabela.existe(expr):
            return tabela.obter(expr)["tipo"]
        else:
            # Se não existe na tabela, assume que é string literal
            return "string"

    if isinstance(expr, tuple):
        op = expr[0]

        if op in ('+', '-', '*', 'div', 'mod', '/'):
            t1 = inferir_tipo(tabela, expr[1])
            t2 = inferir_tipo(tabela, expr[2])
            if t1 == "real" or t2 == "real":
                return "real"
            return "integer"

        if op == 'relop':
            return "boolean"

        if op in ('and', 'or', 'not'):
            return "boolean"

        if op == 'array_acesso':
            nome_array = expr[1]
            if tabela.existe(nome_array):
                tipo_array = tabela.obter(nome_array)["tipo"]
                if isinstance(tipo_array, tuple) and tipo_array[0] == "array":
                    return tipo_array[3]  # tipo do elemento
            return "desconhecido"

        if op == 'call':
            nome_funcao = expr[1]
            if tabela.existe(nome_funcao):
                return tabela.obter(nome_funcao)["tipo"]

    return "desconhecido"

def verificar_variavel_existe(tabela, nome):
    if not tabela.existe(nome):
        print(f"Erro semântico: variável '{nome}' não declarada.")
        return False
    return True


def verificar_atribuicao(tabela, destino, valor):
    if not verificar_variavel_existe(tabela, destino):
        return

    tipo_dest = tabela.obter(destino)["tipo"]
    tipo_valor = inferir_tipo(tabela, valor)

    if tipo_valor == "desconhecido":
        print(f"Erro semântico: tipo do valor atribuído a '{destino}' é desconhecido.")
    elif tipo_dest != tipo_valor:
        print(f"Erro de tipo: '{destino}' é {tipo_dest} mas recebe {tipo_valor}")



def verificar_array_acesso(tabela, nome_array, indice_expr):
    if not tabela.existe(nome_array):
        print(f"Erro semântico: array '{nome_array}' não declarado.")
        return
    tipo = tabela.obter(nome_array)["tipo"]
    if not (isinstance(tipo, tuple) and tipo[0] == "array"):
        print(f"Erro semântico: '{nome_array}' não é um array.")
        return
    tipo_indice = inferir_tipo(tabela, indice_expr)
    if tipo_indice != "integer":
        print(f"Erro de tipo: índice do array '{nome_array}' deve ser inteiro, mas é {tipo_indice}")


def verificar_funcao(tabela, nome):
    if not tabela.existe(nome):
        print(f"Erro semântico: função '{nome}' não declarada.")
        return False
    return True


def verificar_parametros(tabela, parametros):
    nomes = [nome for nome, _ in parametros]
    if len(nomes) != len(set(nomes)):
        print("Erro semântico: parâmetros duplicados.")


def declarar_variaveis(tabela, declaracoes):
    for declaracao in declaracoes:
        _, nomes, tipo = declaracao
        for nome in nomes:
            if tabela.existe_no_escopo_atual(nome):
                print(f"Erro semântico: variável '{nome}' já declarada.")
            else:
                tabela.adicionar(nome, tipo)

def declarar_array(tabela, nome, tipo_array):
    if not (isinstance(tipo_array, tuple) and tipo_array[0] == "array"):
        raise ValueError(f"Tipo inválido para array em '{nome}'.")

    _, limite_inf, limite_sup, tipo_elemento = tipo_array

    if not isinstance(limite_inf, int) or not isinstance(limite_sup, int):
        raise ValueError(f"Limites do array '{nome}' devem ser inteiros.")

    if limite_inf > limite_sup:
        raise ValueError(f"Limites inválidos no array '{nome}': {limite_inf}..{limite_sup}")

    tamanho = limite_sup - limite_inf + 1

    # Adiciona o array à tabela com o tipo e tamanho
    tabela.adicionar(nome, tipo_array, categoria="array", tamanho=tamanho)




def declarar_funcao(tabela, nome, tipo, parametros=None):
    if tabela.existe_no_escopo_atual(nome):
        raise ValueError(f"Função '{nome}' já declarada.")

    tabela.adicionar(nome, tipo, categoria="funcao")

    if parametros:
        tipos = [tipo for (_, tipo) in parametros]
        tabela.escopo_atual[nome]["parametros"] = tipos
    else:
        tabela.escopo_atual[nome]["parametros"] = []




def verificar_instrucao(tabela, instr):
    if instr is None or (isinstance(instr, tuple) and instr[0] == "vazio"):
        return
    if instr[0] == "corpo":
        for i in instr[1]:
            verificar_instrucao(tabela, i)
    elif instr[0] == "bloco":
        for i in instr[1]:
            verificar_instrucao(tabela, i)
    elif instr[0] == "atribuicao":
        nome, valor = instr[1], instr[2]
        verificar_atribuicao(tabela, nome, valor)

        # Verifica se valor é uma chamada de função
        if isinstance(valor, tuple) and valor[0] == "call":
            nome_funcao = valor[1]
            argumento = valor[2]
            verificar_chamada_funcao(tabela, nome_funcao, argumento)

    elif instr[0] == "atribuicao_array":
        nome_array, indice, valor = instr[1], instr[2], instr[3]
        verificar_array_acesso(tabela, nome_array, indice)
        verificar_atribuicao(tabela, nome_array, valor)
    elif instr[0] in ("if", "if-else"):
        verificar_instrucao(tabela, instr[2])
        if instr[0] == "if-else":
            verificar_instrucao(tabela, instr[3])
    elif instr[0] in ("for-to", "for-downto", "while"):
        verificar_instrucao(tabela, instr[-1])

def verificar_chamada_funcao(tabela, nome_funcao, argumento):
    if not tabela.existe(nome_funcao):
        print(f"Erro semântico: função '{nome_funcao}' não declarada.")
        return

    info = tabela.obter(nome_funcao)
    if info["categoria"] != "funcao":
        print(f"Erro semântico: '{nome_funcao}' não é uma função.")
        return

    tipo_param_esperado = info.get("parametros", [])
    if len(tipo_param_esperado) != 1:
        print(f"Erro semântico: função '{nome_funcao}' espera {len(tipo_param_esperado)} argumento(s), mas recebeu 1.")
        return

    tipo_argumento = inferir_tipo(tabela, argumento)
    tipo_esperado = tipo_param_esperado[0]

    if tipo_argumento != tipo_esperado:
        print(f"Erro de tipo: função '{nome_funcao}' espera argumento do tipo '{tipo_esperado}' mas recebeu '{tipo_argumento}'")



def verificar_programa(tabela, ast):
    if ast[0] != "programa":
        print("Erro: AST inválido.")
        return

    cabecalho = ast[1]
    corpo = ast[2]

    titulo = cabecalho[1]
    funcoes = cabecalho[2]

    # Verificar todas as funções
    for func in funcoes:
        nome, tipo, parametros, bloco = func

        try:
            declarar_funcao(tabela, nome, tipo, parametros)
        except ValueError as e:
            print(f"Erro semântico: {e}")

        tabela.entrar_funcao()

        for nome_param, tipo_param in parametros:
            try:
                tabela.adicionar(nome_param, tipo_param, categoria="parametro")
            except ValueError as e:
                print(f"Erro semântico: parâmetro duplicado: {e}")

        declaracoes, corpo_funcao = bloco

        for declaracao in declaracoes:
            _, nomes, tipo_var = declaracao
            for nome_var in nomes:
                try:
                    if isinstance(tipo_var, tuple) and tipo_var[0] == "array":
                        declarar_array(tabela, nome_var, tipo_var)
                    else:
                        tabela.adicionar(nome_var, tipo_var)
                except ValueError as e:
                    print(f"Erro semântico: variável local duplicada: {e}")

        verificar_instrucao(tabela, corpo_funcao)

        tabela.sair_funcao()

    # Verificar corpo principal
    verificar_instrucao(tabela, corpo)
