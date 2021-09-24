from faker import Faker

from src.page_obj.Locators import Locator
from src.page_obj.pages.Base import BasePage


class CheckoutPage(BasePage):
    PURCHASE_LINK = "Purchase"
    BILLING_ADDRESS = "Billing Address"
    SHIPPING_ADDRESS = "Shipping Address"
    PAYMENT_DETAILS = "Payment Details"
    SAME_AS_BILLING = "Same as billing address."
    CONFIRM_CBX = "You sure you want this fruit?"

    fake = Faker()

    def fill_out_address(self, section):
        name = self.fake.name().split()
        address_1 = '{building_num} {street}'.format(building_num=self.fake.building_number(),
                                                     street=self.fake.street_name())
        bill_ship = self.BILLING_ADDRESS if section.lower() == 'billing' else self.SHIPPING_ADDRESS

        self.send_text_by_section_and_label(bill_ship, "First Name", name[0])
        self.send_text_by_section_and_label(bill_ship, "Last Name", name[1])
        self.send_text_by_section_and_label(bill_ship, "Address 1", address_1)
        self.send_text_by_section_and_label(bill_ship, "Address 2", self.fake.secondary_address())
        self.send_text_by_section_and_label(bill_ship, "City", self.fake.city())
        self.send_text_by_section_and_label(bill_ship, "Zip Code", self.fake.postcode())
        self.select_dropdown_by_section_and_label(bill_ship, "State", self.fake.state_abbr())

    def set_same_as_billing_checked(self, checked):
        ele = self.driver.find_element_by_xpath(Locator.checkbox_by_label.format(label_text=self.SAME_AS_BILLING))
        if checked and not ele.is_selected():
            ele.click()
        elif not checked and ele.is_selected():
            ele.click()

    def fill_out_payment(self):
        self.send_text_by_section_and_label(self.PAYMENT_DETAILS, "Credit Card Number", self.fake.credit_card_number())
        self.send_text_by_section_and_label(self.PAYMENT_DETAILS, "Security Code",
                                            self.fake.credit_card_security_code())
        self.select_dropdown_by_section_label_count(self.PAYMENT_DETAILS, "Expiration", 1,
                                                    self.fake.month().lstrip('0'))
        self.select_dropdown_by_index(self.PAYMENT_DETAILS, "Expiration", 2, 3)
        self.click_checkbox_by_label(self.CONFIRM_CBX)
