"""
Skrypt do tworzenia placeholder logo
"""

from PIL import Image, ImageDraw, ImageFont

# Utwórz obraz 400x400 pikseli
img = Image.new('RGB', (400, 400), color='#3498db')

# Dodaj kształty
draw = ImageDraw.Draw(img)

# Narysuj białe koło jako tło
draw.ellipse([50, 50, 350, 350], fill='white')

# Narysuj niebieskie koło wewnętrzne
draw.ellipse([75, 75, 325, 325], fill='#3498db')

# Dodaj tekst "C"
try:
    # Spróbuj użyć systemowej czcionki
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 180)
except:
    # Jeśli nie ma, użyj domyślnej
    font = ImageFont.load_default()

# Narysuj literę C
text = "C"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
position = ((400 - text_width) / 2, (400 - text_height) / 2 - 20)

draw.text(position, text, fill='white', font=font)

# Zapisz obraz
img.save('certyfikator/assets/logo.png')

print("Logo zostało utworzone: certyfikator/assets/logo.png")
