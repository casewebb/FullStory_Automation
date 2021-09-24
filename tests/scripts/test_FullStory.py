import time

from src.WebdriverSetup import WebDriverSetup
from src.page_obj.pages import Landing, Market, MyCart, Checkout
from src.util import network_traffic_util


class FullStoryTest(WebDriverSetup):
    def test_FullStoryCartFlow(self):
        driver = self.driver
        landing_page = Landing.LandingPage(driver)
        market_page = Market.MarketPage(driver)
        my_cart_page = MyCart.MyCartPage(driver)
        checkout_page = Checkout.CheckoutPage(driver)

        # Landing Page interactions
        landing_page.go_to_url('https://fruitshoppe.firebaseapp.com')
        landing_page.click_link_by_text(landing_page.MARKET_LINK)

        time.sleep(10)
        requests = network_traffic_util.get_all_fs_bundle_requests(driver)
        self.assertTrue(network_traffic_util.is_user_going_to_market_evnt_present(requests),
                        msg='No event for market navigation found.')

        # Market page interactions
        market_page.add_fruit_to_cart('Dragon Fruit')
        market_page.search_and_add_fruit_to_cart('Oranges de Florida')

        # Validate FS Add Product Event
        time.sleep(10)
        requests = network_traffic_util.get_all_fs_bundle_requests(driver)
        self.assertTrue(network_traffic_util.is_product_added_evnt_present(requests, 'Dragon Fruit'))

        market_page.click_link_by_text(market_page.MY_CART_LINK)

        # Cart Page interactions
        my_cart_page.click_link_by_text(my_cart_page.CHECKOUT_LINK)

        # Checkout Page interactions
        checkout_page.fill_out_address("billing")
        checkout_page.fill_out_address("shipping")
        checkout_page.fill_out_payment()
        checkout_page.click_link_by_text(checkout_page.PURCHASE_LINK)
        requests = network_traffic_util.get_all_fs_bundle_requests(driver)
        self.assertTrue(network_traffic_util.is_sequential_bundles(requests))

        time.sleep(10)

