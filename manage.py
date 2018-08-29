import os
import psycopg2
from app import create_app
from app.database import Database

app = create_app('PRODUCTION')
db = Database('postgres://sxeryejnkxvdyl:fe0c442231427f6b1874f34a2608f09568dcbf48d4a65c22af4e5697a769761f@ec2-54-235-242-63.compute-1.amazonaws.com:5432/df6pburvodvkqn')

if __name__ == '__main__':
    db.create_tables()
    port = int(os.environ.get('PORT', 8000))
    app.run(port=port)
