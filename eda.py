# Import Libraries
import pandas as pd
import numpy as np


# Visualisasi
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

def run():
    st.image('JobMate.png')
    st.markdown(
    """
    <h1 style="text-align: center;">Asisten Pencarian Kerja Berbasis AI</h1>
    """,
    unsafe_allow_html=True
)
    st.write('JobMate adalah asisten pencarian kerja berbasis AI yang dirancang untuk membantu pencari kerja menemukan peluang karier terbaik dengan cepat dan efisien. Dengan antarmuka yang ramah pengguna dan kemampuan pemrosesan data cerdas, **JobMate** mempersonalisasi setiap pencarian berdasarkan keterampilan, pengalaman, dan preferensi pengguna.')




    st.write('---')
    st.write('### Data Lowongan Pekerjaan')

    data = pd.read_csv('job_data.csv')

    st.dataframe(data.head(10))
    st.write('Berikut adalah Data lowongan pekerjaan terbaru yang menyajikan data terperinci yang akan digunakan untuk mendalami lebih jauh analisis ini.')
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

    # Menambahkan judul
    # plt.title('Distribution of Job Categories', fontsize=14)

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

    st.write('#### 2. Pekerjaan Data di Jabodetabek')
    # Fungsi untuk mendapatkan top 5 pekerjaan di wilayah tertentu
    def get_top_jobs_in_city(city_name, data, top_n=5):
        city_df = data[(data['location'].str.contains(city_name, case=False, na=False)) & (data['job_category'] != "Other")]
        top_jobs = city_df['job_category'].value_counts().head(top_n)
        return top_jobs

    # Dapatkan top 5 pekerjaan di setiap wilayah
    top_jobs_jakarta = get_top_jobs_in_city('jakarta', data)
    top_jobs_bogor = get_top_jobs_in_city('bogor', data)
    top_jobs_depok = get_top_jobs_in_city('depok', data)
    top_jobs_tangerang = get_top_jobs_in_city('tangerang', data)
    top_jobs_bekasi = get_top_jobs_in_city('bekasi', data)

    fig = fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10), constrained_layout=True)

    # Daftar kota dan data pekerjaan
    cities_and_jobs = [
        ('Jakarta', top_jobs_jakarta),
        ('Bogor', top_jobs_bogor),
        ('Depok', top_jobs_depok),
        ('Tangerang', top_jobs_tangerang),
        ('Bekasi', top_jobs_bekasi)
    ]

    # Plot setiap top job di subplot
    for ax, (city_name, top_jobs) in zip(axes.flatten(), cities_and_jobs):
        sns.barplot(y=top_jobs.values, x=top_jobs.index, palette='Set2', hue=top_jobs.index, ax=ax)
        ax.set_title(f'Lowongan Kerja di {city_name.capitalize()}', fontsize=16)
        ax.set_xlabel('Number of Jobs', fontsize=12)
        ax.set_ylabel('Job Title', fontsize=12)
        ax.grid(True, linestyle = '--', color = 'grey', alpha = 0.3)
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{int(height)}', 
                        (p.get_x() + p.get_width() / 2., height), 
                        fontsize=12, fontweight='bold', ha='center', va='center', 
                        xytext=(0, 5), textcoords='offset points')


    # Matikan axis kosong
    for ax in axes.flatten()[len(cities_and_jobs):]:
        ax.axis('off')

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