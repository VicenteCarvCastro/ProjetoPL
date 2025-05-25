class TabelaSimbolos:
    def __init__(self):
        self.global_scope = {}  # Variáveis globais e funções
        self.local_scope = None  # Tabela local ativa
        self.escopo_atual = self.global_scope

    def entrar_funcao(self):
        self.local_scope = {}
        self.escopo_atual = self.local_scope

    def sair_funcao(self):
        self.local_scope = None
        self.escopo_atual = self.global_scope

    def adicionar(self, nome, tipo, categoria="variavel", tamanho=4, endereco=None):
        if nome in self.escopo_atual:
            raise ValueError(f"Identificador já declarado: {nome}")
        self.escopo_atual[nome] = {
            "tipo": tipo,
            "categoria": categoria,
            "tamanho": tamanho,
            "endereco": endereco
        }

    def obter(self, nome):
        if self.local_scope and nome in self.local_scope:
            return self.local_scope[nome]
        return self.global_scope.get(nome)

    def existe(self, nome):
        return self.obter(nome) is not None

    def __str__(self):
        result = "Tabela de Símbolos:\n"
        result += "  [Global]\n"
        for nome, props in self.global_scope.items():
            props_str = ", ".join(f"{k}={v}" for k, v in props.items())
            result += f"    {nome}: {props_str}\n"
        if self.local_scope:
            result += "  [Local]\n"
            for nome, props in self.local_scope.items():
                props_str = ", ".join(f"{k}={v}" for k, v in props.items())
                result += f"    {nome}: {props_str}\n"
        return result

    def em_funcao(self, nome):
        """Verifica se estamos dentro da função de nome `nome`."""
        return self.escopo_atual == self.local_scope and self.local_scope is not None and nome not in self.global_scope