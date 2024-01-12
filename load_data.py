# import pandas as pd
# from sqlalchemy import create_engine
# from web_app import db, ssh_tunnel
# from config import *
#
#
# # This function handles the loading of movie data into the database.
# def load_movies_data():
#     # Read the CSV
#     movies_df = pd.read_csv('csv file')
#
#     # Add a 'year' column if not present in CSV
#     if 'year' not in movies_df.columns:
#         movies_df['year'] = None
#
#     # Connect to MYSQL database
#     # pymysql: Specifies the MySQL driver to be used for the connection.
#     # pymysql is a Python library that provides a MySQL driver for Python.
#     engine = create_engine(
#         f"mysql+pymysql://{db_username}:{db_password}@localhost:{ssh_tunnel.local_bind_port}/{db_name}")
#
#     # Insert data into the 'movies' table
#     # to_sql method to insert the data from the Pandas DataFrame into the 'movies' table in the MySQL database.
#     movies_df.to_sql('movies', con=engine, if_exists='replace', index=False)
#
#
# # # function is executed only when the script is run directly, not when it is imported as a module.
# # if __name__ == "__main__":
# #     load_movies_data()
