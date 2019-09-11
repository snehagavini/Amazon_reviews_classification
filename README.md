
1.	Save 50 reviews from Amazon. Try to use 5 star and 1-2 star reviews to get a comprehensive training set.
2.	Identify 10 keywords or key phrases indicative of buyer’s attitude. Use these words or phrases as features. 
3.	Reviews should be classified as positive (class 1) or negative (class 2).
4.	Train Naïve Bayes classifier using 40 reviews as training examples.
5.	Validate your classifier on the remaining 10 reviews. Report the accuracy of your classifier.
6.	Apply your classifier to 10 reviews not from your training set. Report how your results agree with the numbers of stars given by the authors of that reviews.

----------------------

Process :

This requires python3
Install python3, pip and go to command line from this folder.
Create a virutal environment as follows

```
python3 -m virtualenv venv
```

Activate the virtual environment as follows

```windows
venv\Scripts\activate
```

```mac or linux
source venv/bin/activate
```

Then install the requried libraries as follows

```
pip install -r requirements.txt
```
After the above steps we need to run the scrapper to collect the data, preprocess to prepare the data and Classifier to train and test the data

**Step 1**

Scraping of data from the url: In order to gather the reviews from the amazon page for the product, run the scraper.py file (homework1/src/scraper) as follows:

```
python scrapper.py B01L7PWBRG
```
Give the system arugment as B01L7PWBRG ( product code for 
bose ear phones) and run the scraper file.
The requried data is collected into data.json file (homework1/data/data.json)

**Step 2** 

Processing the data : In order to pre process the data for the classification run the preprocess.py file (homework1/src/preprocess) as follows:

```
python preprocess.py
```
During this stage, the data is processed like removing of stop words, removal of unwanted characters, stemming of data.
Then based on the word frequency the features are selected for classifying of data and data frame of reviews and the faetures is constructed.

The processed data is collected into data.csv file (homework1/data/data.json)

**Step 3**

Building the classifier: The Naive Baye's classifier is built and it is done by ruuning the classifier.py (homework1/src/classifier)

```
python classifier.py
```

The data is categorised into training data set and testing data set. The naive baye's classifier is trained by using 40 reviews.
The trained classifier is used to test the remaining 10 reviews from the tesing data set.The testing is done and the results of ratings in testing are collected. 

The results are compared to the actual ratings of the reviews and the accuracy is caluclated and it is 70%, i.e out 10 reviews 7 reviews are correctly classified.









        

