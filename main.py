import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import seaborn as sns   
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import scipy 
# Load data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# Preprocess data
df = preprocessor.preprocess(df, region_df)
st.sidebar.image('qq.png', use_column_width=True, channels="RGBA")

# Sidebar
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete Wise Analysis')
)

# Medal Tally Section
if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_telly = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Display title based on selection
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f'Medal Tally in {selected_year} Olympics')
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f'{selected_country} overall performance')
    else:
        st.title(f'{selected_country} performance in {selected_year} Olympics')

    st.table(medal_telly)

# Overall Analysis Section
if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()




    st.title(f'Top Statistics')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nation_over_time = helper.data_over_time(df,'region')
    st.subheader("Number of Participating Nations Over Time")
    fig = px.line(
	nation_over_time,
	x='Edition',
	y='Number of regions',
	title='Number of Nations Over the Years'
    )
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    st.subheader("Number of Participating Events Over Time")
    fig = px.line(
	events_over_time,
	x='Edition',
	y='Number of Events',
	title='Number of Events Over the Years'
    )
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df,'Name')
    st.subheader("Number of Participating Athletes Over Time")
    fig = px.line(
        athletes_over_time,
        x='Edition',
        y='Number of Names',  # <-- fixed here
        title='Number of Athletes Over the Years'
    )
    st.plotly_chart(fig)

    st.title('Number of Events Over Time by Sport')
    # Prepare data: count unique events per sport per year
    events_heatmap = (
        df.drop_duplicates(['Year', 'Sport', 'Event'])
        .groupby(['Sport', 'Year'])
        .size()
        .unstack(fill_value=0)
        .astype(int)
    )
    fig, ax = plt.subplots(figsize=(16, len(events_heatmap) * 0.5 + 4))
    fig.patch.set_facecolor('#f9f9f9')  
    ax.set_facecolor('#f9f9f9')         
    sns.heatmap(events_heatmap, cmap='Greys', annot=True, fmt='d', linewidths=0.5, ax=ax)
    plt.xlabel('Year')
    plt.ylabel('Sport')
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x=helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.header('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select Country', country_list)
    country_df = helper.yearwise_medal_tally(df, selected_country)
    st.title(f'{selected_country} Medal Tally Over the Years')
    fig = px.line(country_df, x='Year', y='Medal')
    st.plotly_chart(fig)

    st.title(f'{selected_country} Performance Over the Years')
    pt = helper.country_event_heatmap(df, selected_country)    
    plt.figure(figsize=(20, 20))
    sns.heatmap(
        pt,
        cmap='Greys',
        fmt='d',
        annot=True,
        linewidths=0.5
    )
    plt.title(f'{selected_country} Event Participation Heatmap')
    st.pyplot(plt)

    st.title(f'Top 10 Athletes from {selected_country}')
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete Wise Analysis':

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna().tolist()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna().tolist()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna().tolist()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna().tolist()
    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        group_labels=['Overall Age', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'],
        show_hist=False,
        show_rug=False
    )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Age Distribution of Athletes')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = [sport for sport in [
        'Basketball', 'Football', 'Hockey', 'Tennis', 'Swimming', 
        'Athletics', 'Gymnastics', 'Boxing', 'Wrestling', 'Volleyball',
        'Badminton', 'Table Tennis', 'Archery', 'Fencing', 'Shooting', 
        'Cycling', 'Rowing', 'Judo', 'Taekwondo', 'Weightlifting', 'Diving', 
        'Surfing', 'Skateboarding', 'Triathlon', 'Rugby', 'Handball', 'Softball', 
        'Baseball', 'Cricket', 'Golf', 'Equestrian', 'Sailing', 'Canoeing', 'Kayaking', 
        'Luge', 'Bobsleigh', 'Skeleton', 'Curling', 'Biathlon', 'Cross-Country Skiing', 
        'Alpine Skiing', 'Snowboarding', 'Speed Skating', 'Figure Skating', 'Short Track Speed Skating',
        'Freestyle Skiing', 'Nordic Combined', 'Ski Jumping', 'Ice Hockey', 'Water Polo'
    ] if sport in athlete_df['Sport'].unique()]
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        ages = temp_df[temp_df['Medal']=='Gold']['Age'].dropna()
        if len(ages) > 0:
            x.append(ages)
            name.append(sport)
    
    if x:  
        fig = ff.create_distplot(
            x,
            group_labels=name,
            show_hist=False,
            show_rug=False
        )    
        
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title('Age Distribution of Gold Medalists by Sport')
        st.plotly_chart(fig) 
    else:
        st.warning("No gold medalist age data available for the selected sports.")
    

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title('Height vs Weight of Athletes')
    selected_sport = st.selectbox('Select a Sport', sport_list) 
    if selected_sport == 'Overall':
        temp_df = df.dropna(subset=['Weight', 'Height'])
        title = 'Height vs Weight of Athletes (All Sports)'
    else:        
        temp_df=helper.weight_v_height(df, selected_sport)
        title = f'Height vs Weight of Athletes in {selected_sport}'
    fig = px.scatter(
        temp_df,
        x='Weight',
        y='Height', 
        color='Medal',
        symbol='Sex',
        title=title
    )
    st.plotly_chart(fig)

    man_woman_df = helper.man_vs_woman(df)
    st.title('Male and Female Athletes Participation Over the Years')
    fig = px.line(
    man_woman_df,
    x='Year',
    y=['Male', 'Female'],
    labels={'value':'Number of Athletes', 'variable':'Sex'}
    )
    st.plotly_chart(fig)