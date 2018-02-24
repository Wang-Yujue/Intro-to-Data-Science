import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National',
          'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana',
          'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho',
          'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan',
          'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico',
          'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa',
          'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana',
          'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California',
          'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island',
          'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia',
          'ND': 'North Dakota', 'VA': 'Virginia'}


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states from the
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''

    data = pd.read_table('university_towns.txt', names=["State", "RegionName"])
    states_edit = [state_name + '[edit]' for state_name in
              states.values()]  # add [edit] to dict for finding states in the data
    state_index = data.loc[data['State'].isin(states_edit)].index  # get state index from the state region combined list
    data['RegionName'] = data.drop(state_index)  # creat new region column with states dropped
    data.replace(np.nan, 0, True)  # do not know why np.nan can not be slected, assign it to be 0 for the next step
    region_index = data.loc[
        data['RegionName'] != 0].index  # region index now are those indice in state col with value of NaN
    data['State'] = data.drop(region_index)  # drop region items in state col
    data.replace(np.nan, 0, True)

    state_list = []
    i = 0
    for state in data[
        'State']:  # loop for assign the NaN values to states according to states and regions current position in the DataFrame
        state_list.append(state)
        if state == 0:
            state_list[i] = state_list[
                i - 1]  # simply assign the last value to the next NaN, because the condition always starts with the first NaN after the conrresponding state
        i = i + 1

    data['State'] = state_list  # assign new state list to State col, now the states and regions are paired
    data = data.drop(state_index).reset_index(
        drop=True)  # drop 0s in region which corresponding to the state_index in region col and then reindex the DataFrame
    data['State'] = data['State'].str.replace('\[.*\]', '')
    data['RegionName'] = data['RegionName'].str.replace('\[.*\]', '').str.replace('\s+\(.*\)',
                                                                                  '')  # eventurally remove [], () and contents in them
    data['RegionName'].loc[[33, 141, 216, 218, 237]] = ['Pomona', 'Lexington', 'Duluth', 'Mankato', 'Fulton']
    # fix some odd items with extra dot sign or single bracket
    return data


# print(get_list_of_university_towns())


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3'''
    # A recession is defined as starting with two consecutive quarters of GDP decline,
    # and ending with two consecutive quarters of GDP growth.
    data = pd.read_excel('gdplev.xls')
    data = data[data['Unnamed: 4'] >= '2000q1']
    # For this assignment, only look at GDP data from the first quarter of 2000 onward
    data.drop(1, inplace=True)
    # use the chained value in 2009 dollars
    data = data[['Unnamed: 4', 'Unnamed: 6']].reset_index(drop=True)
    data.columns = ['Quarter', 'GDP']
    for i in range(1, 66):
        if data['GDP'].iloc[i] < data['GDP'].iloc[i - 1] and data['GDP'].iloc[i] > data['GDP'].iloc[i + 1]:
            break
    recess_start = data['Quarter'].iloc[i - 1]
    return recess_start


# print(get_recession_start())


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a
    string value in a format such as 2005q3'''
    data = pd.read_excel('gdplev.xls')
    data = data[data['Unnamed: 4'] >= '2008q3']
    # For this assignment, only look at GDP data from the first quarter of 2000 onward
    data.drop(1, inplace=True)
    # use the value of curent dollars
    data = data[['Unnamed: 4', 'Unnamed: 5']].reset_index(drop=True)
    data.columns = ['Quarter', 'GDP']
    for i in range(1, 66):
        if data['GDP'].iloc[i] > data['GDP'].iloc[i - 1] and data['GDP'].iloc[i] < data['GDP'].iloc[i + 1]:
            break
    recess_end = data['Quarter'].iloc[i+1]
    return recess_end


# print(get_recession_end())


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a
    string value in a format such as 2005q3'''
    # A recession bottom is the quarter within a recession which had the lowest GDP.
    data = pd.read_excel('gdplev.xls')
    data = data[(data['Unnamed: 4'] >= '2008q3') & (data['Unnamed: 4'] <= '2009q4')]
    # For this assignment, only look at GDP data from the first quarter of 2000 onward
    # use the value of curent dollars
    data = data[['Unnamed: 4', 'Unnamed: 5']].reset_index(drop=True)
    data.columns = ['Quarter', 'GDP']
    recess_bot = data['Quarter'].iloc[np.argmin(data['GDP'])]
    return recess_bot


# print(get_recession_bottom())


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.'''
    data = pd.read_csv('City_Zhvi_AllHomes.csv')
    data.drop(['RegionID', 'Metro', 'CountyName', 'SizeRank'], axis=1, inplace=True)
    data['State'] = data['State'].map(states)
    data.set_index(['State', 'RegionName'], inplace=True)
    data = data.loc[:, '2000-01':]

    start = 0
    for year in range(2000, 2017):
        for q in ['q1', 'q2', 'q3', 'q4']:
            data[str(year) + q] = data.iloc[:, start:start + 2].mean(axis=1)
            start = start + 3

    data.drop(data.loc[:, '2000-01':'2016-08'], axis=1, inplace=True)
    data.drop(['2016q4'], axis=1, inplace=True)
    return data


# print(convert_housing_data_to_quarters())


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    data = convert_housing_data_to_quarters()
    uni_towns = get_list_of_university_towns()
    # ratio is defined as the quarter before the recession starts(2008q3 - quarter) compared to the recession bottom
    data['price_ratio'] = data['2008q2'] / data['2009q2']
    data = data['price_ratio']

    data_uni_index = []
    for i in range(len(uni_towns)):
        for j in range(len(data)):
            if tuple(uni_towns.values[i]) == data.index.values[j]:
                data_uni_index.append(j)  # find uni towns indices in housing price data

    uni = data.iloc[data_uni_index]  # select out all uni towns in the housing price data
    n_uni = data.drop(uni.index)  # drop uni towns to get non uni towns data
    _, p = ttest_ind(uni.dropna(), n_uni.dropna())  # t_test pvalue smaller than 0.01,
                                                    # there is difference between uni and non_uni
    if p < 0.01:
        different = True
    else:
        different = False
    if uni.mean() < n_uni.mean():
        better = 'university town'
    else:
        better = 'non-university town'
    return different, p, better


print(run_ttest())
