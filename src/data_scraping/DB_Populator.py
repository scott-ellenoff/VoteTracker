import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import json
import requests

# ----------------------------------------------------CONSTANTS---------------------------------------------------------
# DB Constants
DB_USER = 'VoteTrackrMaster'
DB_PASS = 'VotePass'
DB_HOST = 'votetrackr-db.cv1xcgegsskz.us-east-2.rds.amazonaws.com'
DB_PORT = '3306'
DB_NAME = 'deploy_db'

# Server Constants
SERVER_BASE = 'http://52.15.86.243:8080/api/v1/'
L_BASE = SERVER_BASE + 'legislators/'
B_BASE = SERVER_BASE + 'bills/'
V_BASE = SERVER_BASE + 'votes/'

# ---------------------------------------------------DB_LOGISTICS-------------------------------------------------------
# Opens the database connection using given arguments
def open_db_conn(user, password, host, port, db):
    try:
        conn = mysql.connector.connect(user=user, password=password, host=host, port=port, database=db)
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


# Prints out a table from the database with a given name
def print_table(table_name):
    db = pd.read_sql('select * from ' + table_name, con=conn)
    print(db.to_string())

# Obtain the db token
def get_db_token():
    r = requests.post(SERVER_BASE + 'login/', data={'username': 'admin', 'password': 'thisis220'})
    return json.loads(r.content)['key']


# ----------------------------------------------------SQL_FUNCTIONS-----------------------------------------------------
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

    add_query = 'INSERT INTO ' + table_name + '(' + ', '.join(list(args.keys())) + \
                ') VALUES(' + ','.join(['%s'] * len(args.values())) + ')'
    print('Query is: ', add_query)
    print(list(args.values()))
    cursor.execute(add_query, list(args.values()))


# Update a specific entry with key ID in a specified database
# Args is a dictionary of arguments
def update_table_entry(conn, cursor, table_name, id, args):
    if not valid_table_entry(conn, cursor, table_name, args):
        return False

    id_val = args[id]
    args.pop(id)

    query_string = ', '.join(["{} = '{}'".format(k, v) for k, v in args.items()])

    upd_query = 'UPDATE ' + table_name + \
                ' SET ' + query_string + \
                ' WHERE ' + id + " = '" + id_val + "'"

    # print('Query is: ', upd_query)
    # print (list(args.values()))
    cursor.execute(upd_query)


# Populate the legislators table from the clean_legislators.json
def populate_legislators_old(conn, cursor):
    # Populate legislators table
    new_legislators = json.loads(open('Dictionaries/Clean/clean_legislators.json').read())
    for leg in new_legislators:
        # print(leg)
        try:
            add_table_entry(conn, cursor, 'Legislators', leg)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print('Tried to input duplicate entry for key: ', leg['LID'])
                try:
                    update_table_entry(conn, cursor, 'Legislators', 'LID', leg)
                except:
                    print(err, ' occured while checking trying to update the row')
            else:
                print(err, ' occured while checking trying to add the entry')
            continue


# Populate the bills table from the clean_house_bills.json and clean senate_bills.json
def populate_bills_old(conn, cursor):
    # Populate bills table
    new_house_bills = json.loads(open('Dictionaries/Clean/clean_house_bills.json').read())
    new_senate_bills = json.loads(open('Dictionaries/Clean/clean_senate_bills.json').read())

    new_bills = new_house_bills + new_senate_bills
    # print(len(new_bills))
    for bill in new_bills:
        print(bill)
        try:
            add_table_entry(conn, cursor, 'Bills', bill)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print('Tried to input duplicate entry for key: ', bill['BID'])
                try:
                    update_table_entry(conn, cursor, 'Bills', 'BID', bill)
                except:
                    print(err, ' occured while checking trying to update the row')
            else:
                print(err, ' occured while checking trying to add the entry')
            continue


# ----------------------------------------------------DJANGO_FUNCTIONS--------------------------------------------------
# Populate the bills table from the clean_house_bills.json and clean senate_bills.json
def populate_legislators():
    # Populate legislators table
    new_legislators = json.loads(open('Dictionaries/Clean/clean_legislators.json').read())
    url = L_BASE
    for l in new_legislators[0:1]:
        print(l)
        data = {
            'LID': l['LID'],
            'fullname': l['FullName'],
            'district': l['District'],
            'state': l['State'],
            'senator': l['isSenator'],
            'affiliation': l['Affiliation'],
            'dwnominate': l['DWNominate'],
            'url': l['URL']
        }
        # Form a request to a db
        auth_token = get_db_token()
        headers = {'Authorization': 'Token ' + auth_token}
        r = requests.post(url, data=data, headers=headers)
        print(r.status_code)
        print(r.text)


# Populate the bills table from the clean_house_bills.json and clean senate_bills.json
def populate_bills():
    # Populate bills table
    new_house_bills = json.loads(open('Dictionaries/Clean/clean_house_bills.json').read())
    new_senate_bills = json.loads(open('Dictionaries/Clean/clean_senate_bills.json').read())

    new_bills = new_house_bills + new_senate_bills
    url = B_BASE

    for bill in new_bills[0:1]:
        print(bill)
        data = {
            'BID': bill['BID'],
            'name': bill['Name'],
            'description': bill['Description'],
            'date_introduced': bill['DateIntroduced'],
            'status': bill['Status'],
            'voted_on': bill['VotedOn'],
            'congress_n': bill['CongressN'],
            'chamber': bill['Chamber'],
            'date_voted': bill['DateVoted'],
            'url': bill['URL']
        }
        # Form a request to a db
        auth_token = get_db_token()
        headers = {'Authorization': 'Token ' + auth_token}
        r = requests.post(url, data=data, headers=headers)
        print(r.status_code)
        print(r.text)


# Populate the votes table with the votes of legislators for the bills in the db
def populate_votes():
    # Populate legislators votes
    votes = json.loads(open('Dictionaries/Clean/collected_votes.json').read())
    counter = 0
    for vote in votes:
        for l in votes[vote]:
            url = V_BASE
            if votes[vote][l] == 'Yes':
                res = 'Y'
            elif votes[vote][l] == 'No':
                res = 'N'
            else:
                res = 'A'

            data = {
                'bill': B_BASE + vote + '/',
                'legislator': L_BASE + l + '/',
                'vote': res
            }

            # Form a request to a db
            auth_token = get_db_token()
            # print(auth_token)
            headers = {'Authorization': 'Token ' + auth_token}
            r = requests.post(url, data=data, headers=headers)
            counter += 1
            print(counter)
            # print(r.status_code)
            # print(r.text)

if __name__ == "__main__":
    conn, cursor = open_db_conn(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, db=DB_NAME)
    # print(get_db_token())
    # Get a list of columns we have in our table and their types
    # Drop all tables in db
    # cursor.execute('SHOW TABLES')
    # all_tables = [a[0] for a in cursor.fetchall()]
    # print(all_tables)
    # cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
    # for table in all_tables:
    #     cursor.execute('DROP TABLE ' + table)
    # cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

    # Clean one specified table
    # cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
    # cursor.execute('TRUNCATE TABLE Bills')
    # cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

    # Populate the Bill and Legislators tables using the SQL
    # populate_legislators_old(conn, cursor)
    # print_table('Legislators')
    #
    # populate_bills_old(conn, cursor)
    # print_table('Bills')


    # Populate the Bill, Legislator, and Votes tabels using requests
    # populate_legislators()
    # populate_bills()
    # populate_votes()

    close_db_conn(conn, cursor)

    exit()
