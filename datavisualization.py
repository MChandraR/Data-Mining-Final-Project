import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = '/mnt/data/Laporan_11_bulan.xlsx'
data = pd.read_excel(file_path, sheet_name='Data Penjualan')

cleaned_sales_data = data.iloc[2:].reset_index(drop=True)
cleaned_sales_data.columns = ['No', 'Aroma', 'Jumlah', 'Unused', 'Bulan', 
                              'Total Jenis Parfum', 'Total Item Terjual']
cleaned_sales_data = cleaned_sales_data.drop(columns=['Unused'])

cleaned_sales_data['Jumlah'] = pd.to_numeric(cleaned_sales_data['Jumlah'], errors='coerce')
cleaned_sales_data['Total Jenis Parfum'] = pd.to_numeric(cleaned_sales_data['Total Jenis Parfum'], errors='coerce')
cleaned_sales_data['Total Item Terjual'] = pd.to_numeric(cleaned_sales_data['Total Item Terjual'], errors='coerce')

plt.figure(figsize=(10, 6))
sns.barplot(x='Aroma', y='Jumlah', data=cleaned_sales_data, palette='viridis')
plt.title('Jumlah Parfum Terjual per Aroma', fontsize=14)
plt.xlabel('Aroma', fontsize=12)
plt.ylabel('Jumlah Terjual', fontsize=12)
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(8, 8))
cleaned_sales_data.groupby('Bulan')['Total Item Terjual'].sum().plot.pie(
    autopct='%1.1f%%', colors=sns.color_palette('pastel'), startangle=140)
plt.title('Distribusi Total Item Terjual per Bulan', fontsize=14)
plt.ylabel('')
plt.show()

plt.figure(figsize=(10, 6))
sns.lineplot(x='Bulan', y='Total Item Terjual', data=cleaned_sales_data, marker='o', sort=False)
plt.title('Tren Total Item Terjual per Bulan', fontsize=14)
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Total Item Terjual', fontsize=12)
plt.show()
