// modern_lebenslauf.typ
#set document(title: "Lebenslauf", author: "Bewerber")
#set page(paper: "a4", margin: (top: 0mm, bottom: 0mm, left: 0mm, right: 0mm))
#set text(font: "Helvetica", size: 10pt, lang: "de")

#let data = json("data.json")
#let personal = data.personal
#let primary_color = rgb("#1a5f7a") // Deep blue

#grid(
  columns: (7cm, 1fr),
  rows: (100%),
  // Sidebar
  rect(fill: primary_color, width: 100%, height: 100%, inset: (top: 20mm, left: 10mm, right: 10mm))[
    #set text(fill: white)
    
    #if "photo" in personal and personal.photo != none [
      #align(center)[
        #box(width: 4cm, height: 5.3cm, stroke: 2pt + white, radius: 2mm, clip: true)[
          #image(personal.photo, width: 100%, height: 100%, fit: "cover")
        ]
      ]
      #v(10mm)
    ]
    
    #text(weight: "bold", size: 14pt)[Kontakt]\
    #v(2mm)
    #set text(size: 9pt)
    #if personal.address != "" and personal.address != none [#personal.address\]
    #if personal.postal_code != "" and personal.postal_code != none [#personal.postal_code\]
    #if personal.phone != "" and personal.phone != none [#personal.phone\]
    #if personal.email != "" and personal.email != none [#personal.email\]
    
    #if "links" in data and data.links.len() > 0 [
      #v(10mm)
      #text(weight: "bold", size: 14pt)[Profile]\
      #v(2mm)
      #for link in data.links [
        #link.platform: #link.url\
      ]
    ]
    
    #if data.skills.len() > 0 [
      #v(10mm)
      #text(weight: "bold", size: 14pt)[Kenntnisse]\
      #v(2mm)
      #for skill in data.skills [
        #skill.skill_name\
        #text(size: 8pt, fill: white.lighten(40%))[#skill.level]\
        #v(1mm)
      ]
    ]
    
    #if data.languages.len() > 0 [
      #v(10mm)
      #text(weight: "bold", size: 14pt)[Sprachen]\
      #v(2mm)
      #for lang in data.languages [
        #lang.language: #lang.cefr_level\
      ]
    ]
  ],
  // Main Content
  pad(top: 20mm, left: 10mm, right: 15mm, bottom: 20mm)[
    #text(weight: "bold", size: 28pt, fill: primary_color)[Lebenslauf]\
    #text(size: 18pt, weight: "bold")[#personal.first_name #personal.last_name]\
    #v(10mm)
    
    #let section_title(title) = {
      block(breakable: false)[
        #v(5mm)
        #text(weight: "bold", size: 14pt, fill: primary_color)[#title]
        #v(-2mm)
        #line(length: 100%, stroke: 1.5pt + primary_color)
        #v(3mm)
      ]
    }
    
    #let cv_entry(date, title, subtitle: none, description: none) = {
      block(breakable: false)[
        #grid(
          columns: (3cm, 1fr),
          gutter: 5mm,
          [#text(weight: "bold", fill: rgb("555555"))[#date]],
          [
            #text(weight: "bold", size: 11pt)[#title]\
            #if subtitle != none [#text(style: "italic")[#subtitle]\ ]
            #if description != none [#v(1mm) #description]
          ]
        )
        #v(4mm)
      ]
    }
    
    #block(breakable: false)[
      #section_title("Persönliche Daten")
      #grid(
        columns: (3cm, 1fr),
        gutter: 5mm,
        [Geburtsdatum:], [#personal.birth_date],
        [Geburtsort:], [#personal.birth_place]
      )
    ]
    
    #if data.experience.len() > 0 [
      #block(breakable: false)[
        #section_title("Berufserfahrung")
        #for exp in data.experience [
          #cv_entry(
            exp.start_date + " - " + exp.end_date,
            exp.job_title,
            subtitle: exp.company,
            description: exp.description
          )
        ]
      ]
    ]
    
    #if data.education.len() > 0 [
      #block(breakable: false)[
        #section_title("Bildungsweg")
        #for edu in data.education [
          #cv_entry(
            edu.start_date + " - " + edu.end_date,
            edu.degree,
            subtitle: edu.institution,
            description: edu.description
          )
        ]
      ]
    ]
    
    #if "hobbies" in data and data.hobbies.len() > 0 [
      #block(breakable: false)[
        #section_title("Interessen")
        #data.hobbies.join(", ")
      ]
    ]
    
    #v(15mm)
    #personal.postal_code.split(" ").last(), den #datetime.today().display("[day].[month].[year]")
  ]
)
