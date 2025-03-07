import pandas as pd
import random
def training_testing_split(df):    
    # Creating the empty data frames
    train_df = pd.DataFrame()
    test_df = pd.DataFrame()

    # Positive reviews
    pstv_rvw = df['rating'].unique()[1]        # pstv_rvw='positive'
    p = df['rating'] == pstv_rvw               # true,true,false
    pdf = df[p]
    positive_index = list(pdf.index)        # INdex of the positive reviews
    

    # Negative reviews
    ngtv_rvw = df['rating'].unique()[0]
    n = df['rating'] == ngtv_rvw
    ndf = df[n]
    negative_index = list(ndf.index)        # INdex of the negative reviews - there is a mistake
    

    # Shuffling the lists
    random.Random(30).shuffle(positive_index)
    random.Random(30).shuffle(negative_index)
    
    # Taking the first 5 elements from shuffled lists 
    test_positive = positive_index[:5]
    test_negative = negative_index[:5]

    # Taking the other elements from the shuffled lists
    train_positive = positive_index[5:]
    train_negative = negative_index[5:]

    # Appending to the approprite data frames
    train_df = train_df.append(df.loc[train_positive,:])
    train_df = train_df.append(df.loc[train_negative,:])
    test_df = test_df.append(df.loc[test_positive,:])
    test_df = test_df.append(df.loc[test_negative,:])   
    
    return train_df, test_df

def train(train_df):

    # Calculating the prior
    prior = dict(train_df['rating'].value_counts()/len(train_df))
    
    # Splitting into positive and negative 
    positive_df = train_df[train_df['rating'] == 'positive']
    negative_df = train_df[train_df['rating'] == 'negative']

    positive_likelihood = []
    negative_likelihood = []

    for i in train_df.columns[:-1]:
        positive_likelihood.append(dict(positive_df[i].value_counts()/len(positive_df)))
        negative_likelihood.append(dict(negative_df[i].value_counts()/len(negative_df)))
        
    return positive_likelihood, negative_likelihood, prior

def test(test_df, positive_likelihood, negative_likelihood, prior):
    no_ratings_df = test_df.drop(columns = ['rating'], inplace=False)
    predictions = []
    for index, row in no_ratings_df.iterrows():  
        positive_posterior = prior['positive']  
        negative_posterior = prior['negative']

        for i in range(10):
            if row[i] in positive_likelihood[i]:
                positive_posterior *= positive_likelihood[i][row[i]]    # row[i] = value of the column, ,chepu
            else:
                positive_posterior *= 0
            
            if row[i] in negative_likelihood[i]:
                negative_posterior *= negative_likelihood[i][row[i]]
            else:
                negative_posterior *= 0
            
        
        if positive_posterior >= negative_posterior:
            predictions.append('positive')
        else:
            predictions.append('negative')

    return predictions

def main():
    # Reading the file
    df = pd.read_csv('../../data/data.csv')
    train_df, test_df = training_testing_split(df)

    # Dropping the unnamed: 0 column
    train_df = train_df.loc[:, ~train_df.columns.str.contains('^Unnamed')]
    test_df = test_df.loc[:, ~test_df.columns.str.contains('^Unnamed')]
    
    positive_likelihood, negative_likelihood, prior = train(train_df)
    predictions = test(test_df, positive_likelihood, negative_likelihood, prior)
    test_df['predictions'] = predictions
    print(test_df)
    #print(test_df[['rating','predictions']])

    accuracy = sum(test_df['rating'] == test_df['predictions'])*100/len(test_df)
    print('Accuracy =', accuracy)
    mispredicted_rnum = test_df[test_df['predictions'] != test_df['rating']].index
    print('The mispredicted rows are ' ,mispredicted_rnum)

if __name__ == '__main__':
    main()