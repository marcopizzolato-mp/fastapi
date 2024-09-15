# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import pandas as pd
from ricardo.ee.fastapi.app.db.session import get_db_session
from ricardo.ee.fastapi.app.models.parks import Parks
                                                 
from ricardo.ee.fastapi.app.models.parks_visits import ParkVisits
from ricardo.ee.fastapi.app.models.visitors import Visitors
from ricardo.ee.fastapi.app.models.species import Species
from ricardo.ee.fastapi.app.models.parks_species import ParksSpecies
from ricardo.ee.fastapi.app.models.parks_facilities import ParkFacilities

# -

def upload_df_to_db(df, orm_model):
    with get_db_session() as db_session:
        try: 
            # Convert dataframe to list of dictionaries
            data_dict = df.to_dict(orient='records')
            # Map the data to the ORM Model
            db_session.bulk_insert_mappings(orm_model, data_dict)
            db_session.commit()
            print("Data uploaded successfully!")
        except Exception as e:
            print(f"An error occurred during data upload: {e}")
            db_session.rollback()
        


# National Parks
national_parks = pd.read_csv('../data/italy_all_parks_data.csv')
upload_df_to_db(national_parks, Parks)

# +
from datetime import datetime, timedelta
import random

# Helper functions
def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))

def random_name():
    # Generate a list of 100 Italian names and surnames
    italian_first_names = [
        "Alessandro", "Giulia", "Lorenzo", "Francesca", "Leonardo", "Sofia", "Matteo", "Aurora", "Gabriele", "Ginevra",
        "Edoardo", "Alice", "Tommaso", "Greta", "Federico", "Anna", "Riccardo", "Chiara", "Michele", "Vittoria",
        "Andrea", "Beatrice", "Antonio", "Martina", "Giovanni", "Elena", "Filippo", "Camilla", "Marco", "Sara",
        "Nicolo", "Rachele", "Simone", "Arianna", "Christian", "Gaia", "Emanuele", "Noemi", "Davide", "Alessia",
        "Pietro", "Caterina", "Francesco", "Elisa", "Samuele", "Veronica", "Luca", "Rebecca", "Manuel", "Mia",
        "Diego", "Carlotta", "Mattia", "Emma", "Giacomo", "Eleonora", "Carlo", "Sabrina", "Jacopo", "Nicole",
        "Matilde", "Alessandra", "Valerio", "Margherita", "Sergio", "Paola", "Raffaele", "Ilaria", "Giulio", "Claudia",
        "Paolo", "Roberta", "Enrico", "Giorgia", "Daniele", "Erika", "Stefano", "Elisabetta", "Maurizio", "Fabiola",
        "Fabio", "Angelica", "Salvatore", "Valentina", "Alberto", "Maria", "Vincenzo", "Simona", "Cristiano", "Teresa",
        "Massimo", "Patrizia", "Angelo", "Giovanna", "Dario", "Rita", "Claudio", "Michela", "Giorgio", "Silvia"
    ]
    
    italian_last_names = [
        "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco",
        "Bruno", "Gallo", "Conti", "De Luca", "Costa", "Giordano", "Mancini", "Rizzo", "Lombardi", "Moretti",
        "Barbieri", "Fontana", "Santoro", "Mariani", "Rinaldi", "Caruso", "Ferrara", "Galli", "Martini", "Leone",
        "Longo", "Gentile", "Martinelli", "Vitale", "Lombardo", "Serra", "Coppola", "De Santis", "D'Amico", "Marchi",
        "Parisi", "Villa", "Conte", "Ferraro", "Ferri", "Fabbri", "Bianco", "Marini", "Grassi", "Valentini",
        "Messina", "Sala", "De Angelis", "Gatti", "Pellegrini", "Palumbo", "Sanna", "Farina", "Rizzi", "Monti",
        "Cattaneo", "Morelli", "Amato", "Silvestri", "Mazza", "Testa", "Grasso", "Guerra", "Negri", "Piras",
        "Vitali", "Lorenzi", "Pagano", "Riva", "Donati", "Piras", "Battaglia", "Piazza", "Sartori", "Neri",
        "Marchetti", "Caputo", "De Simone", "Orlando", "Cattaneo", "Benedetti", "Amoroso", "Carbone", "Marconi", "Palumbo",
        "Bellini", "Fiorentino", "Leoni", "Fontana", "Santini", "Ferrara", "Sorrentino", "Basile", "Barone", "Montanari"
    ]

    # Create a list of 100 full names by combining first names and last names
    return [(i,f"{random.choice(italian_first_names)} {random.choice(italian_last_names)}") for i in range(1,501)]
                              
# Generate Visitors
def generate_visitors_with_patterns(num_records, start_date, end_date, parks):
    visits = []
    visitor_names_list = random_name()
    visitors_df = pd.DataFrame(visitor_names_list, columns=["visitor_id", "name"])
    email_providers = ["gmail.com", "yahoo.com", "outlook.com", "icloud.com"]
    visitors_df["email"] = visitors_df["name"].str.lower().str.replace(' ', '').apply(lambda x: f"{x}@{random.choice(email_providers)}")

    holidays = [
        # 2018
        datetime(2018, 5, 1), datetime(2018, 6, 2), datetime(2018, 8, 15), datetime(2018, 11, 1), datetime(2018, 12, 25),
        # 2019
        datetime(2019, 1, 1), datetime(2019, 4, 22), datetime(2019, 5, 1), datetime(2019, 6, 2), datetime(2019, 8, 15),
        datetime(2019, 11, 1), datetime(2019, 12, 25),
        # 2020
        datetime(2020, 1, 1), datetime(2020, 4, 13), datetime(2020, 5, 1), datetime(2020, 6, 2), datetime(2020, 8, 15),
        datetime(2020, 11, 1), datetime(2020, 12, 25),
        # 2021
        datetime(2021, 1, 1), datetime(2021, 4, 5), datetime(2021, 5, 1), datetime(2021, 6, 2), datetime(2021, 8, 15),
        datetime(2021, 11, 1), datetime(2021, 12, 25),
        # 2022
        datetime(2022, 1, 1), datetime(2022, 4, 18), datetime(2022, 5, 1), datetime(2022, 6, 2), datetime(2022, 8, 15),
        datetime(2022, 11, 1), datetime(2022, 12, 25),
        # 2023
        datetime(2023, 1, 1), datetime(2023, 4, 10), datetime(2023, 5, 1), datetime(2023, 6, 2), datetime(2023, 8, 15),
        datetime(2023, 11, 1)
    ]
    
    for i in range(num_records):
        # visitor_id = random.choice(visitor_ids)
        visitor_id, name = random.choice(visitor_names_list)
        park_id = int(random.choice(parks["park_id"]))
        visitor_date = random_date(start_date, end_date)
        
        # Randomly select a date
        if random.random() < 0.15:  # 10% chance to fall on a holiday
            visitor_start_date = random.choice(holidays)
            visitor_end_date = visitor_start_date
        elif random.random() < 0.35:  # 35% chance to fall in summer months (June to September)
            summer_start = datetime(visitor_date.year, 5, 15)
            summer_end = datetime(visitor_date.year, 9, 30)
            visitor_start_date = random_date(summer_start, summer_end)
            # Ensure the end date is within 7 days of the start date
            visitor_end_date = visitor_start_date + timedelta(days=random.randint(0, 7))        
        else:
            visitor_start_date = visitor_date
            visitor_end_date = visitor_date + timedelta(days=random.randint(0, 7))  
        
        # Decrease visits during COVID-19 in 2020
        if visitor_date.year == 2020 and random.random() < 0.7:  # 70% chance to skip
            continue
        
        visits.append({
            "visitor_id":visitor_id,
            "park_id": park_id,
            "visit_start_date": visitor_start_date,
            "visit_end_date": visitor_end_date,
        })
    
    return visits, visitors_df

# Generate the data with patterns

# Generate the data
start_date = datetime(2018, 1, 1)
end_date = datetime(2023, 12, 31)
num_records = 10500

visits_data_with_patterns, visitors_df = generate_visitors_with_patterns(num_records, start_date, end_date, national_parks)

# Save to disk
visitors_df.to_csv("../data/visitors.csv", index=False)
visits_df = pd.DataFrame(visits_data_with_patterns)
visits_df.to_csv("../data/visits.csv", index=False)
# -

visits_df = pd.DataFrame("../data/visits.csv")    
upload_df_to_db(visits_df, ParkVisits)

visitors_df = pd.DataFrame("../data/visitors.csv")    
upload_df_to_db(visitors_df, Visitors)

species_data_df = pd.read_csv("../data/species_data.csv")
upload_df_to_db(species_data_df, Species)

park_species_allocation = pd.read_csv("../data/park_species_allocation.csv")
upload_df_to_db(park_species_allocation, ParksSpecies)

park_facilities_allocation = pd.read_csv("../data/park_facilities_allocation.csv")
upload_df_to_db(park_facilities_allocation, ParkFacilities)
