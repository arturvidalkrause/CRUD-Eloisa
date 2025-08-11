import customtkinter as ctk

class FilterImovelFrame(ctk.CTkFrame):
    def __init__(self, master, controller, app):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        ctk.CTkLabel(self, text="Detalhamento Geo Imóvel | Filtro", font=("Poppins", 24, "bold")).pack(pady=20, anchor="w")
        self.entry_endereco = self.create_entry("Filtrar por Endereço...")
        self.entry_cep = self.create_entry("Filtrar por CEP...")
        self.entry_zona = self.create_entry("Filtrar por Zona...")
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")
        ctk.CTkButton(button_frame, text="Aplicar", command=self.apply_filter).pack(side="left", padx=(0, 10))
        ctk.CTkButton(button_frame, text="Cancelar", command=self.cancel, fg_color="gray").pack(side="left")

    def create_entry(self, placeholder):
        entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=400, height=35)
        entry.pack(pady=8, anchor="w")
        return entry

    def apply_filter(self):
        filters = {
            "Endereço": self.entry_endereco.get(),
            "CEP": self.entry_cep.get(),
            "Zona": self.entry_zona.get()
        }
        self.controller.apply_table_filter(filters)

    def cancel(self):
        self.controller.show_table_view()