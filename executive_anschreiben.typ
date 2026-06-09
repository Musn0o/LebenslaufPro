// executive_anschreiben.typ
#set document(title: "Bewerbung", author: "Bewerber")
#set page(paper: "a4", margin: (top: 27mm, bottom: 20mm, left: 25mm, right: 20mm))
#set text(font: "Helvetica", size: 11pt, lang: "de")

#let data = json("data.json")
#let personal = data.personal
#let accent_color = rgb("#333333") // Anthracite

// Sender Info Header (appears once)
#rect(fill: accent_color, width: 100%, inset: 5mm)[
  #grid(
    columns: (1fr, auto),
    [
      #text(weight: "bold", size: 16pt, fill: white)[#personal.first_name #personal.last_name]\
      #text(size: 9pt, fill: rgb("CCCCCC"))[#personal.address | #personal.postal_code]
    ],
    [
      #text(size: 9pt, fill: rgb("CCCCCC"))[#personal.email\ #personal.phone]
    ]
  )
]

#v(20mm)

// Receiver Info
#align(left)[
  #text(weight: "bold")[#data.company.name]\
  #if "contact_person" in data.company and data.company.contact_person != "" [
    z. Hd. #data.company.contact_person\
  ]
  #data.company.address
]

#v(15mm)
#align(right)[#datetime.today().display("[day].[month].[year]")]

#v(10mm)

// Subject
#text(weight: "bold", size: 13pt, fill: accent_color)[Bewerbung als #data.company.job_title]

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
