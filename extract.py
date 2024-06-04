import requests
from bs4 import BeautifulSoup
import pandas as pd

web = requests.get("https://bmcophthalmol.biomedcentral.com/articles/10.1186/s12886-023-02888-3")
soup = BeautifulSoup(web.content,"html.parser")
print(soup.prettify())

title = soup.find('title').text
journal_name = soup.find('meta', {'name': 'prism.publicationName'})['content']
article_number = soup.find('meta', {'name': 'prism.number'})['content']
#abstract = soup.find('meta', {'name': 'citation_abstract'})['content']

# Define a function to extract the text from sections
#def extract_section(soup, section_title):
    #section = soup.find('section', {'data-title': section_title})
    #return section.get_text(separator="\n").strip() if section else "Not found"

def extract_section(soup, header):
    header_tag = soup.find(['h2','h3'], text=header)
    if not header_tag:
        return "Not found"
    section_text = ""
    for sibling in header_tag.find_next_siblings():
        if sibling.name in ['h2','h3']:
            break
        section_text += sibling.get_text(separator="\n").strip() + "\n"
    return section_text.strip()

# Extracting the relevant sections
abstract = extract_section(soup, 'Abstract')
purpose = extract_section(soup, 'Purpose')
methods = extract_section(soup, 'Methods')
results = extract_section(soup, 'Results')
conclusion = extract_section(soup, 'Conclusion')

if conclusion == "Not found":
    conclusion = extract_section(soup, 'Conclusions')  # Handle plural form



introduction_heading = soup.find(lambda tag: tag.name == "h2" and "Introduction" in tag.text)

# Extract the text of the introduction section
if introduction_heading:
    introduction_text = []
    for sibling in introduction_heading.find_next_siblings():
        if sibling.name == "h2":  # Stop if another section starts
            break
        introduction_text.append(sibling.get_text())

    # Join all the parts of the introduction section into a single string
    introduction_text = "\n".join(introduction_text)
else:
    introduction_text = "Introduction section not found."



data = {
    'Title': title,
    'Journal Name': journal_name,
    'Article Number': article_number,
    'Abstract': abstract,
    'Methods' : methods,
    'Results' : results,
    'Conclusion' : conclusion,
    'Introduction' : introduction_text
}

df = pd.DataFrame([data],['headers'])
df.to_csv('preprocessed_data.csv', index=False)

import csv

with open('preprocessed_data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)


