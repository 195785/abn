from abc import ABC , abstractclassmethod
from datetime import datetime

class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self,conta,transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self,nome,data_nascimento,cpf,endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        
class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero,cliente)
    @property
    def saldo (self):
        return self._saldo
    @property
    def numero (self):
        return self._numero
    @property
    def agencia (self):
        return self._agencia
    @property
    def cliente (self):
        return self._cliente
    @property
    def historico (self):
        return self._historico
    def sacar (self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("\n000 operação falhou! você não tem saldo suficiente. 000")
        elif valor >0:
            self._saldo -= valor
            print("\n000 saque realizado com sucesso! 000")
            return True
        else:
            print("\n000 operação falhou! o valor informado é inválido. 000")
            return False
    def depositar (self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n000 depósito realizado com sucesso! 000")
        else:
            print("\n000 operação falhou! o valor informado é inválido. 000")
        return True
class ContaCorrente(Conta):
    def __init__(self,numero,cliente,limite=500,limite_saques=3):
        super().__init__(numero,cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    def sacar(self,valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == saque.__name__])
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques
        if excedeu_limite:
            print("\n000 operação falhou! o valor do saque excede o limite. 000")
        elif excedeu_saques:
            print("\n000 operção falhou! númmero máximo de saques excedido. 000")
        else:
            return super().sacar(valor)
        return False
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
class Historico:
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes (self):
        return self._transacoes
    def adicionar_transacao(self,transacao):
        self._transacoes.append({"tipo": transacao.__class__.__name__, 
                                 "valor": transacao.valor, 
                                 "data": datetime.now().strftime 
                                 ("%d-%m-%y   %H:%M:%S"),})
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass
class saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor (self):
        return self._valor
    def registrar (self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor (self):
        return self._valor
    def registrar (self, conta):
        sucesso_transacao = conta.depositar(self,valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
def menu():
    menu = """\n
    """"""""""""""""""" MENU """""""""""""
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair
    == """
    
    return input(textwrap.dedent(menu))
def filtrar_clientes(cpf,clientes):
    clientes_filtratos = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtratos[0] if clientes_filtratos else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    # FIXME: não permite cliente escolher a conta
    return cliente.conta[0]

def depositar(clientes):
    cpf = input("Informe o CPF do Cliente:")
    cliente = filtrar_clientes(cpf,clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    valor = float(input("Informe o valor do depósito:"))
    Transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, Transacao)
    
def sacar(clientes):
    cpf = input("Informe o CPF do cliente:")
    Cliente = filtrar_clientes(cpf, clientes)
    
    if not Cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = saque(valor)
    
    Conta = recuperar_conta_cliente(Cliente)
    if not Conta:
        return
    Cliente.realizar_transacao(Conta, transacao)
    
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    Cliente = filtrar_clientes(cpf, clientes)
    
    if not Cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    Conta = recuperar_conta_cliente(Cliente)
    if not Conta:
        return
    print("\n|||||||||||||||||| EXTRATO ||||||||||||||||||")
    transacoes = Conta.Historico.transacoes 
    
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizados movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\n\tR$ {transacao["valor"]:.2f}"
    print(extrato)
    print(f"\nSaildo:\n\tR$ {conta.saldo:.2f}")
    print("|||||||||||||||||||||||||||")
    
def criar_contas(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_clientes(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontado, fluxo de criação de conta encerrado! @@@")
        return
    
    Conta = contacorrente.nova_conta(Cliente=Cliente,numero=numero_conta)
    contas.append(Conta)
    
    print("\n@@@ Conta criada com sucesso! @@@")
    
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente numeros): ")
    
    if cliente:
        print("\n@@@ Já existe cliente com esse CPF: @@@")
        return
    nome = input("Informe o nome cpmpleto: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logadouro,nro-bairro-cidade/sigla estado): ")
    
    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)
    
    clientes.append(cliente)
    
    print("\n@@@ Cliente criado com Sucesso! @@@") 
      
         
        
    
    
    

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "d":
            depositar(clientes)
        
        elif opcao == "s":
            sacar(clientes)
            
        elif opcao == "e":
            exibir_extrato(clientes)
            
        elif opcao == "nu":
            criar_cliente(clientes)
            
        elif opcao == "nc":
            numero_conta = len(contas)
            criar_conta(numero_conta,clientes,contas)
            
        elif opcao == "lc":
            listar_contas(contas)
            
        elif opcao == "q":
            break

            
        
                                                                
    
        
            
        
                                
        
        