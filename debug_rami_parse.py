from bs4 import BeautifulSoup

try:
    with open("ila_source3.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' | ', strip=True)
    print("PAGE TEXT DUMP (results):")
    # Print the text where 'תוצאות' (results) or 'מספר' (number) occurs to see actual tender items
    import re
    sections = re.split(r'תוצאות', text)
    if len(sections) > 1:
        print(sections[1][:2500])
    elif "מכרז" in text:
        idx = text.find("מכרז")
        print(text[idx:idx+2500])
    else:
        print("Could not find table text.")

except Exception as e:
    print("Error:", e)
