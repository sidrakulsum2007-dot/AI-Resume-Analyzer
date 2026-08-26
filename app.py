
import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
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
