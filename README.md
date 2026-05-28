# Gerador de EAN ISBN by Jair Lima

Ferramenta Windows para gerar códigos de barras EAN-13 no padrão ISBN, com interface gráfica e CLI global.

## Funcionalidades

- Geração de código EAN-13 a partir de ISBN (978/979) com validação do dígito verificador
- Processamento em lote via arquivo `.txt`
- Exportação em PNG, JPG ou BMP com DPI configurável (300 / 600 / 1200)
- Cópia direta da imagem para a área de transferência do Windows
- Duas interfaces independentes: GUI desktop e CLI instalável no PATH

## Stack

| Componente | Tecnologia |
|---|---|
| Linguagem | Python 3 |
| Geração EAN | `python-barcode` |
| Imagem | `Pillow` |
| Clipboard | `pywin32` |
| Build | `PyInstaller` |

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

**CLI:**
```bash
gerador-isbn 978-65-266-7102-3
gerador-isbn 978-65-266-7102-3 -c          # copia para clipboard
gerador-isbn lista.txt --formato png --dpi 600
```

**GUI:**
```bash
python gui.py
```

## Build dos executáveis

```bash
# GUI standalone
pyinstaller --onefile --windowed gui.py --name "Gerador de EAN ISBN by Jair Lima"

# CLI global
pyinstaller --onefile cli.py --name "gerador-isbn"
```

Os executáveis ficam em `dist/` e podem ser copiados para `~/bin`.

## Autor

**Jair Lima** — [github.com/jairslima](https://github.com/jairslima)