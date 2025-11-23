import json
import os
from arvore_avl import ArvoreAVL # Importa a classe da arvore

#Função de ordenação implementada QUICKSORT
def quicksort(array):
    if len(array) < 2:
        return array
    else:
        pivo = array[0]
        menores = [i for i in array[1:] if i <= pivo]
        maiores = [i for i in array[1:] if i > pivo]
        return quicksort(menores) + [pivo] + quicksort(maiores)

#Funções de persistência implementadas com JSON
def carregar_dados(arquivo):
    #Carrega os arquivos JSON
    if os.path.exists(arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def salvar_dados(arquivo, dados):
    #Salva arquivos JSON
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

#Inicializa os dados dos arquivos
cardapio = carregar_dados('dados/cardapio.json')
proximo_codigo_item = max([item['id'] for item in cardapio], default=0) + 1

clientes = carregar_dados('dados/clientes.json')
proximo_codigo_cliente = max([cliente['id'] for cliente in clientes], default=0) + 1

fila_pedidos_pendentes = carregar_dados('dados/pedidos_pendentes.json')
todos_os_pedidos = carregar_dados('dados/todos_os_pedidos.json')
proximo_codigo_pedido = max([pedido['id'] for pedido in todos_os_pedidos], default=0) + 1

fila_pedidos_aceitos = carregar_dados('dados/pedidos_aceitos.json')
fila_pedidos_prontos = carregar_dados('dados/pedidos_prontos.json')

# Inicializa as arvores para busca rapida
arvore_cardapio = ArvoreAVL()
arvore_pedidos = ArvoreAVL()

# Carrega dados do json nas arvores
for item in cardapio:
    arvore_cardapio.inserir_elemento(item['id'], item)

for pedido in todos_os_pedidos:
    arvore_pedidos.inserir_elemento(pedido['id'], pedido)

# ========== LOOP PRINCIPAL DO PROGRAMA ==========
opcao_principal = None

while opcao_principal != 5:
    print("\n" * 3)
    print("="*40)
    print("   Sistema de Pedidos Tia Lu Delivery")
    print("="*40)
    print("1. Gerenciar Menu de Itens")
    print("2. Gerenciar Menu de Pedidos")
    print("3. Consultas e Relatórios")
    print("4. Gerenciar Clientes")
    print("5. Sair do Sistema")
    print("="*40)
    
    opcao_principal = input("Escolha uma opção: ")

    # === MÓDULO 1: GERENCIAR MENU DE ITENS =========
    match opcao_principal:
        case '1':
            print("\n" * 3)
            print("--- Gerenciar Menu de Itens ---")
            print("1. Cadastrar Item")
            print("2. Consultar Itens")
            print("3. Atualizar Item")
            print("4. Voltar ao Menu Principal")
            opcao_itens = input("Escolha uma opção: ")

            # --- Cadastrar Item ---
            match opcao_itens:
                case '1':
                    print("\n" * 3)
                    print("-- Cadastro de Novo Item --")
                    nome = input("Nome do item: ")
                    descricao = input("Descrição do item: ")
                    try:
                        preco = float(input("Preço (ex: 45.50): "))
                        estoque = int(input("Quantidade em estoque: "))
                        
                        novo_item = {
                            'id': proximo_codigo_item,
                            'nome': nome,
                            'descrição': descricao,
                            'preço': preco,
                            'estoque': estoque
                        }
                        cardapio.append(novo_item)
                        # Adiciona tambem na arvore
                        arvore_cardapio.inserir_elemento(novo_item['id'], novo_item)
                        
                        proximo_codigo_item += 1
                        
                        salvar_dados('dados/cardapio.json', cardapio)
                        
                        print(f"\nItem '{nome}' cadastrado com sucesso! id: {novo_item['id']}")
                    except ValueError:
                        print("\nERRO: Preço e estoque devem ser números. Operação cancelada.")
                    input("Pressione Enter para continuar...")

                # --- Consultar Itens ---
                case '2':
                    print("\n" * 3)
                    print("-- Cardápio Completo --")
                    if not cardapio:
                        print("Cardápio vazio.")
                    else:
                        for item in cardapio:
                            print(f"Cód: {item['id']} | {item['nome']} | R${item['preço']:.2f} | Estoque: {item['estoque']} | Desc: {item['descrição']}")
                    input("\nPressione Enter para continuar...")

                # --- Atualizar Item ---
                case '3':
                    print("\n" * 3)
                    print("-- Atualização de Item --")
                    if not cardapio:
                        print("Cardápio vazio.")
                    else:
                        for item in cardapio:
                            print(f"Cód: {item['id']} | Nome: {item['nome']} | Estoque: {item['estoque']}")
                        try:
                            cod_atualizar = int(input("Digite o id do item para atualizar: "))
                            
                            # Busca o item usando a arvore avl
                            item_encontrado = arvore_cardapio.buscar_elemento(cod_atualizar)
                            
                            if item_encontrado:
                                print(f"\nAtualizando item: {item_encontrado['nome']}")
                                novo_nome = input(f"Novo nome (deixe em branco para manter '{item_encontrado['nome']}'): ")
                                novo_preco_str = input(f"Novo preço (deixe em branco para manter R${item_encontrado['preço']:.2f}): ")
                                novo_estoque_str = input(f"Novo estoque (deixe em branco para manter {item_encontrado['estoque']}): ")

                                try:
                                    if novo_nome: item_encontrado['nome'] = novo_nome
                                    if novo_preco_str: item_encontrado['preço'] = float(novo_preco_str)
                                    if novo_estoque_str: item_encontrado['estoque'] = int(novo_estoque_str)
                                    
                                    salvar_dados('dados/cardapio.json', cardapio)
                                    
                                    print("\nItem atualizado com sucesso!")
                                except ValueError:
                                    print("\nERRO: Preço ou estoque inválido. A atualização foi cancelada.")
                            else:
                                print("\nid do item não encontrado.")
                        except ValueError:
                            print("\nERRO: O id deve ser um número. Operação cancelada.")
                    input("Pressione Enter para continuar...")

                case '4':
                    pass
                case _:
                    input("Opção inválida. Pressione Enter para continuar...")

    # === MÓDULO 2: GERENCIAR MENU DE PEDIDOS =======
        case '2':
            print("\n" * 3)
            print("--- Gerenciar Menu de Pedidos ---")
            print("1. Criar Pedido")
            print("2. Processar Pedido Pendente")
            print("3. Atualizar Status de Pedido")
            print("4. Cancelar Pedido")
            print("5. Voltar ao Menu Principal")
            opcao_pedidos = input("Escolha uma opção: ")

            match opcao_pedidos:
                case '1':
                    print("\n" * 3)
                    print("-- Criação de Novo Pedido --")
                    if not cardapio:
                        print("Não é possível criar pedidos, pois o cardápio está vazio.")
                    elif not clientes:
                        print("Não é possível criar pedidos, pois não há clientes cadastrados.")
                    else:
                        print("-- Clientes Cadastrados --")
                        for cliente in clientes:
                            print(f"ID: {cliente['id']} | Nome: {cliente['nome']}")
                        
                        try:
                            cliente_id = int(input("\nDigite o ID do cliente para o pedido: "))
                            cliente_selecionado = None
                            for cliente in clientes:
                                if cliente['id'] == cliente_id:
                                    cliente_selecionado = cliente
                                    break
                            
                            if not cliente_selecionado:
                                print("ID do cliente não encontrado. Operação cancelada.")
                            else:
                                itens_do_pedido = []
                                subtotal = 0.0
                                
                                while True:
                                    print("\n-- Cardápio --")
                                    for item in cardapio:
                                        print(f"Cód: {item['id']} | {item['nome']} | R${item['preço']:.2f} | Estoque: {item['estoque']}")
                                    
                                    codigo_str = input("Digite o id do item para adicionar (ou 'F' para finalizar): ").upper()
                                    if codigo_str == 'F':
                                        break
                                    
                                    try:
                                        cod_item_pedido = int(codigo_str)
                                        
                                        # Busca o item na arvore
                                        item_selecionado = arvore_cardapio.buscar_elemento(cod_item_pedido)
                                        
                                        if item_selecionado:
                                            qtd = int(input(f"Quantidade de '{item_selecionado['nome']}': "))
                                            if 0 < qtd <= item_selecionado['estoque']:
                                                itens_do_pedido.append({
                                                    'id': item_selecionado['id'],
                                                    'nome': item_selecionado['nome'],
                                                    'quantidade': qtd,
                                                    'preco_unitario': item_selecionado['preço']
                                                })
                                                subtotal += item_selecionado['preço'] * qtd
                                                item_selecionado['estoque'] -= qtd
                                                print(f"-> {qtd}x {item_selecionado['nome']} adicionado(s).")
                                            else:
                                                print("Quantidade inválida ou estoque insuficiente.")
                                        else:
                                            print("id do item não encontrado.")
                                    except ValueError:
                                        print("Entrada inválida. Por favor, digite um número ou 'F'.")
                                
                                if not itens_do_pedido:
                                    print("\nNenhum item adicionado. Pedido cancelado.")
                                else:
                                    total = subtotal
                                    cupom = input("Digite o cupom de desconto (ou deixe em branco): ").upper()
                                    if cupom == "DESCONTO10":
                                        total *= 0.9
                                        print("Desconto de 10% aplicado!")

                                    novo_pedido = {
                                        'id': proximo_codigo_pedido,
                                        'cliente': cliente_selecionado['nome'],
                                        'itens': itens_do_pedido,
                                        'total': total,
                                        'status': 'AGUARDANDO APROVACAO'
                                    }
                                    
                                    fila_pedidos_pendentes.append(novo_pedido)
                                    todos_os_pedidos.append(novo_pedido)
                                    
                                    # Indexa o novo pedido na arvore
                                    arvore_pedidos.inserir_elemento(novo_pedido['id'], novo_pedido)

                                    proximo_codigo_pedido += 1
                                    
                                    salvar_dados('dados/pedidos_pendentes.json', fila_pedidos_pendentes)
                                    salvar_dados('dados/todos_os_pedidos.json', todos_os_pedidos)
                                    salvar_dados('dados/cardapio.json', cardapio)
                                    
                                    print(f"\nPedido Cód: {novo_pedido['id']} criado com sucesso para o cliente {cliente_selecionado['nome']}!")
                        
                        except ValueError:
                            print("\nERRO: O ID do cliente deve ser um número. Operação cancelada.")
                    input("Pressione Enter para continuar...")

                case '2':
                    print("\n" * 3)
                    print("-- Processamento de Pedidos Pendentes --")
                    if not fila_pedidos_pendentes:
                        print("Não há pedidos pendentes para processar.")
                    else:
                        pedido_a_processar = fila_pedidos_pendentes[0]
                        
                        print(f"Processando Pedido Cód: {pedido_a_processar['id']} | Cliente: {pedido_a_processar['cliente']}")
                        for item_p in pedido_a_processar['itens']:
                            print(f"- {item_p['quantidade']}x {item_p['nome']}")
                        print(f"Total: R${pedido_a_processar['total']:.2f}")
                        
                        decisao = input("\nDigite (A) para Aceitar ou (R) para Rejeitar o pedido: ").upper()
                        
                        if decisao == 'A':
                            pedido_aceito = fila_pedidos_pendentes.pop(0)
                            pedido_aceito['status'] = 'ACEITO'
                            fila_pedidos_aceitos.append(pedido_aceito)
                            
                            salvar_dados('dados/pedidos_pendentes.json', fila_pedidos_pendentes)
                            salvar_dados('dados/pedidos_aceitos.json', fila_pedidos_aceitos)
                            salvar_dados('dados/todos_os_pedidos.json', todos_os_pedidos)
                            
                            print("Pedido Aceito e movido para a fila de preparo.")
                        elif decisao == 'R':
                            pedido_rejeitado = fila_pedidos_pendentes.pop(0)
                            pedido_rejeitado['status'] = 'REJEITADO'
                            for item_pedido in pedido_rejeitado['itens']:
                                for item_cardapio in cardapio:
                                    if item_pedido['id'] == item_cardapio['id']:
                                        item_cardapio['estoque'] += item_pedido['quantidade']
                                        break
                            
                            salvar_dados('dados/pedidos_pendentes.json', fila_pedidos_pendentes)
                            salvar_dados('dados/cardapio.json', cardapio)
                            salvar_dados('dados/todos_os_pedidos.json', todos_os_pedidos)
                            
                            print("Pedido Rejeitado. Estoque dos itens foi restaurado.")
                        else:
                            print("Decisão inválida. O pedido permanece na fila.")
                    input("Pressione Enter para continuar...")

                case '3':
                    print("\n" * 3)
                    print("-- Atualizar Status de Pedido --")
                    if not todos_os_pedidos:
                        print("Nenhum pedido registrado para atualizar.")
                    else:
                        for p in todos_os_pedidos:
                            print(f"ID: {p['id']} | Cliente: {p['cliente']} | Status: {p['status']}")
                        try:
                            pedido_id = int(input("\nDigite o ID do pedido para atualizar o status: "))
                            
                            # Busca o pedido na arvore
                            pedido_encontrado = arvore_pedidos.buscar_elemento(pedido_id)
                            
                            if not pedido_encontrado:
                                print("Pedido não encontrado.")
                            else:
                                status_atual = pedido_encontrado['status']
                                proximo_status = None
                                
                                match status_atual:
                                    case 'ACEITO':
                                        proximo_status = 'FAZENDO'
                                    case 'FAZENDO':
                                        proximo_status = 'FEITO'
                                    case 'FEITO':
                                        proximo_status = 'ESPERANDO ENTREGADOR'
                                    case 'ESPERANDO ENTREGADOR':
                                        proximo_status = 'SAIU PARA ENTREGA'
                                    case 'SAIU PARA ENTREGA':
                                        proximo_status = 'ENTREGUE'

                                if proximo_status:
                                    confirmacao = input(f"Mudar status de '{status_atual}' para '{proximo_status}'? (S/N): ").upper()
                                    if confirmacao == 'S':
                                        pedido_encontrado['status'] = proximo_status
                                        print(f"Status do pedido {pedido_encontrado['id']} atualizado para {proximo_status}.")
                                        if proximo_status == 'FEITO':
                                            if pedido_encontrado in fila_pedidos_aceitos:
                                                fila_pedidos_aceitos.remove(pedido_encontrado)
                                            fila_pedidos_prontos.append(pedido_encontrado)
                                        
                                        salvar_dados('dados/todos_os_pedidos.json', todos_os_pedidos)
                                        salvar_dados('dados/pedidos_aceitos.json', fila_pedidos_aceitos)
                                        salvar_dados('dados/pedidos_prontos.json', fila_pedidos_prontos)

                                    else:
                                        print("Operação cancelada.")
                                else:
                                    print(f"O pedido com status '{status_atual}' não pode ser avançado.")

                        except ValueError:
                            print("ID do pedido inválido.")
                    input("Pressione Enter para continuar...")

                case '4':
                    print("\n" * 3)
                    print("-- Cancelar Pedido --")
                    if not todos_os_pedidos:
                        print("Nenhum pedido para cancelar.")
                    else:
                        for p in todos_os_pedidos:
                            if p['status'] in ['AGUARDANDO APROVACAO', 'ACEITO']:
                                print(f"ID: {p['id']} | Cliente: {p['cliente']} | Status: {p['status']}")
                        try:
                            pedido_id = int(input("\nDigite o ID do pedido para cancelar: "))
                            
                            # Busca o pedido na arvore para cancelar
                            pedido_a_cancelar = arvore_pedidos.buscar_elemento(pedido_id)
                            
                            if not pedido_a_cancelar:
                                print("Pedido não encontrado.")
                            elif pedido_a_cancelar['status'] not in ['AGUARDANDO APROVACAO', 'ACEITO']:
                                print(f"Não é possível cancelar um pedido com status '{pedido_a_cancelar['status']}'.")
                            else:
                                pedido_a_cancelar['status'] = 'CANCELADO'
                                for item_pedido in pedido_a_cancelar['itens']:
                                    for item_cardapio in cardapio:
                                        if item_pedido['id'] == item_cardapio['id']:
                                            item_cardapio['estoque'] += item_pedido['quantidade']
                                            break
                                
                                salvar_dados('dados/todos_os_pedidos.json', todos_os_pedidos)
                                salvar_dados('dados/cardapio.json', cardapio)
                                
                                print(f"Pedido {pedido_a_cancelar['id']} cancelado com sucesso. Estoque restaurado.")
                        except ValueError:
                            print("ID do pedido inválido.")
                    input("Pressione Enter para continuar...")

                case '5':
                    pass
                case _:
                    input("Opção inválida. Pressione Enter para continuar...")

    # === MÓDULO 3: CONSULTAS E RELATÓRIOS ==========
        case '3':
            print("\n" * 3)
            print("--- Consultas e Relatórios ---")
            print("1. Exibir todos os pedidos")
            print("2. Filtrar pedidos por status")
            print("3. Exibir preços ordenados")
            print("4. Listar clientes em ordem alfabética")
            print("5. Listar IDs de pedidos ordenados")
            print("6. Voltar ao Menu Principal")
            opcao_consultas = input("Escolha uma opção: ")

            match opcao_consultas:
                case '1':
                    print("\n" * 3)
                    print("-- Todos os Pedidos Registrados --")
                    if not todos_os_pedidos:
                        print("Nenhum pedido foi criado ainda.")
                    else:
                        for p in todos_os_pedidos:
                            print(f"Cód: {p['id']} | Cliente: {p['cliente']} | Total: R${p['total']:.2f} | Status: {p['status']}")
                    input("\nPressione Enter para continuar...")

                case '2':
                    print("\n" * 3)
                    status_filtro = input("Digite o status para filtrar (ex: FAZENDO, ACEITO): ").upper()
                    print(f"\n-- Pedidos com Status: {status_filtro} --")
                    encontrados = False
                    for p in todos_os_pedidos:
                        if p['status'] == status_filtro:
                            print(f"Cód: {p['id']} | Cliente: {p['cliente']} | Total: R${p['total']:.2f}")
                            encontrados = True
                    if not encontrados:
                        print(f"Nenhum pedido encontrado com o status '{status_filtro}'.")
                    input("\nPressione Enter para continuar...")

                case '3':
                    print("\n" * 3)
                    print("-- Preços dos Itens Ordenados --")
                    if not cardapio:
                        print("Cardápio vazio.")
                    else:
                        precos = [item['preço'] for item in cardapio]
                        precos_ordenados = quicksort(precos)
                        print("Preços em ordem crescente:")
                        for preco in precos_ordenados:
                            print(f"  R${preco:.2f}")
                    input("\nPressione Enter para continuar...")

                case '4':
                    print("\n" * 3)
                    print("-- Clientes em Ordem Alfabética --")
                    if not clientes:
                        print("Nenhum cliente cadastrado.")
                    else:
                        nomes_clientes = [cliente['nome'] for cliente in clientes]
                        nomes_ordenados = quicksort(nomes_clientes)
                        print("Clientes em ordem alfabética:")
                        for nome in nomes_ordenados:
                            print(f"  {nome}")
                    input("\nPressione Enter para continuar...")

                case '5':
                    print("\n" * 3)
                    print("-- IDs de Pedidos Ordenados --")
                    if not todos_os_pedidos:
                        print("Nenhum pedido registrado.")
                    else:
                        ids_pedidos = [pedido['id'] for pedido in todos_os_pedidos]
                        ids_ordenados = quicksort(ids_pedidos)
                        print("IDs de pedidos em ordem crescente:")
                        for id_pedido in ids_ordenados:
                            print(f"  Pedido nº {id_pedido}")
                    input("\nPressione Enter para continuar...")

                case '6':
                    pass
                case _:
                    input("Opção inválida. Pressione Enter para continuar...")

    # === MÓDULO 4: GERENCIAR CLIENTES ===============
        case '4':
            print("\n" * 3)
            print("-- Gerenciar Clientes --")
            print("1. Cadastrar novo cliente")
            print("2. Listar todos os clientes")
            print("3. Voltar ao Menu Principal")
            opcao_clientes = input("Escolha uma opção: ")

            match opcao_clientes:
                case '1':
                    nome = input("Nome do cliente: ")
                    telefone = input("Telefone do cliente: ")
                    endereco = input("Endereço do cliente: ")
                    
                    novo_cliente = {
                        'id': proximo_codigo_cliente,
                        'nome': nome,
                        'telefone': telefone,
                        'endereco': endereco
                    }

                    clientes.append(novo_cliente)
                    
                    salvar_dados('dados/clientes.json', clientes)
                    
                    print(f"\nCliente '{nome}' cadastrado com sucesso! id: {novo_cliente['id']}")
                    proximo_codigo_cliente += 1
                    input("Pressione Enter para continuar...")
                
                case '2':
                    print("\n" * 3)
                    print("-- Lista de Clientes Cadastrados --")
                    if not clientes:
                        print("Nenhum cliente cadastrado.")
                    else:
                        for cliente in clientes:
                            print(f"Cód: {cliente['id']} | Nome: {cliente['nome']} | Telefone: {cliente['telefone']}")
                    input("Pressione Enter para continuar...")

                case '3':
                    pass

                case _:
                    input("Opção inválida. Pressione Enter para continuar...")

        # === SAÍDA DO SISTEMA ===
        case '5':
            print("Saindo do sistema. Obrigado por usar o Tia Lu Delivery!")
            break
        case _:
            input("Opção principal inválida. Pressione Enter para continuar...")