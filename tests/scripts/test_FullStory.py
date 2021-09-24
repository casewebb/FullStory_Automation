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

        landing_page.wait_for_bundle(10)
        requests = network_traffic_util.get_all_fs_bundle_requests(driver)
        self.assertTrue(network_traffic_util.is_user_going_to_route_evnt_present(requests, "market"),
                        msg='No event for market navigation found.')

        # Market page interactions
        market_page.add_fruit_to_cart('Dragon Fruit')
        market_page.search_and_add_fruit_to_cart('Oranges de Florida')
        fruits = ['Dragon Fruit', 'Oranges de Florida']

        # Validate FS Add Product Events
        market_page.wait_for_bundle(10)
        requests = network_traffic_util.get_all_fs_bundle_requests(driver)
        self.assertTrue(network_traffic_util.is_product_added_evnt_present(requests, 'Dragon Fruit'),
                        msg="No event for Dragon Fruit added to cart found.")
        self.assertTrue(network_traffic_util.is_product_added_evnt_present(requests, 'Oranges de Florida'),
                        msg="No event for Oranges de Florida added to cart found.")

        market_page.click_link_by_text(market_page.MY_CART_LINK)
        market_page.wait_for_bundle(10)
        requests = network_traffic_util.get_all_fs_bundle_requests(driver)
        self.assertTrue(network_traffic_util.is_user_going_to_route_evnt_present(requests, "cart"),
                        msg='No event for cart navigation found.')

        # Cart Page interactions
        my_cart_page.click_link_by_text(my_cart_page.CHECKOUT_LINK)
        my_cart_page.wait_for_bundle(10)
        requests = network_traffic_util.get_all_fs_bundle_requests(driver)
        self.assertTrue(network_traffic_util.is_user_going_to_route_evnt_present(requests, "checkout"),
                        msg='No event for checkout navigation found.')

        # Checkout Page interactions
        checkout_page.fill_out_address("billing")
        checkout_page.fill_out_address("shipping")
        checkout_page.fill_out_payment()
        checkout_page.click_link_by_text(checkout_page.PURCHASE_LINK)

        # Validate order completed event with all added fruits
        checkout_page.wait_for_bundle(10)
        requests = network_traffic_util.get_all_fs_bundle_requests(driver)
        self.assertTrue(network_traffic_util.is_order_completed_evnt_present(requests, fruits))

        # Validate that all bundles through the test case were sent sequentially
        # and bundletime chaining aligns
        self.assertTrue(network_traffic_util.is_sequential_bundles(requests))


