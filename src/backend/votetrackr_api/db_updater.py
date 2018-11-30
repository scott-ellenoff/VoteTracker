import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import json
import requests
import shutil
from congress import Congress

# ----------------------------------------------------CONSTANTS---------------------------------------------------------
# DB Constants
DB_USER = 'VoteTrackrMaster'
DB_PASS = 'VotePass'
DB_HOST = 'votetrackr-db.cv1xcgegsskz.us-east-2.rds.amazonaws.com'
DB_PORT = '3306'
DB_NAME = 'test_db'

# Server Constants
SERVER_BASE = 'http://52.15.86.243:8080/api/v1/'
L_BASE = SERVER_BASE + 'legislators/'
B_BASE = SERVER_BASE + 'bills/'
V_BASE = SERVER_BASE + 'votes/'

# ProPublica API Constants
PROPUBLICA_API_KEY = 'AfFAT83Y5LHoCEvkGgwjbjrtVrZgVSgp18YXiF0R'

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
def print_table(conn, table_name):
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
    # print(table_cols)

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
    # print('Query is: ', add_query)
    # print(list(args.values()))
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

# ---------------------------------------------------DB_UPDATER_CLASS---------------------------------------------------
class db_updater():

    # Checks if new bills that fit our criteria came out
    # Current criteria: More than 50 cosponsors in House, 8 in Senate
    def update_bills(self):
        try:
            bills_to_add = []
            for chamber in ['house', 'senate']:
                congress = Congress(PROPUBLICA_API_KEY)
                new_bills = congress.bills.recent(chamber=chamber)
                # print(new_bills)

                for cur_bill in new_bills['bills']:
                    if chamber == 'house' and (cur_bill['cosponsors'] < 50):
                        continue

                    if chamber == 'senate' and (cur_bill['cosponsors'] < 8):
                        continue

                    # All the new bills here have not been voted on, otherwise it should already be in our db
                    if 'res' in cur_bill['bill_type'] or cur_bill['last_vote']:
                        continue

                    print(cur_bill)
                    cur_dict = {'BID': cur_bill['bill_id'], 'Description': cur_bill['title'],
                                'Name': cur_bill['short_title'],
                                'DateIntroduced': cur_bill['introduced_date'], 'Status': cur_bill['latest_major_action'],
                                'CongressN': cur_bill['bill_id'][-3:], 'URL': cur_bill['govtrack_url'],
                                'Chamber': new_bills['chamber'], 'VotedOn': 0, 'DateVoted': 0}

                    # cur_dict['RollCallID'] = 0

                    bills_to_add.append(cur_dict)

            # Open connection to the database
            conn, cursor = open_db_conn(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, db=DB_NAME)

            # Add bills into db
            for bill in bills_to_add:
                # Add the bid to the list of unvoted for all users


                try:
                    add_table_entry(conn, cursor, 'Bills', bill)
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        print('Tried to input duplicate entry for key: ', bill['BID'])
                    else:
                        print(err, ' occured while checking trying to add the entry')
                    continue

            # Close db connection
            close_db_conn(conn, cursor)

            # Delete the un-needed cache generated automatically by the Congress library
            shutil.rmtree('.cache')

            return True
        except:
            print('An error occurred while trying to update the Bills db. Please examine the printed log.')
            return False

    # Checks if new votes came in on some of the bills we have in our db
    def update_votes(self):
        try:
            # Open connection to the database
            conn, cursor = open_db_conn(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, db=DB_NAME)

            # Get the BIDs for the bills in our database that have not been voted on yet
            cursor.execute('select * from Bills where VotedOn=0')
            unvoted_bids = [b[0] for b in cursor.fetchall()]

            # Check if any of the recent votes were for the bills in our db
            votes_to_add = {}
            for chamber in ['senate', 'house']:
                # Year and month in the method below default to the current date
                congress = Congress(PROPUBLICA_API_KEY)
                votes = congress.votes.by_month(chamber=chamber)
                for vote in votes['votes']:
                    if not vote['bill'] or vote['bill']['bill_id'] not in unvoted_bids:
                        continue
                    else:
                        cur_vote = congress.votes.get(vote['chamber'], vote['roll_call'], vote['session'])
                        # print(cur_vote)
                        cur_vote_bid = cur_vote['votes']['vote']['bill']['bill_id']
                        cur_vote_breakdown = cur_vote['votes']['vote']['positions']

                        votes_to_add[cur_vote_bid] = {}
                        for l in cur_vote_breakdown:
                            votes_to_add[cur_vote_bid][l['member_id']] = l['vote_position']

                        # Mark bill as voted on
                        update_table_entry(conn, cursor, 'Bills', 'BID', {'BID': vote['bill']['bill_id'], 'VotedOn': 1})

            print(votes_to_add)
            # Add votes into the db
            for vote in votes_to_add:
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
                    headers = {'Authorization': 'Token '+ auth_token}
                    r = requests.post(url, data=data, headers=headers)
                    print(r.status_code)
                    print(r.text)

            # Close db connection
            close_db_conn(conn, cursor)

            # Delete the un-needed cache generated automatically by the Congress library
            shutil.rmtree('.cache')

            return True
        except:
            print('An error occurred while trying to update the Votes db. Please examine the printed log.')
            return False

    def push_notifications(self):
        return True


if __name__ == "__main__":
    new_updater = db_updater()
    new_updater.update_bills()
    new_updater.update_votes()
    exit()
