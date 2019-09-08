# Importing the requried libraries
import re
import json
import sys
from nltk.stem import PorterStemmer

# Input : reading the data from data.

"""
    Process: 
        - remove the stop words
        -group all the strings
        -count the word frequency
        -select the 10 fetaures basing on the word count
        - caluclate each feature count for all 50 reviews
        -build a table or data frame 
        -get the output
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
    porter = PorterStemmer()
    review = [porter.stem(i) for i in review]
    return rem_stopwords(review)   


def grp_reviews(processed_review):
    grouped_review = []
    for k in processed_review:
        grouped_review.extend(k)
    return grouped_review

    

def word_count(grouped_reviews):
    return [{x : grouped_reviews.count(x)} for x in set(grouped_reviews)]      


  

def select_feature():
    """
    Input: 
    process : 
    Out put:
    """
    pass
    
def revw_ftr_count():
    """
    Input: 
    process : 
    Out put:
    """
    pass
   
def data_frame():
    """
    Input: 
    process : 
    Out put:
    """
    pass


def main():
    review_data_path = '../../data/data.json'
    ratings,reviews = get_ratings_reviews(review_data_path)
    processed_review = []
    for a in reviews:
        processed_review.append(process_review(a))
    grouped_reviews = grp_reviews(processed_review)
    print(word_count(grouped_reviews))

if __name__ == "__main__":
    main()
