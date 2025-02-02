import streamlit as st
from jinja2 import Template
from fpdf import FPDF
import tempfile

# Define a basic resume template
TEMPLATE = """
{{ name }}
{{ email }} | {{ phone }} | {{ linkedin }}

### Summary
{{ summary }}

### Experience
{% for job in experience %}
- **{{ job.position }} at {{ job.company }}** ({{ job.duration }})
  - {{ job.description }}
{% endfor %}

### Education
{% for edu in education %}
- **{{ edu.degree }} in {{ edu.field }}** at {{ edu.institution }} ({{ edu.year }})
{% endfor %}

### Skills
{{ skills }}
"""

# Streamlit UI
def main():
    st.title("📄 AI Resume Generator")
    st.subheader("Fill in the details below to generate your resume")

    # User input fields
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn Profile")
    summary = st.text_area("Summary")

    # Experience input
    experience = []
    num_experience = st.number_input("Number of Job Experiences", min_value=0, step=1)
    for i in range(int(num_experience)):
        st.subheader(f"Job {i+1}")
        position = st.text_input(f"Job {i+1} - Position")
        company = st.text_input(f"Job {i+1} - Company")
        duration = st.text_input(f"Job {i+1} - Duration")
        description = st.text_area(f"Job {i+1} - Description")
        experience.append({"position": position, "company": company, "duration": duration, "description": description})

    # Education input
    education = []
    num_education = st.number_input("Number of Educational Qualifications", min_value=0, step=1)
    for i in range(int(num_education)):
        st.subheader(f"Education {i+1}")
        degree = st.text_input(f"Education {i+1} - Degree")
        field = st.text_input(f"Education {i+1} - Field of Study")
        institution = st.text_input(f"Education {i+1} - Institution")
        year = st.text_input(f"Education {i+1} - Year of Completion")
        education.append({"degree": degree, "field": field, "institution": institution, "year": year})
    
    skills = st.text_area("Skills (comma-separated)")

    if st.button("Generate Resume"):
        filled_template = Template(TEMPLATE).render(
            name=name, email=email, phone=phone, linkedin=linkedin,
            summary=summary, experience=experience, education=education, skills=skills
        )
        pdf_file = generate_pdf(filled_template)
        st.download_button("Download Resume PDF", pdf_file, file_name="resume.pdf", mime="application/pdf")

# PDF Generator
def generate_pdf(content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        return tmpfile.name

if __name__ == "__main__":
    main()
