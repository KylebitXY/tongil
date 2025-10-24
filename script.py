import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tongmoodoo.settings')
django.setup()

import csv
from datetime import date
from main1.models import Athlete  # Ensure this matches the actual app name and model name

# Define the genders and categories
genders = ['male', 'female']
categories = [
    'Fin Weight Division', 'Fly Weight Division', 'Bantam Weight Division',
    'Feather Weight Division', 'Light Weight Division', 'Welter Weight Division',
    'Middle Weight Division', 'Heavy Weight Division',
    'Super Heavy Weight Division', 'Super Heavy Weight Division Level 1',
    'Super Heavy Weight Division Level 0', 'Unknown Category'
]

# Helper function to calculate age from dob
def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# Function to filter and generate CSV files
def generate_csv():
    for gender in genders:
        for category in categories:
            # Filter athletes by gender
            athletes = Athlete.objects.filter(gender=gender)

            # Further filter based on age and category
            filtered_athletes = [
                athlete for athlete in athletes
                if calculate_age(athlete.dob) >= 18 and athlete.get_weight_category == category
            ]

            if filtered_athletes:  # Only create a file if there are athletes
                # Naming the file appropriately
                filename = f"{gender}_{category.replace(' ', '_').lower()}.csv"
                
                # Write to CSV
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = ['name', 'age', 'weight', 'belt', 'gender', 'category']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for athlete in filtered_athletes:
                        writer.writerow({
                            'name': athlete.name,
                            'age': calculate_age(athlete.dob),
                            'weight': athlete.weight,
                            'belt': athlete.belt,  # Use the name of the belt
                            'gender': athlete.gender,
                            'category': athlete.get_weight_category  # Access the property without parentheses
                        })
                print(f"Generated {filename}")

# Run the script
generate_csv()
