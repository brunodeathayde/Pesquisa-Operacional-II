import numpy as np
import matplotlib
matplotlib.use("Agg")  # evita abrir janela externa
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, Entry, filedialog, Frame, Text, END
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ovrp_reading import ovrp_reading
from grasp_operators import (
    distance_matrix,
    construction_phase,
    cost_solution,
    plot_routes,   # mantém a função original
    reallocation,
    swap,
    two_opt_route
)

class OVRPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface OVRP - Tkinter")

        # Frame de parâmetros
        param_frame = Frame(root, bd=2, relief="groove")
        param_frame.pack(fill="x", padx=5, pady=5)
        Label(param_frame, text="Parâmetros do algoritmo", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=6)

        Label(param_frame, text="Alpha:").grid(row=1, column=0)
        self.alpha_input = Entry(param_frame, width=8)
        self.alpha_input.insert(0, "0.25")
        self.alpha_input.grid(row=1, column=1)

        Label(param_frame, text="Max Iter:").grid(row=1, column=2)
        self.max_iter_input = Entry(param_frame, width=8)
        self.max_iter_input.insert(0, "1000")
        self.max_iter_input.grid(row=1, column=3)

        self.open_btn = Button(param_frame, text="Abrir Instância", command=self.open_filechooser)
        self.open_btn.grid(row=1, column=4, padx=5)

        self.run_btn = Button(param_frame, text="Rodar Algoritmo", command=self.run_algorithm)
        self.run_btn.grid(row=1, column=5, padx=5)

        # Área inferior dividida em dois painéis
        bottom_frame = Frame(root)
        bottom_frame.pack(fill="both", expand=True)

        # Planilha da instância (esquerda)
        self.instance_frame = Frame(bottom_frame, bd=2, relief="groove")
        self.instance_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        Label(self.instance_frame, text="Instância (Depósito, Entrega, Clientes)", font=("Arial", 12, "bold")).pack()

        self.tree = ttk.Treeview(self.instance_frame, columns=("Tipo", "X", "Y", "Demanda"), show="headings", height=15)
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("X", text="X")
        self.tree.heading("Y", text="Y")
        self.tree.heading("Demanda", text="Demanda")

        # Ajuste da largura das colunas
        self.tree.column("Tipo", width=100, anchor="center")
        self.tree.column("X", width=60, anchor="center")
        self.tree.column("Y", width=60, anchor="center")
        self.tree.column("Demanda", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # Rotas (direita) com gráfico em cima e texto embaixo
        self.routes_frame = Frame(bottom_frame, bd=2, relief="groove")
        self.routes_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        Label(self.routes_frame, text="Rotas", font=("Arial", 12, "bold")).pack()

        # Área para gráfico (em cima)
        self.graph_frame = Frame(self.routes_frame)
        self.graph_frame.pack(fill="both", expand=True)

        # Área para texto das rotas (embaixo)
        self.routes_text = Text(self.routes_frame, height=10, wrap="word")
        self.routes_text.pack(fill="x", padx=5, pady=5)

        # Distância total abaixo das rotas
        self.distance_label = Label(self.routes_frame, text="Distância total: -", font=("Arial", 11))
        self.distance_label.pack(anchor="w", padx=5, pady=(0, 5))

        # Estado
        self.dist_matrix = None
        self.demands = None
        self.depot = None
        self.delivery = None
        self.clients = None

    def open_filechooser(self):
        filename = filedialog.askopenfilename(title="Selecione o arquivo", filetypes=[("Text files", "*.txt")])
        if filename:
            self.filename = filename
            depot, delivery, clients = ovrp_reading(self.filename)
            self.depot, self.delivery, self.clients = depot, delivery, clients
            self.demands = clients[:, 2]
            self.dist_matrix = distance_matrix(depot, delivery, clients)

            # Preencher planilha
            for row in self.tree.get_children():
                self.tree.delete(row)
            self.tree.insert("", "end", values=("Depósito", depot[0], depot[1], "-"))
            self.tree.insert("", "end", values=("Entrega", delivery[0], delivery[1], "-"))
            for i, c in enumerate(clients):
                self.tree.insert("", "end", values=(f"Cliente {i+1}", c[0], c[1], c[2]))

            # Limpa painel de rotas
            self.routes_text.delete("1.0", END)
            self.distance_label.config(text="Distância total: -")
            for widget in self.graph_frame.winfo_children():
                widget.destroy()

    def run_algorithm(self):
        if self.dist_matrix is None:
            self.routes_text.delete("1.0", END)
            self.routes_text.insert(END, "Abra uma instância primeiro.\n")
            return

        alpha = float(self.alpha_input.get())
        max_iter = int(self.max_iter_input.get())
        capacidade = 20

        best_solution_found = float("inf")
        best_routes_found = None
        best = []

        for iteration in range(1, max_iter + 1):
            routes = construction_phase(alpha, capacidade, self.dist_matrix, self.demands)
            solution = cost_solution(routes, self.dist_matrix)

            # Reallocation
            new_routes = reallocation(routes, capacidade, self.demands, self.dist_matrix)
            new_solution = cost_solution(new_routes, self.dist_matrix)
            if new_solution < solution:
                solution, routes = new_solution, new_routes

            # Swap
            new_routes = swap(routes, capacidade, self.demands, self.dist_matrix)
            new_solution = cost_solution(new_routes, self.dist_matrix)
            if new_solution < solution:
                solution, routes = new_solution, new_routes

            # 2-opt
            new_routes = [two_opt_route(r, self.dist_matrix) for r in routes]
            new_solution = cost_solution(new_routes, self.dist_matrix)
            if new_solution < solution:
                solution, routes = new_solution, new_routes

            if solution < best_solution_found:
                best_solution_found = solution
                best_routes_found = routes

            best.append(best_solution_found)

        # Desenha gráfico usando a função original
        plot_routes(best_routes_found, self.depot, self.delivery, self.clients)

        # Captura a figura atual e embute no dashboard
        fig = plt.gcf()
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Lista rotas em texto
        self.routes_text.delete("1.0", END)
        for i, route in enumerate(best_routes_found, start=1):
            # Exclui índices de depósito (0) e entrega (len(clients)+1) na listagem textual
            clientes = [f"Cliente {c}" for c in route if c not in [0, len(self.clients) + 1]]
            self.routes_text.insert(END, f"Rota {i}: {', '.join(clientes)}\n")

        # Atualiza distância total
        self.distance_label.config(text=f"Distância total: {best_solution_found:.2f}")

if __name__ == "__main__":
    root = Tk()
    app = OVRPApp(root)
    root.mainloop()
