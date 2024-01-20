import streamlit as st
import math
import pandas as pd
from team_info import team_logos

def get_team_points(team_name):
    seasons = ["2023"]
    team_points_for = []
    team_points_against = []

    for season in seasons:
        url = f"https://www.pro-football-reference.com/years/{season}/games.htm"
        dfs = pd.read_html(url, flavor="lxml", index_col=False)

        df = dfs[0]
        df.columns = ["Week", "Day", "Date", "Time", "Winner/Tie", "H/A", "Loser/Tie", "Boxscore", "Pts_winner", "Pts_loser", "YdsW", "TOW", "YdsL", "TOL"]
        
        # Filter rows for the specific team and extract points
        for index, row in df.iterrows():
            if row['Winner/Tie'] == team_name:
                team_points_for.append(row['Pts_winner'])
                team_points_against.append(row['Pts_loser'])
            elif row['Loser/Tie'] == team_name:
                team_points_for.append(row['Pts_loser'])
                team_points_against.append(row['Pts_winner'])

    # Remove nan values from the array
    team_points_for = [x for x in team_points_for if not math.isnan(float(x))]
    team_points_against = [x for x in team_points_against if not math.isnan(float(x))]
    # convert to integers
    team_points_for = [int(x) for x in team_points_for]
    team_points_against = [int(x) for x in team_points_against]

    return {
        "points_for": team_points_for,
        "points_against": team_points_against
    }

def calculate_averages(points_for, points_against):
    last4_for = points_for[-4:]
    last4_against = points_against[-4:]

    averages = {
        "average_points_for": round(sum(points_for) / len(points_for)),
        "average_last4_points_for": round(sum(last4_for) / len(last4_for)),
        "average_points_against": round(sum(points_against) / len(points_against)),
        "average_last4_points_against": round(sum(last4_against) / len(last4_against)),
    }
    return averages

def calculate_weighted_average(team1_averages, team2_averages):
    team1_points = ((0.3 * team1_averages["average_points_for"] + (0.7 * team1_averages["average_last4_points_for"])) + ((0.3 * team2_averages["average_points_against"]) + (0.7 * team2_averages["average_last4_points_against"]))) / 2
    team2_points = ((0.3 * team2_averages["average_points_for"] + (0.7 * team2_averages["average_last4_points_for"])) + ((0.3 * team1_averages["average_points_against"]) + (0.7 * team1_averages["average_last4_points_against"]))) / 2

    return {"team1": round(team1_points), "team2": round(team2_points)}

def calculate_three_game_average(points_for, points_against):
    moving_averages = {
        "moving_average_points_for": [],
        "moving_average_points_against": [],
    }

    for i in range(len(points_for)):
        if i < 2:
            moving_averages["moving_average_points_for"].append(0)
            moving_averages["moving_average_points_against"].append(0)
        else:
            moving_averages["moving_average_points_for"].append(
                round((points_for[i - 2] + points_for[i - 1] + points_for[i]) / 3)
            )
            moving_averages["moving_average_points_against"].append(
                round(
                    (points_against[i - 2] + points_against[i - 1] + points_against[i])
                    / 3
                )
            )

    return moving_averages

def find_previous_meeting(team1, team2):
    seasons = ["2021", "2022", "2023"]
    found_matches = []
    for season in seasons:
        url = f"https://www.pro-football-reference.com/years/{season}/games.htm"
        dfs = pd.read_html(url, flavor="lxml", index_col=False)

        # Access the first (and only) dataframe
        df = dfs[0]
        df.columns = ["Week", "Day", "Date", "Time", "Winner/Tie", "H/A", "Loser/Tie", "Boxscore", "Pts_winner", "Pts_loser", "YdsW", "TOW", "YdsL", "TOL"]
        
        # Filter rows for the specific team and extract points
        for index, row in df.iterrows():
            # check for nan values
            if row['Winner/Tie'] == team1 and row['Loser/Tie'] == team2 and not math.isnan(float(row['Pts_winner'])) and not math.isnan(float(row['Pts_loser'])):
              found_matches.append({
                  "winner": team1,
                  "winner_score": int(row['Pts_winner']),
                  "loser": team2,
                  "loser_score": int(row['Pts_loser']),
                  "week": row['Week'],
                  "season": season
              })
            elif row['Winner/Tie'] == team2 and row['Loser/Tie'] == team1 and not math.isnan(float(row['Pts_winner'])) and not math.isnan(float(row['Pts_loser'])):
              found_matches.append({
                  "winner": team2,
                  "winner_score": int(row['Pts_winner']),
                  "loser": team1,
                  "loser_score": int(row['Pts_loser']),
                  "week": row['Week'],
                  "season": season
              })
    return found_matches

def display_score(team1, team2, team1_score, team2_score):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if team1 in team_logos:
            # Centering using column width and st.image for logo
            st.image(team_logos[team1], width=50)

    with col2:
        # Center Team 1 score using HTML and CSS
        st.markdown(f"<h1 style='font-weight: bold; line-height: 1; padding: 0; margin: 0;'>{team1_score}</h1>", unsafe_allow_html=True)

    with col3:
        if team2 in team_logos:
            # Centering using column width and st.image for logo
            st.image(team_logos[team2], width=50)

    with col4:
        # Center Team 2 score using HTML and CSS
        st.markdown(f"<h1 style='font-weight: bold; line-height: 1; padding: 0; margin: 0;'>{team2_score}</h1>", unsafe_allow_html=True)

