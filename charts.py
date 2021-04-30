
import matplotlib.pyplot as plt

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

    removed_values_list = ['undisclosed']
  
    # get list of values that have 30 or more occurances in the column and set X axis to those values
    for column in column_list:
        
        if column == 'Household Income':

            value_list = ['40K and Under', '40K+ to 75K', '75K+ to 100K', '100K+ to 125K', 'Over 125K']

        elif column == 'Household Income: Above or Below $75K':

            value_list = ['Under $75K','Over $75K']

        elif column == 'Pregnancy Stage':

            value_list = ['2nd Trimester','3rd Trimester', '1 Year After Birth', '2 Years After Birth']

        else:
        
            value_list = [value for value in set(df[f'{column}']) if df[f'{column}'].value_counts()[value] >= 25 and value not in removed_values_list]

        X = [str(value) for value in value_list]

        # get list of y values and plot chart
        for need in need_list:

            # y = rows where column equals value and need equals one divided by rows where column equals value 
            y = [round((df[(df[f'{column}'] == value) & (df[f'{need}'] == 1)].shape[0] / df[df[f'{column}'] == value].shape[0])*100,0) for value in value_list]

            plt.figure(figsize=(11, 6))
            plt.bar(X, y, align='center', alpha=0.5)
            plt.ylim([0,100])

            plt.ylabel('% of Respondents in Each Catagory')
            plt.title(f'Percent of Respondents Identifying {need} Among Most Helpful Supports by {column}')

            plt.show()

            output = [str(round(num)) + '%' for num in y]        
            print(output)


def get_hierarchy(df):

    column_list = ['Household Income', 'Household Income: Above or Below $75K', 'Race',
                   'Hispanic or Latinx', 'Survey Language', 'County', 'Virginia Health District', 
                   'Nurture Area', 'Planning District 15', 'Pregnancy Stage']

    need_list = ['No Support',   'Diapers', 'Formula','Food', 'Housing', 'Transportation', 'COVID 19 Education','Health Insurance',
                 'Financial','Postpartum Doula', 'Birth Doula', 'Lactation', 'Mental Health', 'Social']

    removed_values_list = ['undisclosed', False]

    for column in column_list:

        value_list = [value for value in set(df[f'{column}']) if df[f'{column}'].value_counts()[value] >= 25 and value not in removed_values_list]

        X = need_list 

        for value in value_list:

            # respondants identifiying as value and chose need devided by respondants identifiying as value
            y = [round((df[(df[column] == value) & (df[need] == 1)].shape[0] / df[df[column] == value].shape[0])*100,0) for need in need_list]

            plt.barh(X,y)

            plt.ylabel('Needs')
            plt.xlabel('% of Respondents Identifying Need as Among Most Helpful')
            plt.title(f'Hierarchy of Supports {column}: {value}')
            plt.xlim([0,100])
            plt.show()

            output = [str(round(num)) + '%' for num in y]
            output.reverse()

            print(output)