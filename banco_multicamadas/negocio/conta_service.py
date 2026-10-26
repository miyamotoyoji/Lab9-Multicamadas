from decimal import Decimal, InvalidOperation

from dados.conta_repositorio import ContaRepositorio
from entidades.cliente import Cliente
from entidades.conta import Conta


class RegraNegocioError(Exception):
    """Erro lançado quando uma operação viola uma regra do banco."""


class ContaService:
    """Camada de Negócios: protege as regras do banco.

    A apresentação nunca altera uma Conta diretamente; ela sempre passa por aqui.
    """

    def __init__(self, repositorio: ContaRepositorio):
        self.repositorio = repositorio

    def criar_conta(self, nome: str, cpf: str, saldo_inicial: str) -> Conta:
        nome = nome.strip()
        cpf = self._somente_digitos(cpf)

        if not nome:
            raise RegraNegocioError("Informe o nome do cliente.")
        if len(cpf) != 11:
            raise RegraNegocioError("O CPF deve ter 11 dígitos.")
        if self.repositorio.buscar_por_cpf(cpf):
            raise RegraNegocioError("Já existe uma conta para este CPF.")
        saldo = self._converter_valor(saldo_inicial or "0")
        if saldo < 0:
            raise RegraNegocioError("O saldo inicial não pode ser negativo.")

        conta = Conta(self.repositorio.proximo_numero(), Cliente(nome, cpf), saldo)
        self.repositorio.salvar(conta)
        return conta

    def buscar_conta(self, cpf: str) -> Conta:
        conta = self.repositorio.buscar_por_cpf(self._somente_digitos(cpf))
        if conta is None:
            raise RegraNegocioError("Nenhuma conta encontrada para este CPF.")
        return conta

    def depositar(self, cpf: str, valor: str) -> Conta:
        conta = self.buscar_conta(cpf)
        quantia = self._valor_positivo(valor)
        conta.depositar(quantia)
        self.repositorio.salvar(conta)
        return conta

    def sacar(self, cpf: str, valor: str) -> Conta:
        conta = self.buscar_conta(cpf)
        quantia = self._valor_positivo(valor)
        if quantia > conta.saldo:
            raise RegraNegocioError("Saldo insuficiente para este saque.")
        conta.sacar(quantia)
        self.repositorio.salvar(conta)
        return conta

    def _valor_positivo(self, valor: str) -> Decimal:
        quantia = self._converter_valor(valor)
        if quantia <= 0:
            raise RegraNegocioError("O valor deve ser maior que zero.")
        return quantia

    @staticmethod
    def _converter_valor(valor: str) -> Decimal:
        try:
            quantia = Decimal(valor.strip().replace(",", "."))
        except InvalidOperation:
            raise RegraNegocioError("Valor inválido.")
        if not quantia.is_finite():
            raise RegraNegocioError("Valor inválido.")
        return quantia.quantize(Decimal("0.01"))

    @staticmethod
    def _somente_digitos(texto: str) -> str:
        return "".join(c for c in texto if c.isdigit())
