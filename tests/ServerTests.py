import unittest

class TestStringMethods(unittest.TestCase):
    #strings
    realUID = # A UID already existing in our database
    fakeUID = # Nonexistent UID
    realLID = # A LID already existing in our database
    fakeLID = # Nonexistent LID
    realBID = # A BID already existing in our database
    fakeBID = # Nonexistent BID
    billName = 
    #JSON objects
    userInfo = # Userinfo string for a user with realUID in our database
    billInfo = # Billinfo string for a bill with realBID in our database
    
    
    #tests addUser
    #actually adding a user
    #adding a user with no name
    #adding a user with no district
    #adding a user with wrong name (prohibited characters)
    #adding a user with wrong district(more numbers in zipcode)
    #adding a user with wrong district(wrong chars in zipcode)
    def test_addUser(self):
        self.assertTrue(addUser('Derrick Gilroy', '10128'))
        self.assertFalse(addUser('', '10128'))
        self.assertFalse(addUser('Kahlan', ''))
        self.assertFalse(addUser('Derrick_6536456_Gilroy', '1012234238'))
        self.assertFalse(addUser('Derrick Gilroy', '1012234238'))
        self.assertFalse(addUser('Derrick Gilroy', '606fd7'))

        
    #tests getUser
    #using a real UID
    #using a fake UID
    #suing an empty UID
    #using no UID
    def test_getUser(self):
        self.assertEqual(getUser(realUID), userInfo)
        self.assertEqual(getUser(fakeUID), '')
        self.assertEqual(getUser(''), '')

        
    #tests removeUser
    #using a real UID
    #using a fake UID
    #using an empty UID
    def test_removeUser(self):
        self.assertTrue(removeUser(realUID))
        self.assertFalse(removeUser(fakeUID))
        self.assertFalse(removeUser(''))

        
    #tests setUserInfo which takes username, zip, and a legislator of preference(if any)
    #tests with accurate information
    #tests with fake UID
    #tests with no UID
    #tests with various wrong info inputs
    def test_setUserInfo(self):
        self.assertTrue(setUserInfo(realUID, 'Ken', '60637', 'Cory Booker'))
        self.assertTrue(setUserInfo(realUID, 'Ken', '60637', ''))
        self.assertFalse(setUserInfo(fakeUID, 'Ken', '60637', 'Cory Booker'))
        self.assertFalse(setUserInfo('', 'Ken', '60637', 'Cory Booker'))
        
        self.assertFalse(setUserInfo(realUID, 'fak3///].', '60637', 'Cory Booker'))
        self.assertFalse(setUserInfo(realUID, '', '60637', 'Cory Booker'))
        self.assertFalse(setUserInfo(realUID, 'Ken', '6536346325', 'Cory Booker'))
        self.assertFalse(setUserInfo(realUID, 'Ken', '', 'Cory Booker'))
        self.assertFalse(setUserInfo(realUID, 'Ken', '60637', 'Booker')) # Legislator not in our DB

    #tests addVote
    #tests with accurate information (UID/LID/BID)
    #tests with inaccurate information (UID/LID/BID)
    #tests with no LID/UID
    #tests with no BID
    #tests with no vote
    #tests with wrong vote input
    def test_addVote(self):
        self.assertTrue(addVote(realUID, realBID, 'yay'))
        self.assertTrue(addVote(realLID, realBID, 'nay'))
        
        self.assertFalse(addVote(fakeUID, realBID, 'nay'))
        self.assertFalse(addVote(fakeLID, realBID, 'nay'))
        
        self.assertFalse(addVote(realLID, fakeBID, 'nay'))
        
        self.assertFalse(addVote('', realBID, 'nay'))
        self.assertFalse(addVote(realUID, '', 'nay'))
        self.assertFalse(addVote(realUID, realBID, ''))
        self.assertFalse(addVote(realUID, realBID, 'njdfssljd'))

        
    #tests getBill
    #tests with accurate BID
    #tests with fake BID
    #tests with no BID
    def test_getBill(self):
        self.assertEqual(getBill(realBID), billInfo)
        self.assertEqual(getBill(fakeBID), '')
        self.assertEqual(getBill(''), '')
        
        
    #tests addBill which takes billID and Description
    #tests with valid bill info inputs (No description is valid)
    #tests with no information
    def test_addBill(self):
        self.assertTrue(addBill('b123', 'Short descr'))
        self.assertFalse(addBill('b123', 'Short descr')) # Can't add a bill with same id twice
        self.assertTrue(addBill('b321', ''))
        
        self.assertFalse(addBill('b123**.,]', 'Short descr'))
        self.assertFalse(addBill(''))

      
    #tests ChangeBillStatus
    #tests with accurate BID and status
    #tests with fake BID
    #tests with no BID
    #tests with wrong status
    #tests with no status
    def test_changeBillStatus(self):
        self.assertTrue(changeBillStatus(realBID, 'passed'))
        self.assertFalse(changeBillStatus(fakeBID, 'passed'))
        self.assertFalse(changeBillStatus('', 'passed'))
        self.assertFalse(changeBillStatus(realBID, 'somethinthatdoesntmakesense'))
        self.assertFalse(changeBillStatus(realBID, ''))

        
    #tests getLegislator
    #tests with a senators name that is already in our DB
    #tests with False name
    def test_getLegislator(self):
        self.assertTrue(getLegislator('Cory Booker'))
        self.assertFalse(getLegislator('Corey Booker'))

if __name__ == '__main__':
    unittest.main()
        
