import csv
from datetime import datetime
import numpy as np
from overrides.typing_utils import unknown
from db import db
from models.location import Location
from models.terror_events import TerrorEvent
import pandas as pd
from sqlalchemy import extract



def init_first_data():
    df = pd.read_csv("../Data/globalterrorismdb_0718dist-1000 rows.csv", encoding='latin_1')
    df.replace({'': None, 'Unknown': None, np.NaN: None}, inplace=True)

    num_columns = ['iyear', 'imonth', 'iday', 'nkill', 'nwound']
    df[num_columns] = df[num_columns].fillna(0)

    for index, row in df.iterrows():
        print(row)
        location = Location(region = row.get('region'),
                            country = row.get('country_txt'),
                            city = row.get('city'),
                            latitude = row.get('latitude'),
                            longitude = row.get('longitude'))

        # Check if location already exists by coordinates
        existing_location = db.session.query(Location).filter(
            Location.latitude.like(f'{row.get('latitude')}') &
            Location.longitude.like(f'{row.get('longitude')}')).first()

        if existing_location:
            location_id = existing_location.id
            print(f"location {location_id} already exists")
        else:
            db.session.add(location)
            db.session.commit()
            location_id = location.id
            print(f'added {location_id}')

        year = int(row["iyear"]) if row['iyear'] != 0 else 1
        month = int(row['imonth']) if row['imonth'] != 0 else 1
        day = int(row['iday']) if row['iday'] != 0 else 1
        date= datetime(year, month, day)
        terror_event = TerrorEvent(year = int(row.get("iyear")),
                                   month = int(row.get('imonth')),
                                   day = int(row.get('iday')),
                                   date = date,
                                   terror_group = row.get('gname'),
                                   kills = row.get('nkill'),
                                   wounds = row.get('nwound'),
                                   attack_type= row.get('attacktype1_txt'),
                                   weapon_type = row.get('weaptype1_txt'),
                                   target_type = row.get('targtype1_txt'),
                                   location_id = location_id)
        event_exists = db.session.query(TerrorEvent).filter((TerrorEvent.location_id == terror_event.location_id) & (TerrorEvent.date == terror_event.date)).first()
        if event_exists:
            print(f"event already exists")
        else:
            db.session.add(terror_event)
            db.session.commit()
    db.session.close()



def init_second_data():
    df = pd.read_csv("../Data/RAND_Database_of_Worldwide_Terrorism_Incidents - 5000 rows.csv", encoding='latin_1')
    df.replace({'': None, 'Unknown': None, np.NaN: None, 'Other': None}, inplace=True)

    num_columns = ['Injuries', 'Fatalities']
    df[num_columns] = df[num_columns].fillna(0)

    for index, row in df.iterrows():
        print(row)
        location = Location(region = None,
                            country = row.get('Country'),
                            city = row.get('City'),
                            latitude = None,
                            longitude = None)

        # Check if location already exists by coordinates
        existing_location = db.session.query(Location).filter(
            Location.country.like(f'{row.get('Country')}') &
            Location.city.like(f'{row.get('City')}') & (Location.longitude.is_(None)) & (Location.latitude.is_(None))).first()

        if existing_location:
            location_id = existing_location.id
            print(f"location {location_id} already exists")
        else:
            db.session.add(location)
            db.session.commit()
            location_id = location.id
            print(f'added {location_id}')

        date = datetime.strptime(row.get("Date"), '%d-%b-%y')
        terror_event = TerrorEvent(year = date.year,
                                   month = date.month,
                                   day = date.day,
                                   date = date,
                                   terror_group = row.get('Perpetrator'),
                                   kills = row.get('Fatalities'),
                                   wounds = row.get('Injuries'),
                                   attack_type= row.get('Weapon'),
                                   weapon_type = row.get('Weapon'),
                                   target_type = None,
                                   location_id = location_id)
        event_exists = db.session.query(TerrorEvent).filter((TerrorEvent.location_id == terror_event.location_id) & (TerrorEvent.date == terror_event.date)).first()
        if event_exists:
            print(f"event already exists")
        else:
            db.session.add(terror_event)
            db.session.commit()
    db.session.close()

def get_terror_events_df():
    df = pd.read_sql("terror_event", db.engine)
    return df
def get_location_df():
    df = pd.read_sql("location", db.engine)
    return df
