import os
import re
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
import io

def clean_isbn(isbn_str):
    """Remove tudo que não for dígito."""
    return re.sub(r'\D', '', isbn_str)

def validate_ean13_checksum(digits):
    """Valida o dígito verificador do EAN-13."""
    if len(digits) != 13:
        return False
    
    checksum = 0
    for i in range(12):
        multiplier = 1 if i % 2 == 0 else 3
        checksum += int(digits[i]) * multiplier
    
    remainder = checksum % 10
    check_digit = 10 - remainder if remainder != 0 else 0
    
    return check_digit == int(digits[12])

def copy_image_to_clipboard_windows(image_path):
    """Copia a imagem gerada para a área de transferência no Windows."""
    import win32clipboard
    from io import BytesIO
    
    image = Image.open(image_path)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]  # Header BMP tem 14 bytes
    output.close()
    
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def generate_ean_barcode(isbn_input, output_filename=None, dpi=300, fmt="png"):
    """
    Gera o código de barras EAN-13 para o ISBN fornecido com suporte a DPI e formato.
    """
    digits = clean_isbn(isbn_input)
    if len(digits) != 13:
        raise ValueError(f"O ISBN deve conter exatamente 13 dígitos. Encontrado: {len(digits)}")
    
    if not validate_ean13_checksum(digits):
        raise ValueError("O ISBN fornecido é inválido (falha no dígito verificador matemático do EAN-13).")
        
    if not output_filename:
        output_filename = isbn_input.replace(' ', '_')
        
    fmt = fmt.lower()
    if fmt not in ["png", "jpg", "jpeg", "bmp"]:
        fmt = "png"
        
    if output_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        final_path = output_filename
    else:
        final_path = f"{output_filename}.{fmt}"

    ean = barcode.get('ean13', digits, writer=ImageWriter())
    
    scale = dpi / 300.0 if dpi else 1.0
    
    writer_options = {
        'module_height': 15.0 * scale,
        'module_width': 0.3 * scale,
        'font_size': int(10 * scale),
        'text_distance': 5.0 * scale,
        'quiet_zone': 6.5 * scale,
        'dpi': dpi
    }
    
    temp_filename = f"temp_{digits}"
    ean.save(temp_filename, options=writer_options)
    temp_path = temp_filename + ".png"
    
    try:
        img = Image.open(temp_path)
        width, height = img.size
        
        top_margin = int(40 * scale)
        new_height = height + top_margin
        
        new_img = Image.new("RGB", (width, new_height), "white")
        new_img.paste(img, (0, top_margin))
        
        draw = ImageDraw.Draw(new_img)
        
        try:
            font = ImageFont.truetype("arial.ttf", int(20 * scale))
        except IOError:
            font = ImageFont.load_default()
            
        text = f"ISBN {isbn_input}"
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) / 2
        y = (top_margin - text_height) / 2 - (2 * scale)
        
        draw.text((x, y), text, fill="black", font=font)
        
        save_fmt = "JPEG" if fmt in ["jpg", "jpeg"] else fmt.upper()
        new_img.save(final_path, format=save_fmt, dpi=(dpi, dpi))
        
        return final_path
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    print(f"Testando com ISBN: 978-65-266-7102-3")
    print("Salvo em:", generate_ean_barcode("978-65-266-7102-3"))
