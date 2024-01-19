# PrismDeck

![imir](https://github.com/NomNomNavigator/PrismDeck/assets/122006390/a9808c0b-cb1b-4a66-b4f8-f45126d104e2)






This application will be used to recommend movies the users based on their input. For instance, if the 
user likes comedies, ratings that are between 3-5 stars and a certain time that movies were released, they will get recommnedations based on that very input.

- **Favorites**:
  - Users will have a favorites list upon creation to save their favorite moveies that they enjoy. The application will give
    recommendations based on that as well

- **Match & Rank**
  - The application will pick out movies based off a algorithm or rules and a trained model
    
- **Movie Link**
  - When useres are recommended the list of movies, when the user clicks on the movie, iut will send them to the movie's website so that they may get further information on their recommneded movie
 
- **Tools**:
  - the tools that we will be using for this project are Python, Pandas, Jupyter Notebook, Apache Spark, Flask, HTML, CSS, CSVs, Kubernetes, MySQL, SQLAlchemy

## Dataset:
That the data set we will be using is from a folder of csv files gathered from Movie Lens - https://grouplens.org/datasets/movielens/latest/ . We will be using the csv files to help with the rules algorithm as well as using the data to help train our model
  

## Rating Stars CSS/HTML
Modified to our needs from open-source code, permission granted under MIT License.  See NOTICE.md

## Model Training
With this being a recommendation system for users and such a large dataset, we leveraged Python with Apache Spark to use the `Alternating Least Sqaured (ALS)` algorithm. The data was split for 80% trainig of the model and 20% for testing the model. We then tested it's accuracy using the metric `Root Mean Squared Error (RMSE)`. This metric as of now has given us back `0.8009857963477534` as our results with the metric. The model is also loaded into our Flask application in one of our various routes.

