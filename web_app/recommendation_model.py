from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession

# Load  the pre-trained ALS model
def load_als_model(model_path):
    return ALS Model.load(model_path)


# Use the ALS model to generate recommendations for a user
def get_recommendations(model, spark, user_id, num_rec=10):
    user_df = spark.createDataFrame([(user_id,)], ['userId'])
    recommendations = model.recommendfor