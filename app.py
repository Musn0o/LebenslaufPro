import streamlit as st
import json
import os
import datetime
from PIL import Image
from streamlit_cropper import st_cropper
from llm_manager import translate_and_format_cv, parse_existing_cv
from generator import generate_mappe

st.set_page_config(
    page_title="LebenslaufPro - AI German CV Maker",
    page_icon="📄",
    layout="wide"
)

# Initialize Session State
if 'step' not in st.session_state:
    st.session_state.step = 0

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'options': {
            'generate_cover_letter': True,
            'template': 'classic'
        },
        'company': {},
        'personal': {},
        'experience': [],
        'education': [],
        'skills': [],
        'languages': [],
        'links': [],
        'hobbies': [],
        'photo': None,
    }
    
if 'attachments_paths' not in st.session_state:
    st.session_state.attachments_paths = []

if 'ai_output' not in st.session_state:
    st.session_state.ai_output = None

if 'mappe_path' not in st.session_state:
    st.session_state.mappe_path = None

if 'prefilled' not in st.session_state:
    st.session_state.prefilled = False

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def main():
    st.title("LebenslaufPro 📄")
    st.markdown("### Your AI-Powered German Job Application Builder")
    
    # Check for API key
    if not st.secrets.get("GEMINI_API_KEY") and not os.environ.get("GEMINI_API_KEY"):
        st.warning("⚠️ Gemini API Key not found. Please set GEMINI_API_KEY in .streamlit/secrets.toml")
        
    # High-visibility warning if pre-filled
    if st.session_state.prefilled:
        st.markdown(
            """
            <div style="background-color: #ff4b4b; padding: 20px; border-radius: 10px; border: 3px solid #ffffff; margin-bottom: 25px;">
                <h2 style="color: white; margin: 0; text-align: center;">⚠️ ACTION REQUIRED: VERIFY YOUR DATA</h2>
                <p style="color: white; font-size: 1.2rem; text-align: center; margin-top: 10px;">
                    Our AI has pre-filled the form from your uploaded CV. <b>Please carefully verify all information</b> in the following steps before generating the final document.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # Progress bar
    progress = st.progress(st.session_state.step / 6)
    
    steps = ["General Options", "Personal Info", "Experience", "Education", "Skills, Links & Hobbies", "Attachments", "Review & Generate"]
    st.markdown(f"**Step {st.session_state.step}:** {steps[st.session_state.step]}")
    st.divider()

    if st.session_state.step == 0:
        step_options()
    elif st.session_state.step == 1:
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

def step_options():
    st.header("1. General Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("What do you want to generate?")
        doc_type = st.radio(
            "Select Document Type", 
            ["CV & Cover Letter (Lebenslauf & Anschreiben)", "Only CV (Nur Lebenslauf)"],
            index=0 if st.session_state.user_data['options']['generate_cover_letter'] else 1
        )
        st.session_state.user_data['options']['generate_cover_letter'] = "Cover Letter" in doc_type
        
        st.subheader("Design Template")
        st.markdown("Wähle ein Layout für deine Bewerbungsmappe:")
        col_a, col_b, col_c = st.columns(3)
        
        templates = [
            {"key": "classic", "name": "Classic Professional", "desc": "Clean B&W, serifenlos, standard", "badge": "🖤🤍", "color": "#ffffff", "text_color": "#333333", "border_color": "#999999"},
            {"key": "modern", "name": "Modern Minimal", "desc": "Dunkelblaue Seitenleiste", "badge": "💙⬜", "color": "#1a5f7a", "text_color": "#ffffff", "border_color": "#1a5f7a"},
            {"key": "executive", "name": "Executive Sleek", "desc": "Edelstahl-Akzente (Anthrazit)", "badge": "⬛⬜", "color": "#333333", "text_color": "#ffffff", "border_color": "#333333"},
        ]
        
        for idx, (col, tmpl) in enumerate(zip([col_a, col_b, col_c], templates)):
            is_selected = st.session_state.user_data['options']['template'] == tmpl["key"]
            with col:
                border_style = f"3px solid #4CAF50" if is_selected else f"1px solid {tmpl['border_color']}"
                bg_accent = tmpl["color"]
                fg_accent = tmpl["text_color"]
                
                st.markdown(f"""
                <div style="border: {border_style}; border-radius: 10px; padding: 0; text-align: center; 
                            background: white; margin-bottom: 6px; overflow: hidden; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                    <div style="height: 100px; background: {bg_accent}; display: flex; align-items: center; 
                                justify-content: center; font-size: 32px; color: {fg_accent};">
                        {tmpl['badge']}
                    </div>
                    <div style="padding: 10px 8px;">
                        <div style="font-weight: bold; font-size: 13px; color: #222;">{tmpl['name']}</div>
                        <div style="font-size: 11px; color: #666; margin-top: 4px;">{tmpl['desc']}</div>
                        { '✅ <div style="color: #2e7d32; font-size: 12px; font-weight: bold; margin-top: 6px; border: 1px solid #2e7d32; border-radius: 4px; padding: 2px 0;">Ausgewählt</div>' if is_selected else '' }
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Select {tmpl['name']}", key=f"tmpl_btn_{idx}", use_container_width=True):
                    st.session_state.user_data['options']['template'] = tmpl["key"]
                    st.rerun()

    with col2:
        st.subheader("Fast-Track: Pre-fill from existing CV")
        st.write("Upload your old CV and our AI will extract the data for you!")
        uploaded_cv = st.file_uploader("Upload CV (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])
        
        if uploaded_cv and not st.session_state.prefilled:
            if st.button("✨ Extract Info & Pre-fill Form"):
                with st.spinner("AI is reading your CV..."):
                    try:
                        file_bytes = uploaded_cv.read()
                        mime_type = uploaded_cv.type
                        extracted_json = parse_existing_cv(file_bytes, mime_type)
                        
                        # Clean up JSON
                        if "```json" in extracted_json:
                            extracted_json = extracted_json.split("```json")[1].split("```")[0].strip()
                        elif "```" in extracted_json:
                            extracted_json = extracted_json.split("```")[1].split("```")[0].strip()
                            
                        parsed_data = json.loads(extracted_json)
                        
                        # Merge extracted data into session state
                        for key in parsed_data:
                            if key in st.session_state.user_data:
                                st.session_state.user_data[key] = parsed_data[key]
                        
                        st.session_state.prefilled = True
                        st.success("Information extracted successfully! Please proceed to the next steps to verify.")
                        st.rerun()
                    except Exception as e:
                        err_msg = str(e)
                        if "||" in err_msg:
                            _, user_message = err_msg.split("||", 1)
                            st.error(user_message)
                        else:
                            st.error(f"❌ Der Lebenslauf konnte nicht gelesen werden: {err_msg}")

    if st.session_state.user_data['options']['generate_cover_letter']:
        st.divider()
        st.subheader("Target Company Information")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.user_data['company']['name'] = st.text_input("Company Name", st.session_state.user_data['company'].get('name', ''))
            st.session_state.user_data['company']['job_title'] = st.text_input("Target Job Title", st.session_state.user_data['company'].get('job_title', ''))
        with col2:
            st.session_state.user_data['company']['address'] = st.text_area("Company Address", st.session_state.user_data['company'].get('address', ''))
            st.session_state.user_data['company']['contact_person'] = st.text_input("Contact Person (Optional)", st.session_state.user_data['company'].get('contact_person', ''))

    st.write("")
    missing = []
    if st.session_state.user_data['options']['generate_cover_letter']:
        if not st.session_state.user_data['company'].get('name', '').strip():
            missing.append("Firmenname (Company Name)")
        if not st.session_state.user_data['company'].get('job_title', '').strip():
            missing.append("Stellentitel (Job Title)")
    
    if st.button("Continue to Personal Info ➡️") or st.session_state.get('_force_continue', False):
        if missing:
            st.error(f"⚠️ Bitte fülle die folgenden Pflichtfelder aus: {', '.join(missing)}")
            st.session_state['_force_continue'] = False
        else:
            st.session_state['_force_continue'] = False
            next_step()
            st.rerun()

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
        
        # Parse birth date from pre-filled string if available
        default_birth = None
        if st.session_state.user_data['personal'].get('birth_date'):
            try:
                default_birth = datetime.datetime.strptime(st.session_state.user_data['personal']['birth_date'], "%d.%m.%Y").date()
            except:
                pass
                
        birth_date = st.date_input("Date of Birth", value=default_birth, min_value=datetime.date(1950, 1, 1))
        if birth_date:
            st.session_state.user_data['personal']['birth_date'] = birth_date.strftime("%d.%m.%Y")
            
        st.session_state.user_data['personal']['birth_place'] = st.text_input("Place of Birth", st.session_state.user_data['personal'].get('birth_place', ''))

    st.subheader("Biometric Photo")
    uploaded_photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
    
    if uploaded_photo:
        img = Image.open(uploaded_photo)
        st.write("Crop your photo (3:4 ratio):")
        cropped_img = st_cropper(img, aspect_ratio=(3, 4), box_color='#0000FF')
        if cropped_img:
            cropped_img.convert('RGB').save("photo.jpg")
            st.session_state.user_data['photo'] = "photo.jpg"
            st.success("Photo cropped and saved!")

    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next: Experience ➡️"):
            next_step()
            st.rerun()

def step_experience():
    st.header("Work Experience")
    exp_list = st.session_state.user_data['experience']
    
    with st.expander("Add New Experience", expanded=len(exp_list) == 0):
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.text_input("Start Date (e.g. 05/2020)")
        with col2:
            end_date = st.text_input("End Date (e.g. Present)")
        description = st.text_area("Description")
        
        if st.button("Add Experience"):
            if job_title and company:
                exp_list.append({"job_title": job_title, "company": company, "start_date": start_date, "end_date": end_date, "description": description})
                st.rerun()
                
    st.subheader("Current Entries:")
    for i, exp in enumerate(exp_list):
        col_main, col_btn = st.columns([6, 1])
        with col_main:
            st.write(f"**{exp['job_title']}** at {exp['company']} ({exp['start_date']} - {exp['end_date']})")
        with col_btn:
            if st.button(f"Remove", key=f"rm_exp_{i}"):
                exp_list.pop(i)
                st.rerun()

    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next: Education ➡️"):
            next_step()
            st.rerun()

def step_education():
    st.header("Education")
    edu_list = st.session_state.user_data['education']
    
    with st.expander("Add New Education", expanded=len(edu_list) == 0):
        degree = st.text_input("Degree / Program")
        institution = st.text_input("Institution")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.text_input("Start Date (e.g. 09/2018)", key="edu_start")
        with col2:
            end_date = st.text_input("End Date (e.g. 06/2022)", key="edu_end")
        description = st.text_area("Description / Grades", key="edu_desc")
        
        if st.button("Add Education"):
            if degree and institution:
                edu_list.append({"degree": degree, "institution": institution, "start_date": start_date, "end_date": end_date, "description": description})
                st.rerun()
                
    st.subheader("Current Entries:")
    for i, edu in enumerate(edu_list):
        col_main, col_btn = st.columns([6, 1])
        with col_main:
            st.write(f"**{edu['degree']}** at {edu['institution']} ({edu['start_date']} - {edu['end_date']})")
        with col_btn:
            if st.button(f"Remove", key=f"rm_edu_{i}"):
                edu_list.pop(i)
                st.rerun()

    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next: Skills ➡️"):
            next_step()
            st.rerun()

def step_skills():
    st.header("Languages, Skills, Links & Hobbies")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Languages")
        lang_list = st.session_state.user_data['languages']
        with st.expander("Add Language"):
            language = st.text_input("Language")
            level_desc = st.text_input("Level (Native/Fluent/Basic)")
            if st.button("Add Language"):
                if language:
                    lang_list.append({"language": language, "level_desc": level_desc})
                    st.rerun()
        for i, l in enumerate(lang_list):
            col_l, col_r = st.columns([4, 1])
            col_l.write(f"- {l['language']} ({l['level_desc']})")
            if col_r.button("X", key=f"rm_lang_{i}"):
                lang_list.pop(i)
                st.rerun()
                
        st.subheader("Profile Links")
        link_list = st.session_state.user_data['links']
        with st.expander("Add Link"):
            platform = st.text_input("Platform (LinkedIn, GitHub)")
            url = st.text_input("URL")
            if st.button("Add Link"):
                if platform and url:
                    link_list.append({"platform": platform, "url": url})
                    st.rerun()
        for i, l in enumerate(link_list):
            col_l, col_r = st.columns([4, 1])
            col_l.write(f"- {l['platform']}: {l['url']}")
            if col_r.button("X", key=f"rm_link_{i}"):
                link_list.pop(i)
                st.rerun()

    with col2:
        st.subheader("IT & Other Skills")
        skill_list = st.session_state.user_data['skills']
        with st.expander("Add Skill"):
            skill_name = st.text_input("Skill")
            s_level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced", "Expert"])
            if st.button("Add Skill"):
                if skill_name:
                    skill_list.append({"skill_name": skill_name, "level": s_level})
                    st.rerun()
        for i, s in enumerate(skill_list):
            col_l, col_r = st.columns([4, 1])
            col_l.write(f"- {s['skill_name']} ({s['level']})")
            if col_r.button("X", key=f"rm_skill_{i}"):
                skill_list.pop(i)
                st.rerun()
                
        st.subheader("Hobbies & Interests")
        hobby_list = st.session_state.user_data['hobbies']
        with st.expander("Add Hobby"):
            hobby = st.text_input("Hobby")
            if st.button("Add Hobby"):
                if hobby:
                    hobby_list.append(hobby)
                    st.rerun()
        for i, h in enumerate(hobby_list):
            col_l, col_r = st.columns([4, 1])
            col_l.write(f"- {h}")
            if col_r.button("X", key=f"rm_hobby_{i}"):
                hobby_list.pop(i)
                st.rerun()

    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next: Attachments ➡️"):
            next_step()
            st.rerun()

def step_attachments():
    st.header("Attachments (Anlagen)")
    uploaded_files = st.file_uploader("Choose Files (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state.attachments_paths = []
        for uf in uploaded_files:
            if uf.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = f"temp_{uf.name.split('.')[0]}.pdf"
                img = Image.open(uf).convert('RGB')
                img.save(file_path)
            else:
                file_path = f"temp_{uf.name}"
                with open(file_path, "wb") as f:
                    f.write(uf.getbuffer())
            st.session_state.attachments_paths.append(file_path)
        st.success(f"Uploaded {len(uploaded_files)} files.")

    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next: Review ➡️"):
            next_step()
            st.rerun()

def step_review():
    st.header("Review & Generate")
    with st.expander("View Collected Data"):
        st.json(st.session_state.user_data)

    # Validate required fields before generation
    personal = st.session_state.user_data.get('personal', {})
    missing = []
    if not personal.get('first_name', '').strip():
        missing.append("Vorname (First Name)")
    if not personal.get('last_name', '').strip():
        missing.append("Nachname (Last Name)")
    if not personal.get('email', '').strip():
        missing.append("E-Mail")
    if st.session_state.user_data['options'].get('generate_cover_letter', False):
        company = st.session_state.user_data.get('company', {})
        if not company.get('name', '').strip():
            missing.append("Firmenname (Company Name)")
        if not company.get('job_title', '').strip():
            missing.append("Stellentitel (Job Title)")

    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
            st.rerun()
            
    with col2:
        if st.button("✨ Generate German Application", type="primary"):
            if missing:
                st.error(f"⚠️ Bitte fülle alle Pflichtfelder aus: {', '.join(missing)}")
                st.stop()
            with st.spinner("✨ Creating your professional German application..."):
                try:
                    # 1. AI Translation
                    result_json_str = translate_and_format_cv(st.session_state.user_data)
                    
                    if "```json" in result_json_str:
                        result_json_str = result_json_str.split("```json")[1].split("```")[0].strip()
                    elif "```" in result_json_str:
                        result_json_str = result_json_str.split("```")[1].split("```")[0].strip()
                        
                    st.session_state.ai_output = json.loads(result_json_str)
                    
                    if st.session_state.user_data.get('photo'):
                        st.session_state.ai_output['personal']['photo'] = st.session_state.user_data['photo']
                    
                    # 2. PDF Generation
                    st.session_state.mappe_path = generate_mappe(
                        st.session_state.ai_output, 
                        st.session_state.attachments_paths,
                        st.session_state.user_data['options']['generate_cover_letter'],
                        st.session_state.user_data['options']['template']
                    )
                    st.balloons()
                    st.success("Successfully generated!")
                except json.JSONDecodeError:
                    st.error("⚠️ Die KI hat ein unerwartetes Format zurückgegeben. Bitte klicke erneut auf den Button.")
                except Exception as e:
                    err_msg = str(e)
                    if "||" in err_msg:
                        _, user_message = err_msg.split("||", 1)
                        st.error(user_message)
                    elif "429" in err_msg or "quota" in err_msg.lower():
                        st.error("⏳ Der KI-Dienst ist gerade ausgelastet. Bitte warte etwa 30 Sekunden und versuche es erneut.")
                    elif "invalid" in err_msg.lower() or "api_key" in err_msg.lower():
                        st.error("🔑 Es gibt ein Problem mit der KI-Konfiguration. Bitte überprüfe deinen API-Schlüssel.")
                    else:
                        st.error(f"❌ Es gab ein kleines Problem bei der Verbindung mit der KI: {err_msg}. Bitte versuche es erneut.")

    if st.session_state.mappe_path and os.path.exists(st.session_state.mappe_path):
        st.success("Your Bewerbungsmappe is ready!")
        with open(st.session_state.mappe_path, "rb") as f:
            st.download_button(label="⬇️ Download Bewerbungsmappe (PDF)", data=f, file_name="Bewerbungsmappe.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
