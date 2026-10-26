import tkinter as tk
from tkinter import messagebox

from negocio.conta_service import ContaService, RegraNegocioError


def formatar_reais(valor) -> str:
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def formatar_cpf(cpf: str) -> str:
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


class ContaView:
    """Camada de Apresentação: só lê a tela e mostra resultados.

    Toda regra fica na camada de negócios (ContaService).
    """

    def __init__(self, root: tk.Tk, service: ContaService):
        self.root = root
        self.service = service
        self.root.title("Banco - Multicamadas")
        self.root.resizable(False, False)

        cadastro = tk.LabelFrame(root, text="Criar Conta", padx=10, pady=10)
        cadastro.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(cadastro, text="Nome:").grid(row=0, column=0, sticky="w")
        self.entrada_nome = tk.Entry(cadastro, width=35)
        self.entrada_nome.grid(row=0, column=1, pady=2)
        tk.Label(cadastro, text="CPF:").grid(row=1, column=0, sticky="w")
        self.entrada_cpf = tk.Entry(cadastro, width=35)
        self.entrada_cpf.grid(row=1, column=1, pady=2)
        tk.Label(cadastro, text="Saldo Inicial (R$):").grid(row=2, column=0, sticky="w")
        self.entrada_saldo = tk.Entry(cadastro, width=35)
        self.entrada_saldo.grid(row=2, column=1, pady=2)
        self.botao_criar = tk.Button(cadastro, text="Criar Conta", command=self.criar_conta)
        self.botao_criar.grid(row=3, column=0, columnspan=2, pady=(8, 0))

        operacoes = tk.LabelFrame(root, text="Operações", padx=10, pady=10)
        operacoes.pack(fill="x", padx=10, pady=5)
        tk.Label(operacoes, text="CPF da conta:").grid(row=0, column=0, sticky="w")
        self.entrada_cpf_operacao = tk.Entry(operacoes, width=25)
        self.entrada_cpf_operacao.grid(row=0, column=1, columnspan=2, pady=2, sticky="w")
        tk.Label(operacoes, text="Valor (R$):").grid(row=1, column=0, sticky="w")
        self.entrada_valor = tk.Entry(operacoes, width=25)
        self.entrada_valor.grid(row=1, column=1, columnspan=2, pady=2, sticky="w")
        botoes = tk.Frame(operacoes)
        botoes.grid(row=2, column=0, columnspan=3, pady=(8, 0))
        self.botao_depositar = tk.Button(botoes, text="Depositar", width=10, command=self.depositar)
        self.botao_depositar.pack(side="left", padx=3)
        self.botao_sacar = tk.Button(botoes, text="Sacar", width=10, command=self.sacar)
        self.botao_sacar.pack(side="left", padx=3)
        self.botao_consultar = tk.Button(botoes, text="Ver Histórico", width=12, command=self.consultar)
        self.botao_consultar.pack(side="left", padx=3)

        dados = tk.LabelFrame(root, text="Dados da Conta", padx=10, pady=10)
        dados.pack(fill="both", padx=10, pady=(5, 10))
        self.texto_dados = tk.Text(dados, width=52, height=14, font=("Consolas", 10), state="disabled")
        self.texto_dados.pack(fill="both")

    # Ações dos botões: repassam os dados para a camada de negócios
    def criar_conta(self) -> None:
        try:
            conta = self.service.criar_conta(
                self.entrada_nome.get(), self.entrada_cpf.get(), self.entrada_saldo.get())
        except RegraNegocioError as erro:
            self.exibir_erro(str(erro))
            return
        for entrada in (self.entrada_nome, self.entrada_cpf, self.entrada_saldo):
            entrada.delete(0, tk.END)
        self.entrada_cpf_operacao.delete(0, tk.END)
        self.entrada_cpf_operacao.insert(0, conta.cliente.cpf)
        self.exibir_conta(conta)

    def depositar(self) -> None:
        self._operar(self.service.depositar)

    def sacar(self) -> None:
        self._operar(self.service.sacar)

    def consultar(self) -> None:
        try:
            conta = self.service.buscar_conta(self.entrada_cpf_operacao.get())
        except RegraNegocioError as erro:
            self.exibir_erro(str(erro))
            return
        self.exibir_conta(conta)

    def _operar(self, operacao) -> None:
        try:
            conta = operacao(self.entrada_cpf_operacao.get(), self.entrada_valor.get())
        except RegraNegocioError as erro:
            self.exibir_erro(str(erro))
            return
        self.entrada_valor.delete(0, tk.END)
        self.exibir_conta(conta)

    # Saídas
    def exibir_conta(self, conta) -> None:
        linhas = [
            f"Conta nº: {conta.numero}",
            f"Cliente:  {conta.cliente.nome}",
            f"CPF:      {formatar_cpf(conta.cliente.cpf)}",
            f"Saldo:    {formatar_reais(conta.saldo)}",
            "",
            "Histórico:",
        ]
        for t in conta.historico:
            linhas.append(f"{t.data_hora:%d/%m %H:%M}  {t.tipo:<9} {formatar_reais(t.valor):>14}"
                          f"  saldo {formatar_reais(t.saldo_apos)}")
        self.texto_dados.config(state="normal")
        self.texto_dados.delete("1.0", tk.END)
        self.texto_dados.insert("1.0", "\n".join(linhas))
        self.texto_dados.config(state="disabled")

    def exibir_erro(self, mensagem: str) -> None:
        messagebox.showerror("Erro", mensagem)
