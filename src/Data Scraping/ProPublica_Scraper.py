# Scraper for the VoteTrackr Project that uses ProPublica API
from congress import Congress
import json

# Constants
PROPUBLICA_API_KEY = 'AfFAT83Y5LHoCEvkGgwjbjrtVrZgVSgp18YXiF0R'
congress = Congress(PROPUBLICA_API_KEY)


# Scrapes all relevant bills from the ProPublica API for the 155th congress
def scrape_bills():
    senate_bills = []
    for i in range(0, 3500):
        try:
            cur_bill = congress.bills.get('s'+str(i))
        except:
            continue

        if (cur_bill['cosponsors'] < 10) or ('res' in cur_bill['bill_type']) or not cur_bill['last_vote']:
            continue
        print(cur_bill)
        cur_dict = {'BID': cur_bill['bill_slug'], 'Description': cur_bill['title'],
                    'DateIntroduced': cur_bill['introduced_date'], 'Status': cur_bill['latest_major_action'],
                     'CongressN': cur_bill['bill_id'][-3:], 'URL': cur_bill['govtrack_url']}
        if not cur_bill['last_vote']:
            cur_dict['VotedOn'] = 0
            cur_dict['DateVoted'] = 0
            cur_dict['RollCallID'] = 0
        else:
            cur_dict['VotedOn'] = 1
            cur_dict['DateVoted'] = cur_bill['last_vote']
            cur_dict['RollCallID'] = 0

        senate_bills.append(cur_dict)
    print(len(senate_bills))

    with open('Data Scraping/Dictionaries/Clean/clean_senate_bills.json', 'w') as outfile:
        json.dump(senate_bills, outfile, ensure_ascii=True)
    outfile.close()

    # Scraping recent house bills
    house_bills = []
    for i in range(0, 7200):
        try:
            cur_bill = congress.bills.get('hr'+str(i))
        except:
            continue

        if (cur_bill['cosponsors'] < 8) or ('res' in cur_bill['bill_type']) or not cur_bill['last_vote']:
            continue
        print(cur_bill)
        cur_dict = {'BID': cur_bill['bill_id'], 'Description': cur_bill['title'],
                    'DateIntroduced': cur_bill['introduced_date'], 'Status': cur_bill['latest_major_action'],
                     'CongressN': cur_bill['bill_id'][:-3], 'URL': cur_bill['govtrack_url']}
        if not cur_bill['last_vote']:
            cur_dict['VotedOn'] = 0
            cur_dict['DateVoted'] = 0
            cur_dict['RollCallID'] = 0
        else:
            cur_dict['VotedOn'] = 1
            cur_dict['DateVoted'] = cur_bill['last_vote']
            cur_dict['RollCallID'] = 0

        house_bills.append(cur_dict)

    with open('Data Scraping/Dictionaries/Clean/clean_house_bills.json', 'w') as outfile:
        json.dump(house_bills, outfile, ensure_ascii=True)
    outfile.close()


# Scrapes the votes from the ProPublica API
def scrape_votes():
    # Getting most recent senate votes
    senate_votes = []
    votes = congress.votes.by_month(chamber='senate', year='2018', month='10')
    for vote in votes['votes']:
        # print(vote)
        if vote['bill'] == {}:
            continue
        else:
            senate_votes.append({'bill': vote['bill'], 'congress': vote['congress'], 'chamber': vote['chamber'],
                                 'session': vote['session'], 'roll_call': vote['roll_call'], 'date': vote['date'],
                                 'description': vote['description'], 'result': vote['result'],
                                 'breakdown': congress.votes.get(vote['chamber'], vote['roll_call'], vote['session'])})

    with open('Data Scraping/Dictionaries/Clean/clean_senate_votes.json', 'w') as outfile:
        json.dump(senate_votes, outfile, ensure_ascii=True)
    outfile.close()

    # Getting most recent house votes
    house_votes = []
    votes = congress.votes.by_month(chamber='house', year='2018', month='9')
    print(votes)
    for vote in votes['votes']:
        print(vote)
        if vote['bill'] == {}:
            continue
        else:
            house_votes.append({'bill': vote['bill'], 'congress': vote['congress'], 'chamber': vote['chamber'],
                                 'session': vote['session'], 'roll_call': vote['roll_call'], 'date': vote['date'],
                                 'description': vote['description'], 'result': vote['result'],
                                 'breakdown': congress.votes.get(vote['chamber'], vote['roll_call'], vote['session'])})

    with open('Data Scraping/Dictionaries/Clean/clean_house_votes.json', 'w') as outfile:
        json.dump(house_votes, outfile, ensure_ascii=True)
    outfile.close()


if __name__ == "__main__":
    scrape_bills()

    exit()
