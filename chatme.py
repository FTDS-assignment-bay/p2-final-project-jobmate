import openai
import streamlit as st
from pymongo import MongoClient
import PyPDF2
import re
# Set up OpenAI API key
openai.api_key = "OPENAI_API_KEY"
# MongoDB Connection
MONGO_URI = "MONGO_URI"
client = MongoClient(MONGO_URI)
db = client["finpro"]
jobs_collection = db["jobmate"]

def run():
    # st.set_page_config(page_title="JobMate")
    # st.title("JobMate")
    # st.write("Welcome to the JobMate application! Use this tool to find jobs based on your preferences.")

    # Function to query job database dynamically
    def query_jobs(role, exclude_role, skills, location, exclude_location):
        query = {"$and": []}

        if role:
            query["$and"].append({"job_title": {"$regex": re.escape(role), "$options": "i"}})
        if exclude_role:
            query["$and"].append({"job_title": {"$not": {"$regex": re.escape(exclude_role), "$options": "i"}}})
        if skills:
            query["$and"].append({"$or": [{"skills": {"$regex": re.escape(skill), "$options": "i"}} for skill in skills]})
        if location:
            if "luar jakarta" in location.lower():
                query["$and"].append({"location": {"$not": {"$regex": re.escape("jakarta"), "$options": "i"}}})
            else:
                query["$and"].append({"location": {"$regex": re.escape(location), "$options": "i"}})
        if exclude_location:
            query["$and"].append({"location": {"$not": {"$regex": re.escape(exclude_location), "$options": "i"}}})

        if not query["$and"]:
            return list(jobs_collection.find().limit(10))

        return list(jobs_collection.find(query).limit(10))

    # Function to extract information from a sentence using LLM
    def extract_info_from_sentence(chat_history):
        prompt = """
        Based on the entire chat history, extract the following details:
        - Role: The job role mentioned.
        - Exclude Role: Roles to exclude.
        - Skills: List of skills mentioned.
        - Location: Job location.
        - Exclude Location: Locations to exclude.

        If the information is not provided, use 'None'.
        Provide the response in this exact format:
        Role: <role>
        Exclude Role: <exclude role>
        Skills: <skills>
        Location: <location>
        Exclude Location: <exclude location>
        """
        messages = [{"role": "system", "content": "You are an assistant that extracts job-related information."}]
        messages += chat_history
        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=200
        )
        content = response['choices'][0]['message']['content'].strip()

        def safe_extract(label):
            try:
                return content.split(f"{label}: ")[1].split("\n")[0].strip()
            except IndexError:
                return ""

        role = safe_extract("Role")
        exclude_role = safe_extract("Exclude Role")
        skills_line = safe_extract("Skills")
        location = safe_extract("Location")
        exclude_location = safe_extract("Exclude Location")

        role = role if role.lower() != "none" else ""
        exclude_role = exclude_role if exclude_role.lower() != "none" else ""
        skills = [skill.strip().lower() for skill in skills_line.split(",") if skill] if skills_line.lower() != "none" else []
        location = location if location.lower() != "none" else ""
        exclude_location = exclude_location if exclude_location.lower() != "none" else ""

        return role, exclude_role, skills, location, exclude_location

    # Function to extract skills from a PDF resume
    def extract_skills_from_pdf(uploaded_file):
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Use GPT to extract skills from the resume text
            prompt = f"Extract key skills from the following resume text:\n{text}\n\nProvide a list of skills separated by commas."
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You extract key skills from resumes."},
                        {"role": "user", "content": prompt}],
                max_tokens=200
            )
            skills_text = response['choices'][0]['message']['content'].strip()
            return [skill.strip().lower() for skill in skills_text.split(",") if skill]
        except Exception as e:
            st.error(f"Error extracting skills from resume: {e}")
            return []

    # Streamlit UI
    # st.set_page_config(page_title="JobMate", page_icon="🌐")
    # st.title("🌐 JobMate")
    st.image('JobMate.png')
    st.write("")

    st.header("🔍 Temukan Pekerjaan Impian Anda!")
    # st.write("Gunakan asisten chatbot kami untuk menemukan pekerjaan yang sesuai dengan preferensi Anda. Unggah CV/Resume Anda untuk hasil yang lebih akurat.")

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # File upload for resume
    uploaded_file = st.file_uploader("Gunakan asisten chatbot kami untuk menemukan pekerjaan yang sesuai dengan preferensi Anda. Unggah CV/Resume Anda untuk hasil yang lebih akurat.", type=["pdf"])
    resume_skills = []
    if uploaded_file:
        st.info("Memproses resume anda...")
        resume_skills = extract_skills_from_pdf(uploaded_file)
        if resume_skills:
            st.success(f"Extracted skills: {', '.join(resume_skills)}")

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Bagaimana saya dapat membantu anda untuk rekomendasi pekerjaan?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Retrieve the entire chat history
        chat_history = st.session_state.messages

        try:
            with st.spinner("Sedang memproses permintaan anda..."):
                role, exclude_role, skills, location, exclude_location = extract_info_from_sentence(chat_history)
                all_skills = list(set(skills + resume_skills))  # Combine input skills and resume skills
                matching_jobs = query_jobs(role, exclude_role, all_skills, location, exclude_location)

            if matching_jobs:
                response = "Berikut beberapa rekomendasi pekerjaan:\n\n"
                for job in matching_jobs:
                    job_title = job.get('job_title', 'Unknown Position')
                    company_name = job.get('company_name', 'Unknown Company')
                    job_location = job.get('location', 'Unknown Location')
                    job_link = job.get('job_link', '#')
                    response += f"- [**{job_title}**]({job_link}) at **{company_name}** - *{job_location}*\n"
            else:
                response = "Maaf, saya tidak dapat menemukan rekomendasi pekerjaan yang sesuai dengan kriteria anda. Coba perbaiki pencarian anda."
        except Exception as e:
            response = f"An error occurred: {str(e)}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


if __name__ == '__main__':
    run()
