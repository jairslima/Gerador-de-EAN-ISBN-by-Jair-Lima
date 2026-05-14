import argparse
import sys
import os
from generator import generate_ean_barcode, copy_image_to_clipboard_windows

def process_single(isbn, output, dpi, fmt, copy_clipboard):
    print(f"Gerando código de barras para o ISBN: {isbn}...")
    try:
        path = generate_ean_barcode(isbn, output, dpi, fmt)
        print(f"Sucesso! Imagem salva em: {path}")
        if copy_clipboard:
            try:
                copy_image_to_clipboard_windows(path)
                print("Imagem copiada para a área de transferência!")
            except Exception as e:
                print(f"Aviso: Não foi possível copiar para a área de transferência: {e}")
    except Exception as e:
        print(f"Erro: {e}")

def process_batch(batch_file, output_dir, dpi, fmt):
    if not os.path.exists(batch_file):
        print(f"Erro: Arquivo '{batch_file}' não encontrado.")
        sys.exit(1)
        
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(batch_file, 'r', encoding='utf-8') as f:
        isbns = [line.strip() for line in f if line.strip()]
        
    print(f"Processando {len(isbns)} ISBN(s) em lote...")
    success_count = 0
    
    for isbn in isbns:
        try:
            out_path = None
            if output_dir:
                # Basic filename from ISBN
                base_name = isbn.replace(' ', '_').replace('-', '')
                out_path = os.path.join(output_dir, base_name)
                
            generate_ean_barcode(isbn, out_path, dpi, fmt)
            success_count += 1
        except Exception as e:
            print(f"Erro ao processar '{isbn}': {e}")
            
    print(f"Lote concluído! {success_count}/{len(isbns)} gerados com sucesso.")

def main():
    parser = argparse.ArgumentParser(description="Gera códigos de barras EAN-13 em imagens a partir de ISBN(s).")
    parser.add_argument("isbn", nargs='?', help="O número do ISBN (ex: 978-65-266-7102-3). Omitir se usar --batch.")
    parser.add_argument("-o", "--output", help="Nome do arquivo de saída (ou diretório de saída se usar --batch).", default=None)
    parser.add_argument("-b", "--batch", help="Arquivo de texto com vários ISBNs (um por linha) para processamento em lote.", default=None)
    parser.add_argument("-d", "--dpi", type=int, help="Resolução da imagem em DPI (padrão: 300).", default=300)
    parser.add_argument("-f", "--fmt", choices=['png', 'jpg', 'jpeg', 'bmp'], help="Formato da imagem (padrão: png).", default='png')
    parser.add_argument("-c", "--clipboard", action="store_true", help="Copia a imagem resultante para a área de transferência (apenas para ISBN único).")
    
    args = parser.parse_args()
    
    if args.batch:
        process_batch(args.batch, args.output, args.dpi, args.fmt)
    elif args.isbn:
        process_single(args.isbn, args.output, args.dpi, args.fmt, args.clipboard)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
