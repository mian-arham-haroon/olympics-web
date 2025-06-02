import numpy as np

def fetch_medal_tally(df,year,country):
    global temp_df
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag=1
        temp_df = medal_df[medal_df['region']==country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year']==int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region']==country) & (medal_df['Year']==int(year))]
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    return x

def medal_telly(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                             ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    return medal_tally
def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return year,country

def data_over_time(df,col):
    data_over_time = df.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    data_over_time.rename(columns={f'Year':'Edition','count':f'Number of {col}s'}, inplace=True)
    return data_over_time

def most_successful(df, sport):
    temp_df = df if sport == 'Overall' else df[df['Sport'] == sport]
    temp_df = temp_df[temp_df['Medal'].notnull()]
    top_athletes = temp_df['Name'].value_counts().reset_index().head(20)
    top_athletes.columns = ['Athlete', 'Medal Count']
    result = top_athletes.merge(df, left_on='Athlete', right_on='Name', how='left')[['Athlete', 'region', 'Sport', 'Medal Count']].drop_duplicates('Athlete')
    return result

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(subset=['Team','NOC','Games','Year','City', 'Sport','Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    temp_df = df[df['region'] == country]
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    p = temp_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    return p

def most_successful_countrywise(df, country):
    temp_df = df[df['region'] == country]
    temp_df = temp_df[temp_df['Medal'].notnull()]
    top_athletes = temp_df['Name'].value_counts().reset_index().head(20)
    top_athletes.columns = ['Athlete', 'Medal Count']
    result = top_athletes.merge(df, left_on='Athlete', right_on='Name', how='left')[['Athlete', 'Sport', 'Medal Count']].drop_duplicates('Athlete')
    return result.head(10)

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    temp_df = athlete_df[athlete_df['Sport'] == sport]  
    return temp_df

def man_vs_woman(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left' )
    final.rename(columns={'Name_x':'Male','Name_y':'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final