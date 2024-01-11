import pandas as pd
from sqlalchemy import
from web_app import db


def load_movies_data():
    # Read the CSV
    movies_df =