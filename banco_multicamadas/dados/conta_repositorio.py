from entidades.conta import Conta


class ContaRepositorio:
    """Camada de Dados: guarda as contas em uma lista na memória."""

    def __init__(self):
        self._contas: list[Conta] = []

    def proximo_numero(self) -> int:
        return len(self._contas) + 1

    def salvar(self, conta: Conta) -> None:
        if conta not in self._contas:
            self._contas.append(conta)

    def buscar_por_numero(self, numero: int) -> Conta | None:
        for conta in self._contas:
            if conta.numero == numero:
                return conta
        return None

    def buscar_por_cpf(self, cpf: str) -> Conta | None:
        for conta in self._contas:
            if conta.cliente.cpf == cpf:
                return conta
        return None

    def listar(self) -> list[Conta]:
        return list(self._contas)
