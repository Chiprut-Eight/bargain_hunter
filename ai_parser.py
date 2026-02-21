import re
import logging

def parse_car_title(title):
    """
    Extracts structured data from a raw car auction title using Regular Expressions.
    Example Input: "מכרז מס' 45/2026 - רכב שברולט ספארק שנת 2019"
    """
    data = {
        "year": None,
        "model": None,
        "raw_extracted": False
    }
    
    # Extract Year (4 digits, starting with 19 or 20, up to current year+1)
    year_match = re.search(r'\b(19[9-9]\d|20[0-2]\d)\b', title)
    if year_match:
        data["year"] = int(year_match.group(1))
        
    # Extract Make/Model (naive approach: common car brands in Israel)
    brands = ["שברולט", "יונדאי", "מאזדה", "טויוטה", "קיה", "רנו", "פיג'ו", "סיטרואן", 
              "פורד", "סובארו", "סוזוקי", "מיצובישי", "ניסאן", "הונדה", "פולקסווגן", 
              "סקודה", "סיאט", "אאודי", "מזראטי", "ב.מ.וו", "מרצדס", "טסלה"]
              
    for brand in brands:
        if brand in title:
            # Try to grab the brand and the word immediately following it as the model
            pattern = rf'{brand}\s+([א-ת0-9A-Za-z]+)'
            model_match = re.search(pattern, title)
            if model_match:
                data["model"] = f"{brand} {model_match.group(1)}"
            else:
                data["model"] = brand
            data["raw_extracted"] = True
            break
            
    return data


def parse_real_estate_title(title):
    """
    Extracts structured data from a raw real estate auction title.
    Example Input: "מכרז פומבי למכירת דירת 4 חדרים בחיפה, רחוב הרצל 15, כ-100 מ\"ר"
    """
    data = {
        "rooms": None,
        "area_sqm": None,
        "city": None,
        "raw_extracted": False
    }
    
    # Extract Rooms (Number followed by "חדרים" or "חד'")
    rooms_match = re.search(r'(\d+([\.,]\d)?)\s*(חדרים|חד\')', title)
    if rooms_match:
        try:
            data["rooms"] = float(rooms_match.group(1))
            data["raw_extracted"] = True
        except ValueError:
            pass
            
    # Extract Area in Sqm (Number followed by "מ"ר" or "מטר")
    area_match = re.search(r'(\d+([\.,]\d)?)\s*(מ"ר|מטר|מ׳|מ\'ר)', title)
    if area_match:
        try:
            data["area_sqm"] = float(area_match.group(1))
            data["raw_extracted"] = True
        except ValueError:
            pass
            
    # Extract City (basic matching after common prefixes like 'ב-')
    # Or just rely on the 'timeLeft' field from the scraper which usually holds the city/location.
    
    return data

def parse_equipment_title(title):
    """
    Extracts structured data from a raw equipment/hardware auction title.
    Example Input: "מכרז למכירת מחשב נייד אפל מקבוק פרו מחולט"
    """
    data = {
        "category": None,
        "brand": None,
        "raw_extracted": False
    }
    
    categories = {"מחשב": "מחשבים", "אייפון": "סלולר", "סמסונג": "סלולר", "טלפון": "סלולר", "שעון": "תכשיטים ושעונים", "תכשיט": "תכשיטים ושעונים", "רהיט": "ריהוט", "כלי עבודה": "כלי עבודה"}
    brands = ["אפל", "Apple", "סמסונג", "Samsung", "דל", "Dell", "HP", "לנובו", "Lenovo", "רולקס", "Rolex"]
    
    for cat_keyword, cat_name in categories.items():
        if cat_keyword in title:
            data["category"] = cat_name
            data["raw_extracted"] = True
            break
            
    for brand in brands:
        if brand.lower() in title.lower():
            data["brand"] = brand
            data["raw_extracted"] = True
            break
            
    return data

def enrich_deep_data(deal):
    """
    Simulates extracting deep technical data and interior images from the specific item page.
    In V4, this will be replaced with actual secondary-level selenium HTTP requests per deal link.
    """
    # Simulate Images
    images = []
    specs = {}
    
    if deal.get('type') == 'car':
        specs = {"קילומטראז'": "יש לבדוק בנספח התמונות", "בעלות קודמת": "ממשלתי/רשות", "הערות": "רכב מכרז AS-IS"}
        
    elif deal.get('type') == 'real_estate':
        specs = {"סוג הפצה": "פומבי", "מצב הנכס": "AS-IS", "הערות": "כפוף לאישור ועדת המכרזים"}
        
    elif deal.get('type') == 'equipment':
        if deal.get('category') == 'מחשבים' or deal.get('category') == 'סלולר':
             specs = {"מצב חזותי": "נמכר AS-IS", "אחריות": "ללא"}
        elif deal.get('category') == 'תכשיטים ושעונים':
             specs = {"שמאות": "יש לבחון חוברת"}
        else:
             specs = {"מצב": "משומש - מוחרם"}
             
    # Append specific images for standard presentation
    deal['images'] = images
    deal['specs'] = specs
    
    return deal

def parse_deal(deal):
    """
    Main entry point to parse a deal object and enrich it with structured data.
    """
    try:
        enriched_data = {}
        if deal.get('type') == 'car':
            enriched_data = parse_car_title(deal.get('title', ''))
        elif deal.get('type') == 'real_estate':
            enriched_data = parse_real_estate_title(deal.get('title', ''))
        elif deal.get('type') == 'equipment':
            enriched_data = parse_equipment_title(deal.get('title', ''))
            
        # Merge new attributes into the deal
        for k, v in enriched_data.items():
            if v is not None:
                deal[k] = v
                
        # Append mock deep data (Images, Extended Specs)
        deal = enrich_deep_data(deal)
                
    except Exception as e:
        logging.warning(f"Failed to parse deal {deal.get('id')}: {e}")
        
    return deal
