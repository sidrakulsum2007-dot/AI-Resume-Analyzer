import streamlit as st
from pypdf import PdfReader
import re

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🤖 AI Resume Analyzer")

st.write(
    "Analyze your resume, check skills, compare it with a job description, "
    "and get personalized improvement suggestions."
)

# =========================================================
# SKILLS DATABASE
# =========================================================

skills = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "flask",
    "django",
    "git",
    "github",
    "excel",
    "power bi",
    "tableau"
]

# =========================================================
# RESUME VALIDATION
# =========================================================

def validate_resume(text):
    """
    Determines whether the uploaded PDF is likely to be a resume.
    Uses multiple signals instead of checking for only one keyword.
    """

    if not text or len(text.strip()) < 100:
        return False, "The uploaded document contains too little readable text."

    text_lower = text.lower()

    # -----------------------------------------------------
    # Resume-related sections
    # -----------------------------------------------------

    resume_sections = [
        "education",
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "skills",
        "technical skills",
        "projects",
        "certifications",
        "internship",
        "internships",
        "achievements",
        "career objective",
        "objective",
        "summary",
        "profile",
        "professional summary",
        "qualifications",
        "academic qualifications",
        "contact"
    ]

    section_matches = 0

    for section in resume_sections:
        if section in text_lower:
            section_matches += 1

    # -----------------------------------------------------
    # Contact information
    # -----------------------------------------------------

    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)'

    has_email = bool(re.search(email_pattern, text))
    has_phone = bool(re.search(phone_pattern, text))

    contact_score = 0

    if has_email:
        contact_score += 1

    if has_phone:
        contact_score += 1

    # -----------------------------------------------------
    # Professional profile indicators
    # -----------------------------------------------------

    professional_indicators = [
        "linkedin",
        "github",
        "developer",
        "engineer",
        "student",
        "intern",
        "internship",
        "bachelor",
        "b.e.",
        "btech",
        "b.tech",
        "m.e.",
        "mtech",
        "m.tech",
        "university",
        "college"
    ]

    professional_matches = 0

    for indicator in professional_indicators:
        if indicator in text_lower:
            professional_matches += 1

    # -----------------------------------------------------
    # Resume skill indicators
    # -----------------------------------------------------

    skill_matches = 0

    for skill in skills:
        if skill in text_lower:
            skill_matches += 1

    # -----------------------------------------------------
    # Book / article indicators
    # -----------------------------------------------------

    non_resume_indicators = [
        "chapter 1",
        "chapter 2",
        "chapter 3",
        "chapter 4",
        "chapter 5",
        "table of contents",
        "bibliography",
        "references",
        "isbn",
        "copyright",
        "publisher",
        "foreword",
        "preface",
        "contents",
        "index",
        "volume",
        "edition"
    ]

    non_resume_matches = 0

    for indicator in non_resume_indicators:
        if indicator in text_lower:
            non_resume_matches += 1

    # -----------------------------------------------------
    # Calculate resume confidence
    # -----------------------------------------------------

    resume_score = 0

    if section_matches >= 6:
        resume_score += 5
    elif section_matches >= 4:
        resume_score += 4
    elif section_matches >= 3:
        resume_score += 3
    elif section_matches >= 2:
        resume_score += 1

    if contact_score == 2:
        resume_score += 3
    elif contact_score == 1:
        resume_score += 2

    if professional_matches >= 4:
        resume_score += 3
    elif professional_matches >= 2:
        resume_score += 2
    elif professional_matches >= 1:
        resume_score += 1

    if skill_matches >= 5:
        resume_score += 2
    elif skill_matches >= 2:
        resume_score += 1

    if non_resume_matches >= 4:
        resume_score -= 6
    elif non_resume_matches >= 2:
        resume_score -= 3

    # -----------------------------------------------------
    # Final decision
    # -----------------------------------------------------

    if resume_score >= 7:
        return True, ""

    if section_matches >= 4 and contact_score >= 1:
        return True, ""

    if section_matches >= 5 and skill_matches >= 2:
        return True, ""

    return False, (
        "The uploaded PDF does not appear to be a resume. "
        "Please upload a valid resume containing information such as "
        "education, skills, projects, experience, certifications, "
        "or contact details."
    )


# =========================================================
# RESUME UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "📄 Upload your resume",
    type=["pdf"]
)

# =========================================================
# JOB DESCRIPTION
# =========================================================

job_description = st.text_area(
    "📝 Paste the Job Description",
    height=200,
    placeholder="Paste the job description here..."
)

# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button("🔍 Analyze Resume", type="primary"):

    # -----------------------------------------------------
    # Check PDF upload
    # -----------------------------------------------------

    if uploaded_file is None:
        st.warning("⚠️ Please upload your resume PDF.")
        st.stop()

    # -----------------------------------------------------
    # Read PDF
    # -----------------------------------------------------

    try:
        reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += "\n" + text

    except Exception:
        st.error(
            "❌ Unable to read this PDF. "
            "Please upload a valid, text-readable PDF resume."
        )
        st.stop()

    # -----------------------------------------------------
    # Check extracted text
    # -----------------------------------------------------

    if not resume_text.strip():
        st.error(
            "❌ No readable text was found in this PDF. "
            "Please upload a text-based resume PDF."
        )
        st.stop()

    resume_lower = resume_text.lower()

    # -----------------------------------------------------
    # VALIDATE WHETHER DOCUMENT IS A RESUME
    # -----------------------------------------------------

    is_resume, validation_message = validate_resume(resume_text)

    if not is_resume:
        st.error("🚫 This document does not appear to be a resume.")

        st.info(
            "Please upload your actual resume instead of a book, "
            "article, notes, or other document."
        )
        st.stop()

    # -----------------------------------------------------
    # Resume accepted
    # -----------------------------------------------------

    st.success("✅ Resume detected successfully!")

    # =====================================================
    # DETECT SKILLS
    # =====================================================

    found_skills = []

    for skill in skills:
        if skill in resume_lower:
            found_skills.append(skill)

    # =====================================================
    # RESUME ATS SKILL SCORE
    # =====================================================

    skill_score = (len(found_skills) / len(skills)) * 100

    st.subheader("📊 Resume Score")

    st.metric(
        "ATS Skill Score",
        f"{skill_score:.1f}/100"
    )

    # =====================================================
    # SKILLS FOUND
    # =====================================================

    st.subheader("✅ Skills Found")

    if found_skills:
        st.write(", ".join(found_skills))
    else:
        st.write("No matching technical skills detected.")

    # =====================================================
    # JOB DESCRIPTION ANALYSIS
    # =====================================================

    if job_description.strip():

        job_lower = job_description.lower()

        # -------------------------------------------------
        # Detect skills required by job
        # -------------------------------------------------

        job_skills = []

        for skill in skills:
            if skill in job_lower:
                job_skills.append(skill)

        # -------------------------------------------------
        # Matching skills
        # -------------------------------------------------

        matched_skills = []

        for skill in job_skills:
            if skill in resume_lower:
                matched_skills.append(skill)

        # -------------------------------------------------
        # Missing skills
        # -------------------------------------------------

        missing_skills = []

        for skill in job_skills:
            if skill not in resume_lower:
                missing_skills.append(skill)

        # -------------------------------------------------
        # SMART JOB MATCH SCORE
        # -------------------------------------------------

        if job_skills:

            # Skill matching = 50%
            skill_match = (
                len(matched_skills) / len(job_skills)
            ) * 50

            # Projects / experience = 20%
            experience_score = 0

            if "experience" in resume_lower:
                experience_score += 10

            if "project" in resume_lower or "projects" in resume_lower:
                experience_score += 10

            # Education = 15%
            education_score = 0

            if (
                "education" in resume_lower
                or "b.e" in resume_lower
                or "btech" in resume_lower
                or "b.tech" in resume_lower
                or "degree" in resume_lower
                or "university" in resume_lower
                or "college" in resume_lower
            ):
                education_score = 15

            # Resume completeness = 15%
            completeness_score = 0

            if "skills" in resume_lower:
                completeness_score += 5

            if "contact" in resume_lower or "@" in resume_text:
                completeness_score += 5

            if (
                "certification" in resume_lower
                or "certifications" in resume_lower
            ):
                completeness_score += 5

            # Final score
            match_score = (
                skill_match
                + experience_score
                + education_score
                + completeness_score
            )

        else:
            match_score = 0

        # =================================================
        # JOB MATCH SCORE
        # =================================================

        st.subheader("🎯 Job Match Score")

        st.metric(
            "Job Description Match",
            f"{match_score:.1f}%"
        )

        # =================================================
        # REQUIRED SKILLS
        # =================================================

        st.subheader("📌 Skills Required by Job")

        if job_skills:
            st.write(", ".join(job_skills))
        else:
            st.write(
                "No skills from the current skills database "
                "were detected in the job description."
            )

        # =================================================
        # MATCHING SKILLS
        # =================================================

        st.subheader("✅ Matching Skills")

        if matched_skills:
            st.write(", ".join(matched_skills))
        else:
            st.write("No matching skills found.")

        # =================================================
        # MISSING SKILLS
        # =================================================

        st.subheader("❌ Missing Skills")

        if missing_skills:
            st.write(", ".join(missing_skills))
        else:
            st.write("🎉 No detected skills are missing!")

    else:
        st.info(
            "💡 Paste a job description to calculate the job match score."
        )

    # =====================================================
    # RESUME IMPROVEMENT SUGGESTIONS
    # =====================================================

    st.subheader("💡 Resume Improvement Suggestions")

    suggestions = []

    if "project" not in resume_lower:
        suggestions.append(
            "Add a Projects section with relevant academic or personal projects."
        )

    if "github" not in resume_lower:
        suggestions.append(
            "Add your GitHub profile to showcase your projects."
        )

    if "linkedin" not in resume_lower:
        suggestions.append(
            "Add your LinkedIn profile."
        )

    if "experience" not in resume_lower and "internship" not in resume_lower:
        suggestions.append(
            "Add internship, training, or practical experience if applicable."
        )

    if "certification" not in resume_lower:
        suggestions.append(
            "Add relevant certifications and courses."
        )

    if len(resume_text.split()) < 200:
        suggestions.append(
            "Add more relevant details about your education, skills, projects, and achievements."
        )

    if suggestions:
        for suggestion in suggestions:
            st.write("• " + suggestion)
    else:
        st.write(
            "🎉 Your resume contains the major sections we checked."
        )

    # =====================================================
    # SUCCESS MESSAGE
    # =====================================================

    st.success("Analysis completed successfully! 🎉")


# =========================================================
# AI CAREER ASSISTANT
# =========================================================

st.divider()

st.subheader("🤖 AI Career Assistant")

st.write(
    "Ask me anything about your resume, career, jobs, or internships!"
)

user_question = st.chat_input(
    "Ask a question about your career..."
)

if user_question:

    question = user_question.lower()

    # -----------------------------------------------------
    # User message
    # -----------------------------------------------------

    with st.chat_message("user"):
        st.write(user_question)

    # -----------------------------------------------------
    # Career Assistant responses
    # -----------------------------------------------------

    if "resume" in question:
        answer = """
To improve your resume, keep it clear, professional, and easy to read.

Highlight your technical skills, projects, internships,
certifications, education, and achievements.

Use relevant keywords from the job description.
"""

    elif "skill" in question:
        answer = """
For an AI/ML career, focus on Python, SQL, Machine Learning,
Deep Learning, NumPy, Pandas, scikit-learn, Git, and GitHub.

Building practical projects is one of the best ways to strengthen
your profile.
"""

    elif "internship" in question:
        answer = """
To get an AI/ML internship, build 2–3 practical projects,
create a strong resume, maintain a GitHub profile,
and apply regularly for relevant internships.

Also practice Python, SQL, and basic Machine Learning concepts.
"""

    elif "job" in question or "career" in question:
        answer = """
AI/ML students can explore careers such as:

• AI/ML Engineer
• Junior ML Engineer
• AI Engineer
• Data Analyst
• Python Developer
• Data Scientist

Start with Python, data analysis, Machine Learning,
and practical projects.
"""

    elif "python" in question:
        answer = """
Python is one of the most useful programming languages
for AI and Machine Learning.

Start with:

• Variables and data types
• Conditions and loops
• Functions
• OOP
• File handling
• NumPy
• Pandas
• Machine Learning libraries
"""

    elif "github" in question:
        answer = """
GitHub is useful for showcasing your projects to recruiters.

Keep your repositories organized and add a README explaining:

• Project purpose
• Technologies used
• Features
• Installation steps
• How to run the project
"""

    elif "project" in question:
        answer = """
Good AI/ML project ideas include:

• AI Resume Analyzer
• Recommendation System
• Sentiment Analysis
• Spam Detection
• Student Performance Prediction
• Fake News Detection
• Image Classification
• Chatbot
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

Try asking:

"What skills should I learn for an AI/ML internship?"
"""

    # -----------------------------------------------------
    # Assistant message
    # -----------------------------------------------------

    with st.chat_message("assistant"):
        st.write(answer)
