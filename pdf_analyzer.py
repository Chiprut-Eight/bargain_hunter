import os
import re
import requests
import logging
from PyPDF2 import PdfReader

# List of critical negative keywords to flag
RISK_KEYWORDS = [
    "פגיעת שלדה", "שאסי", "אובדן להלכה", "טוטאל לוס", "עבר תאונה", 
    "נזילת שמן", "מנוע רועש", "בעיה בגיר", "פולש", "חריגות בניה", 
    "צו הריסה", "ללא היתר", "מושכר", "בעיות רטיבות", "שריפה",
    "שעבוד", "עיקול"
]

def analyze_pdf_for_risks(pdf_url, filename="temp_tender.pdf"):
    """
    Downloads a PDF from a URL and scans it for risk keywords.
    Returns a list of identified risk flags.
    """
    found_risks = []
    
    if not pdf_url or not pdf_url.lower().endswith('.pdf'):
        return found_risks

    try:
        # Download the file
        logging.info(f"Downloading PDF for risk analysis: {pdf_url}")
        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
            
        # Parse the PDF text
        reader = PdfReader(filename)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + " "
            
        # Optional: remove the temp file
        if os.path.exists(filename):
            os.remove(filename)
            
        # Look for keywords
        for keyword in RISK_KEYWORDS:
            if re.search(rf'\b{keyword}\b', full_text):
                found_risks.append(keyword)
                
    except Exception as e:
        logging.warning(f"Failed to analyze PDF {pdf_url}: {e}")
        
    return found_risks

def append_risk_analysis(deal):
    """
    Appends a risk analysis field to a deal if a direct PDF link is available.
    """
    if "pdf_link" in deal and deal["pdf_link"]:
        risks = analyze_pdf_for_risks(deal["pdf_link"])
        if risks:
            deal["risk_flags"] = risks
            logging.info(f"Identified risks for {deal.get('id')}: {risks}")
        else:
            deal["risk_flags"] = []
    return deal
