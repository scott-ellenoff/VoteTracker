import unittest

class TestStringMethods(unittest.TestCase):
    #strings
    realUID =
    realLID =
    realBID =
    billName =
    #JSON objects
    userInfo =
    billInfo = 
    
    #tests addUser
    #actually adding a user
    #adding a user with no name
    #adding a user with no district
    def test_addUser(self):
        self.assertTrue(addUser('Derrick Gilroy', '10128'))
        self.assertFalse(addUser('', '10128'))
        self.assertFalse(addUser('Kahlan', ''))

    #tests getUser
    #using a real UID
    #using no UID
    def test_getUser(self):
        self.assertEqual(getUser(realUID), userInfo)
        self.assertEqual(getUser(''), '')

    #tests removeUser
    #using a real UID
    #using no UID
    def test_removeUser(self):
        self.assertTrue(removeUser(realUID))
        self.assertFalse(removeUser(''))

    #tests setUserInfo
    #tests with accurate information
    #tests with no UID
    #tests with no name
    #tests with no district
    def test_setUserInfo(self):
        self.assertTrue(setUserInfo(realUID, 'Ken', '60637', 'Cory Booker'))
        self.assertFalse(setUserInfo('', 'Ken', '60637', 'Cory Booker'))
        self.assertFalse(setUserInfo(realUID, '', '60637', 'Cory Booker'))
        self.assertFalse(setUserInfo(realUID, 'Ken', '', 'Cory Booker'))

    #tests addVote
    #tests with accurate information (UID)
    #tests with accurate information (LID)
    #tests with no LID/UID
    #tests with no BID
    #tests with no vote
    def test_addVote(self):
        self.assertTrue(addVote(realUID, realBID, 'yay'))
        self.assertTrue(addVote(realLID, realBID, 'nay'))
        self.assertFalse(addVote('', realBID, 'nay'))
        self.assertFalse(addVote(realUID, '', 'nay'))
        self.assertFalse(addVote(realUID, realBID, ''))

    #tests getBill
    #tests with accurate bill name
    #tests with no bill name
    def test_getBill(self):
        self.assertEqual(getBill(billName), billInfo)
        self.assertEqual(getBill(''), '')
    #tests addBill
    #tests with accurate bill json object
    #tests with no information
    def test_addBill(self):
        self.asser

    #tests ChangeBillStatus
    #tests with accurate BID and status
    #tests with no BID
    #tests with no status
    def test_changeBillStatus(self):
        self.assertTrue(changeBillStatus(realBID, 'passed'))
        self.assertFalse(changeBillStatus('', 'passed'))
        self.assertFalse(changeBillStatus(realBID, ''))

    #tests getLegislator
    #tests with a senators name
    #tests with False name
    def test_getLegislator(self):
        self.assertTrue(getLegislator('Cory Booker'))
        self.assertFalse(getLegislator('Corey Booker'))

if __name__ == '__main__':
    unittest.main()
        
