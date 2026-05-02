import requests 
import json
import sys
import os
from pprint import pprint

# Use environment variable for API key (security best practice)
API_KEY = os.environ.get('FIXER_API_KEY', 'your_default_key_here')
url = f"http://data.fixer.io/api/latest?access_key={API_KEY}"

def get_rates():
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data.get('success'):
            print(f"API Error: {data.get('error', {}).get('info', 'Unknown error')}")
            return None
        return data["rates"]
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None

currencies = [
    "AED : Emirati Dirham", "AFN : Afghan Afghani", "ALL : Albanian Lek",
    "AMD : Armenian Dram", "ANG : Dutch Guilder", "AOA : Angolan Kwanza",
    "ARS : Argentine Peso", "AUD : Australian Dollar", "AWG : Aruban Guilder",
    "AZN : Azerbaijan Manat", "BAM : Bosnian Mark", "BBD : Barbadian Dollar",
    "BDT : Bangladeshi Taka", "BGN : Bulgarian Lev", "BHD : Bahraini Dinar",
    "BIF : Burundian Franc", "BMD : Bermudian Dollar", "BND : Bruneian Dollar",
    "BOB : Bolivian Boliviano", "BRL : Brazilian Real", "BSD : Bahamian Dollar",
    "BTC : Bitcoin", "BTN : Bhutanese Ngultrum", "BWP : Botswana Pula",
    "BYN : Belarusian Ruble", "BZD : Belizean Dollar", "CAD : Canadian Dollar",
    "CDF : Congolese Franc", "CHF : Swiss Franc", "CLP : Chilean Peso",
    "CNY : Chinese Yuan", "COP : Colombian Peso", "CRC : Costa Rican Colon",
    "CUP : Cuban Peso", "CVE : Cape Verde Escudo", "CZK : Czech Koruna",
    "DJF : Djiboutian Franc", "DKK : Danish Krone", "DOP : Dominican Peso",
    "DZD : Algerian Dinar", "EGP : Egyptian Pound", "ERN : Eritrean Nakfa",
    "ETB : Ethiopian Birr", "EUR : Euro", "FJD : Fijian Dollar",
    "FKP : Falkland Pound", "GBP : British Pound", "GEL : Georgian Lari",
    "GHS : Ghanaian Cedi", "GIP : Gibraltar Pound", "GMD : Gambian Dalasi",
    "GNF : Guinean Franc", "GTQ : Guatemalan Quetzal", "GYD : Guyanese Dollar",
    "HKD : Hong Kong Dollar", "HNL : Honduran Lempira", "HRK : Croatian Kuna",
    "HTG : Haitian Gourde", "HUF : Hungarian Forint", "IDR : Indonesian Rupiah",
    "ILS : Israeli Shekel", "INR : Indian Rupee", "IQD : Iraqi Dinar",
    "IRR : Iranian Rial", "ISK : Icelandic Krona", "JMD : Jamaican Dollar",
    "JOD : Jordanian Dinar", "JPY : Japanese Yen", "KES : Kenyan Shilling",
    "KGS : Kyrgyzstani Som", "KHR : Cambodian Riel", "KMF : Comorian Franc",
    "KPW : North Korean Won", "KRW : South Korean Won", "KWD : Kuwaiti Dinar",
    "KYD : Caymanian Dollar", "KZT : Kazakhstani Tenge", "LAK : Lao Kip",
    "LBP : Lebanese Pound", "LKR : Sri Lankan Rupee", "LRD : Liberian Dollar",
    "LSL : Basotho Loti", "LYD : Libyan Dinar", "MAD : Moroccan Dirham",
    "MDL : Moldovan Leu", "MGA : Malagasy Ariary", "MKD : Macedonian Denar",
    "MMK : Burmese Kyat", "MNT : Mongolian Tughrik", "MOP : Macau Pataca",
    "MRU : Mauritanian Ouguiya", "MUR : Mauritian Rupee", "MVR : Maldivian Rufiyaa",
    "MWK : Malawian Kwacha", "MXN : Mexican Peso", "MYR : Malaysian Ringgit",
    "MZN : Mozambican Metical", "NAD : Namibian Dollar", "NGN : Nigerian Naira",
    "NIO : Nicaraguan Cordoba", "NOK : Norwegian Krone", "NPR : Nepalese Rupee",
    "NZD : New Zealand Dollar", "OMR : Omani Rial", "PAB : Panamanian Balboa",
    "PEN : Peruvian Sol", "PGK : Papua New Guinean Kina", "PHP : Philippine Peso",
    "PKR : Pakistani Rupee", "PLN : Polish Zloty", "PYG : Paraguayan Guarani",
    "QAR : Qatari Riyal", "RON : Romanian Leu", "RSD : Serbian Dinar",
    "RUB : Russian Ruble", "RWF : Rwandan Franc", "SAR : Saudi Riyal",
    "SBD : Solomon Dollar", "SCR : Seychellois Rupee", "SDG : Sudanese Pound",
    "SEK : Swedish Krona", "SGD : Singapore Dollar", "SHP : Saint Helena Pound",
    "SLL : Sierra Leonean Leone", "SOS : Somali Shilling", "SRD : Surinamese Dollar",
    "STN : Sao Tomean Dobra", "SVC : Salvadoran Colon", "SYP : Syrian Pound",
    "SZL : Swazi Lilangeni", "THB : Thai Baht", "TJS : Tajikistani Somoni",
    "TMT : Turkmenistani Manat", "TND : Tunisian Dinar", "TOP : Tongan Pa'anga",
    "TRY : Turkish Lira", "TTD : Trinidadian Dollar", "TWD : Taiwan Dollar",
    "TZS : Tanzanian Shilling", "UAH : Ukrainian Hryvnia", "UGX : Ugandan Shilling",
    "USD : US Dollar", "UYU : Uruguayan Peso", "UZS : Uzbekistani Som",
    "VEF : Venezuelan Bolivar", "VND : Vietnamese Dong", "VUV : Vanuatu Vatu",
    "WST : Samoan Tala", "XAF : Central African CFA", "XCD : East Caribbean Dollar",
    "XOF : West African CFA", "XPF : CFP Franc", "YER : Yemeni Rial",
    "ZAR : South African Rand", "ZMW : Zambian Kwacha", "ZWL : Zimbabwean Dollar",
]

def show_currencies(page=1, per_page=20):
    start = (page - 1) * per_page
    end = start + per_page
    for currency in currencies[start:end]:
        print(currency)
    if end < len(currencies):
        print(f"\nPage {page}/{ (len(currencies) + per_page - 1) // per_page }")
        next_page = input("Press Enter for next page, or 'q' to quit: ")
        if next_page.lower() != 'q':
            show_currencies(page + 1, per_page)

def convert_currency(fx_rates):
    while True:
        query = input(
            "\nEnter: <amount> <from_currency> <to_currency>\n"
            "Or type 'SHOW' to see currencies\n"
            "Or 'Q' to quit\n"
            "> "
        ).strip()
        
        if query.upper() == "Q":
            sys.exit()
        elif query.upper() == "SHOW":
            show_currencies()
            continue
        
        try:
            parts = query.split()
            if len(parts) != 3:
                print("Invalid format. Use: 100 USD EUR")
                continue
            
            qty, fromC, toC = parts
            qty = float(qty)
            fromC = fromC.upper()
            toC = toC.upper()
            
            if fromC not in fx_rates or toC not in fx_rates:
                print("Invalid currency code. Type SHOW to see available currencies.")
                continue
            
            amount = round(qty * fx_rates[toC] / fx_rates[fromC], 2)
            print(f"{qty} {fromC} = {amount} {toC}")
        except ValueError:
            print("Invalid amount. Please enter a number.")
        except Exception as e:
            print(f"Error: {e}")

def main():
    print("Fetching exchange rates...")
    fx_rates = get_rates()
    
    if not fx_rates:
        print("Failed to fetch exchange rates. Using EUR as base.")
        # Fallback: try to use a different endpoint or exit
        sys.exit(1)
    
    print("Exchange rates loaded successfully!")
    convert_currency(fx_rates)

if __name__ == "__main__":
    main()