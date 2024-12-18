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

plt.figure(figsize=(8, 6))
sns.scatterplot(x='Total Jenis Parfum', y='Total Item Terjual', hue='Bulan', data=cleaned_sales_data, palette='Set2', s=100)
plt.title('Hubungan Total Jenis Parfum dan Total Item Terjual', fontsize=14)
plt.xlabel('Total Jenis Parfum', fontsize=12)
plt.ylabel('Total Item Terjual', fontsize=12)
plt.legend(title='Bulan')
plt.show()

plt.figure(figsize=(8, 6))
sns.heatmap(cleaned_sales_data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Korelasi Antar Variabel', fontsize=14)
plt.show()

plt.figure(figsize=(8, 6))
sns.histplot(cleaned_sales_data['Jumlah'], bins=10, kde=True, color='blue')
plt.title('Distribusi Jumlah Parfum Terjual', fontsize=14)
plt.xlabel('Jumlah Parfum', fontsize=12)
plt.ylabel('Frekuensi', fontsize=12)
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(x='Aroma', y='Jumlah', data=cleaned_sales_data, palette='Set3')
plt.title('Distribusi Jumlah Terjual per Aroma', fontsize=14)
plt.xlabel('Aroma', fontsize=12)
plt.ylabel('Jumlah Terjual', fontsize=12)
plt.xticks(rotation=45)
plt.show()

stacked_data = cleaned_sales_data.groupby(['Bulan', 'Aroma'])['Jumlah'].sum().unstack().fillna(0)
stacked_data.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Paired')
plt.title('Jumlah Terjual per Aroma per Bulan', fontsize=14)
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Jumlah Terjual', fontsize=12)
plt.legend(title='Aroma')
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(x='Total Jenis Parfum', y='Total Item Terjual', size='Jumlah', hue='Bulan', data=cleaned_sales_data, alpha=0.6, sizes=(50, 500))
plt.title('Bubble Chart: Total Jenis Parfum vs Total Item Terjual', fontsize=14)
plt.xlabel('Total Jenis Parfum', fontsize=12)
plt.ylabel('Total Item Terjual', fontsize=12)
plt.legend(title='Bulan')
plt.show()
