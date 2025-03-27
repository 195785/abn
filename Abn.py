import textwrap

AGENCIA = "0001"
LIMITE_SAQUE = 3

def depositar(saldo,valor,extrato):
    if valor > 0:
        saldo += valor
        extrato.append (f"DEPÓSITO: +R${valor:.2f}")
        print("\nDEPÓSITO REALIZADO COM SUCESSO!")
    else:
        print("\nVALOR INVÁLIDO PARA DEPÓSITO.")
    return saldo,extrato

def sacar (saldo,valor,extrato,limite,numero_saques):
    if valor > saldo:
        print("\nSALDO INSUFICIENTE.")
    elif   valor > limite:
        print("\nO VALOR DO SAQUE EXCEDE O LIMITE PERMITIDO") 
    elif numero_saques >= LIMITE_SAQUE:
        print("\nNÚMERO MÁXIMO DE SAQUES EXCEDIDO")
    elif valor > 0:
        saldo -= valor
        extrato.append (f"SAQUE: -=R${valor:.2f}")
        numero_saques += 1
        print("\nSAQUE REALIZADO COM SUCESSO!")
    else:
        print("\nVALOR INVALIDO PARA SAQUE.")
    return saldo,extrato,numero_saques

def exibir_extrato(saldo,extrato):
    print("\n" + "="*30)
    print("EXTRATO" .center(30))
    print("="*30)
    if extrato:
        for movimento in extrato:
            print(movimento)
    else:
        print("NÃO HÁ MOVIMENTAÇÕES")
    print("="*30)
    print(f"SALDO ATUAL: R$ {saldo:.2f}")
    
def criar_usuario(usuarios):
    cpf = input("INFORME O CPF (APENAS NÚMEROS):")
    if filtar_usuario(cpf,usuarios):
        print("\nERRO: CPF JÁ CADASTRADO.")
        return
    nome = input("NOME COMPLETO")
    data_nascimento = input("DATA DE NASCIMENTO (dd/mm/aaaa): ")
    endereco = input("ENDEREÇO (LOGRADOURO,NÚMERO - BAIRRO - CIDADE/ SIGLA ESTADO):")
    usuarios.append({"NOME":nome, "CPF":cpf,"DATA_NASCIMENTO":data_nascimento,"ENDEREÇO":endereco})
    print("\nUSUARIO CRIADO COM SUCESSO!")
    
def filtar_usuario(cpf,usuarios):
    for usuario in usuarios:
        if usuario["CPF"] == cpf:
            return usuario
    return None

def criar_conta(agencia,numero_conta,usuarios,contas):
    cpf = input("INFORME O CPF DO USUÁRIO:")
    usuario = filtar_usuario(cpf,usuarios)
    if usuario:
        contas.append({"AGENCIA": agencia,"NUMERO_CONTA": numero_conta,"USUARIO": usuario})
        print("\nCONTA CRIADA COM SUCESSO!")
    else:
        print("\nUSUÁRIO NÃO ENCONTRADO. CADASTRE O USUARIO PRIMEIRO.")
        
def listrar_contas(contas):
    print("\n==========LISTA DE CONTAS ==========")
    for conta in contas:
        print(f"AGENCIA: {conta["AGENCIA"]} | CONTA:{conta["NUMERO_CONTA"]} | TITULAR:{conta["USUARIO"]["NOME"]}")
print("===========================================================================")

def main():
    saldo = 0
    limite = 500
    extrato = []
    numero_saque = 0
    usuarios = []
    contas = []
    numero_conta = 1
    
    while True:
        print(textwrap.dedent("""\n==========MENU===========
                                 [1] DEPOSITAR
                                 [2] SACAR
                                 [3] EXTRATO
                                 [4] NOVO USUÁRIO
                                 [5] NOVA CONTA
                                 [6] LISTAR CONTAS
                                 [7] SAIR  
                                 """))
        opcao = input("ESCOLHA UMA OPÇÃO:")
        if opcao == "1":
            valor = float(input("INFORME O VALOR DO DEPOSITO: R$"))
            saldo,extrato = depositar(saldo,valor,extrato)
        elif opcao == "2":
            valor = float(input("INFORME O VALOR DO SAQUE: R$"))
            saldo,extrato,numero_saque = sacar(saldo,valor,extrato,limite,numero_saque)
        elif opcao == "3":
            exibir_extrato(saldo,extrato)
        elif opcao == "4":
            criar_usuario(usuarios)
        elif opcao == "5":
            criar_conta(AGENCIA,numero_conta,usuarios,contas)
            numero_conta += 1
        elif opcao == "6":
            listrar_contas(contas)
        elif opcao == "7":
            print("SAINDO... OBRIGADO POR USAR O ABN ")
            break
        else:
            print("\nOPÇÃO INVÁLIDA. TENTE NOVAMENTE.")
if __name__ == "__main__":
    main()
    
            
        
    
        
 