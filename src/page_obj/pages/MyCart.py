from src.page_obj.pages.Base import BasePage


class MyCartPage(BasePage):
    CHECKOUT_LINK = "Checkout"
    my_cart_delete_fruit_xpath = "//ul[contains(@class, 'cart-list')]//li[not(contains(@class, 'header'))]//div[" \
                                 "contains(.,'{fruit}') and contains(@class, 'row')]//span[contains(@ng-click, " \
                                 "'itemRemove')] "

    def delete_fruit_from_cart(self, fruit):
        self.driver.find_element_by_xpath(self.my_cart_delete_fruit_xpath.format(fruit=fruit)).click()
