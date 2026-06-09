// lebenslauf.typ
#set document(title: "Lebenslauf", author: "Bewerber")
#set page(paper: "a4", margin: (top: 25mm, bottom: 25mm, left: 25mm, right: 25mm))
#set text(font: "Helvetica", size: 10pt, lang: "de")

#let data = json("data.json")
#let personal = data.personal

#grid(
  columns: (1fr, auto),
  [
    #text(weight: "bold", size: 24pt)[Lebenslauf]\
    #v(5mm)
    #text(size: 14pt, weight: "bold")[#personal.first_name #personal.last_name]
  ],
  [
    #if "photo" in personal and personal.photo != none [
      #box(width: 4.5cm, height: 6cm, stroke: 1pt + gray, radius: 2mm, clip: true)[
        #image(personal.photo, width: 100%, height: 100%, fit: "cover")
      ]
    ] else [
      #box(width: 4.5cm, height: 6cm, stroke: 1pt + rgb("666666"), radius: 2mm)[
        #align(center + horizon)[#text(fill: rgb("666666"))[Bewerbungsfoto]]
      ]
    ]
  ]
)

#v(10mm)

// Helper for section titles
#let section_title(title) = {
  block(breakable: false)[
    v(5mm)
    text(weight: "bold", size: 12pt, fill: rgb("333333"))[#title]
    line(length: 100%, stroke: 0.5pt + rgb("CCCCCC"))
    v(2mm)
  ]
}

// Helper for tabular entries
#let cv_entry(date, title, subtitle: none, description: none) = {
  block(breakable: false)[
    #grid(
      columns: (4cm, 1fr),
      gutter: 5mm,
      [#text(weight: "bold")[#date]],
      [
        #text(weight: "bold")[#title]\
        #if subtitle != none [#text(style: "italic")[#subtitle]\ ]
        #if description != none [#v(1mm) #description]
      ]
    )
    #v(3mm)
  ]
}

// Personal Information
#block(breakable: false)[
  #section_title("Persönliche Daten")
  #grid(
    columns: (4cm, 1fr),
    gutter: 5mm,
    [Adresse:], [#personal.address, #personal.postal_code],
    [Telefon:], [#personal.phone],
    [E-Mail:], [#personal.email],
    [Geburtsdatum:], [#personal.birth_date],
    [Geburtsort:], [#personal.birth_place]
  )
]

#if "links" in data and data.links.len() > 0 [
  #block(breakable: false)[
    #v(2mm)
    #grid(
      columns: (4cm, 1fr),
      gutter: 5mm,
      [Profile:], 
      [
        #for link in data.links [
          #link.platform: #link.url\
        ]
      ]
    )
  ]
]

// Berufserfahrung
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

// Bildungsweg
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

// Kenntnisse & Fähigkeiten
#if data.languages.len() > 0 or data.skills.len() > 0 [
  #block(breakable: false)[
    #section_title("Kenntnisse & Fähigkeiten")
    #if data.languages.len() > 0 [
      #grid(
        columns: (4cm, 1fr),
        gutter: 5mm,
        [Sprachen:],
        [
          #for lang in data.languages [
            #lang.language (#lang.cefr_level)\
          ]
        ]
      )
      #v(2mm)
    ]

    #if data.skills.len() > 0 [
      #grid(
        columns: (4cm, 1fr),
        gutter: 5mm,
        [IT-Kenntnisse:],
        [
          #for skill in data.skills [
            #skill.skill_name (#skill.level)\
          ]
        ]
      )
    ]
  ]
]

#if "hobbies" in data and data.hobbies.len() > 0 [
  #block(breakable: false)[
    #section_title("Hobbys und Interessen")
    #grid(
      columns: (4cm, 1fr),
      gutter: 5mm,
      [Interessen:],
      [
        #data.hobbies.join(", ")
      ]
    )
  ]
]

#v(15mm)
#align(left)[
  #if personal.postal_code != "" and personal.postal_code != none [
    #personal.postal_code.split(" ").last(), den 
  ]
  #datetime.today().display("[day].[month].[year]")\
  #v(10mm)
  #personal.first_name #personal.last_name
]
