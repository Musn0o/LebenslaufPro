// modern_anschreiben.typ
#set document(title: "Bewerbung", author: "Bewerber")
#set page(paper: "a4", margin: (top: 27mm, bottom: 20mm, left: 25mm, right: 20mm))
#set text(font: "Helvetica", size: 11pt, lang: "de")

#let data = json("data.json")
#let personal = data.personal
#let primary_color = rgb("#1a5f7a") // Deep blue

// Header (sender appears once)
#grid(
  columns: (1fr, auto),
  [
    #text(weight: "bold", size: 18pt, fill: primary_color)[#personal.first_name #personal.last_name]\
    #text(size: 9pt, fill: rgb("555555"))[#personal.address | #personal.postal_code | #personal.email]
  ],
  [
    #text(size: 8pt, fill: rgb("555555"))[#datetime.today().display("[day].[month].[year]")]
  ]
)

#v(20mm)

// Receiver Info
#align(left)[
  #text(weight: "bold")[#data.company.name]\
  #if "contact_person" in data.company and data.company.contact_person != "" [
    z. Hd. #data.company.contact_person\
  ]
  #data.company.address
]

#v(20mm)

// Subject
#text(weight: "bold", size: 13pt, fill: primary_color)[Bewerbung als #data.company.job_title]

#v(10mm)

#if "cover_letter_text" in data [
  #data.cover_letter_text
] else [
  Sehr geehrte Damen und Herren,
  
  [Hier kommt der durch die KI generierte Text für das Anschreiben hin...]
  
  Mit freundlichen Grüßen
]

#v(15mm)
#personal.first_name #personal.last_name
