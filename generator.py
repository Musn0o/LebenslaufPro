import json
import os
import typst
from pypdf import PdfWriter, PdfReader

def compile_typst(data_json_path, template_path, output_pdf_path):
    """Compiles a Typst template into a PDF using the provided data."""
    try:
        # typst python bindings compile function
        typst.compile(template_path, output=output_pdf_path)
        return True
    except Exception as e:
        print(f"Error compiling typst: {e}")
        return False

def generate_mappe(user_data, attachments_paths, generate_cover_letter=True, template_prefix="classic", output_mappe_path="Bewerbungsmappe.pdf"):
    """
    Generates the full application bundle.
    1. Writes user_data to data.json
    2. Conditionally compiles anschreiben.typ to anschreiben.pdf
    3. Compiles lebenslauf.typ to lebenslauf.pdf
    4. Merges into output_mappe_path
    """
    
    # 1. Write data to data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)
        
    # 2. Compile Anschreiben
    anschreiben_pdf = "temp_anschreiben.pdf"
    anschreiben_typ = f"{template_prefix}_anschreiben.typ"
    
    if generate_cover_letter:
        if not os.path.exists(anschreiben_typ):
            anschreiben_typ = "classic_anschreiben.typ" # Fallback
            
        if not compile_typst("data.json", anschreiben_typ, anschreiben_pdf):
            raise Exception(f"Failed to compile {anschreiben_typ}")
        
    # 3. Compile Lebenslauf
    lebenslauf_pdf = "temp_lebenslauf.pdf"
    lebenslauf_typ = f"{template_prefix}_lebenslauf.typ"
    
    if not os.path.exists(lebenslauf_typ):
        lebenslauf_typ = "classic_lebenslauf.typ" # Fallback
        
    if not compile_typst("data.json", lebenslauf_typ, lebenslauf_pdf):
        raise Exception(f"Failed to compile {lebenslauf_typ}")
        
    # 4. Bundle (Mappe)
    merger = PdfWriter()
    
    # Add Cover Letter
    if generate_cover_letter and os.path.exists(anschreiben_pdf):
        merger.append(anschreiben_pdf)
    
    # Add CV
    merger.append(lebenslauf_pdf)
    
    # Add Attachments
    for att_path in attachments_paths:
        if os.path.exists(att_path):
            merger.append(att_path)
            
    # Write final Mappe
    merger.write(output_mappe_path)
    merger.close()
    
    # Cleanup temps
    if os.path.exists(anschreiben_pdf):
        os.remove(anschreiben_pdf)
    if os.path.exists(lebenslauf_pdf):
        os.remove(lebenslauf_pdf)
    if os.path.exists("data.json"):
        os.remove("data.json")
        
    return output_mappe_path
