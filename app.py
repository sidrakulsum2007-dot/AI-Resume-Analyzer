
import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
hf_client = InferenceClient(
    api_key=st.secrets["HF_TOKEN"]
)

st.title("🤖 AI Resume Analyzer")
st.write("Analyze your resume, check skills, and compare it with a job description.")

# Skills database
skills = [
    "python", "java", "c", "c++", "sql",
    "html", "css", "javascript",
    "machine learning", "deep learning",
    "artificial intelligence", "data science",
    "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch",
    "flask", "django", "git", "github",
    "excel", "power bi", "tableau"
]

# Upload resume
uploaded_file = st.file_uploader(
    "📄 Upload your resume",
    type=["pdf"]
)

# Job description
job_description = st.text_area(
    "📝 Paste the Job Description",
    height=200
)

if st.button("🔍 Analyze Resume"):

    if uploaded_file is None:
        st.warning("Please upload your resume.")
        st.stop()

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text

    resume_lower = resume_text.lower()

    # Detect skills
    found_skills = []
    for skill in skills:
        if skill in resume_lower:
            found_skills.append(skill)

    # Resume score
    skill_score = (len(found_skills) / len(skills)) * 100

    st.subheader("📊 Resume Score")
    st.metric(
        "ATS Skill Score",
        f"{skill_score:.1f}/100"
    )

    # Display skills
    st.subheader("✅ Skills Found")

    if found_skills:
        st.write(", ".join(found_skills))
    else:
        st.write("No matching skills detected.")

    # Job matching
    if job_description:

        job_lower = job_description.lower()

        job_skills = [
            skill for skill in skills
            if skill in job_lower
        ]

        matched_skills = [
            skill for skill in job_skills
            if skill in resume_lower
        ]

        missing_skills = [
            skill for skill in job_skills
            if skill not in resume_lower
        ]

        if job_skills:
            match_score = (
                len(matched_skills) /
                len(job_skills)
            ) * 100
        else:
            match_score = 0

        st.subheader("🎯 Job Match Score")

        st.metric(
            "Job Description Match",
            f"{match_score:.1f}%"
        )

        st.subheader("✅ Matching Skills")

        if matched_skills:
            st.write(", ".join(matched_skills))
        else:
            st.write("No matching skills found.")

        st.subheader("❌ Missing Skills")

        if missing_skills:
            st.write(", ".join(missing_skills))
        else:
            st.write("🎉 No detected skills are missing!")

    # Suggestions
    st.subheader("💡 Resume Improvement Suggestions")

    if "project" not in resume_lower:
        st.write("• Add a Projects section with relevant projects.")

    if "github" not in resume_lower:
        st.write("• Add your GitHub profile.")

    if "experience" not in resume_lower:
        st.write("• Add internship or practical experience if applicable.")

    if len(resume_text.split()) < 200:
        st.write("• Add more relevant details about your skills and projects.")

    st.success("Analysis completed successfully! 🎉")
# 🤖 AI Career Assistant

st.subheader("🤖 AI Career Assistant")

st.write("Ask me anything about your resume, career, jobs, or internships!")

user_question = st.chat_input("Ask a question about your career...")

if user_question:

    question = user_question.lower()

    with st.chat_message("user"):
        st.write(user_question)

    # Career Assistant responses

    if "resume" in question:
        answer = """
        To improve your resume, keep it clear and professional.
        Highlight your technical skills, projects, internships,
        certifications, education, and achievements.
        """

    elif "skill" in question:
        answer = """
        For an AI/ML career, focus on Python, SQL, Machine Learning,
        Deep Learning, NumPy, Pandas, scikit-learn, Git, and GitHub.
        Building practical projects will make your profile stronger.
        """

    elif "internship" in question:
        answer = """
        To get an AI/ML internship, build 2–3 practical projects,
        create a strong resume, maintain a GitHub profile, and
        apply regularly for relevant internships.
        """

    elif "job" in question or "career" in question:
        answer = """
        AI/ML students can explore careers such as AI/ML Engineer,
        Data Analyst, Python Developer, Junior ML Engineer, and
        AI Engineer. Start with Python, data analysis, Machine Learning,
        and practical projects.
        """

    elif "python" in question:
        answer = """
        Python is one of the most useful languages for AI and Machine
        Learning. Start with variables, functions, OOP, file handling,
        NumPy, Pandas, and Machine Learning libraries.
        """

    elif "github" in question:
        answer = """
        GitHub is useful for showcasing your projects to recruiters.
        Keep your repositories organized and add a README explaining
        the project, technologies used, features, and how to run it.
        """

    elif "project" in question:
        answer = """
        Good AI/ML project ideas include an AI Resume Analyzer,
        recommendation system, sentiment analysis system,
        spam detection system, or student performance prediction.
        """

    else:
        answer = """
        I can help you with:

        • Resume improvement
        • AI/ML skills
        • Internship preparation
        • Job and career guidance
        • Python
        • GitHub
        • AI/ML project ideas

        Try asking something like:
        "What skills should I learn for an AI/ML internship?"
        """

    with st.chat_message("assistant"):
        st.write(answer)