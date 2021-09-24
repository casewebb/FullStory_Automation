import time
import unittest

from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


# This is something I would never have for general UI test automation
# but to test human-type interactions being captured by FullStory's script
# this feels necessary. Without it the script completes in just several seconds so only 1 or 2 bundles are sent.
class EventListener(AbstractEventListener):
    def after_find(self, by, value, driver):
        time.sleep(1)


class WebDriverSetup(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        options.add_argument('allow-running-insecure-content')

        self.driver = EventFiringWebDriver(
            webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                             options=options), EventListener())
        self.driver.implicitly_wait(10)

    def tearDown(self):
        if self.driver is not None:
            self.driver.close()
            self.driver.quit()
