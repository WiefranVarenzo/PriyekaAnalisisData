import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

PAGE_CONFIG = {"page_title":"StColab.io","page_icon":":smiley:","layout":"centered"}

all_df = pd.read_csv("data.csv")

def main():
	st.title("Proyek Analisis Data Menggunakan Python")


	menu = ["Home","Pertanyaan 1","Pertanyaan 2","Pertanyaan 3","Pertanyaan 4","Pertanyaan 5", "Pertanyaan 6"]
	choice = st.sidebar.selectbox('Menu',menu)
	if choice == 'Home':
		st.subheader("Pertanyaan-pertanyaan bisnis: ")
		st.text('1. Bagaimana persebaran rating dari penjualan produk berdasarkan kategorinya ?')
		st.text('2. Berapa persen pesanan yang datang sesuai atau bahkan lebih cepat dari estimasi?')
		st.text('3. Tipe pembayaran apa yang paling banyak dan paling sedikit dipakai?')
		st.text('4. Kota apa dengan sebaran pelanggan terbanyak?')
		st.text('5. Kategori produk apa yang paling diminati yang tidak diminiati oleh pelanggan?')
		st.text('6. Apakah karakteristik barang yang dikirimkan berpengaruh terhadap biaya pengiriman (shipping/freight value)?')
	elif choice == 'Pertanyaan 1':
		# Sort the data first
		st.subheader("1. Bagaimana persebaran rating dari penjualan produk berdasarkan kategorinya ?")

		grouped_data = all_df.groupby(['product_category_name_english', 'review_score']).size().reset_index(name='Jumlah')
		grouped_data = grouped_data.sort_values(by="Jumlah", ascending=False)

		# Take the top and worst 5 categories
		top_5_categories = grouped_data.head(5)
		worst_5_categories = grouped_data.tail(5)

		# Create the plot
		fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 6))
		colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

		# Bar plot for the top categories
		sns.barplot(x="Jumlah", y="product_category_name_english", data=top_5_categories, palette=colors, ax=ax1)
		ax1.set_ylabel(None)
		ax1.set_xlabel(None)
		ax1.set_title("Best Performing Product", loc="center", fontsize=15)
		ax1.tick_params(axis='y', labelsize=12)

		# Bar plot for the worst categories
		sns.barplot(x="Jumlah", y="product_category_name_english", data=worst_5_categories, palette=colors, ax=ax2)
		ax2.set_ylabel(None)
		ax2.set_xlabel(None)
		ax2.invert_xaxis()
		ax2.yaxis.set_label_position("right")
		ax2.yaxis.tick_right()
		ax2.set_title("Worst Performing Product", loc="center", fontsize=15)
		ax2.tick_params(axis='y', labelsize=12)

		plt.suptitle("Best Performing Product by Number of Sales (5 Star Rating)", fontsize=20)

		# Display the plot in Streamlit
		st.pyplot(fig)
		st.text('''Conclution Pertanyaan 1: 
		  Dari persebaran rating dari penjualan produk berdasarkan kategorinya, 
		  maka bisa kita lihat bahwa health_beauty dan bed_bath_table merupakan 
		  yang paling banyak mendapat rating 5 paling banyak, 
		  yaitu sekitar lebih dari 600 orderan.''')


	elif choice == 'Pertanyaan 2':
		st.subheader("2. Berapa persen pesanan yang datang sesuai atau bahkan lebih cepat dari estimasi?")
		all_df["order_delivered_customer_date"] = pd.to_datetime(all_df["order_delivered_customer_date"])
		all_df["order_delivered_carrier_date"] = pd.to_datetime(all_df["order_delivered_carrier_date"])
		all_df["order_estimated_delivery_date"] = pd.to_datetime(all_df["order_estimated_delivery_date"])

		delivery_time = all_df["order_delivered_customer_date"] - all_df["order_delivered_carrier_date"]
		delivery_time = delivery_time.apply(lambda x: x.total_seconds() / 86400)  # Menghitung dalam hari
		all_df["delivery_time"] = delivery_time

		def is_on_time(row):
			timedelta = row["order_estimated_delivery_date"] - row["order_delivered_carrier_date"]
			return row["delivery_time"] <= timedelta.total_seconds() / 86400

		all_df["on_time"] = all_df.apply(is_on_time, axis=1)

		#Variabel yang menyatakan berapa banyak yang tepat waktu dan mana pesanan yang terlambat
		tepat_waktu = all_df["on_time"].sum()
		terlambat = len(all_df) - tepat_waktu

		# Membuat plot
		fig, ax = plt.subplots()
		plt.title("Persentase Pesanan Tepat Waktu vs. Terlambat")
		data_label = ("Tepat waktu", "Terlambat")
		votes = (tepat_waktu, terlambat)
		colors = ('#E67F0D', '#93C572')
		explode = (0, 0)

		ax.pie(
			x=votes,
			labels=data_label,
			autopct='%1.1f%%',
			colors=colors,
			explode=explode
		)
		st.pyplot(fig)

		st.text('''conclution pertanyaan 2: 
		  Terdapat 91% yang sesuai dengan jadwal sedangkan 9% lainnya terlambat, 
		  hal ini merupakan hal baik sebab lebih dari 90% pesanan sesuai dengan jadwal, 
		  namun hal ini bisa ditingkatkan pula.''')
		

	elif choice == 'Pertanyaan 3':
		st.subheader('3. Tipe pembayaran apa yang paling banyak dan paling sedikit dipakai')
		payment_counts = all_df['payment_type'].value_counts().reset_index()
		payment_counts.columns = ['payment type', 'Jumlah']

		#membuat subplot
		fig, ax = plt.subplots()
		data_label = payment_counts['payment type']
		votes = payment_counts['Jumlah']
		colors = ('#8B4513','#E67F0D', '#93C572', '#FFF8DC')
		explode = (0, 0,0,0)

		# Buat pie chart
		plt.figure(figsize=(8, 8))
		ax.pie(votes, labels=data_label, autopct='%1.1f%%', colors=colors)

		# Tambahkan judul
		plt.title("Persentase Pembayaran Berdasarkan Jenis Pembayaran")

		# Tampilkan pie chart
		st.pyplot(fig)
		
		st.text('''conclution pertanyaan 3: 
		  Tipe pembayaran paling banyak dipakai adalah credit_card 
		  yaitu sebanyak 73,9% dan setelah itu ada boleto sebanyak 19%, kemudian 5.6% untuk voucher, 
		  lalu ada sebanyak 1.5% yang menggunakan kartu debit''')
	
	elif choice == 'Pertanyaan 4':
		st.subheader('4. Kota apa dengan sebaran pelanggan terbanyak?')
		city_customer_counts = all_df['customer_city'].value_counts().reset_index()
		city_customer_counts.columns = ['customer_city', 'customer_count']

		sorted_city_customers = city_customer_counts.sort_values(by="customer_count", ascending=False)

		# Ambil 5 kategori teratas
		top_5_customers_location = sorted_city_customers.head(5)

		# Buat plot
		fig, ax = plt.subplots(figsize=(24, 6))
		colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
		sns.barplot(x="customer_city", y="customer_count", data=top_5_customers_location, palette=colors, ax=ax)
		ax.set_ylabel(None)
		ax.set_xlabel(None)
		ax.set_title("Best Performing Product", loc="center", fontsize=15)
		ax.tick_params(axis='y', labelsize=12)

		plt.suptitle("Which city has the highest customer distribution?", fontsize=20)
		st.pyplot(fig)
		st.text('''conclution pertanyaan 4: 
		  Kota yang paling banyak memiliki persebaran data adalah 
		  saopaolo dengan sebanyak lebih dari 15000 orderan yang berada di saopolo, 
		  diikuti dengan rio de jeinaro sebanyak 6000 orderan, belo horizonte 
		  sekitaran lebih dari 2000 oderan.''')
	
	elif choice == 'Pertanyaan 5':
		st.subheader('5. Kategori produk apa yang paling diminati yang tidak diminiati oleh pelanggan?')
		grouped_order_dataset = all_df.groupby(['product_category_name_english']).size().reset_index(name='Jumlah')
		grouped_order_data = grouped_order_dataset.sort_values(by="Jumlah", ascending=False)

		# Ambil 5 kategori teratas
		top_5_order_categories = grouped_order_data.head(5)
		lowest_5_order_categories = grouped_order_data.tail(5)


		# Buat plot
		fig, axes = plt.subplots(1, 2, figsize=(24, 6))

		colors = sns.color_palette('pastel')  

		# Plot terbaik
		sns.barplot(x="Jumlah", y="product_category_name_english", data=top_5_order_categories, palette=colors, ax=axes[0])
		axes[0].set_ylabel(None)
		axes[0].set_xlabel(None)
		axes[0].set_title("Best Performing Product", loc="center", fontsize=15)
		axes[0].tick_params(axis='y', labelsize=12)

		# Plot terburuk
		sns.barplot(x="Jumlah", y="product_category_name_english", data=lowest_5_order_categories.sort_values(by="Jumlah", ascending=True).head(5), palette=colors, ax=axes[1])
		axes[1].set_ylabel(None)
		axes[1].set_xlabel(None)
		axes[1].invert_xaxis()
		axes[1].yaxis.set_label_position("right")
		axes[1].yaxis.tick_right()
		axes[1].set_title("Worst Performing Product", loc="center", fontsize=15)
		axes[1].tick_params(axis='y', labelsize=12)

		plt.suptitle("Best Performing Product by Selling Quantity", fontsize=20)
		st.pyplot(fig)
		st.text('''conluction pertanyaan 5: 
		  Kateogri yang paling diminati adalah bed_bath_table sebanyak lebih dari 1100 orderan, 
		  kemudian diikuti dengan health_beauty.''')

	
	elif choice == 'Pertanyaan 6':
		st.subheader('6. Apakah ada pengaruh karakteristik fisik barang yang dikirimkan terhadap biaya pengiriman (shipping/freight value)?')
		selected_columns = all_df[["volumeBarang","freight_value"]]
		# Contoh data (gantilah ini dengan data sebenarnya)
		selected_columns_sorted = selected_columns.sort_values(by="volumeBarang", ascending=True)
		data = selected_columns_sorted["volumeBarang"]

		# Hitung Q1 dan Q3
		q1 = np.percentile(data, 25)
		q3 = np.percentile(data, 75)

		# Filter data yang berada di antara Q1 dan Q3
		filtered_data = selected_columns_sorted[(data >= q1) & (data <= q3)].sample(n=500)  # Ubah jumlah sampel sesuai kebutuhan

		# Buat scatterplot dengan data yang telah difilter
		fig,ax = plt.subplots(figsize=(10, 6))  # Sesuaikan ukuran gambar sesuai kebutuhan
		sns.scatterplot(data=filtered_data, x="freight_value", y="volumeBarang")
		st.pyplot(fig)

		selected_columns = all_df[["product_weight_g","freight_value"]]
		# Contoh data (gantilah ini dengan data sebenarnya)
		selected_columns_sorted = selected_columns.sort_values(by="product_weight_g", ascending=True)
		data = selected_columns_sorted["product_weight_g"]

		# Hitung Q1 dan Q3
		q1 = np.percentile(data, 25)
		q3 = np.percentile(data, 75)

		# Filter data yang berada di antara Q1 dan Q3
		filtered_data = selected_columns_sorted[(data >= q1) & (data <= q3)].sample(n=500)  # Ubah jumlah sampel sesuai kebutuhan

		# Buat scatterplot dengan data yang telah difilter
		fig,ax = plt.subplots(figsize=(10, 6))  # Sesuaikan ukuran gambar sesuai kebutuhan
		sns.scatterplot(data=filtered_data, x="freight_value", y="product_weight_g")
		st.pyplot(fig)
		st.text('''conclution pertanyaan 6: 
		  Dari korelasi yang bisa saya lihat, volume barang tidak terlalu 
		  memberikan korelasi dari data yang ada. Lalu untuk berat, 
		  memberikan korelasi yang tidak terlalu kuat juga.''')
		
if __name__ == '__main__':
	main()