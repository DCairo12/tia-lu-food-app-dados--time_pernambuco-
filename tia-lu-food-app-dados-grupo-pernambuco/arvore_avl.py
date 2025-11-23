class No:
    def __init__(self, id, dado):
        self.id = id
        self.dado = dado
        self.esquerda = None
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def get_altura(self, no):
        if not no:
            return 0
        return no.altura

    def get_balanceamento(self, no):
        if not no:
            return 0
        return self.get_altura(no.esquerda) - self.get_altura(no.direita)

    def rotacionar_direita(self, y):
        x = y.esquerda
        T2 = x.direita

        # Rotação
        x.direita = y
        y.esquerda = T2

        # Atualiza alturas
        y.altura = 1 + max(self.get_altura(y.esquerda), self.get_altura(y.direita))
        x.altura = 1 + max(self.get_altura(x.esquerda), self.get_altura(x.direita))

        return x

    def rotacionar_esquerda(self, x):
        y = x.direita
        T2 = y.esquerda

        # Rotação
        y.esquerda = x
        x.direita = T2

        # Atualiza alturas
        x.altura = 1 + max(self.get_altura(x.esquerda), self.get_altura(x.direita))
        y.altura = 1 + max(self.get_altura(y.esquerda), self.get_altura(y.direita))

        return y

    def inserir(self, no, id, dado):
        # 1. Inserção normal de BST
        if not no:
            return No(id, dado)

        if id < no.id:
            no.esquerda = self.inserir(no.esquerda, id, dado)
        elif id > no.id:
            no.direita = self.inserir(no.direita, id, dado)
        else:
            # ID duplicado, atualiza o dado ou retorna
            no.dado = dado
            return no

        # 2. Atualiza altura do ancestral
        no.altura = 1 + max(self.get_altura(no.esquerda), self.get_altura(no.direita))

        # 3. Verifica o fator de balanceamento
        balanceamento = self.get_balanceamento(no)

        # 4. Se estiver desbalanceado, aplica as rotações

        # Caso Esquerda-Esquerda
        if balanceamento > 1 and id < no.esquerda.id:
            return self.rotacionar_direita(no)

        # Caso Direita-Direita
        if balanceamento < -1 and id > no.direita.id:
            return self.rotacionar_esquerda(no)

        # Caso Esquerda-Direita
        if balanceamento > 1 and id > no.esquerda.id:
            no.esquerda = self.rotacionar_esquerda(no.esquerda)
            return self.rotacionar_direita(no)

        # Caso Direita-Esquerda
        if balanceamento < -1 and id < no.direita.id:
            no.direita = self.rotacionar_direita(no.direita)
            return self.rotacionar_esquerda(no)

        return no

    def inserir_elemento(self, id, dado):
        self.raiz = self.inserir(self.raiz, id, dado)

    def buscar(self, no, id):
        if not no or no.id == id:
            return no
        
        if id < no.id:
            return self.buscar(no.esquerda, id)
        
        return self.buscar(no.direita, id)

    def buscar_elemento(self, id):
        resultado = self.buscar(self.raiz, id)
        if resultado:
            return resultado.dado # Retorna o dicionário do dado
        return None
    
    def em_ordem(self, no, lista_resultado):
        # Útil para gerar relatórios ordenados ou salvar de volta no JSON
        if no:
            self.em_ordem(no.esquerda, lista_resultado)
            lista_resultado.append(no.dado)
            self.em_ordem(no.direita, lista_resultado)