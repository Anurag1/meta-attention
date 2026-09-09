import unittest
from discovery_cortex import discovery

class TestDiscoveryCortex(unittest.TestCase):
    def test_generates_hypothesis_and_test(self):
        result = discovery('How could an AI detect and correct its own reasoning errors?')
        self.assertTrue(result['bridges'])
        self.assertTrue(result['bridges'][0]['hypothesis'])
        self.assertTrue(result['bridges'][0]['test'])
        self.assertGreaterEqual(len(result['questions']), 3)

if __name__ == '__main__':
    unittest.main()
