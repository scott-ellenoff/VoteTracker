import unittest

class TestAPIMethods(unittest.TestCase):
    #strings
    validBID = # Valid BID to request from the API
    invlaidBID = # Some made up nonsensical string

    #tests getBillInfo
    #tests with existing bill
    #tests with nonexisting bill
    #tests with wrong inputs into the request
    def test_getBillInfo(self):
        self.assertTrue(getBillInfo(validBID))
        self.assertFalse(getBillInfo(invalidBID))
        self.assertFalse(getBillInfo(''))
        
        
        
 if __name__ == '__main__':
    unittest.main()
