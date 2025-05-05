import pandas as pd
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

content = """Trinamool Congress leader Mahua Moitra has moved the Supreme Court against her expulsion 
from the Lok Sabha over the cash-for-query allegations against her. Moitra was ousted from the Parliament 
last week after the Ethics Committee of the Lok Sabha found her guilty of jeopardising national security 
by sharing her parliamentary portal's login credentials with businessman Darshan Hiranandani."""

doc = nlp(content)

print("\nNamed Entities:")
for ent in doc.ents:
    print(f"{ent.text:<30} Start: {ent.start_char:<3} End: {ent.end_char:<3} Label: {ent.label_}")

entities = [(ent.text, ent.label_, ent.lemma_) for ent in doc.ents]
df = pd.DataFrame(entities, columns=['Text', 'Type', 'Lemma'])

print("\nEntity DataFrame:")
print(df)

html = displacy.render(doc, style="ent", page=True)
with open("ner_visualization.html", "w", encoding="utf-8") as f:
    f.write(html)
print("\n✔ Entity visualization saved to ner_visualization.html")
