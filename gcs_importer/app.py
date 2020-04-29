from psycopg2 import connect
from importer import download_and_import_google_image_index

conn = connect(**{
    "dbname": "gcs",
    "user": "docker",
    "password": "docker",
    "host": "127.0.0.1",
    "port": 25432
})

download_and_import_google_image_index(conn)
