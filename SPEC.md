# Projeto: Gerador de EAN ISBN by Jair Lima

## Objetivo
Ferramenta ágil (CLI global e GUI desktop) para gerar códigos de barras EAN-13 no padrão ISBN, com suporte a processamento em lote, validação matemática, configurações de exportação e integração com a área de transferência do Windows.

## Escopo e Funcionalidades
- **Validação Matemática**: Cálculo e verificação do dígito verificador EAN-13.
- **Processamento Individual e Lote**: Geração a partir de um ISBN único ou leitura de arquivos `.txt`.
- **Exportação Customizável**: Suporte a formatos (PNG, JPG, BMP) e resolução (300, 600, 1200 DPI).
- **Integração Clipboard**: Cópia direta da imagem gerada para a área de transferência (Windows).
- **Duas Interfaces**:
  - *GUI*: Interface Tkinter empacotada como executável standalone (`Gerador de EAN ISBN by Jair Lima.exe`).
  - *CLI*: Ferramenta de terminal global (`gerador-isbn.exe`), instalada no PATH do usuário.

## Arquitetura e Decisões
- **Linguagem**: Python.
- **Bibliotecas**: `python-barcode` (geração EAN), `Pillow` (renderização e margens), `pywin32` (clipboard no Windows), `pyinstaller` (build de executáveis).
- **Core (`generator.py`)**: Centraliza as regras de negócio, validação e manipulação de imagem.
- **Módulos**: A separação entre `cli.py` e `gui.py` permite a compilação independente de cada interface.

## Pendências
- Nenhuma. O projeto atingiu maturidade funcional e está estabilizado.

## Critérios de Aceite Atendidos
- Margens, posicionamento e legibilidade do código ISBN conforme padrão editorial.
- Identificação de erros (ex: número faltando ou dígito verificador incorreto).
- Executáveis isolados funcionais sem necessidade de ambiente Python local.

## Instruções Operacionais
- O executável CLI está em `C:\Users\jairs\bin\gerador-isbn.exe`. Uso: `gerador-isbn 978-65-266-7102-3 -c`
- O executável GUI é interativo e deve ser utilizado quando for necessário processamento visual.
