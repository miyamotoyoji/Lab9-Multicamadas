from datetime import datetime
from decimal import Decimal


class Transacao:
    def __init__(self, tipo: str, valor: Decimal, saldo_apos: Decimal):
        self.tipo = tipo
        self.valor = valor
        self.saldo_apos = saldo_apos
        self.data_hora = datetime.now()
