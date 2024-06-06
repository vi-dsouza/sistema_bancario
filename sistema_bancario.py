def apresenta_menu():
    menu = """    
    ======== SISTEMA BANCÁRIO =======
    [1] DEPOSITAR
    [2] SACAR
    [3] EXTRATO
    [0] SAIR
    ================================="""
    print(menu)
    return int(input("\nEscolha a operação: "))

def deposito(saldo, extrato):
    valor = float(input("\nInforme o valor para depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Deposito: R${valor:.2f}\n"
        print("\nDeposito realizado com sucesso.")
    else:
        print("\nImpossível depositar valores negativos!")
    return saldo, extrato

def sacar(saldo, extrato, numero_saques, limite, LIMITE_SAQUE):
    valor_saque = float(input("\nQual valor deseja sacar? "))
    if valor_saque > 0:
        if saldo > 0:
            if numero_saques <= LIMITE_SAQUE:
                if valor_saque < limite:
                        saldo -= valor_saque
                        extrato += f"Saque: R${valor_saque:.2f}\n"
                        numero_saques += 1
                        print("\nSaque realizado com sucesso.")
                else:
                    print(f"\nVocê atingiu o limite máximo de R${limite} por saque!\nRealize um saque abaixo do limite.")
            else: 
                print(f"\nLimite diario de {LIMITE_SAQUE} saques atingido!")
        else:
            print(f"\nSaldo insuficiente! Você possui R${saldo} em conta.")
    else:
        print("\nImpossível sacar valores negativos! Tente novamente.")
    return saldo, numero_saques, extrato

def mostrar_extrato(saldo, extrato):
    print("\n============== EXTRATO ==============\n")

    if not extrato:
        print("\nNão foram realizadas movimentações.")
    else:
        print(extrato)
    print(f"\nSaldo: R${saldo:.2f}")
    print("=====================================")

saldo = 0
limite = 500
extrato = ""
numero_saques = 1
LIMITE_SAQUE = 3 

while True:
    opcao = apresenta_menu()

    if opcao == 1:
        saldo, extrato = deposito(saldo, extrato)
    elif opcao == 2:
        saldo, numero_saques, extrato = sacar(saldo, extrato, numero_saques, limite, LIMITE_SAQUE)
    elif opcao == 3:
        mostrar_extrato(saldo, extrato)
    elif opcao == 0:
        print("\nEncerrando a operação...\n")
        break
    else:
        print("OPERAÇÃO INVÁLIDA! TENTE NOVAMENTE")

