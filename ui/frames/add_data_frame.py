import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox
import pandas as pd
import os
import shutil
from core.config import DATA_DIR, SQL_MODEL_PATH, EXCEL_MODEL_PATH, CSV_MODEL_PATH, JSON_MODEL_PATH # Importar do config

class AddDataFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        self.DATA_DIR = DATA_DIR # Usar o DATA_DIR do config

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
        
        models = [
            ("Modelo .sql", SQL_MODEL_PATH),
            ("Modelo .xlsx", EXCEL_MODEL_PATH),
            ("Modelo .csv", CSV_MODEL_PATH),
            ("Modelo .json", JSON_MODEL_PATH)
        ]
        for text, path in models:
            model_link = ctk.CTkButton(models_frame, text=text, fg_color="transparent", text_color="#1E90FF", hover=False, command=lambda p=path: self.download_model(p))
            model_link.pack(side="left", padx=10)

    def download_model(self, model_path):
        if not os.path.exists(model_path):
            messagebox.showerror("Erro", f"Modelo não encontrado: {os.path.basename(model_path)}")
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=os.path.splitext(model_path)[1],
            initialfile=os.path.basename(model_path),
            title="Salvar Modelo Como"
        )
        if save_path:
            try:
                shutil.copy(model_path, save_path)
                messagebox.showinfo("Sucesso", f"Modelo salvo em: {save_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o modelo: {e}")

    def add_file(self):
        # ... (restante da função add_file, sem alterações na lógica de cópia e preview)
        file_path = filedialog.askopenfilename(
            title="Selecione um arquivo de dados",
            filetypes=(("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv"), ("SQL files", "*.sql"), ("JSON files", "*.json"), ("All files", "*.*"))
        )
        if not file_path: return
        filename = os.path.basename(file_path)
        destination_path = os.path.join(self.DATA_DIR, filename)

        try:
            shutil.copy(file_path, destination_path)
            messagebox.showinfo("Sucesso", f"Arquivo \'{filename}\' importado com sucesso!")
            print(f"Arquivo copiado para: {destination_path}")

            # --- Lógica de preview para CSV e Excel ---
            df = None
            if filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(destination_path)
            elif filename.endswith(".csv"):
                df = pd.read_csv(destination_path)
            # Adicionar tratamento para JSON se necessário
            elif filename.endswith(".json"):
                try:
                    df = pd.read_json(destination_path)
                except ValueError: # Se o JSON não for tabular
                    print("Conteúdo JSON (não tabular):\n")
                    with open(destination_path, 'r') as f:
                        print(f.read()[:500]) # Imprime os primeiros 500 caracteres

            if df is not None and not df.empty:
                print("Preview dos dados importados:")
                print(df.head())

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao importar o arquivo: {e}")