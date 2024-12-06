import matplotlib.pyplot as plt

# Data penjualan parfum (Nama dan Jumlah penjualan)
parfum_names = [
    "Arende", "Azura", "B London", "Ba Man", "Ba Rose", "Bhester", "Black In",
    "Blue Sky", "Bs Women", "Crokred Man", "Debut", "Eiffel", "Escary",
    "Heart Button", "Imagination", "Imperial", "J. Parker", "Marimar", "Meva",
    "Ovium", "Retaxe", "Rubi Rainer", "Saxy Gvt", "Scandal", "Scandalious",
    "Selego", "Soft", "Sweet Bale", "Taj Mahal", "Vanilla Lace", "One Way"
]

sales = [
    34, 19, 12, 4, 21, 11, 17, 10, 17, 24, 26, 31, 49, 10, 19, 31, 11, 5, 25, 
    49, 77, 43, 11, 6, 48, 31, 31, 22, 55, 9, 2
]

# Membuat bar chart
plt.figure(figsize=(15, 8))
plt.bar(parfum_names, sales, color='skyblue')
plt.title("Penjualan Aroma Parfum dalam 11 Bulan", fontsize=14)
plt.xlabel("Nama Parfum", fontsize=12)
plt.ylabel("Jumlah Penjualan", fontsize=12)
plt.xticks(rotation=90, fontsize=10)
plt.tight_layout()
plt.show()