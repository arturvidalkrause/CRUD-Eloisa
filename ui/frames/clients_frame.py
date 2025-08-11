import customtkinter as ctk
from tkinter import ttk, messagebox
from core.crud_operations import get_all_clients, delete_clients_by_cpf

class ClientsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(top_frame, text="Clientes", font=("Poppins", 24, "bold")).pack(side="left")
        
        ctk.CTkButton(top_frame, text="Filtro").pack(side="right")

        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.create_table(table_frame)
        self.load_data_into_table()

        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=10)

        delete_button = ctk.CTkButton(bottom_frame, text="Deletar clientes", command=self.delete_selected_clients)
        delete_button.pack(side="left")

    def create_table(self, parent_frame):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Poppins", 12, "bold"), background="#555555", foreground="white", padding=10)
        style.configure("Treeview", rowheight=30, font=("Poppins", 11), background="white", foreground="black")
        style.map("Treeview", background=[('selected', '#c40000')])
        
        columns = ("Nome", "Sobrenome", "CPF", "Email")
        
        self.table = ttk.Treeview(parent_frame, columns=columns, show="headings", style="Treeview", selectmode="extended")

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=150, anchor="w")

        self.table.pack(fill="both", expand=True)

    def load_data_into_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

        clients_df = get_all_clients()

        if not clients_df.empty:
            for index, row in clients_df.iterrows():
                self.table.insert("", "end", values=(
                    row.get("Nome", ""),
                    row.get("Sobrenome", ""),
                    row.get("CPF", ""),
                    row.get("Email", "")
                ))
    
    def delete_selected_clients(self):
        """
        Pega os itens selecionados, pede confirmação e chama a função de exclusão.
        """
        selected_items = self.table.selection()
        if not selected_items:
            messagebox.showinfo("Nenhuma seleção", "Por favor, selecione um ou mais clientes para deletar.")
            return

        cpfs_to_delete = [self.table.item(item, "values")[2] for item in selected_items]

        confirm = messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Você tem certeza que deseja deletar {len(cpfs_to_delete)} cliente(s)?\nEsta ação não pode ser desfeita."
        )

        if confirm:
            result = delete_clients_by_cpf(cpfs_to_delete)
            if result["status"] == "sucesso":
                messagebox.showinfo("Sucesso", result["mensagem"])
            else:
                messagebox.showerror("Erro", result["mensagem"])
            
            self.load_data_into_table()