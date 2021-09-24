from src.page_obj.pages.Base import BasePage


class MarketPage(BasePage):
    SEARCH_PLACEHOLDER = "Search Fruit"
    fruit_add_cart_xpath = '//div[starts-with(@class,"fruit-box") and contains(.,"{fruit}")]//a[' \
                           '@ng-click="addToCart(fruit)"]'

    def add_fruit_to_cart(self, fruit):
        self.driver.find_element_by_xpath(self.fruit_add_cart_xpath.format(fruit=fruit)).click()

    def search_and_add_fruit_to_cart(self, fruit):
        self.send_text_by_placeholder(self.SEARCH_PLACEHOLDER, fruit)
        self.add_fruit_to_cart(fruit)
