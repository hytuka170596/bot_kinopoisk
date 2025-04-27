from peewee import SqliteDatabase
import os

database_dir = os.path.join(os.getcwd(), "database")

MOVIE_DB = SqliteDatabase(os.path.join(database_dir, "movie_db.db"))
