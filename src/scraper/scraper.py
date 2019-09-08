from lxml import html
from json import dump, loads
from requests import get
import json
from re import sub
from time import sleep
import sys
def get_html(url):
    """
        Returns the response for a given url
    """
    headers = {'User-Agent': 'Defined'}
    response = get(url, headers = headers, verify = False, timeout = 30)
    if response.status_code == 404:
        print("Page not found error")
        exit(-1)
    if response.status_code != 200:
        print("Error = ",response.status_code)
        exit(-1)
    
    # Remove all the null bytes from the response
    cleaned_response = response.text.replace('\x00','')

    parser = html.fromstring(cleaned_response)
    return parser
    
def get_a_url(parser_object, XPATH):
    """
        This function gets the url from the given XPATH
    """
    req_url = parser_object.xpath(XPATH)[0].get("href")
    return 'http://www.amazon.com'+req_url

def get_reviews(parser_object, total_reviews):
    
    XPATH_REVIEW_SECTION = '//div[@data-hook="review"]'
    reviews = parser_object.xpath(XPATH_REVIEW_SECTION)
    reviews_list = []

    for review in reviews:
        XPATH_RATING = './/i[@data-hook="review-star-rating"]//text()'
        XPATH_REVIEW = './/span[@data-hook="review-body"]/span/text()'

        rating = review.xpath(XPATH_RATING)
        rating = float(''.join(rating).replace('out of 5 stars', ''))

        if rating == 1 or rating == 2 or rating == 5:
            review_text = review.xpath(XPATH_REVIEW)
            review_text = ' '.join(review_text)
            review_dict = {
                'rating' : rating,
                'review' : review_text
            }
            reviews_list.append(review_dict)
            total_reviews += 1
    
    return reviews_list, total_reviews

def main():
    if len(sys.argv) !=2:
        print('Usage: python scrapper.py <product unique code>\nEx:B01L7PWBRG')
        exit(-1)

    # XPATHS for the required tags
    XPATH_ALL_REVIEWS = '//*[@id="reviews-medley-footer"]/div[2]/a'
    XPATH_NEXT_PAGE = '//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a'

        # Getting all reviews url
    amazon_url = "http://www.amazon.com/dp/"+sys.argv[1]
    page = get_html(amazon_url)
    extracted_data = []
    total_reviews = 0
    count = 0

    while total_reviews != 50:
        if count == 0:
            XPATH = XPATH_ALL_REVIEWS
        else:
            XPATH = XPATH_NEXT_PAGE
        
        reviews_url = get_a_url(page, XPATH)
        sleep(5)
        page = get_html(reviews_url)
        reviews, total_reviews = get_reviews(page, total_reviews)
        extracted_data = extracted_data + reviews
        count += 1
    
    f = open('../../data/data.json', 'w')
    dump(extracted_data, f, indent=4)
    f.close()

if __name__ == '__main__':
    main()