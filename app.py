
import streamlit as st
import pymupdf
import re
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS - PURPLE SAAS DESIGN
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #f8f7ff, #f1efff);
    font-family: 'Inter', sans-serif;
    color: #211b3a;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #21134d, #392078);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

h1 {
    color: #24164d !important;
    font-size: 38px !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #30205d !important;
}

p, label {
    color: #51466e;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e7defe;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 5px 20px rgba(75, 45, 130, 0.07);
}

div[data-testid="stMetricLabel"] {
    color: #71648f;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #6d3bd1;
    font-weight: 800;
}

.stButton > button {
    background: linear-gradient(90deg, #7139d4, #a044e8);
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 12px 25px;
    font-weight: 700;
    width: 100%;
    min-height: 45px;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #5723b5, #8528d5);
    box-shadow: 0 5px 15px rgba(112, 57, 212, 0.3);
}

.stDownloadButton > button {
    background: #30205d;
    color: white !important;
    border-radius: 10px;
    width: 100%;
}

div[data-testid="stFileUploader"] {
    background: white;
    border: 2px dashed #a78bfa;
    border-radius: 15px;
    padding: 15px;
}

textarea {
    background: white !important;
    border-radius: 12px !important;
}

div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #7139d4, #bc70ed);
}

.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e8e0fa;
    box-shadow: 0 5px 20px rgba(75, 45, 130, 0.06);
    margin-bottom: 15px;
}

.hero {
    background: linear-gradient(110deg, #392078, #7139d4, #a044e8);
    padding: 30px;
    border-radius: 20px;
    color: white !important;
    margin-bottom: 25px;
}

.hero h2, .hero p {
    color: white !important;
}

.score-circle {
    width: 175px;
    height: 175px;
    border-radius: 50%;
    margin: 15px auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 10px solid #eee7fc;
    background: white;
    box-shadow: 0 5px 25px rgba(112, 57, 212, 0.12);
}

.score-number {
    font-size: 42px;
    font-weight: 800;
    color: #7139d4;
}

.score-label {
    color: #75688f;
    font-size: 13px;
}

.skill-tag {
    display: inline-block;
    background: #f0eaff;
    color: #6633bd;
    padding: 9px 14px;
    border-radius: 8px;
    margin: 5px;
    font-size: 13px;
    font-weight: 600;
}

.missing-tag {
    display: inline-block;
    background: #fff0ed;
    color: #d44b40;
    padding: 9px 14px;
    border-radius: 8px;
    margin: 5px;
    font-size: 13px;
    font-weight: 600;
}

#MainMenu, footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 🤖 ResumeAI")

    st.caption("SMART CAREER ASSISTANT")

    st.divider()

    st.markdown("### Navigation")

    st.markdown("📊 Dashboard")
    st.markdown("📄 Resume Analyzer")
    st.markdown("💼 Job Matching")
    st.markdown("📈 Skill Insights")
    st.markdown("📥 Reports")

    st.divider()

    st.markdown("### About Project")

    st.write(
        "AI-powered resume analysis platform "
        "that helps candidates improve their "
        "job application performance."
    )

    st.divider()

    st.caption("Developed using Python & Streamlit")

    st.caption("Version 2.0")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h2>Welcome to ResumeAI 👋</h2>
    <p>
        Analyze your resume, discover skill gaps
        and improve your chances of getting hired.
    </p>
</div>
""", unsafe_allow_html=True)

st.title("AI Resume Analyzer")

st.write(
    "Upload your resume and compare it with "
    "your desired job description."
)

# --------------------------------------------------
# SKILLS DATABASE
# --------------------------------------------------

skills_list = [
    "Python", "Java", "SQL", "HTML", "CSS",
    "JavaScript", "Machine Learning",
    "Data Analysis", "Git", "GitHub",
    "Flask", "Django", "Streamlit",
    "Pandas", "NumPy", "Scikit-learn",
    "TensorFlow", "PyTorch", "React",
    "Node.js", "C", "C++", "MongoDB",
    "MySQL", "PostgreSQL", "REST API",
    "Docker", "AWS", "Linux",
    "Deep Learning", "Power BI",
    "Excel", "Tableau"
]


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

st.markdown("## 📄 Upload Your Resume")

col1, col2 = st.columns([1, 1])

with col1:

    st.markdown("### Resume Upload")

    uploaded_file = st.file_uploader(
        "Choose your resume PDF",
        type=["pdf"]
    )

with col2:

    st.markdown("### Job Description")

    job_description = st.text_area(
        "Paste the job description:",
        height=150,
        placeholder=(
            "Enter job role, required skills, "
            "qualifications and responsibilities..."
        )
    )


# --------------------------------------------------
# ANALYZE RESUME
# --------------------------------------------------

if st.button("🚀 Analyze My Resume"):

    if uploaded_file is None:

        st.error("Please upload your resume first.")

    elif not job_description.strip():

        st.warning("Please enter a job description.")

    else:

        try:

            # Extract PDF text

            pdf_document = pymupdf.open(
                stream=uploaded_file.getvalue(),
                filetype="pdf"
            )

            resume_text = ""

            for page in pdf_document:
                resume_text += page.get_text()

            pdf_document.close()

            if not resume_text.strip():

                st.error(
                    "No readable text found. "
                    "Please upload a text-based PDF."
                )

                st.stop()

            # ------------------------------------------
            # SKILL DETECTION
            # ------------------------------------------

            def contains_skill(text, skill):

                pattern = (
                    r"(?<![a-zA-Z0-9+#])"
                    + re.escape(skill).replace(r"\ ", r"\s+")
                    + r"(?![a-zA-Z0-9+#])"
                )

                return bool(
                    re.search(pattern, text, re.IGNORECASE)
                )

            detected_skills = [
                skill for skill in skills_list
                if contains_skill(resume_text, skill)
            ]

            required_skills = [
                skill for skill in skills_list
                if contains_skill(job_description, skill)
            ]

            matched_skills = [
                skill for skill in required_skills
                if skill in detected_skills
            ]

            missing_skills = [
                skill for skill in required_skills
                if skill not in matched_skills
            ]

            # ------------------------------------------
            # SKILL MATCH SCORE - 70%
            # ------------------------------------------

            if required_skills:

                skill_score = (
                    len(matched_skills)
                    / len(required_skills)
                ) * 100

            else:

                skill_score = 0

            # ------------------------------------------
            # KEYWORD MATCH SCORE - 20%
            # ------------------------------------------

            stop_words = {
                "the", "and", "for", "with", "from",
                "that", "this", "are", "you", "will",
                "have", "has", "our", "your", "job",
                "role", "work", "years", "using",
                "ability", "knowledge", "experience",
                "required", "responsibilities",
                "develop", "working", "team",
                "candidate", "looking", "strong"
            }

            job_words = set(
                re.findall(
                    r"\b[a-zA-Z][a-zA-Z+#.]{1,}\b",
                    job_description.lower()
                )
            ) - stop_words

            resume_words = set(
                re.findall(
                    r"\b[a-zA-Z][a-zA-Z+#.]{1,}\b",
                    resume_text.lower()
                )
            )

            if job_words:

                keyword_score = (
                    len(job_words & resume_words)
                    / len(job_words)
                ) * 100

            else:

                keyword_score = 0

            # ------------------------------------------
            # EDUCATION SCORE - 10%
            # ------------------------------------------

            education_keywords = [
                "b.tech", "bachelor", "b.e.",
                "computer science", "m.tech",
                "master", "degree"
            ]

            required_education = [
                word for word in education_keywords
                if word in job_description.lower()
            ]

            if not required_education:

                education_score = 100

            elif any(
                word in resume_text.lower()
                for word in required_education
            ):

                education_score = 100

            else:

                education_score = 0

            # ------------------------------------------
            # FINAL ATS SCORE
            # ------------------------------------------

            match_score = round(
                skill_score * 0.70
                + keyword_score * 0.20
                + education_score * 0.10,
                2
            )

            # ------------------------------------------
            # STORE RESULTS
            # ------------------------------------------

            st.session_state["analysis"] = {
                "resume_text": resume_text,
                "detected_skills": detected_skills,
                "required_skills": required_skills,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "skill_score": skill_score,
                "keyword_score": keyword_score,
                "education_score": education_score,
                "match_score": match_score
            }

        except Exception as e:

            st.error(f"Error processing resume: {e}")


# --------------------------------------------------
# DISPLAY ANALYSIS RESULTS
# --------------------------------------------------

if "analysis" in st.session_state:

    result = st.session_state["analysis"]

    match_score = result["match_score"]

    skill_score = result["skill_score"]

    keyword_score = result["keyword_score"]

    education_score = result["education_score"]

    detected_skills = result["detected_skills"]

    required_skills = result["required_skills"]

    matched_skills = result["matched_skills"]

    missing_skills = result["missing_skills"]

    st.divider()

    st.markdown("## 📊 ATS Resume Analysis")

    # ------------------------------------------
    # ATS SCORE
    # ------------------------------------------

    col1, col2 = st.columns([1, 2])

    with col1:

        st.markdown(
            f"""
            <div class="card" style="text-align:center;">
                <h3>Overall ATS Score</h3>
                <div class="score-circle">
                    <div class="score-number">
                        {match_score}%
                    </div>
                    <div class="score-label">
                        Resume Match
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown("### Your Resume Performance")

        st.progress(int(match_score))

        if match_score >= 80:

            st.success(
                "Excellent! Your resume is a strong match."
            )

        elif match_score >= 60:

            st.info(
                "Good match! A few improvements are needed."
            )

        else:

            st.warning(
                "Your resume needs improvement for this job."
            )

        st.write(
            "This score is an estimated match based on "
            "skills, keywords and education."
        )

    # ------------------------------------------
    # THREE ANALYTICS CARDS
    # ------------------------------------------

    st.markdown("## 📈 Matching Analytics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Skill Match",
        f"{skill_score:.1f}%"
    )

    col2.metric(
        "Keyword Match",
        f"{keyword_score:.1f}%"
    )

    col3.metric(
        "Education Match",
        f"{education_score:.1f}%"
    )

    # ------------------------------------------
    # DETECTED SKILLS
    # ------------------------------------------

    st.markdown("## 🧠 Technical Skills Detected")

    if detected_skills:

        tags = "".join(
            f'<span class="skill-tag">{skill}</span>'
            for skill in detected_skills
        )

        st.markdown(
            f'<div class="card">{tags}</div>',
            unsafe_allow_html=True
        )

    else:

        st.warning("No technical skills detected.")

    # ------------------------------------------
    # MATCHED SKILLS
    # ------------------------------------------

    st.markdown("## ✅ Matched Skills")

    if matched_skills:

        tags = "".join(
            f'<span class="skill-tag">✓ {skill}</span>'
            for skill in matched_skills
        )

        st.markdown(
            f'<div class="card">{tags}</div>',
            unsafe_allow_html=True
        )

    else:

        st.warning("No matching skills found.")

    # ------------------------------------------
    # MISSING SKILLS
    # ------------------------------------------

    st.markdown("## ⚠️ Missing Skills")

    if missing_skills:

        tags = "".join(
            f'<span class="missing-tag">+ {skill}</span>'
            for skill in missing_skills
        )

        st.markdown(
            f'<div class="card">{tags}</div>',
            unsafe_allow_html=True
        )

    else:

        st.success("All identified technical skills are present!")

    # ------------------------------------------
    # IMPROVEMENT SUGGESTIONS
    # ------------------------------------------

    st.markdown("## 💡 Improvement Suggestions")

    if missing_skills:

        for skill in missing_skills:

            st.write(
                f"📌 Learn and demonstrate **{skill}** "
                "in your resume."
            )

    if keyword_score < 70:

        st.write(
            "📌 Include more relevant keywords "
            "from the job description."
        )

    if education_score < 100:

        st.write(
            "📌 Highlight your relevant educational qualifications."
        )

    if not missing_skills and keyword_score >= 70 and education_score == 100:

        st.success(
            "Your resume covers the identified requirements."
        )

    # ------------------------------------------
    # EXTRACTED RESUME TEXT
    # ------------------------------------------

    with st.expander("📄 View Extracted Resume Text"):

        st.text_area(
            "Resume Content",
            result["resume_text"],
            height=250,
            disabled=True
        )

    # ------------------------------------------
    # DOWNLOAD REPORT
    # ------------------------------------------

    st.markdown("## 📥 Download Analysis Report")

    report = f"""
AI RESUME ANALYZER
=====================================

Date: {datetime.now().strftime("%d-%m-%Y %H:%M")}

OVERALL ATS MATCH SCORE: {match_score}%

-------------------------------------

SKILL MATCH: {skill_score:.2f}%
KEYWORD MATCH: {keyword_score:.2f}%
EDUCATION MATCH: {education_score:.2f}%

-------------------------------------

DETECTED SKILLS:
{', '.join(detected_skills)}

MATCHED SKILLS:
{', '.join(matched_skills)}

MISSING SKILLS:
{', '.join(missing_skills)}

-------------------------------------

RECOMMENDATIONS:

{chr(10).join('- Improve ' + skill for skill in missing_skills)
 if missing_skills else '- All identified technical skills are present.'}

Note: This is an estimated resume matching score,
not a guarantee of ATS selection or interview shortlisting.
"""

    st.download_button(
        label="📥 Download Resume Analysis Report",
        data=report,
        file_name="AI_Resume_Analysis_Report.txt",
        mime="text/plain"
    )

    st.divider()

    st.caption(
        "ResumeAI | AI-Powered Resume Analysis Platform | Version 2.0"
    )
