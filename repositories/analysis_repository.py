import folium
import requests
from repositories.data_repository import get_terror_events_df, get_location_df


def terror_events_with_lethality_score():
    terror_events = get_terror_events_df()
    terror_events["lethality_level"] = (terror_events['kills'] * 2 if not None else 0) + terror_events['wounds']
    return terror_events

def lethality_avg_by_area(area):
    if area not in ["country", "city", "region"]:
        return "invalid area"
    terror_events = terror_events_with_lethality_score()
    location = get_location_df()
    res = terror_events.merge(location, left_on="location_id", right_on="id").groupby(f'{area}').mean(
        'lethality_level').sort_values('lethality_level', ascending=False).reset_index()[
        [f'{area}', 'lethality_level']]
    return res


def lethality_change_by_area_and_year(area):
    try:

        terror_events = terror_events_with_lethality_score()
        if terror_events is None or terror_events.empty:
            raise ValueError("Data from terror_events_with_lethality_score is empty or None.")


        location = get_location_df()
        if location is None or location.empty:
            raise ValueError("Data from get_location_df is empty or None.")


        required_columns_terror = {'location_id', 'lethality_level', 'year'}
        required_columns_location = {'id', area}

        if not required_columns_terror.issubset(terror_events.columns):
            raise ValueError(
                f"Missing required columns in terror_events: {required_columns_terror - set(terror_events.columns)}")

        if not required_columns_location.issubset(location.columns):
            raise ValueError(
                f"Missing required columns in location: {required_columns_location - set(location.columns)}")


        group_by_area_and_year = (
            terror_events
            .merge(location, left_on="location_id", right_on="id")
            .groupby([f'{area}', 'year'])
            .sum('lethality_level')
            .sort_values(f'{area}')
            .reset_index()
        )


        group_by_area_and_year['pct_change'] = (
                group_by_area_and_year
                .groupby(f'{area}')['lethality_level']
                .pct_change() * 100
        )


        res = group_by_area_and_year[[f'{area}', 'year', 'pct_change']]
        return res

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None

    except KeyError as ke:
        print(f"KeyError: {ke}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def active_groups_by_area(area, top):
    terror_events = terror_events_with_lethality_score()
    location = get_location_df()
    res = terror_events.merge(location, left_on="location_id", right_on="id").groupby([f'{area}', 'terror_group']).sum(
        'lethality_level').sort_values([f'{area}', "lethality_level"], ascending=[True, False]).reset_index().groupby(
        'country').head(top)
    return res


def most_targeted_location_by_area():
    terror_events = get_terror_events_df()
    location = get_location_df()
    df = terror_events.merge(location, left_on="location_id", right_on="id")

    unique_count_by_location = (df.groupby(['country', 'city', 'longitude', 'latitude'])['terror_group']
                         .nunique()
                         .reset_index()
                         .rename(columns={'terror_group': 'groups_count'}))

    most_attacked_location = (unique_count_by_location.sort_values('groups_count', ascending=False)
               .groupby('country')
               .first()
               .reset_index())

    def get_terror_groups(row):
        mask = ((df['longitude'] == row['longitude']) &
                (df['latitude'] == row['latitude']))
        return df[mask]['terror_group'].unique()

    most_attacked_location['terror_groups'] = most_attacked_location.apply(get_terror_groups, axis=1)

    return most_attacked_location


