import json
import os

def mask_email(email):
    """
    Masks the email field: e.g., vana@gmail.com -> v***@gmail.com
    """
    if not email or '@' not in email:
        return email
    parts = email.split('@')
    # Requirement: first character + *** + @ + domain
    return parts[0][0] + "***@" + parts[1]

def clean_toxic_data():
    # Define file paths based on lab instructions
    # Primary path: morning_v2/toxic_sample.json
    input_path = os.path.join("morning_v2", "toxic_sample.json")
    if not os.path.exists(input_path):
        input_path = "toxic_sample.json" # Fallback to root
        
    output_path = "sanitized_sample.json"

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file {input_path} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {input_path}.")
        return

    sanitized_data = []
    seen_ids = set()

    for item in data:
        # Challenge 2: Deduplication (Ensure each id only appears once)
        item_id = item.get('id')
        if item_id is None or item_id in seen_ids:
            continue
        
        # Challenge 2: Outliers and Sanity Check
        price = item.get('price')
        # Remove items with price > $5,000 or price < 0
        if price is None or price > 5000 or price < 0:
            continue

        # Challenge 1: PII Masking
        # 1. Remove the 'name' field completely
        if 'name' in item:
            del item['name']
        
        # 2. Mask the 'email' field
        if 'email' in item:
            item['email'] = mask_email(item['email'])

        sanitized_data.append(item)
        seen_ids.add(item_id)

    # Final Verification: Output sanitized_sample.json
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sanitized_data, f, indent=4)
    
    print(f"Success! {len(sanitized_data)} records sanitized and saved to {output_path}")

if __name__ == "__main__":
    clean_toxic_data()