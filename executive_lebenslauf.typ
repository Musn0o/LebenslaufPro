// executive_lebenslauf.typ
#set document(title: "Lebenslauf", author: "Bewerber")
#set page(paper: "a4", margin: (top: 20mm, bottom: 20mm, left: 20mm, right: 20mm))
#set text(font: "Helvetica", size: 10pt, lang: "de")

#let data = json("data.json")
#let personal = data.personal
#let accent_color = rgb("#333333") // Anthracite

// Header
#grid(
  columns: (1fr, auto),
  [
    #text(weight: "bold", size: 26pt, fill: accent_color)[LEBENSLAUF]\
    #text(size: 16pt, weight: "light")[#personal.first_name #personal.last_name]
  ],
  [
    #if "photo" in personal and personal.photo != none [
      #box(width: 3.5cm, height: 4.7cm, stroke: 1pt + accent_color, radius: 1mm, clip: true)[
        #image(personal.photo, width: 100%, height: 100%, fit: "cover")
      ]
    ]
  ]
)

#v(5mm)
#line(length: 100%, stroke: 2pt + accent_color)
#v(5mm)

#let section_title(title) = {
  block(breakable: false)[
    v(3mm)
    rect(fill: accent_color, width: 100%, inset: 2mm)[
      #text(weight: "bold", size: 11pt, fill: white)[#title]
    ]
    v(2mm)
  ]
}

#let cv_entry(date, title, subtitle: none, description: none) = {
  block(breakable: false)[
    #grid(
      columns: (3.5cm, 1fr),
      gutter: 5mm,
      [#text(weight: "bold", fill: rgb("555555"))[#date]],
      [
        #text(weight: "bold", size: 11pt)[#title]\
        #if subtitle != none [#text(style: "italic", fill: rgb("555555"))[#subtitle]\ ]
        #if description != none [#v(1mm) #description]
      ]
    )
    #v(3mm)
  ]
}

// Contact Info Grid
#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 2mm,
  [#text(weight: "bold")[E-Mail:] #personal.email],
  [#text(weight: "bold")[Tel:] #personal.phone],
  [#text(weight: "bold")[Ort:] #personal.postal_code]
)

#if data.experience.len() > 0 [
  #block(breakable: false)[
    #section_title("BERUFSERFAHRUNG")
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
    #section_title("AUSBILDUNG")
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

#if data.skills.len() > 0 or data.languages.len() > 0 [
  #block(breakable: false)[
    #grid(
      columns: (1fr, 1fr),
      gutter: 10mm,
      [
        #if data.skills.len() > 0 [
          #section_title("KENNTNISSE")
          #for skill in data.skills [
            #grid(columns: (1fr, 1fr), [#skill.skill_name], [#text(style: "italic", size: 8pt)[#skill.level]])
          ]
        ]
      ],
      [
        #if data.languages.len() > 0 [
          #section_title("SPRACHEN")
          #for lang in data.languages [
            #grid(columns: (1fr, 1fr), [#lang.language], [#lang.cefr_level])
          ]
        ]
      ]
    )
  ]
]

#if "hobbies" in data and data.hobbies.len() > 0 [
  #block(breakable: false)[
    #section_title("INTERESSEN")
    #data.hobbies.join(" • ")
  ]
]

#v(10mm)
#line(length: 100%, stroke: 0.5pt + gray)
#v(2mm)
#text(size: 8pt, fill: rgb("555555"))[#personal.postal_code.split(" ").last(), #datetime.today().display("[day].[month].[year]")]
