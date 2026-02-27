import streamlit as st
from fpdf import FPDF
import tempfile

# ===========================
# Page Title
# ===========================
st.set_page_config(page_title="AI Resume Builder", page_icon="📄")
st.title("Resume Builder")

# ===========================
# User Inputs
# ===========================
st.subheader("Enter Your Details")

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
linkedin = st.text_input("LinkedIn Profile URL (Optional)")
education = st.text_input("Education")
skills = st.text_input("Skills (comma separated)")
projects = st.text_input("Projects (comma separated)")
experience = st.text_input("Experience")
career_goal = st.text_area("Career Goal / Summary")

resume_data = {
    "Name": name,
    "Email": email,
    "Phone": phone,
    "LinkedIn": linkedin,
    "Education": education,
    "Skills": skills,
    "Projects": projects,
    "Experience": experience,
    "Summary": career_goal
}

# ===========================
# 🎨 Colorful PDF Function
# ===========================
def create_colorful_pdf(data, filename="resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # 🎨 Colors
    primary = (41, 128, 185)      # blue
    header_bg = (230, 240, 250)   # light blue
    text_dark = (44, 62, 80)

    # Header background
    pdf.set_fill_color(*header_bg)
    pdf.rect(0, 0, 210, 40, 'F')

    # Name
    pdf.set_text_color(*primary)
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, data["Name"], ln=True, align="C")

    # Contact info
    pdf.set_text_color(*text_dark)
    pdf.set_font("Arial", "", 11)
    contact_line = f"Email: {data['Email']} | Phone: {data['Phone']}"
    if data["LinkedIn"]:
        contact_line += f" | LinkedIn: {data['LinkedIn']}"
    pdf.cell(0, 8, contact_line, ln=True, align="C")
    pdf.ln(5)

    # Section function
    def section(title, content, bullet=False):
        pdf.set_fill_color(*primary)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, title, ln=True, fill=True)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)

        if bullet and content.strip():
            for item in content.split(","):
                pdf.cell(5)
                pdf.multi_cell(0, 7, f"- {item.strip()}")
        else:
            pdf.multi_cell(0, 7, content)

        pdf.ln(2)

    # Sections
    section("SUMMARY", data["Summary"])
    section("EDUCATION", data["Education"])
    section("SKILLS", data["Skills"], bullet=True)
    section("PROJECTS", data["Projects"], bullet=True)
    section("EXPERIENCE", data["Experience"])

    pdf.output(filename)

# ===========================
# Generate PDF Button
# ===========================
if st.button("Generate & Download Colorful PDF"):

    if name.strip() == "":
        st.warning("Please enter at least your name.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_path = tmp.name

        create_colorful_pdf(resume_data, pdf_path)

        st.success("✅ Your colorful resume is ready!")

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download Resume",
                data=f,
                file_name=f"{name}_Resume.pdf",
                mime="application/pdf"
            )
