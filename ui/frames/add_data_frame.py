import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox
import pandas as pd
import os
import shutil

class AddDataFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=20, padx=20, anchor="w")
        ctk.CTkLabel(title_frame, text="Adicionar dados", font=("Poppins", 24, "bold")).pack(side="left")

        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=100, pady=20)

        info_text = (
            "Adicione os seus dados no nosso sistema.\n\n"
            "Os formatos aceitos são: .sql, .xlsx, .xls, .csv e .json.\n\n"
            "Se preferir, disponibilizamos modelos referentes a cada formato!"
        )

        info_label = ctk.CTkLabel(body_frame, text=info_text, font=("Poppins", 16), justify="center")
        info_label.pack(pady=20)

        add_button = ctk.CTkButton(body_frame, text="Adicionar", width=200, height=40, command=self.add_file)
        add_button.pack(pady=30)
        
        models_frame = ctk.CTkFrame(body_frame, fg_color="transparent")
        models_frame.pack(pady=20)
        
        models = ["Modelo .sql", "Modelo .xlsx", "Modelo .xls", "Modelo .csv", "Modelo .json"]
        for model in models:
            model_link = ctk.CTkButton(models_frame, text=model, fg_color="transparent", text_color="#1E90FF", hover=False, command=lambda m=model: self.download_model(m))
            model_link.pack(side="left", padx=10)

    def add_file(self):
        """
        Abre uma janela de diálogo para o usuário selecionar um arquivo
        e o copia para a pasta 'data' do projeto.
        """
        file_path = filedialog.askopenfilename(
            title="Selecione um arquivo de dados",
            filetypes=(("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv"), ("All files", "*.*"))
        )

        if not file_path:
            return

        filename = os.path.basename(file_path)
        destination_path = os.path.join(self.DATA_DIR, filename)

        try:
            shutil.copy(file_path, destination_path)
            messagebox.showinfo("Sucesso", f"Arquivo '{filename}' importado com sucesso!")
            print(f"Arquivo copiado para: {destination_path}")

            if filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(destination_path)
                print("Preview dos dados importados:")
                print(df.head())

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao importar o arquivo: {e}")

    def download_model(self, model_name):
        """Placeholder para a funcionalidade de baixar modelos."""
        print(f"Funcionalidade de baixar o '{model_name}' a ser implementada.")
        messagebox.showinfo("Em desenvolvimento", "Esta funcionalidade ainda está em construção.")