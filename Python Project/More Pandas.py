import pandas as pd
import numpy as np


def answer_one():
    energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skip_footer=280 - 242)
    energy = energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1).replace('...', np.nan)
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy['Energy Supply'] = 1000000 * energy['Energy Supply']
    energy['Country'] = energy['Country'].str.replace('\d+', '').str.replace('\s+\(.*\)', '') \
        .replace(
        ['Republic of Korea', 'United States of America', 'United Kingdom of Great Britain and Northern Ireland',
         'China, Hong Kong Special Administrative Region'], ['South Korea', 'United States', 'United Kingdom',
                                                             'Hong Kong'])

    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP['Country Name'].replace(['Korea, Rep.', 'Iran, Islamic Rep.', 'Hong Kong SAR, China'],
                                ['South Korea', 'Iran', 'Hong Kong'], True)

    ScimEn = pd.read_excel('scimagojr-3.xlsx')

    energy.set_index('Country', inplace=True)
    GDP.set_index('Country Name', inplace=True)
    ScimEn.set_index('Country', inplace=True)

    df = pd.merge(energy, GDP, left_index=True, right_index=True)
    df = pd.merge(df, ScimEn, left_index=True, right_index=True)

    # col = list(df.columns[6:2006-1960+6])
    # df = df.drop(col, axis=1).iloc[0:15]
    df = df[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document',
             'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable',
             '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]\
             .sort_values('Rank').iloc[0:15]
    return df


# print(answer_one())


def answer_two():
    energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skip_footer=280 - 242)
    energy = energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1).replace('...', np.nan)
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy['Energy Supply'] = 1000000 * energy['Energy Supply']
    energy['Country'] = energy['Country'].str.replace('\d+', '').str.replace('\s+\(.*\)', '') \
        .replace(
        ['Republic of Korea', 'United States of America', 'United Kingdom of Great Britain and Northern Ireland',
         'China, Hong Kong Special Administrative Region'], ['South Korea', 'United States', 'United Kingdom',
                                                             'Hong Kong'])

    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP['Country Name'].replace(['Korea, Rep.', 'Iran, Islamic Rep.', 'Hong Kong SAR, China'],
                                ['South Korea', 'Iran', 'Hong Kong'], True)

    ScimEn = pd.read_excel('scimagojr-3.xlsx')

    energy.set_index('Country', inplace=True)
    GDP.set_index('Country Name', inplace=True)
    ScimEn.set_index('Country', inplace=True)

    df_inter = pd.merge(energy, GDP, left_index=True, right_index=True)
    df_inter = pd.merge(df_inter, ScimEn, left_index=True, right_index=True)

    df_union = pd.merge(energy, GDP, how='outer', left_index=True, right_index=True)
    df_union = pd.merge(df_union, ScimEn, how='outer', left_index=True, right_index=True)

    entries_lose = len(df_union) - len(df_inter)
    return entries_lose


# print(answer_two())


def answer_three():
    df = answer_one()
    col = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    avgGDP = df.apply(lambda x: np.mean(x[col]), axis=1).sort_values(ascending=False)
    # avgGDP = np.mean(df[col], axis=1).sort_values(ascending=False)
    return avgGDP


# print(answer_three())


def answer_four():
    df = answer_one()
    df_avgGDP = answer_three()
    country = df.loc[df_avgGDP.index[5]]
    GDP_ch = country['2015'] - country['2006']
    return GDP_ch


# print(answer_four())


# Energy Supply per Capita
def answer_five():
    df = answer_one()
    mean = np.mean(df['Energy Supply per Capita'])
    return mean


# print(answer_five())


def answer_six():
    df = answer_one()
    country = np.argmax(df['% Renewable'])
    per = np.max(df['% Renewable'])
    return country, per


# print(answer_six())


def answer_seven():
    df = answer_one()
    df['Self-Citations to Total Citations'] = df['Self-citations'] / df['Citations']
    country = np.argmax(df['Self-Citations to Total Citations'])
    val = np.max(df['Self-Citations to Total Citations'])
    return country, val


# print(answer_seven())


# third most populous country
def answer_eight():
    df = answer_one()
    df['population'] = df['Energy Supply'] / df['Energy Supply per Capita']
    country_third = df['population'].nlargest(3).index[2]
    return country_third


# print(answer_eight())


def answer_nine():
    df = answer_one()
    df['population'] = df['Energy Supply'] / df['Energy Supply per Capita']
    df['citable documents per person'] = df['Citable documents'] / df['population']
    corr = df['Energy Supply per Capita'].corr(df['citable documents per person'])
    return corr


# print(answer_nine())


def answer_ten():
    df = answer_one()
    df_median = df['% Renewable'].median()
    df['HighRenew'] = df['% Renewable'] >= df_median
    return df['HighRenew'] * 1  # convert boolean values to 1 or 0


# print(answer_ten())


def answer_eleven():
    df = answer_one()
    ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'}
    df['population'] = df['Energy Supply'] / df['Energy Supply per Capita']

    def agg(x):
        names = {'size': np.size(x), 'sum': np.sum(x), 'mean': np.average(x), 'std': np.std(x)}
        names = pd.Series(names, index=['size', 'sum', 'mean', 'std'])
        return names

    df_group = df.groupby(ContinentDict)['population'].apply(agg)

    # alternative
    # df_group = df.groupby(ContinentDict)['population'].\
    #     agg({'size': np.size, 'sum': np.sum, 'mean': np.average, 'std': np.std})

    return df_group


# print(answer_eleven())


def answer_twelve():
    df = answer_one()
    df['% Renewable'] = pd.cut(df['% Renewable'],5)
    ContinentDict = {'China':'Asia',
                      'United States':'North America',
                      'Japan':'Asia',
                      'United Kingdom':'Europe',
                      'Russian Federation':'Europe',
                      'Canada':'North America',
                      'Germany':'Europe',
                      'India':'Asia',
                      'France':'Europe',
                      'South Korea':'Asia',
                      'Italy':'Europe',
                      'Spain':'Europe',
                      'Iran':'Asia',
                      'Australia':'Australia',
                      'Brazil':'South America'}
    df_group = df.groupby([ContinentDict, '% Renewable']).size()
    return df_group


# print(answer_twelve())