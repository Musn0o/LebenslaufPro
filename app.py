import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="LebenslaufPro - AI German CV Maker",
    page_icon="📄",
    layout="wide"
)

# Initialize Session State
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'personal': {},
        'experience': [],
        'education': [],
        'skills': [],
        'languages': [],
        'links': [],
        'photo': None,
        'attachments': []
    }

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def main():
    st.title("LebenslaufPro 📄")
    st.markdown("### Your AI-Powered German Job Application Builder")
    
    # Progress bar
    progress = st.progress((st.session_state.step - 1) / 5)
    
    steps = ["Personal Info", "Experience", "Education", "Skills & Links", "Attachments", "Review & Generate"]
    st.markdown(f"**Step {st.session_state.step} of 6:** {steps[st.session_state.step - 1]}")
    st.divider()

    if st.session_state.step == 1:
        step_personal_info()
    elif st.session_state.step == 2:
        step_experience()
    elif st.session_state.step == 3:
        step_education()
    elif st.session_state.step == 4:
        step_skills()
    elif st.session_state.step == 5:
        step_attachments()
    elif st.session_state.step == 6:
        step_review()

def step_personal_info():
    st.header("Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.user_data['personal']['first_name'] = st.text_input("First Name", st.session_state.user_data['personal'].get('first_name', ''))
        st.session_state.user_data['personal']['last_name'] = st.text_input("Last Name", st.session_state.user_data['personal'].get('last_name', ''))
        st.session_state.user_data['personal']['email'] = st.text_input("Email", st.session_state.user_data['personal'].get('email', ''))
        st.session_state.user_data['personal']['phone'] = st.text_input("Phone Number", st.session_state.user_data['personal'].get('phone', ''))
        
    with col2:
        st.session_state.user_data['personal']['address'] = st.text_input("Street Address", st.session_state.user_data['personal'].get('address', ''))
        st.session_state.user_data['personal']['postal_code'] = st.text_input("Postal Code / City", st.session_state.user_data['personal'].get('postal_code', ''))
        st.session_state.user_data['personal']['birth_date'] = st.date_input("Date of Birth", st.session_state.user_data['personal'].get('birth_date', None))
        st.session_state.user_data['personal']['birth_place'] = st.text_input("Place of Birth", st.session_state.user_data['personal'].get('birth_place', ''))

    st.subheader("Biometric Photo")
    st.info("German CVs standardly include a professional portrait photo. Upload and crop yours below.")
    uploaded_photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
    
    # TODO: Implement streamlit-cropper here
    if uploaded_photo:
        st.success("Photo uploaded! Cropping feature coming soon.")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Next ➡️"):
            next_step()
            st.rerun()

def step_experience():
    st.header("Work Experience")
    st.write("Add your previous working places and descriptions.")
    
    # Placeholder for dynamic list
    st.info("Dynamic list implementation coming soon.")

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next ➡️"):
            next_step()
            st.rerun()

def step_education():
    st.header("Education")
    st.write("Add your educational background and grades.")
    
    st.info("Dynamic list implementation coming soon.")

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next ➡️"):
            next_step()
            st.rerun()

def step_skills():
    st.header("Languages, Skills & Profiles")
    
    st.info("Skill input and profile links coming soon.")

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next ➡️"):
            next_step()
            st.rerun()

def step_attachments():
    st.header("Attachments (Anlagen)")
    st.write("Upload your certificates, degrees, and work references (PDF only).")
    
    st.info("File upload coming soon.")

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next ➡️"):
            next_step()
            st.rerun()

def step_review():
    st.header("Review & Generate")
    st.write("Review your data before sending it to the AI for processing and PDF generation.")
    
    st.json(st.session_state.user_data)

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("✨ Generate German Application"):
            st.success("Generation process will start here.")

if __name__ == "__main__":
    main()
