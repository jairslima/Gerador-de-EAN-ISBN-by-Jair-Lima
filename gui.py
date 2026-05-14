import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
from generator import generate_ean_barcode, copy_image_to_clipboard_windows

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de EAN ISBN")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # ISBN Input
        tk.Label(self.frame, text="Digite o ISBN (ex: 978-65-266-7102-3):").grid(row=0, column=0, columnspan=2, sticky="w")
        self.entry_isbn = tk.Entry(self.frame, width=30, font=("Arial", 12))
        self.entry_isbn.grid(row=1, column=0, columnspan=2, pady=(5, 15), sticky="we")
        
        # Configs
        tk.Label(self.frame, text="DPI:").grid(row=2, column=0, sticky="e", padx=(0, 5))
        self.combo_dpi = ttk.Combobox(self.frame, values=["300", "600", "1200"], width=8, state="readonly")
        self.combo_dpi.current(0)
        self.combo_dpi.grid(row=2, column=1, sticky="w")
        
        tk.Label(self.frame, text="Formato:").grid(row=3, column=0, sticky="e", padx=(0, 5), pady=(5, 15))
        self.combo_fmt = ttk.Combobox(self.frame, values=["PNG", "JPG", "BMP"], width=8, state="readonly")
        self.combo_fmt.current(0)
        self.combo_fmt.grid(row=3, column=1, sticky="w", pady=(5, 15))
        
        # Buttons Frame
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.grid(row=4, column=0, columnspan=2, sticky="we")
        
        self.btn_gerar = tk.Button(self.btn_frame, text="Gerar Imagem", command=self.gerar_unico, bg="#4CAF50", fg="white", font=("Arial", 9, "bold"))
        self.btn_gerar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        self.btn_clipboard = tk.Button(self.btn_frame, text="Gerar e Copiar", command=self.gerar_clipboard, bg="#2196F3", fg="white", font=("Arial", 9, "bold"))
        self.btn_clipboard.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        self.btn_batch = tk.Button(self.btn_frame, text="Lote (TXT)", command=self.gerar_lote, bg="#FF9800", fg="white", font=("Arial", 9, "bold"))
        self.btn_batch.pack(side=tk.LEFT, expand=True, fill=tk.X)

    def get_configs(self):
        return int(self.combo_dpi.get()), self.combo_fmt.get().lower()

    def gerar_unico(self):
        isbn = self.entry_isbn.get().strip()
        if not isbn:
            messagebox.showwarning("Aviso", "Por favor, insira o ISBN.")
            return
            
        dpi, fmt = self.get_configs()
        
        try:
            default_name = isbn.replace(' ', '_') + f".{fmt}"
            filepath = filedialog.asksaveasfilename(
                defaultextension=f".{fmt}",
                initialfile=default_name,
                title="Salvar Código de Barras",
                filetypes=[(f"{fmt.upper()} files", f"*.{fmt}"), ("All files", "*.*")]
            )
            
            if filepath:
                generate_ean_barcode(isbn, filepath, dpi, fmt)
                messagebox.showinfo("Sucesso", f"Código de barras salvo com sucesso em:\n{filepath}")
        except ValueError as ve:
            messagebox.showerror("Erro de Validação", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o código:\n{e}")

    def gerar_clipboard(self):
        isbn = self.entry_isbn.get().strip()
        if not isbn:
            messagebox.showwarning("Aviso", "Por favor, insira o ISBN.")
            return
            
        dpi, fmt = self.get_configs()
        
        try:
            temp_path = generate_ean_barcode(isbn, "temp_clipboard", dpi, fmt)
            copy_image_to_clipboard_windows(temp_path)
            os.remove(temp_path)
            messagebox.showinfo("Sucesso", "Código de barras copiado para a área de transferência!")
        except ValueError as ve:
            messagebox.showerror("Erro de Validação", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar/copiar:\n{e}")

    def gerar_lote(self):
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo TXT com ISBNs",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
            
        output_dir = filedialog.askdirectory(title="Selecione a pasta para salvar as imagens")
        if not output_dir:
            return
            
        dpi, fmt = self.get_configs()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                isbns = [line.strip() for line in f if line.strip()]
                
            if not isbns:
                messagebox.showinfo("Aviso", "O arquivo está vazio.")
                return
                
            sucessos = 0
            for isbn in isbns:
                try:
                    base_name = isbn.replace(' ', '_').replace('-', '')
                    out_path = os.path.join(output_dir, f"{base_name}.{fmt}")
                    generate_ean_barcode(isbn, out_path, dpi, fmt)
                    sucessos += 1
                except Exception:
                    pass # Skip invalid ones in batch
                    
            messagebox.showinfo("Lote Concluído", f"{sucessos} de {len(isbns)} códigos de barras foram gerados com sucesso na pasta:\n{output_dir}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao processar o lote:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
