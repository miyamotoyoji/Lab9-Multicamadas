from decimal import Decimal

from entidades.cliente import Cliente
from entidades.transacao import Transacao


class Conta:
    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: Decimal):
        self.numero = numero
        self.cliente = cliente
        self._saldo = saldo_inicial
        self._historico: list[Transacao] = [Transacao("Abertura", saldo_inicial, saldo_inicial)]

    @property
    def saldo(self) -> Decimal:
        return self._saldo

    @property
    def historico(self) -> list[Transacao]:
        return list(self._historico)

    def depositar(self, valor: Decimal) -> None:
        self._saldo += valor
        self._historico.append(Transacao("Depósito", valor, self._saldo))

    def sacar(self, valor: Decimal) -> None:
        self._saldo -= valor
        self._historico.append(Transacao("Saque", valor, self._saldo))
