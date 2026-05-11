// anschreiben.typ
#set document(title: "Bewerbung", author: "Bewerber")
#set page(paper: "a4", margin: (top: 27mm, bottom: 20mm, left: 25mm, right: 20mm))
#set text(font: "Helvetica", size: 11pt, lang: "de")

#let data = json("data.json")

#let personal = data.personal

// Sender Info
#align(right)[
  #text(weight: "bold")[#personal.first_name #personal.last_name]\
  #personal.address\
  #personal.postal_code\
  #personal.email | #personal.phone
]

#v(20mm)

// Receiver Info (Positioned for DIN 5008 Window)
#align(left)[
  #text(size: 8pt)[#personal.first_name #personal.last_name - #personal.address - #personal.postal_code]\
  #text(weight: "bold")[Musterfirma GmbH]\
  Personalabteilung\
  Musterstraße 123\
  12345 Musterstadt
]

#v(15mm)

// Date
#align(right)[
  #personal.postal_code.split(" ").last(), den #datetime.today().display("[day].[month].[year]")
]

#v(10mm)

// Subject
#text(weight: "bold", size: 12pt)[Bewerbung als [Position]]

#v(5mm)

Sehr geehrte Damen und Herren,

[Hier kommt der durch die KI generierte Text für das Anschreiben hin...]

Mit freundlichen Grüßen

#v(10mm)
#personal.first_name #personal.last_name
