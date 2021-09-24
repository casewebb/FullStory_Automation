from unittest import TestLoader, TestSuite, TextTestRunner

from test.scripts.test_FullStory import FullStoryTest

import testtools as testtools

if __name__ == "__main__":
    test_loader = TestLoader()
    # Test Suite is used since there are multiple test cases
    test_suite = TestSuite((
        test_loader.loadTestsFromTestCase(FullStoryTest),
    ))

    test_runner = TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
