# Importing the requried libraries
import re
import json
import sys
import pandas
import numpy
from nltk.stem import PorterStemmer
from collections import Counter

# Input : reading the data from data.

"""
    Process: 
        - remove the stop words
        -group all the strings
        -count the word frequency
        -select the 10 fetaures basing on the word count
       
"""
# Output : writing the data to csv file

def get_ratings_reviews(file_name):
    
    ratings = []
    reviews = []

    with open(file_name,'r') as json_file:
        reviews_list = json.load(json_file)
        for i in reviews_list:
            reviews.append(i['review'])
            ratings.append(i['rating'])              
    return ratings, reviews

def rem_stopwords(review):

    stop_words = []
    revised_review = []
    with open('../../data/stopwords.txt','r') as x:
        for i in x:
            stop_words.append(i.split('\n')[0])
    
    # Add the product related stopwords
    other_stop_words = ["bose","headphon","ear","use","get","thi","wa","becaus","realli","make","come","devic","phone","ha","ve","ani",
                        "purchas","go","month","year","rubber","thing","also","would","even","m","one","soundsport","tri","still","last","say"]
    stop_words.extend(other_stop_words)
    
    for j in review:
        if j not in stop_words:
            revised_review.append(j)
    return revised_review

def process_review(review):
    regex = re.compile('[^a-zA-Z]')
    review = regex.sub(' ',review)
    review = review.lower()    
    review = review.split()
    # Do stemming here
    no_stop_words = rem_stopwords(review)
    porter = PorterStemmer()
    stemmed_words = [porter.stem(i) for i in no_stop_words] 
    return rem_stopwords(stemmed_words)


def grp_reviews(processed_review):
    grouped_review = []
    for k in processed_review:
        grouped_review.extend(k)
    return grouped_review

    

def word_count(grouped_reviews):
    # return [{x : grouped_reviews.count(x)} for x in set(grouped_reviews)]      
    return Counter(grouped_reviews)

def feature_count(feature_list, processed_review):
    count_vectors = []
    for i in processed_review:
        count_vectors.append([i.count(j) for j in feature_list])    
    return count_vectors   

def assign_categories(dat_frame, condition, cond_vals, col_name, value):

    if condition == 'lt':
        row_indexer = dat_frame[col_name] <= cond_vals[0]
    elif condition == 'bw':
        row_indexer = dat_frame[col_name] > cond_vals[0] and dat_frame[col_name] <= cond_vals[1]

    dat_frame.loc[row_indexer, col_name] = value

def assign_categories_column(dat_frame, bins, names, col_name):
    d = dict(enumerate(names,1))
    dat_frame[col_name] = numpy.vectorize(d.get)(numpy.digitize(dat_frame[col_name], bins))

def assign_Categories_helper(dat_frame):

    # Sound
    # [0-1, 1-2, 2-3, 3-11]
    assign_categories_column(dat_frame, [0,1,2,3], ['low','good','better','best'], 'sound')

    # Quality
    # [0-1, 1-2, 2-5]
    assign_categories_column(dat_frame, [0,1,2], ['poor','better','best'], 'qualiti')

    # good
    # [0, 0-1]
    assign_categories_column(dat_frame, [0,0.5,1], ['bad','good','better'],'good')

    # love
    # [0-1, 1-2]
    assign_categories_column(dat_frame, [0,1], ['bad','good'], 'love')

    
    # comfort
    # [0-1, 1-4]
    assign_categories_column(dat_frame, [0,1],['less', 'more'], 'comfort')
    
    # issu
    # [0-1, 1-3]
    assign_categories_column(dat_frame, [0,1],['less', 'more'], 'issu')
    
    # # never
    # [0, 0-2, 2-3]
    assign_categories_column(dat_frame,[0,0.5,2],['good', 'better', 'best'], 'never')
    
    # # replac
    # [0, 0-4]
    assign_categories_column(dat_frame,[0,0.5,2],['good', 'better', 'best'], 'replac')
 
    # # fall
    # [0, 0-4]
    assign_categories_column(dat_frame,[0,0.5,2],['good', 'better', 'best'], 'fall')

    # # dissapoint
    # [0, 0-2]
    assign_categories_column(dat_frame, [0,0.5],['nice','poor'], 'disappoint')

    # # rating
    # [1-2, 5]
    assign_categories_column(dat_frame, [1,2],['negative','positive'], 'rating')
  
def main():
    review_data_path = '../../data/data.json'
    ratings,reviews = get_ratings_reviews(review_data_path)
    processed_review = []
    for a in reviews:
        processed_review.append(process_review(a))
    grouped_reviews = grp_reviews(processed_review)
    bag_of_words = word_count(grouped_reviews)
    
    # bag_of_words.most_common(100) based on top hundred words 10 features are selected
    # sound, qualiti,good,love,comfort,issu,never,replac,fall,disappoint
    feature_list=['sound','qualiti','good','love','comfort','issu','never','replac','fall','disappoint']      
    count_vectors = feature_count(feature_list, processed_review)   
    
    # Creating the dataframe
    dat_frame = pandas.DataFrame(count_vectors,columns=feature_list)
    dat_frame['rating'] = ratings
    print(dat_frame)
    assign_Categories_helper(dat_frame)
    print(dat_frame)
    dat_frame.to_csv("../../data/data.csv")

if __name__ == "__main__":
    main()