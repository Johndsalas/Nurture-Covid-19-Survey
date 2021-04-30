''' prepares qualitative data for statistical exploration '''

import numpy as np
import pandas as pd
import re
import unicodedata
import pathlib

import nltk
from nltk.corpus import stopwords

def get_data():

    # acquiring data
    df = pd.read_excel('survey_data.xlsx')

    return df

def  income_values(value):
    
    if value == '$125,001 and over.': return "Over 125K"
    elif value == 'S100,001 - $125,000': return "100K+ to 125K"
    elif value == '$75,001 - $100,000': return "75K+ to 100K"
    elif value == '$40,001 - $75,000': return "40K+ to 75K"
    elif value == '$40,000 or under': return "40K and Under"
    else: return  False

def prep_data(df):

    # filling nans with 0's
    df = df.fillna(False)

    # Make Stage column to hold Pregnancy stage
    df['Pregnancy_Stage'] = 0
    df['Pregnancy_Stage'][df['1stTrimester'] == '1stTrimester'] = '1st Trimester'
    df['Pregnancy_Stage'][df['2ndTrimester'] == '2ndTrimester'] = '2nd Trimester'
    df['Pregnancy_Stage'][df['3rdTrimester'] == '3rdTrimester'] = '3rd Trimester'
    df['Pregnancy_Stage'][df['1yrBirth'] == '1yrBirth'] = '1 Year After Birth'
    df['Pregnancy_Stage'][df['2yrBirth'] == '2yrBirth'] = '2 Years After Birth'
    df['Pregnancy_Stage'][df['FamilyMember'] == 'FamilyMember'] = 'Family Member'

    # drop unneeded columns
    df = df[['Income', 'Over$75,001Income', 'RaceEthnicity', 'Are you of Hispanic or Latinx origin or descent?', 'SurveyLanguage', 
             'County', 'VHD', 'NurtureArea', 'PlanningDist15',
             'Pregnancy_Stage',
             'BirthDoula', 'PostpartumDoula', 'Lactation', 'MentalHealth', 'Social', 'Diapers', 'Formula', 'Food', 
             'Housing','Transportation', 'HealthInsurance', 'Financial', 'EducationCOVID19',
             'NoSupport']]

    # Rename columns for graphs
    df = df.rename(columns={
                            'Income' : 'Household Income',
                            'Over$75,001Income' : 'Household Income: Above or Below $75K',
                            'RaceEthnicity' : 'Race',
                            'Are you of Hispanic or Latinx origin or descent?' : 'Hispanic or Latinx',
                            'SurveyLanguage' : 'Survey Language',
                            'VHD' : 'Virginia Health District',
                            'NurtureArea' : 'Nurture Area',
                            'PlanningDist15' : 'Planning District 15',
                            'BirthDoula' : 'Birth Doula',
                            'PostpartumDoula' : 'Postpartum Doula',
                            'MentalHealth' : 'Mental Health',
                            'HealthInsurance' : 'Health Insurance',
                            'EducationCOVID19' : 'COVID 19 Education',
                            'NoSupport' : 'No Support',
                            'Pregnancy_Stage' : 'Pregnancy Stage'})

    # rename values for the charts
    df['Household Income: Above or Below $75K'] = df['Household Income: Above or Below $75K'].apply(lambda value: 'Over $75K' if value == 1 else ('Under $75K' if value == 0 else 'Undisclosed'))
    df['Household Income'] = df['Household Income'].apply(income_values)
    df['Nurture Area'] = df['Nurture Area'].apply(lambda value: 'In Area' if value == 1 else 'Out of Area')
    df['Planning District 15'] = df['Planning District 15'].apply(lambda value: 'In Area' if value == 1 else 'Out of Area')

    return df


def get_qual_preped(df,col):
    '''
    Takes in cleaned survay data as a dataframe and a column name
    returns a dataframe with only rows that have values in the column
    the rows will preped for analysis
    '''

    df = df.dropna(subset=[col])
    df[col] = df[col].apply(basic_clean).apply(lemmatize).apply(remove_stopwords)

    return df[[col, 'race', 'income', 'pregnancy_stage']]

def basic_clean(article):
    '''
    calls child functions preforms basic cleaning on a string
    converts string to lowercase, ASCII characters,
    and eliminates special characters
    '''

    # lowercases letters
    article = article.lower()

    # convert to ASCII characters
    article = get_ASCII(article)

    # remove non characters
    article = purge_non_characters(article)
    
    return article

def get_ASCII(article):
    '''
    normalizes a string into ASCII characters
    '''

    article = unicodedata.normalize('NFKD', article)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    
    return article

def purge_non_characters(article):
    '''
    removes special characters from a string
    '''
    
    article = re.sub(r"[^a-z\s]", ' ', article)
    
    return article

def remove_stopwords(article,extra_words=[],exclude_words=[]):
    '''
    removes stopwords from a string
    user may specify a list of words to add or remove from the list of stopwords
    '''

    # create stopword list using english
    stopword_list = stopwords.words('english')
    
    # remove words in extra_words from stopword list 
    [stopword_list.remove(f'{word}') for word in extra_words]
    
    # add words fin exclude_words to stopword list
    [stopword_list.append(f'{word}') for word in exclude_words]
    
    # slpit article into list of words
    words = article.split()

    # remove words in stopwords from  list of words
    filtered_words = [w for w in words if w not in stopword_list]
    
    # rejoin list of words into article
    article_without_stopwords = ' '.join(filtered_words)
    
    return article_without_stopwords

def lemmatize(article):
    '''
    lemmatizes words in a string
    '''

    # create lemmatize object
    wnl = nltk.stem.WordNetLemmatizer()
    
    # split article into list of words and stem each word
    lemmas = [wnl.lemmatize(word) for word in article.split()]

    #  join words in list into a string
    article_lemmatized = ' '.join(lemmas)
    
    return article_lemmatized