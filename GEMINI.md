# Gerador de EAN ISBN by Jair Lima

Este repositório contém a versão final e completa do gerador de códigos de barras EAN-13 (ISBN), desenvolvido por Jair Lima.
O projeto inclui interfaces Gráfica (GUI) e de Linha de Comando (CLI).

## Estrutura Técnica
- **generator.py**: Motor principal. Implementa validação matemática do EAN-13, manipulação da biblioteca `python-barcode` para barras e da `Pillow` para ajuste de layout (DPI e texto), além de chamadas da API do Windows (`pywin32`) para copiar a imagem para o clipboard.
- **cli.py**: Gerenciador do terminal (`argparse`). Suporta batch processing (`-b`), formato (`-f`), DPI (`-d`) e clipboard (`-c`).
- **gui.py**: Interface em `tkinter` contendo opções visuais (Combobox) para formato, DPI e botões para ações unificadas (gerar e copiar, geração em lote).

## Compilação e Deploy
O projeto possui rotinas de build via PyInstaller:
1. `Gerador de EAN ISBN by Jair Lima.exe` (GUI): Fica na pasta `dist` do repositório.
2. `gerador-isbn.exe` (CLI): Instalado globalmente em `C:\Users\jairs\bin\`.

## Tratamento de Dados
A biblioteca de barras utilizada necessita de ajustes via Pillow para emular fielmente o layout de livros, por isso a criação de margem superior com o texto "ISBN ...". Todos os arquivos temporários são deletados após processamento, e o projeto é agnóstico a barras, espaços ou hífens na entrada.
