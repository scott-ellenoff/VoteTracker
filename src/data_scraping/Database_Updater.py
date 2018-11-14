import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import json
import os

# Constants
DB_USER = 'VoteTrackrMaster'
DB_PASS = 'VotePass'
DB_HOST = 'votetrackr-db.cv1xcgegsskz.us-east-2.rds.amazonaws.com'
DB_PORT = '3306'
DB_NAME = 'test_db'

DICT_DIR = 'Dictionaries'

# Opens the database connection using given arguments
def open_db_conn(user, password, host, port, db):
    try:
        conn = mysql.connector.connect(user=user, password=password, host=host, port=port, database=db)
        # conn = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, database=DB_NAME)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return False
    else:
        cursor = conn.cursor(buffered=True)
        return conn, cursor


# Closes the database connection
def close_db_conn(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


# Check if table exists in our db
def table_exists(conn, cursor, table_name):
    try:
        cursor.execute('SELECT 1 FROM ' + table_name + ' LIMIT 1')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_SUCH_TABLE:
            print('Table', table_name, 'does not exist in db', conn.database)
            return False
        else:
            print(err, ' occured while checking if table exists')
            return False
    else:
        return True


# Validates that args have all the necessary fields to be entered into the specified table
# args here is a dictionary of entries
def valid_table_entry(conn, cursor, table_name, args):
    # Check if table exists in our db in the first place
    if not table_exists(conn, cursor, table_name):
        return False

    # Get a list of columns we have in our table and their types
    cursor.execute('SHOW COLUMNS FROM ' + table_name)
    # print(cursor.fetchall())
    table_cols = {i[0]: i[1] for i in cursor.fetchall()}
    print(table_cols)

    # Check if arguments we are passing have all those fields
    if not set(args.keys()) == set(table_cols.keys()):
        # print(set(args.keys()))
        # print(set(table_cols.keys()))
        print('Tried adding entry that did not have some of the required table columns or had extra keys')
        return False

    # # Check if types of those fields are the same
    # for col in table_cols:
    #     if (table_cols[col])
    return True


# Adds an entry to a specific table in the database
# Args is a dictionary of arguments
def add_table_entry(conn, cursor, table_name, args):
    if not valid_table_entry(conn, cursor, table_name, args):
        return False

    # add_query = 'INSERT INTO ' + table_name + '(' + ', '.join(list(args.keys())) + ') VALUES(%s,%s,%s,%s,%s,%s)'
    add_query = 'INSERT INTO ' + table_name + '(' + ', '.join(list(args.keys())) + \
                ') VALUES(' + ','.join(['%s'] * len(args.values())) + ')'
    print('Query is: ', add_query)
    # print (list(args.values()))
    cursor.execute(add_query, list(args.values()))


# Populate the legislators table from the clean_legislators.json
def populate_legislators(conn, cursor):
    # Populate legislators table
    new_legislators = json.loads(open(os.path.join(DICT_DIR, 'Clean/clean_legislators.json')).read())
    for leg in new_legislators:
        print(leg)
        try:
            add_table_entry(conn, cursor, 'Legislators', leg)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print('Tried to input duplicate entry for key: ', leg['LID'])
            else:
                print(err, ' occured while checking trying to add the entry')
            continue


# Populate the bills table from the clean_house_bills.json and clean senate_bills.json
def populate_bills(conn, cursor):
    # Populate legislators table
    new_house_bills = json.loads(open(os.path.join(DICT_DIR, 'Clean/clean_house_bills.json')).read())
    new_senate_bills = json.loads(open(os.path.join(DICT_DIR, 'Clean/clean_senate_bills.json')).read())

    new_bills = new_house_bills + new_senate_bills
    for bill in new_bills:
        print(bill)
        try:
            add_table_entry(conn, cursor, 'Bills', bill)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print('Tried to input duplicate entry for key: ', bill['BID'])
            else:
                print(err, ' occured while checking trying to add the entry')
            continue


# Prints out a table from the database with a given name
def print_table(table_name):
    db = pd.read_sql('select * from ' + table_name, con=conn)
    print(db)


# scrape()



if __name__ == "__main__":
    conn, cursor = open_db_conn(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, db=DB_NAME)

    populate_legislators(conn, cursor)
    print_table('Legislators')

    populate_bills(conn, cursor)
    print_table('Bills')


    # votes = pd.read_sql('select * from Votes;', con=conn)
    # print(votes)

    close_db_conn(conn, cursor)

    exit()
