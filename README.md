# PrismDeck
This application is a movie recommendation app

## Authors
**Michael Riley**
**Josette Nelson**
**Imir Ransom**
**Corinne Kogut**

## Description

This is our group project from Zip Code Wilmington. PrismDeck is an application designed to recommend movies to users based on their preferences.
Users can input their preferences such as movie genre (e.g., comedies), ratings between 3-5 stars, and specific release time frames. The application employs an algorithm or rules along with a trained model to match and rank movies according to user preferences. The model is trained on giving recommendations to the users for ratings using User_Based Callobrative Filtering.

## Features

- **Favorites**:
  - Users will have a favorites list upon creation to save their favorite moviees that they enjoy. The application will give
    recommendations based on that as well

- **Match & Rank**
  - The application will pick out movies based off a algorithm or rules and a trained model
    
- **Movie Link**
  - When useres are recommended the list of movies, when the user clicks on the movie, iut will send them to the movie's website so that they may get further information on their recommneded movie

## Dependencies
- **Tools**:
  The technologies that we will be using for this project are:
  - Python
  - Pandas
  - Jupyter Notebook
  - Apache Spark
  - Flask
  - HTML
  - CSS
  - CSV Files
  - MySQL
  - SQLAlchemy

### Installing Requirements
Create a virtual environment
```
python3 -m venv /path/to/new/virtual/environment/name_of_environment
```
Then activate the virtual environment
```
source name_of_environment/bin/activate
```
After that, install the requirements to run the app
```
pip install -r requirements.txt
```
Now, you can run the app
```
export FLASK_APP=main
```
```
flask run
```


## Dataset:
That the data set we will be using is from a folder of csv files gathered from Movie Lens - https://grouplens.org/datasets/movielens/latest/ . We will be using the csv files to help with the rules algorithm as well as using the data to help train our model
  
## Rating Stars CSS/HTML
Modified to our needs from open-source code, permission granted under MIT License.  See NOTICE.md

## Model Training
With this being a recommendation system for users and such a large dataset, we leveraged Python with Apache Spark to use the `Alternating Least Sqaured (ALS)` algorithm. The data was split for 80% trainig of the model and 20% for testing the model. We then tested it's accuracy using the metric `Root Mean Squared Error (RMSE)`. This metric as of now has given us back `0.8009857963477534` as our results with the metric. The model is also loaded into our Flask application in one of our various routes.

