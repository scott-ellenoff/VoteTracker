# Scraper for the VoteTrackr Project that uses ProPublica API
# Should be used to produce initial data for the database of bills and votes
from congress import Congress
import json

# Constants
PROPUBLICA_API_KEY = 'AfFAT83Y5LHoCEvkGgwjbjrtVrZgVSgp18YXiF0R'
congress = Congress(PROPUBLICA_API_KEY)


# Scrapes all relevant bills from the ProPublica API for the 155th congress
def scrape_bills():
    senate_bills = []
    for i in range(0, 3700):
        try:
            cur_bill = congress.bills.get('s'+str(i))
        except:
            continue

        if (cur_bill['cosponsors'] < 8) or ('res' in cur_bill['bill_type']) or not cur_bill['last_vote']:
            continue
        print(cur_bill)
        cur_dict = {'BID': cur_bill['bill_id'], 'Description': cur_bill['title'], 'Name': cur_bill['short_title'],
                    'DateIntroduced': cur_bill['introduced_date'], 'Status': cur_bill['latest_major_action'],
                     'CongressN': cur_bill['bill_id'][-3:], 'URL': cur_bill['govtrack_url'], 'Chamber': 'Senate'}
        if not cur_bill['last_vote']:
            cur_dict['VotedOn'] = 0
            cur_dict['DateVoted'] = 0
            # cur_dict['RollCallID'] = 0
        else:
            cur_dict['VotedOn'] = 1
            cur_dict['DateVoted'] = cur_bill['last_vote']
            # cur_dict['RollCallID'] = 0

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

        if (cur_bill['cosponsors'] < 50) or ('res' in cur_bill['bill_type']) or not cur_bill['last_vote']:
            continue
        print(cur_bill)
        cur_dict = {'BID': cur_bill['bill_id'], 'Description': cur_bill['title'], 'Name': cur_bill['short_title'],
                    'DateIntroduced': cur_bill['introduced_date'], 'Status': cur_bill['latest_major_action'],
                     'CongressN': cur_bill['bill_id'][-3:], 'URL': cur_bill['govtrack_url'], 'Chamber': 'House'}
        if not cur_bill['last_vote']:
            cur_dict['VotedOn'] = 0
            cur_dict['DateVoted'] = 0
            # cur_dict['RollCallID'] = 0
        else:
            cur_dict['VotedOn'] = 1
            cur_dict['DateVoted'] = cur_bill['last_vote']
            # cur_dict['RollCallID'] = 0

        house_bills.append(cur_dict)

    with open('Data Scraping/Dictionaries/Clean/clean_house_bills.json', 'w') as outfile:
        json.dump(house_bills, outfile, ensure_ascii=True)
    outfile.close()


# Scrapes the votes from the ProPublica API
def scrape_votes_for_bills():
    # Getting votes for bills already in the db
    all_bills = json.loads(open('Data Scraping/Dictionaries/Clean/clean_house_bills.json').read()) + \
                json.loads(open('Data Scraping/Dictionaries/Clean/clean_senate_bills.json').read())

    all_bids = [bill['BID'] for bill in all_bills]

    chambers = ['senate', 'house']
    years = ['2017', '2018']
    months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    collected_votes = {}
    for chamber in chambers:
        for year in years:
            for month in months:
                votes = congress.votes.by_month(chamber=chamber, year=year, month=month)
                for vote in votes['votes']:
                    if not vote['bill'] or vote['bill']['bill_id'] not in all_bids:
                        continue
                    else:
                        cur_vote = congress.votes.get(vote['chamber'], vote['roll_call'], vote['session'])
                        # print(cur_vote)
                        cur_vote_bid = cur_vote['votes']['vote']['bill']['bill_id']
                        cur_vote_breakdown = cur_vote['votes']['vote']['positions']

                        collected_votes[cur_vote_bid] = {}
                        for l in cur_vote_breakdown:
                            collected_votes[cur_vote_bid][l['member_id']] = l['vote_position']
    print(len(collected_votes))
    with open('Data Scraping/Dictionaries/Clean/collected_votes.json', 'w') as outfile:
        json.dump(collected_votes, outfile, ensure_ascii=True)
    outfile.close()


if __name__ == "__main__":
    # scrape_bills()
    # bills = congress.bills.recent(chamber='house')
    # print(bills)

    scrape_votes_for_bills()
    exit()
