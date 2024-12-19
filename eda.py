# Import Libraries
import pandas as pd
import numpy as np
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
import os

# Memuat environment variables dari file .env
load_dotenv()

# Fungsi untuk koneksi ke MongoDB dan mengambil data
def load_data_from_mongodb():
    # Ambil detail koneksi dari environment variables
    mongo_uri = os.getenv("MONGO_URI")
    database_name = os.getenv("DATABASE_NAME")
    collection_name = os.getenv("COLLECTION_NAME")

    # Validasi jika variabel environment tidak ditemukan
    if not mongo_uri or not database_name or not collection_name:
        raise ValueError("Environment variables for MongoDB are not set properly!")

    # Koneksi ke MongoDB
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Ambil data dari koleksi
    data_cursor = collection.find()
    data = pd.DataFrame(data_cursor)

    # Hapus kolom '_id' jika tidak diperlukan
    if "_id" in data.columns:
        data = data.drop("_id", axis=1)

    return data

def run():
    st.image('JobMate.png')
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Asisten Pencarian Kerja Berbasis AI</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style="text-align: justify; text-justify: inter-word; font-size: 16px; line-height: 1.6;">
            JobMate adalah asisten pencarian kerja berbasis AI yang dirancang untuk membantu pencari kerja menemukan peluang karier terbaik dengan cepat dan efisien. 
            Dengan antarmuka yang ramah pengguna dan kemampuan pemrosesan data cerdas, 
            <b>JobMate</b> mempersonalisasi setiap pencarian berdasarkan keterampilan, pengalaman, dan preferensi pengguna.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write('---')
    st.write('### Data Lowongan Pekerjaan')
    data = load_data_from_mongodb()
    st.write('Berikut adalah Data lowongan pekerjaan terbaru yang menyajikan data terperinci yang akan digunakan untuk mendalami lebih jauh analisis ini.')
    st.dataframe(data)
    
    st.write('### Exploratory Data Analyst')
    st.write('#### 1. Distribusi Kategori Pekerjaan')

    categories = {
        "Data Analyst": ["data analyst", "analyst", "business analyst", "reporting analyst", "intelligence analyst", "research analyst"],
        "Data Scientist": ["data scientist", "machine learning", "ai", "artificial intelligence", "data science", "ds", "scientist", "science", "deep learning", "statistician", "modeling", "predictive analytics", "neural networks"],
        "Data Engineer": ["data engineer", "etl", "integration", "pipeline", "extract", "transform", "load", "big data", "data warehousing", "spark", "hadoop", "database", "schema", "orchestration", "sql", "no-sql"],
        "Freelance": ["freelance", "annotator", "contract", "gig", "independent contractor", "self-employed", "consultant"],
    }

    def categorize_job_title(job_title):
        job_title = job_title.lower()  # Konversi ke huruf kecil untuk pencocokan fleksibel
        
        # Periksa setiap kategori berdasarkan kata kunci
        for category, keywords in categories.items():
            if any(keyword in job_title for keyword in keywords):
                return category
        
        # Jika tidak cocok, masukkan ke kategori "Other"
        return "Other"

    # Terapkan fungsi ini ke kolom job_title
    data['job_category'] = data['job_title'].apply(categorize_job_title)


    def categorize_job_title(job_title):
        job_title = job_title.lower()  # Konversi ke huruf kecil untuk pencocokan fleksibel
        
        # Periksa setiap kategori berdasarkan kata kunci
        for category, keywords in categories.items():
            if any(keyword in job_title for keyword in keywords):
                return category
        
        # Jika tidak cocok, masukkan ke kategori "Other"
        return "Other"

    # Terapkan fungsi ini ke kolom job_title
    data['job_category'] = data['job_title'].apply(categorize_job_title)

    category_summary = data['job_category'].value_counts()

    fig =plt.figure(figsize=(6, 6))

    # Membuat pie chart
    plt.pie(category_summary.values, labels=category_summary.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2", len(category_summary)))

    # Rotate x-axis labels jika panjang
    plt.tight_layout()

    st.pyplot(fig)
    st.write('##### Other')
    st.markdown(
        """
        <div style="text-align: justify;">
            <ul>
                <li>Kategori <strong>Other</strong> dimaksudkan untuk menjadi kumpulan lowongan pekerjaan yang bukan merupakan bidang data. 
                Other memiliki jumlah terbanyak yang jauh berbeda dengan job-job di bidang data. Hal ini kemungkinan disebabkan oleh banyaknya 
                lowongan yang memang bukan di bidang data dan juga terdapat lowongan-lowongan kerja di bidang data yang tidak terfilter 
                ke dalam salah satu dari kelompok bidang data (Data Scientist, Data Analyst, dan Data Engineer).
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Dominasi Data Analyst
    st.write('##### Dominasi Data Analyst')
    st.markdown(
        """
        <div style="text-align: justify;">
            <ul>
                <li>Posisi <strong>Data Analyst</strong> mendominasi dengan selisih yang signifikan dibandingkan job title lainnya. 
                Ini menunjukkan bahwa permintaan untuk Data Analyst sangat tinggi di pasar kerja saat ini.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Peluang Lowongan di Bidang Data
    st.write('##### Peluang Lowongan di Bidang Data')
    st.markdown(
        """
        <div style="text-align: justify;">
            <ul>
                <li>Selain Data Analyst, posisi seperti <strong>Data Engineer</strong> dan <strong>Data Scientist</strong> juga cukup tinggi. 
                Ini menunjukkan bahwa industri yang berkaitan dengan data, seperti analisis dan rekayasa data, sedang berkembang pesat.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Peluang Freelance
    st.write('##### Peluang Freelance')
    st.markdown(
        """
        <div style="text-align: justify;">
            <ul>
                <li>Ada peluang yang signifikan untuk pekerjaan freelance dalam industri ini. Perusahaan mungkin mencari fleksibilitas 
                dengan mengontrak tenaga kerja freelance untuk proyek-proyek tertentu.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write('#### 2. Pekerjaan Data di Jabotabek')

    # Filter hanya job_title tertentu
    selected_jobs = ['Data Analyst', 'Data Scientist', 'Data Engineer', 'Freelance']
    filtered_df = data[data['job_category'].isin(selected_jobs)]

    # Filter hanya untuk lokasi JABODETABEK
    locations = ['Jakarta', 'Bogor','Tangerang', 'Bekasi']
    filtered_df = filtered_df[filtered_df['location'].isin(locations)]

    # Menghitung jumlah lowongan per job_title dan lokasi
    pivot_table = filtered_df.pivot_table(index='job_category', columns='location', aggfunc='size', fill_value=0).reset_index()

    # Mengubah data menjadi format long (melt)
    melted_df = pd.melt(pivot_table, id_vars='job_category', value_vars=locations, 
                        var_name='location', value_name='count')

    # Create a stacked bar chart using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))

    # Define pastel colors
    pastel_colors = sns.color_palette('Set2', len(selected_jobs))

    # Stacked bar chart with pastel colors
    bottom = [0] * len(locations)
    for idx, (job, color) in enumerate(zip(selected_jobs, pastel_colors)):
        heights = melted_df.loc[melted_df['job_category'] == job, 'count'].tolist()
        ax.bar(locations, heights, bottom=bottom, label=job, color=color)
        bottom = [sum(x) for x in zip(bottom, heights)]

    # Add labels and title
    ax.set_title('Jumlah Lowongan Berdasarkan Job Title dan Lokasi (JABOTABEK)', fontsize=16)
    ax.set_xlabel('Lokasi', fontsize=14)
    ax.set_ylabel('Jumlah Lowongan', fontsize=14)
    ax.legend(title='Job Title', fontsize=12)
    ax.set_xticks(range(len(locations)))
    ax.set_xticklabels(locations)
    plt.grid(axis='y',zorder=0,alpha=0.5)

    st.pyplot(fig)

    st.markdown(
        """
        <div style="text-align: justify;">
            <p><a href="https://kompaspedia.kompas.id/baca/paparan-topik/jabodetabek-konsep-sejarah-dan-relasi-wilayah-aglomerasi">Jabodetabek</a> 
            merupakan kawasan metropolitan Jakarta dan sekitarnya yang memiliki jalinan interaksi sosial-ekonomi serta jarak spasial yang mendukung, 
            sehingga kemungkinan banyak lowongan pekerjaan yang tersebar di sana.</p>
                """,
        unsafe_allow_html=True
    )
    st.write('##### Kosentrasi di Jakarta')
    st.markdown(
        """
        <div style="text-align: justify;">
            <ul>
                <li>Jumlah lowongan pekerjaan yang jauh lebih banyak di Jakarta menunjukkan bahwa mantan ibu kota masih menjadi pusat utama untuk pekerjaan 
                di bidang teknologi dan analitik data.</li>
            </ul>
                """,
        unsafe_allow_html=True
    )
    st.write('##### Perbedaan Permintaan')
    st.markdown(
        """
        <div style="text-align: justify;">
            <ul>
                <li>Ada perbedaan signifikan dalam jumlah lowongan pekerjaan di kota-kota lain seperti Bogor, Depok, Tangerang, dan Bekasi dibandingkan dengan Jakarta. 
                Ini menunjukkan konsentrasi perusahaan besar di Jakarta dan kebutuhan untuk mempertimbangkan lokasi kerja bagi pencari kerja.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write('#### 3. Top  5 Lokasi Lowongan Terbanyak ')
    top_5_location = data['location'].value_counts().head()

    fig = plt.figure(figsize=(10, 6)) 
    ax=sns.countplot(data=data, x='location', order=top_5_location.index, palette='Set2',hue='location') 
    plt.title('Top 5 Lokasi Loker',fontsize=16) 
    plt.xlabel('Location',fontsize=12)
    plt.ylabel('Count',fontsize=12)

    for p in ax.patches: 
        height = p.get_height() 
        if height > 350:
            ax.annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height), 
                    fontsize=15, fontweight='bold',ha='center', va='center', 
                    xytext=(0,-15), textcoords='offset points')
        else:
            ax.annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height), 
                    fontsize=15, fontweight='bold',ha='center', va='center', 
                    xytext=(0,10), textcoords='offset points')

    st.pyplot(fig)
    st.markdown(
        """
        <div style="text-align: justify;">
            <strong>Lowongan Pekerjaan:</strong><br>
            <ul>
                <li><strong>Jakarta:</strong><br>
                    Jakarta memiliki jumlah peluang kerja yang jauh lebih tinggi dibandingkan dengan kota-kota lainnya. Hal ini dikarenakan 
                    Jakarta, walaupun sudah bukan sebagai ibu kota Indonesia, masih menjadi <a href="https://m.beritajakarta.id/en/read/43425/fithra-faisal-jakarta-remains-as-business-and-economic-center" target="_blank">pusat bisnis dan pemerintahan</a>, 
                    sehingga banyak perusahaan besar dan kantor pemerintahan yang berlokasi di sana.
                </li>
                <li><strong>Kota-kota Lain:</strong><br>
                    Kota-kota seperti Bali, Bandung, Tangerang, dan Yogyakarta menunjukkan jumlah peluang kerja yang jauh lebih rendah, meskipun kota-kota ini juga memiliki daya tarik dan sektor industri masing-masing. 
                    Bali, misalnya, terkenal dengan sektor pariwisatanya, sedangkan Bandung dikenal dengan industri kreatif dan Tangerang sebagai kota satelit yang berkembang pesat.
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

   
    st.write('#### 4. 7 Perusahaan Teratas dengan Lowongan Pekerjaan Terbanyak')
    top_5_companies = data['company_name'].value_counts().head(7)

    # Sort the job titles by count in descending order
    top_5_companies = top_5_companies.sort_values()

    fig = plt.figure(figsize=(10, 6))
    ax=top_5_companies.plot(kind='barh', color=['#bae1ff', '#baffc9', '#FFF9BF', '#ffdfba', '#CB9DF0','#f7e7b4','#68c4af'])
    plt.title('7 Perusahaan Teratas dengan Lowongan Pekerjaan Terbanyak',fontsize=16)
    plt.xlabel('Count',fontsize=12)
    plt.ylabel('Company Name',fontsize=12)
    for i in ax.patches: 
        plt.text(i.get_width() + 1.5, i.get_y() + i.get_height() / 2, str(int(i.get_width())),
                                fontsize=12, fontweight='bold', ha='center', va='center')

    st.pyplot(fig)
    st.write('##### Pertumbuhan & Perkembangan di Berbagai Sektor')
    st.markdown(
        """
        <div style="text-align: justify;">
            <ul>
                <li><strong>Agoda</strong> dalam industri perhotelan, <strong>Goto Group</strong> dalam layanan on-demand, dan <strong>Kredivo Group</strong> dalam layanan finansial semuanya membutuhkan ahli teknologi dan data. 
                Ini menunjukkan bahwa teknologi dan data menjadi pilar penting di berbagai sektor.</li>
                <li>Perusahaan seperti <strong>Mindrift</strong> dan <strong>TikTok</strong> yang fokus pada inovasi, AI, dan machine learning mencari ahli yang dapat mendorong perkembangan produk dan layanan mereka.</li>
                <li>Perusahaan seperti <strong>Antler</strong> yang bergerak di bidang investasi startup dan <strong>NTT Data Inc.</strong> yang menyediakan layanan konsultasi IT menunjukkan bahwa ada kebutuhan untuk dukungan teknologi dalam ekspansi bisnis dan investasi.</li>
            </ul>
            <p>Secara keseluruhan, kebutuhan akan tenaga kerja di bidang teknologi dan data sangat tinggi dan menyebar di berbagai sektor industri. 
            Ini menunjukkan bahwa memiliki keterampilan di bidang ini memberikan peluang karir yang luas dan beragam.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write('#### 5. Top 10 Keterampilan Data yang Paling Dibutuhkan')
    data_copy = data.copy()
    data_copy['skills'] = data_copy['skills'].apply(eval)
    exploded_data = data_copy.explode('skills')
    skill_counts = exploded_data['skills'].value_counts().head(10)

    skill_data = skill_counts.reset_index()
    skill_data.columns = ['skill', 'count']

    fig = plt.figure(figsize=(15, 6))
    ax=sns.barplot(x='skill', y='count', data=skill_data, palette='Set2', hue='skill')
    plt.title('Top 10 Keterampilan Data yang Paling Dibutuhkan',fontsize=16)
    plt.xlabel('Skills',fontsize=12)
    plt.ylabel('Count',fontsize=12)
    for p in ax.patches: 
        height = p.get_height() 
        ax.annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height), 
                    fontsize=15, fontweight='bold',ha='center', va='center', 
                    xytext=(0,-15), textcoords='offset points')

    st.pyplot(fig)
    st.write('##### Permintaan Tinggi untuk Keterampilan Data dan Teknologi')
    st.markdown(
        """
        <div style="text-align: justify;">
            <ul>
                <li>Ada permintaan yang sangat tinggi untuk keterampilan di bidang data dan teknologi. Keterampilan teknis seperti SQL, Python, Spark, dll., serta keterampilan analitis seperti statistik dan machine learning, sangat diperlukan.</li>
            </ul>
                """,
        unsafe_allow_html=True
    )
    st.write('##### Keterampilan Komunikasi dan Kolaborasi')
    st.markdown(
        """
        <div style="text-align: justify;">
            <ul>
                <li>Keterampilan teknis, kemampuan untuk berkomunikasi dan bekerja sama dengan tim juga sangat dihargai. Ini menunjukkan pentingnya keterampilan interpersonal di samping keterampilan teknis.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    run()
