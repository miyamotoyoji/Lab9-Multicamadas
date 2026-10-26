import tkinter as tk

from apresentacao.conta_view import ContaView
from dados.conta_repositorio import ContaRepositorio
from negocio.conta_service import ContaService


def main():
    # Monta as camadas de baixo para cima: Dados -> Negócios -> Apresentação
    repositorio = ContaRepositorio()
    service = ContaService(repositorio)

    root = tk.Tk()
    ContaView(root, service)
    root.mainloop()


if __name__ == "__main__":
    main()
