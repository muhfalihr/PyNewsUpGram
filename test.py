from PIL import Image, ImageDraw, ImageFont

# Buka gambar
image = Image.open('gambar.jpeg')

# Buat objek ImageDraw untuk menggambar di atas gambar
draw = ImageDraw.Draw(image)

# Tambahkan teks
font = ImageFont.load_default()
draw.text((10, 10), "Contoh Teks", fill="white", font=font)

# Simpan gambar yang sudah di edit
image.save('gambar_edit.jpg')

# Tampilkan gambar
image.show()
