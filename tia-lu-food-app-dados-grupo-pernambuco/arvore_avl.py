# --- FUNÇÕES AUXILIARES DA AV ---

def criar_no(id, dado):
    """Cria um nó representado por um dicionário."""
    return {
        'id': id,
        'dado': dado,     # O objeto completo (item ou pedido)
        'esquerda': None,
        'direita': None,
        'altura': 1
    }

def get_altura(no):
    if not no:
        return 0
    return no['altura']

def get_balanceamento(no):
    if not no:
        return 0
    return get_altura(no['esquerda']) - get_altura(no['direita'])

def rotacionar_direita(y):
    x = y['esquerda']
    T2 = x['direita']

    # Rotação
    x['direita'] = y
    y['esquerda'] = T2

    # Atualiza alturas
    y['altura'] = 1 + max(get_altura(y['esquerda']), get_altura(y['direita']))
    x['altura'] = 1 + max(get_altura(x['esquerda']), get_altura(x['direita']))

    return x

def rotacionar_esquerda(x):
    y = x['direita']
    T2 = y['esquerda']

    # Rotação
    y['esquerda'] = x
    x['direita'] = T2

    # Atualiza alturas
    x['altura'] = 1 + max(get_altura(x['esquerda']), get_altura(x['direita']))
    y['altura'] = 1 + max(get_altura(y['esquerda']), get_altura(y['direita']))

    return y

def inserir(no, id, dado):
    """
    Insere um novo elemento na árvore.
    IMPORTANTE: Em paradigma funcional, você deve sempre capturar o retorno desta função,
    pois ela retorna a nova raiz da subárvore modificada.
    Uso: raiz = inserir(raiz, id, dado)
    """
    # 1. Inserção normal de BST
    if not no:
        return criar_no(id, dado)

    if id < no['id']:
        no['esquerda'] = inserir(no['esquerda'], id, dado)
    elif id > no['id']:
        no['direita'] = inserir(no['direita'], id, dado)
    else:
        # ID duplicado, atualiza o dado e retorna o próprio nó
        no['dado'] = dado
        return no

    # 2. Atualiza altura do ancestral
    no['altura'] = 1 + max(get_altura(no['esquerda']), get_altura(no['direita']))

    # 3. Verifica o fator de balanceamento
    balanceamento = get_balanceamento(no)

    # 4. Se estiver desbalanceado, aplica as rotações

    # Caso Esquerda-Esquerda
    if balanceamento > 1 and id < no['esquerda']['id']:
        return rotacionar_direita(no)

    # Caso Direita-Direita
    if balanceamento < -1 and id > no['direita']['id']:
        return rotacionar_esquerda(no)

    # Caso Esquerda-Direita
    if balanceamento > 1 and id > no['esquerda']['id']:
        no['esquerda'] = rotacionar_esquerda(no['esquerda'])
        return rotacionar_direita(no)

    # Caso Direita-Esquerda
    if balanceamento < -1 and id < no['direita']['id']:
        no['direita'] = rotacionar_direita(no['direita'])
        return rotacionar_esquerda(no)

    return no

def buscar_elemento(no, id):
    """Busca recursiva pelo ID. Retorna o dado (dicionário) ou None."""
    if not no:
        return None
    
    if id == no['id']:
        return no['dado']
    
    if id < no['id']:
        return buscar_elemento(no['esquerda'], id)
    
    return buscar_elemento(no['direita'], id)
