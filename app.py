import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
from calculations import get_team_points, calculate_averages, calculate_weighted_average, calculate_three_game_average, find_previous_meeting, display_score
from color_helpers import are_colors_too_similar, create_logo_placeholder
from team_info import team_colors, team_logos

style.use('dark_background')

# Streamlit app layout
st.markdown('<h1 style="text-align: center;">Game Score Calculator</h1>', unsafe_allow_html=True)

# Creating two main columns for each team's section
main_col1, main_col2 = st.columns(2)

# Team 1 Section
with main_col1:
    col1_1, col1_2, col1_3 = st.columns([1,2,1])  # Ratio 1:2:1 for side and center columns
    logo_placeholder1 = col1_2.empty()  # Place the logo in the center column
    team1 = st.selectbox("Select Team 1:", [None] + list(team_logos.keys()), index=0, key='team1')
    create_logo_placeholder(logo_placeholder1, team_logos.get(team1), height=162)
    if team1:
        team1_points = get_team_points(team1)

# Team 2 Section
with main_col2:
    col2_1, col2_2, col2_3 = st.columns([1,2,1])  # Ratio 1:2:1 for side and center columns
    logo_placeholder2 = col2_2.empty()  # Place the logo in the center column
    team2 = st.selectbox("Select Team 2:", [None] + list(team_logos.keys()), index=0, key='team2')
    create_logo_placeholder(logo_placeholder2, team_logos.get(team2), height=162)
    if team2:
        team2_points = get_team_points(team2)

# Displaying the scores and graphs
if team1 and team2:
    # Determine the minimum length of the two arrays
    # Some teams have playoff games
    min_length = min(len(team1_points["points_for"]), len(team2_points["points_for"]))

    # Trim the arrays to the same length
    trimmed_team1_points_for = team1_points["points_for"][:min_length]
    trimmed_team2_points_for = team2_points["points_for"][:min_length]
    trimmed_team1_points_against = team1_points["points_against"][:min_length]
    trimmed_team2_points_against = team2_points["points_against"][:min_length]

    # Preparing data for 'Points For' graph
    points_for_df = pd.DataFrame({
        team1: trimmed_team1_points_for,
        team2: trimmed_team2_points_for
    })
    points_for_df.index = range(1, min_length + 1)  # Index starting at 1

    # Preparing data for 'Points Against' graph
    points_against_df = pd.DataFrame({
        team1: trimmed_team1_points_against,
        team2: trimmed_team2_points_against
    })
    points_against_df.index = range(1, min_length + 1)  # Index starting at 1

    # Averages
    team1_averages = calculate_averages(team1_points["points_for"], team1_points["points_against"])
    team2_averages = calculate_averages(team2_points["points_for"], team2_points["points_against"])

    # Weighted average prediction
    predictions = calculate_weighted_average(team1_averages, team2_averages)
    st.markdown("<h2>Weighted Average Prediction</h2>", unsafe_allow_html=True)
    display_score(team1, team2, predictions["team1"], predictions["team2"])

    # Three game average prediction
    team1_moving_averages = calculate_three_game_average(team1_points["points_for"], team1_points["points_against"])
    team2_moving_averages = calculate_three_game_average(team2_points["points_for"], team2_points["points_against"])
    st.markdown("<h2>Three Game Average Prediction</h2>", unsafe_allow_html=True)
    display_score(team1, team2, team1_moving_averages["moving_average_points_for"][-1], team2_moving_averages["moving_average_points_for"][-1])

    # Previous meeting
    st.markdown('<h2>Previous Meetings</h2>', unsafe_allow_html=True)

    previous_meeting = find_previous_meeting(team1, team2)
    # display teams in the correct order
    if previous_meeting:
        for meeting in previous_meeting:
            st.write(f"Week {meeting['week']}, {meeting['season']} Season")
            winner, loser = (meeting["winner"], meeting["loser"]) if meeting['winner'] == team1 else (meeting["loser"], meeting["winner"])
            winner_score, loser_score = (meeting["winner_score"], meeting["loser_score"]) if meeting['winner'] == team1 else (meeting["loser_score"], meeting["winner_score"])
            display_score(winner, loser, winner_score, loser_score)
    else:
        st.write("No previous meeting found.")

    # Average of averages
    st.markdown("<h2>Average of Averages</h2>", unsafe_allow_html=True)

    team1_scores = []
    team2_scores = []

    if previous_meeting:
        for meeting in previous_meeting:
            if meeting['winner'] == team1:
                team1_scores.append(meeting["winner_score"])
                team2_scores.append(meeting["loser_score"])
            else:
                team1_scores.append(meeting["loser_score"])
                team2_scores.append(meeting["winner_score"])

        team1_collection = [predictions["team1"], team1_moving_averages["moving_average_points_for"][-1], sum(team1_scores)/len(team1_scores)]
        team2_collection = [predictions["team2"], team2_moving_averages["moving_average_points_for"][-1], sum(team2_scores)/len(team2_scores)]
    else:
        team1_collection = [predictions["team1"], team1_moving_averages["moving_average_points_for"][-1]]
        team2_collection = [predictions["team2"], team2_moving_averages["moving_average_points_for"][-1]]

    display_score(team1, team2, round(sum(team1_collection) / len(team1_collection)), round(sum(team2_collection) / len(team2_collection)))

















    # Plotting
    st.markdown("<h2>Graphs</h2>", unsafe_allow_html=True)
    color_1 = team_colors[team1][0]  # Primary color of Team1
    color_2 = team_colors[team2][0]  # Primary color of Team2

    if are_colors_too_similar(color_1, color_2):
        color_2 = team_colors[team2][1]  # Use secondary color for Team2 if similar

    team_colors_dict = {team1: color_1, team2: color_2}

    plt.figure()
    for team in [team1, team2]:
        if team in points_for_df:
            plt.plot(points_for_df.index, points_for_df[team], label=team, color=team_colors_dict[team])
    plt.title('Season (Points For)')
    plt.xlabel('Week')
    plt.ylabel('Points')
    plt.xticks(points_for_df.index)
    plt.legend()
    st.pyplot(plt)

    # Plotting 'Points Against'
    plt.figure()
    for team in [team1, team2]:
        if team in points_against_df:
            plt.plot(points_against_df.index, points_against_df[team], label=team, color=team_colors_dict[team])
    plt.title('Season (Points Against)')
    plt.xlabel('Week')
    plt.ylabel('Points')
    plt.xticks(points_against_df.index)
    plt.legend()
    st.pyplot(plt)

    # Plotting moving averages
    # Plotting 'Points For'
    plt.figure()
    plt.plot(team1_moving_averages["moving_average_points_for"], label=team1, color=color_1)
    plt.plot(team2_moving_averages["moving_average_points_for"], label=team2, color=color_2)
    plt.title('Three Game Average (Points For)')
    plt.xlabel('Week')
    plt.ylabel('Points')
    plt.legend()
    st.pyplot(plt)

    # Plotting 'Points Against'
    plt.figure()
    plt.plot(team1_moving_averages["moving_average_points_against"], label=team1, color=color_1)
    plt.plot(team2_moving_averages["moving_average_points_against"], label=team2, color=color_2)
    plt.title('Three Game Average (Points Against)')
    plt.xlabel('Week')
    plt.ylabel('Points')
    plt.legend()
    st.pyplot(plt)