import pandas as pd
import numpy as np

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index)
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]


# print(answer_zero())


def answer_one():
    max_gold = df[df['Gold'] == max(df['Gold'])]
    return max_gold.index.values[0]


# print(answer_one())


# biggest difference between their summer and winter gold medal counts
def answer_two():
    gold_diff = abs(df['Gold'] - df['Gold.1'])
    max_gold_diff = gold_diff[gold_diff == max(gold_diff)]
    country = max_gold_diff.index.values[0]
    return country


# print(answer_two())


# biggest difference between their summer gold medal counts and winter gold medal counts
# relative to their total gold medal count
def answer_three():
    df_gold = df[(df['Gold.1'] > 0) & (df['Gold'] > 0)]
    gold_diff = abs(df_gold['Gold'] - df_gold['Gold.1']) / (df_gold['Gold'] + df_gold['Gold.1'])
    max_gold_diff = gold_diff[gold_diff == max(gold_diff)]
    country = max_gold_diff.index.values[0]
    return country


# print(answer_three())


#a Series called "Points" which is a weighted value where each gold medal (Gold.2) counts for 3 points,
# silver medals (Silver.2) for 2 points, and bronze medals (Bronze.2) for 1 point
def answer_four():
    point = df['Gold.2'] * 3 + df['Silver.2'] * 2 + df['Bronze.2'] * 1
    return point


# print(answer_four())


census_df = pd.read_csv('census.csv')


# Which state has the most counties in it?
def answer_five():
    df = census_df.set_index(['STNAME'])
    county_num = [df.loc[state]['COUNTY'].count() for state in census_df['STNAME'].unique()]
    state_index = np.argmax(county_num)
    max_county_state = census_df['STNAME'].unique()[state_index]
    return max_county_state


# print(answer_five())


# only looking at three most populous counties for each state, what are three most populous states
def answer_six():
    df = census_df[census_df['SUMLEV'] == 50]  # ridiculous US counties
    df = df.set_index(['STNAME', 'CTYNAME'])
    pop_county = [df.loc[state].nlargest(4, 'CENSUS2010POP') for state in census_df['STNAME'].unique()]

    # county_name = [[sate_county.index.values[1],
    #                 sate_county.index.values[2],
    #                 sate_county.index.values[3]] for sate_county in pop_county]
    county_three_pop = [sum(sate_county['CENSUS2010POP'].iloc[0:3]) for sate_county in pop_county]
    state_three_index = np.array(county_three_pop).argsort()[-3:][::-1]
    # argsort() returns index ascending, [::-1] concerts it be descending
    state_three = list(census_df['STNAME'].unique()[state_three_index])
    return state_three


# print(answer_six())


# Which county has had the largest absolute change in population
def answer_seven():
    df = census_df[census_df['SUMLEV'] == 50]  # ridiculous US counties
    popcols = ['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012',
               'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']
    cols =['CTYNAME'] + popcols
    dfp = df[cols]
    dfp = dfp.set_index(['CTYNAME'])
    maxx = dfp[popcols].max(axis=1)  # max yearly population of each county
    minn = dfp[popcols].min(axis=1)  # min yearly population of each county
    dfp['diff'] = maxx - minn  # max difference of each county
    county = dfp['diff'].argmax()
    return county


# print(answer_seven())


# counties that belong to regions 1 or 2, whose name starts with 'Washington',
# and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014
def answer_eight():
    df = census_df[['REGION', 'POPESTIMATE2015', 'POPESTIMATE2014', 'CTYNAME', 'STNAME']]
    county = df[((df['REGION'] == 1) | (df['REGION'] == 2)) & (df['POPESTIMATE2015'] > df['POPESTIMATE2014'])
                & (df['CTYNAME'] == 'Washington County')]
    county_de = county[['STNAME', 'CTYNAME']]
    return county_de


print(answer_eight())