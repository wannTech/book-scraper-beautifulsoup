import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://books.toscrape.com/catalogue/"
url = "https://books.toscrape.com/catalogue/page-1.html"

rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
books = []

while url:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.find_all("article", class_="product_pod"):
        judul = book.find("h3").find("a")["title"]
        harga = book.find("p", class_="price_color").text.encode('latin-1').decode('utf-8')
        rating_text = book.find("p", class_="star-rating")["class"][1]
        rating = rating_map[rating_text]

        if rating >= 4:
            books.append({
                "judul": judul,
                "harga": harga,
                "rating": rating
            })

    # Cek ada halaman berikutnya nggak
    next_btn = soup.find("li", class_="next")
    if next_btn:
        next_page = next_btn.find("a")["href"]
        url = base_url + next_page
    else:
        url = None

# Simpan ke CSV
import openpyxl

# Ganti bagian "Simpan ke CSV" dengan ini:
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Books"

# Header
ws.append(["Judul", "Harga", "Rating"])

# Isi data
for book in books:
    ws.append([book["judul"], book["harga"], book["rating"]])

# Rapiin lebar kolom otomatis
for col in ws.columns:
    max_length = max(len(str(cell.value)) for cell in col)
    ws.column_dimensions[col[0].column_letter].width = max_length + 2

wb.save("books_all.xlsx")
print(f"Selesai! {len(books)} buku disimpan ke books_all.xlsx")

print(f"Selesai! {len(books)} buku ditemukan.")