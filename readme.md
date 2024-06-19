SISTEMA BANCÁRIO UTILIZANDO POO EM PYTHON

Principai conceitos do codigo

1. Heranca: 'PessoaFisica' herda de 'Cliente' e 'ContaCorrente' herda de 'Conta'.

2. Encapsulamento: Uso de propriedades (@property) para acessar atributos privados(_saldo, _numero).

3. Polimorfismo: Metodos como 'sacar' sao redefinidos em subclasses (ContaCorrente).

4. Abstração: Uso de classes abstratas (Transacao) para definir interfaces que outras classes devem implementar (Saque, Deposito).

5. Compisição: Classes contem outras classes como atributos ('Conta' tem um 'Historico').

6. List Comprehensions: Utilização para filtrar dados, como em 'filtrar_cliente'.

7. Interação com o usuário: Uso de funções para receber input do usuário e realizar operações com esses dados.

