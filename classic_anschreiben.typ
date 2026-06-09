// anschreiben.typ
#set document(title: "Bewerbung", author: "Bewerber")
#set page(paper: "a4", margin: (top: 27mm, bottom: 20mm, left: 25mm, right: 20mm))
#set text(font: "Helvetica", size: 11pt, lang: "de")

#let data = json("data.json")

#let personal = data.personal

// Sender Info (right-aligned, appears once)
#align(right)[
  #text(weight: "bold")[#personal.first_name #personal.last_name]\
  #personal.address\
  #personal.postal_code\
  #personal.email | #personal.phone
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

// Date
#align(right)[
  #personal.postal_code.split(" ").last(), den #datetime.today().display("[day].[month].[year]")
]

#v(10mm)

// Subject
#text(weight: "bold", size: 12pt)[Bewerbung als #data.company.job_title]

#v(5mm)

#if "cover_letter_text" in data [
  #data.cover_letter_text
] else [
  Sehr geehrte Damen und Herren,
  
  [Hier kommt der durch die KI generierte Text für das Anschreiben hin...]
  
  Mit freundlichen Grüßen
]

#v(10mm)
#personal.first_name #personal.last_name
