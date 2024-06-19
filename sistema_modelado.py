#biblioteca para manipulção de texto
import textwrap
#importa classes abstratas
from abc import ABC, abstractclassmethod, abstractproperty

#define a classe cliente
class Cliente:
    def __init__(self, endereco):
        #inicializa o endereco e a lista de contas do cliente
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        #registra a transacao na conta especifica
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        #adiciona uma nova conta a lista de contas do cliente
        self.contas.append(conta)

#define a classe pessoa fisica que herda de cliente
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        #chama o construtor da classe pai (cliente)
        super().__init__(endereco)
        #inicializa os parametros
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

#define a classe conta
class Conta:
    def __init__(self, numero, cliente):
        #inicia os parametros
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        #associa o cliente a conta
        self._cliente = cliente
        #cria um historico de transacoes
        self._historico = Historico()

    #metodo de classe para criar uma nova conta
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    #mapear as propriedades para acessar saldo, nro, agencia, cliente, historico
    @property
    def saldo(self):
        return self._saldo
        #retorna o saldo

    @property
    def numero(self):
        return self._numero
        #retorna o numero

    @property
    def agencia(self):
        return self._agencia
        #retorna a agencia

    @property
    def cliente(self):
        return self._cliente
        #retorna o cliente associado a connta

    @property
    def historico(self):
        return self._historico
        #retorna o historico de transacoes

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\nOperação falhou! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False

        return True

#define a classe conta corrente que herdade conta
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        #chama o construtor da classe pai (conta)
        super().__init__(numero, cliente)
        #inicializa os parametros
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        #conta o numero de saques realizado
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\nOperação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")

        else:
            #chama o metodo sacar da classe pai (conta)
            return super().sacar(valor)

        return False

    def __str__(self):
        #retorna uma string formatada com as informacoes da conta
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

#classe historico para armazenar transacoes
class Historico:
    def __init__(self):
        #lista de transacoes
        self._transacoes = []

    @property
    def transacoes(self):
        #prorpiedade para acessar a lista de transacoes
        return self._transacoes

    def adicionar_transacao(self, transacao):
        #adiciona uma transacao ao historico
        self._transacoes.append(
            {
                #tipo da transacao (saque ou deposito)
                "tipo": transacao.__class__.__name__,
                #valror da transacao
                "valor": transacao.valor,
            }
        )

#classe abstrata transacao define a interface para transacoes
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

#classe que herda de transacao e implementa os metodos abstratos
class Saque(Transacao):
    def __init__(self, valor):
        #valor do saque
        self._valor = valor

    @property
    #propriedade para acessar o valor do saque
    def valor(self):
        return self._valor

    def registrar(self, conta):
        #realiza o saque da conta
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            #adiciona transacao ao historico
            conta.historico.adicionar_transacao(self)

#classe deposito herda de transacao e implementa os metodos abstratos
class Deposito(Transacao):
    def __init__(self, valor):
        #valor do deposito
        self._valor = valor

    @property
    def valor(self):
        #propriedade para acessar o valor do deposito
        return self._valor

    def registrar(self, conta):
        #realiza o deposito na conta
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            #adiciona a transacao ao historico
            conta.historico.adicionar_transacao(self)

#funcao para exibir o menu de opcoes
def menu():
    menu = """    
    ======== SISTEMA BANCÁRIO =======
    [1] DEPOSITAR
    [2] SACAR
    [3] EXTRATO
    [4] CADASTRAR CLIENTE
    [5] CRIAR CONTA
    [6] LISTAR CONTAS
    [0] SAIR
    ================================="""
    return int(input(textwrap.dedent(menu)))

#funcao para filtrar o cliente por cpf
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

#funcao para recuperar a conta do cliente
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

#funcao para realizar um deposito
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    #se ele nao encontrar o cliente
    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

#funcao para sacar
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    #realiza a transacao de saque
    cliente.realizar_transacao(conta, transacao)

#funcao para exibir extrato
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

#funcao para criar clientes
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    #adiciona cliente a lista de clientes
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

#funcao para criar conta
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    #adiciona conta a lista de contas
    contas.append(conta)
    #adiciona a conta a lista de contas do cliente
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

#funcao para listar contas
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        #exibe a conta
        print(textwrap.dedent(str(conta)))

#funcao principal
def main():
    #lista vazia para clientes
    clientes = []
    #lista vazia para contas
    contas = []

    while True:
        #exibe o menu e le a opcao escolhida
        opcao = menu()

        if opcao == 1:
            depositar(clientes)

        elif opcao == 2:
            sacar(clientes)

        elif opcao == 3:
            exibir_extrato(clientes)

        elif opcao == 4:
            criar_cliente(clientes)

        elif opcao == 5:
            #define o numero da nova conta
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 6:
            listar_contas(contas)

        elif opcao == 0:
            break

        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")

#executa a funcao principal
main()