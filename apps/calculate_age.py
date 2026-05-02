import time
from calendar import isleap
from datetime import datetime

def judge_leap_year(year):
    """Check if a year is a leap year"""
    return isleap(year)

def month_days(month, leap_year):
    """Return number of days in a given month"""
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2 and leap_year:
        return 29
    elif month == 2 and (not leap_year):
        return 28

def get_valid_birth_year():
    """Get and validate birth year"""
    current_year = datetime.now().year
    
    while True:
        try:
            year = int(input("Input your birth year (e.g., 1990): "))
            
            # Validation: year must be between 1900 and current year
            if year < 1900:
                print(f"❌ Year {year} is too old. Please enter a year after 1900.")
                continue
            elif year > current_year:
                print(f"❌ Year {year} is in the future! Please enter a valid year.")
                continue
            elif year > current_year - 150:
                # Reasonable check - age cannot be more than 150 years
                return year
            else:
                print(f"❌ Year {year} would make you more than 150 years old!")
                continue
                
        except ValueError:
            print("❌ Please enter a valid number for the year.")
            continue

def get_valid_birth_month():
    """Get and validate birth month"""
    while True:
        try:
            month = int(input("Input your birth month (1-12): "))
            if 1 <= month <= 12:
                return month
            else:
                print("❌ Month must be between 1 and 12.")
        except ValueError:
            print("❌ Please enter a valid number for the month.")

def get_valid_birth_day(year, month):
    """Get and validate birth day based on month and year"""
    leap_year = judge_leap_year(year)
    max_days = month_days(month, leap_year)
    
    while True:
        try:
            day = int(input(f"Input your birth day (1-{max_days}): "))
            if 1 <= day <= max_days:
                return day
            else:
                print(f"❌ Day must be between 1 and {max_days} for this month.")
        except ValueError:
            print("❌ Please enter a valid number for the day.")

def calculate_age():
    """Main function to calculate age"""
    print("\n" + "="*50)
    print("AGE CALCULATOR")
    print("="*50)
    
    # Get name
    name = input("\nInput your name: ").strip()
    if not name:
        name = "User"
    
    # Get birth date with validation
    print("\n--- Enter Your Birth Date ---")
    birth_year = get_valid_birth_year()
    birth_month = get_valid_birth_month()
    birth_day = get_valid_birth_day(birth_year, birth_month)
    
    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    
    # Calculate age
    age_years = current_year - birth_year
    age_months = current_month - birth_month
    age_days = current_day - birth_day
    
    # Adjust if days are negative
    if age_days < 0:
        age_months -= 1
        # Get days in previous month
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        days_in_prev_month = month_days(prev_month, judge_leap_year(prev_year))
        age_days += days_in_prev_month
    
    # Adjust if months are negative
    if age_months < 0:
        age_years -= 1
        age_months += 12
    
    # Calculate total approximate days (for fun, not exact)
    total_days_approx = age_years * 365 + age_months * 30 + age_days
    total_months = age_years * 12 + age_months
    
    # Display result
    print("\n" + "="*50)
    print(f" {name}'s Age Calculator Results")
    print("="*50)
    print(f" Birth Date: {birth_year}-{birth_month:02d}-{birth_day:02d}")
    print(f" Current Date: {current_year}-{current_month:02d}-{current_day:02d}")
    print("-"*50)
    print(f" {name}'s age is:")
    print(f"   • {age_years} years")
    print(f"   • {total_months} months (approximately)")
    print(f"   • {total_days_approx} days (approximately)")
    
    # Birthday message
    if age_months == 0 and age_days == 0:
        print(f"\n HAPPY BIRTHDAY {name.upper()}! ")
    elif age_months == 0 and age_days == 1:
        print(f"\n Happy Birthday for tomorrow, {name}!")
    elif age_months == 0 and age_days == -1:
        print(f"\n Hope you had a great birthday yesterday, {name}!")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    try:
        calculate_age()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n An error occurred: {e}")