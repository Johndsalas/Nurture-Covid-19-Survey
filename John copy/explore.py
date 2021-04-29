''' Functions for exploring qualitative data '''

import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns

def only_words(text):
    '''
    Turn text into list of words in text
    '''

    words = re.sub(r'[^\w\s]', '', text).split()
    
    return [word for word in words]


def  get_master_list(ngram_lists):
    
    master_ngram_list = []

    for lst in ngram_lists:
        for item in lst:
            master_ngram_list.append(item)
            
    return master_ngram_list


def get_ngram_value_counts(df,col,n,chart=True,return_df=True):
    '''
    Takes in a dataframe a column in that dataframe and a number 
    returns value count of ngrams in the specified column   
    '''

    # convert text in text column values to a list of bigrams for the full text column and for values representing each color
    ngram_list = df[col].apply(lambda text: list(nltk.ngrams(text.split(),n)))


    # combine lists in series into one master list
    ngram_master_list = get_master_list(ngram_list)


    # convert each master list to a series then convert each of those tuples into strings
    ngram_series = pd.Series(ngram_master_list).apply(lambda tup: str(tup))


    # get value count for each string tuple in the series
    ngram_freq = ngram_series.value_counts()
    
    # convert to dataframe
    ngram_frame = ngram_freq.to_frame(name=col)

    # make a bar chart if chart equals True
    if chart == True:

        ngram_frame.sort_values(by=col).tail(20).plot.barh(figsize=(7,7))
        plt.title(f"Most frequent {n}grams in {col}")

    # return dataframe if return_df equals True
    if return_df == True:

        return ngram_frame


def grams_race(df,col,n):
    '''
    '''

    # get set of values in race that have non null counterpart in the input column
    df_value_list = set(df.race.to_list())


    # convert text in text column values to a list of bigrams for the full text column and for values representing each color
    ngram_white = df[df.race == 'White'][col].apply(lambda text: list(nltk.ngrams(text.split(),n)))

    # combine lists in series into one master list
    ngram_white_master_list = get_master_list(ngram_white)


    # convert each master list to a series then convert each of those tuples into strings
    ngram_white_series = pd.Series(ngram_white_master_list).apply(lambda tup: str(tup))


    # get value count for each string tuple in the series
    ngram_white_freq = ngram_white_series.value_counts()
    
    # convert to dataframe
    ngram_white_frame = ngram_white_freq.to_frame(name=col)

    # make a bar chart if chart equals True
    if chart == True:

        ngram_frame.sort_values(by=col).tail(20).plot.barh(figsize=(7,7))
        plt.title(f"Most frequent {n}grams in {col}")

    # return dataframe if return_df equals True
    if return_df == True:

        return ngram_frame


def omnichart(df):
    '''
    Create a chart for each support showing the percentage of respondants for each value of a given column who
    identified as needing that support.
    '''

    column_list = ['Household Income', 'Household Income: Above or Below $75K', 'Race',
                   'Hispanic or Latinx', 'Survey Language', 'County', 'Virginia Health District', 
                   'Nurture Area', 'Planning District 15', 'Pregnancy Stage']
    
    need_list = ['Birth Doula', 'Postpartum Doula', 'Lactation','Mental Health', 'Social', 'Diapers', 'Formula', 'Food', 'Housing',
                 'Transportation', 'Health Insurance', 'Financial', 'COVID 19 Education','No Support']

    removed_values_list = ['undisclosed',0]
  
    # get list of values that have 30 or more occurances in the column and set X axis to those values
    for column in column_list:
        
        value_list = [value for value in set(df[f'{column}']) if df[f'{column}'].value_counts()[value] >= 25 and value not in removed_values_list]
        
        if column == 'Income':
            
            value_list = ['$40,000 or under','$40,001 - $75,000', '$75,001 - $100,000', 'S100,001 - $125,000', '$125,001 and over.']
                  
        X = [str(value) for value in value_list]

        # get list of y values and plot chart
        for need in need_list:

            # y = rows where column equals value and need equals one divided by rows where column equals value 
            y = [round((df[(df[f'{column}'] == value) & (df[f'{need}'] == 1)].shape[0] / df[df[f'{column}'] == value].shape[0])*100,0) for value in value_list]

            plt.figure(figsize=(11, 6))
            plt.bar(X, y, align='center', alpha=0.5)
            plt.ylim([0,100])

            plt.ylabel('% of Respondents in Each Catagory')
            plt.title(f'Percent of Respondants Identifying {need} as support needed by {column}')

            plt.show()

            print(y)