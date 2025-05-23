from simbolos import TabelaSimbolos

# simbolos.py
tabela = TabelaSimbolos()

proximo_endereco_global = 0


# ---------
# Funcoes Auxiliares Semantica
# ----------

def inferir_tipo(expr):
    if isinstance(expr, bool):
        return "boolean"
    if isinstance(expr, int):
        return "integer"
    if isinstance(expr, float):
        return "real"
    if isinstance(expr, str):
        if expr.startswith('"') or expr.startswith("'"):
            return "string"
        if tabela.existe(expr):
            return tabela.obter(expr)["tipo"]
        return "string"  # assume literal string

    if isinstance(expr, tuple):
        if expr[0] == 'call':
            nome_funcao = expr[1]
            if tabela.existe(nome_funcao):
                info = tabela.obter(nome_funcao)
                if info["categoria"] == "funcao":
                    return info["tipo"]
                else:
                    print(f"Erro semântico: '{nome_funcao}' não é uma função.")
                    return "desconhecido"
            else:
                print(f"Erro semântico: função '{nome_funcao}' não declarada.")
                return "desconhecido"

        if expr[0] == '+':
            t1 = inferir_tipo(expr[1])
            t2 = inferir_tipo(expr[2])
            if t1 == "real" or t2 == "real":
                return "real"
            return "integer"
        if expr[0] == 'relop':
            return "boolean"
        if expr[0] == 'array_acesso':
            nome = expr[1]
            tipo = tabela.obter(nome)["tipo"]
            if tipo == "string":
                return "char"  # ou "string" se preferires
            elif isinstance(tipo, tuple) and tipo[0] == "array":
                return tipo[3]  # tipo dos elementos
            else:
                return "desconhecido"

    return "desconhecido"

def verificar_variavel_existe(nome):
    if not tabela.existe(nome):
        print(f"Erro semântico: variável '{nome}' não declarada.")
        return False
    return True

def verificar_atribuicao(destino, valor):
    if not verificar_variavel_existe(destino):
        return

    tipo_dest = tabela.obter(destino)["tipo"]
    tipo_valor = inferir_tipo(valor)

    if tipo_dest != tipo_valor and tipo_valor != "desconhecido":
        print(f"Erro de tipo: '{destino}' é {tipo_dest} mas recebe {tipo_valor}")

def verificar_array_acesso(nome, indice):
    if not verificar_variavel_existe(nome):
        return

    tipo = tabela.obter(nome)["tipo"]

    if tipo == "string":
        tipo_indice = inferir_tipo(indice)
        if tipo_indice != "integer":
            print(f"Erro de tipo: índice de string deve ser inteiro, mas é {tipo_indice}")
    elif isinstance(tipo, tuple) and tipo[0] == "array":
        tipo_indice = inferir_tipo(indice)
        if tipo_indice != "integer":
            print(f"Erro de tipo: índice de array deve ser inteiro, mas é {tipo_indice}")
    else:
        print(f"Erro semântico: '{nome}' não é um array nem string indexável.")


def verificar_funcao(nome, tipo):
    if tabela.existe(nome):
        print(f"Erro semântico: função '{nome}' já declarada.")
    else:
        tabela.adicionar(nome, tipo, categoria="funcao")

def verificar_parametros(parametros):
    nomes_usados = set()
    for nome, tipo in parametros:
        if nome in nomes_usados:
            print(f"Erro semântico: parâmetro duplicado: {nome}")
        else:
            nomes_usados.add(nome)
            tabela.adicionar(nome, tipo, categoria="parametro")


def declarar_variaveis(lista_nomes, tipo):
    global proximo_endereco_global
    for nome in lista_nomes:
        if tabela.existe_no_escopo_atual(nome):
            print(f"Erro semântico: Identificador já declarado: {nome}")
        else:
            tabela.adicionar(nome, tipo, endereco=proximo_endereco_global)
            proximo_endereco_global += 1




def declarar_array(nome, tipo_array):
    global proximo_endereco_global
    if tabela.existe_no_escopo_atual(nome):
        print(f"Erro semântico: Identificador já declarado: {nome}")
    else:
        tabela.adicionar(nome, tipo_array, endereco=proximo_endereco_global)
        proximo_endereco_global += 1



def declarar_funcao(nome, tipo):
    if tabela.existe_no_escopo_atual(nome):
        print(f"Erro semântico: Função '{nome}' já declarada.")
    else:
        tabela.adicionar(nome, tipo, categoria="funcao")

