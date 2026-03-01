import re
import json


def normalize_price(price_str: str) -> float:
    """
    Convert price string like '1 200,00' to float 1200.00
    """
    cleaned = price_str.replace(" ", "").replace(",", ".").strip()
    return float(cleaned)


def extract_products(text: str):
    """
    Extract structured product data from receipt.
    """
    products = []

    product_pattern = re.compile(
        r'(\d+)\.\s*\n'                     # Item number
        r'(.+?)\n'                          # Product name
        r'([\d,]+)\s*x\s*([\d ]+,\d{2})\n'  # Quantity x unit price
        r'([\d ]+,\d{2})\n'                 # Total price
        r'Стоимость',
        re.DOTALL
    )

    matches = product_pattern.findall(text)

    for match in matches:
        item_number = int(match[0])
        name = match[1].strip()
        quantity = float(match[2].replace(",", "."))
        unit_price = normalize_price(match[3])
        total_price = normalize_price(match[4])

        products.append({
            "item_number": item_number,
            "name": name,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": total_price
        })

    return products


def extract_all_prices(text: str):
    """
    Extract all monetary values safely (no newline capture).
    """
    price_pattern = re.compile(r'\d[\d ]*,\d{2}')
    prices = price_pattern.findall(text)
    return [normalize_price(p) for p in prices]


def extract_total(text: str):
    """
    Extract total amount after 'ИТОГО:'
    """
    total_pattern = re.search(r'ИТОГО:\s*\n?([\d ]+,\d{2})', text)
    if total_pattern:
        return normalize_price(total_pattern.group(1))
    return None


def extract_payment_method(text: str):
    """
    Extract payment method.
    """
    payment_pattern = re.search(r'(Банковская карта|Наличные)', text)
    if payment_pattern:
        return payment_pattern.group(1)
    return None


def extract_datetime(text: str):
    """
    Extract date and time.
    """
    datetime_pattern = re.search(r'Время:\s*([\d\.]+\s+[\d:]+)', text)
    if datetime_pattern:
        return datetime_pattern.group(1)
    return None


def calculate_total_from_products(products):
    """
    Calculate total sum from parsed products.
    """
    return round(sum(p["total_price"] for p in products), 2)


def parse_receipt(file_path: str):
    """
    Main receipt parsing function.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    products = extract_products(text)
    all_prices = extract_all_prices(text)
    extracted_total = extract_total(text)
    payment_method = extract_payment_method(text)
    datetime_value = extract_datetime(text)
    calculated_total = calculate_total_from_products(products)

    structured_output = {
        "datetime": datetime_value,
        "payment_method": payment_method,
        "products": products,
        "calculated_total": calculated_total,
        "extracted_total": extracted_total,
        "totals_match": calculated_total == extracted_total,
        "all_prices_found": all_prices
    }

    return structured_output


if __name__ == "__main__":
    result = parse_receipt("raw.txt")
    print(json.dumps(result, indent=4, ensure_ascii=False))