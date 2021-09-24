from unittest import TestLoader, TestSuite, TextTestRunner

from tests.scripts.test_FullStory import FullStoryTest

if __name__ == "__main__":
    test_loader = TestLoader()
    test_suite = TestSuite((
        test_loader.loadTestsFromTestCase(FullStoryTest),
    ))

    test_runner = TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
