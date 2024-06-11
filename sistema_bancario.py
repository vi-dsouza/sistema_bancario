def apresenta_menu():
    menu = """    
    ======== SISTEMA BANCÁRIO =======
    [1] DEPOSITAR
    [2] SACAR
    [3] EXTRATO
    [4] CADASTRAR CLIENTE
    [5] CRIAR CONTA
    [0] SAIR
    ================================="""
    print(menu)
    return int(input("\nEscolha a operação: "))

#recebe os parametros por posição
def deposito(saldo, extrato, /):
    valor = float(input("\nInforme o valor para depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Deposito: R${valor:.2f}\n"
        print("\nDeposito realizado com sucesso.")
    else:
        print("\nImpossível depositar valores negativos!")
    return saldo, extrato

#recebe os parametros de forma nomeada
def sacar(*, saldo, extrato, numero_saques, limite, limite_saque):
    valor_saque = float(input("\nQual valor deseja sacar? "))
    if valor_saque > 0:
        if saldo > 0:
            if numero_saques <= limite_saque:
                if valor_saque < limite:
                        saldo -= valor_saque
                        extrato += f"Saque: R${valor_saque:.2f}\n"
                        numero_saques += 1
                        print("\nSaque realizado com sucesso.")
                else:
                    print(f"\nVocê atingiu o limite máximo de R${limite} por saque!\nRealize um saque abaixo do limite.")
            else: 
                print(f"\nLimite diario de {limite_saque} saques atingido!")
        else:
            print(f"\nSaldo insuficiente! Você possui R${saldo} em conta.")
    else:
        print("\nImpossível sacar valores negativos! Tente novamente.")
    return saldo, numero_saques, extrato

def mostrar_extrato(saldo, /, *, extrato):
    print("\n============== EXTRATO ==============\n")

    if not extrato:
        print("\nNão foram realizadas movimentações.")
    else:
        print(extrato)
    print(f"\nSaldo: R${saldo:.2f}")
    print("=====================================")

def extrai_numero_cpf(cpf_cadastrado):
    return ''.join(filter(str.isdigit, cpf_cadastrado))

def cadastra_cliente():
    print("\nSeja bem vindo ao cadastro de clientes.\n")

    nome = str(input("Informe se nome: "))
    dt_nascimento = str(input("Data de nascimento: "))
    cpf = str(input("CPF: "))
    cpf_cadastro = extrai_numero_cpf(cpf)
    lagradouro = str(input(("Lagradouro: ")))
    nro = int(input("Número: "))
    bairro = str(input("Bairro: "))
    cidade = str(input("Cidade/estado: "))

    for cliente in clientes:
        if cliente["cpf"] == cpf_cadastro:
            print("\nImpossível cadastrar 2 usuários com mesmo cpf! Tente novamente.\n")
            return
        
    cliente_novo = {"nome":nome, "data_nasc":dt_nascimento, "cpf":cpf_cadastro, "contas": [], "endereco":{"lagradouro":lagradouro, "nro":nro, 
                                                                                    "bairro":bairro, "cidade/estado":cidade}}

    clientes.append(cliente_novo)
    print("\nCadastro realizado com sucesso..\n")

def cadastra_conta(clientes):
    AGENCIA = "0001"
    numero_conta = sum(len(cliente['contas']) for cliente in clientes) + 1
    usuario_cpf = extrai_numero_cpf(str(input("\nInforme o cpf do titular da conta: \n")))

    conta_criada = {"agencia": AGENCIA, "conta":numero_conta, "cpf_titular":usuario_cpf}

    for cliente in clientes:
        if cliente["cpf"] == usuario_cpf:
            cliente["contas"].append(conta_criada)
            print("\nConta criada com sucesso..\n")
            return
        
    print("\nUsuario não existe!")

saldo = 0
limite = 500
extrato = ""
numero_saques = 1
LIMITE_SAQUE = 3 
clientes = []
contas = []

while True:
    opcao = apresenta_menu()

    if opcao == 1:
        saldo, extrato = deposito(saldo, extrato)
    elif opcao == 2:
        saldo, numero_saques, extrato = sacar(saldo=saldo, extrato=extrato, numero_saques=numero_saques, limite=limite, limite_saque=LIMITE_SAQUE)
    elif opcao == 3:
        mostrar_extrato(saldo, extrato=extrato)
    elif opcao == 4:
        cadastra_cliente()
    elif opcao == 5:
        cadastra_conta(clientes)
    elif opcao == 0:
        print("\nEncerrando a operação...\n")
        break
    else:
        print("OPERAÇÃO INVÁLIDA! TENTE NOVAMENTE")

