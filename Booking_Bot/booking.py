import os
import Booking_Bot.booking_constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from Booking_Bot.booking_filter import BookingFiltration
from Booking_Bot.booking_report import BookingReport


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"/usr/local/bin/selenium_driver", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
    
    def change_currency(self, currency=None):
        currency_element = self.find_element(
            [By.CSS_SELECTOR, 'Button[data-tooltip-text="Choose your currency"]']
        )
        currency_element.click()
        selected_currency_element = self.find_element(
            [By.CSS_SELECTOR, f'a[data-modal-header-async-url-param*="selected_currency={currency}"]']
        )
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(
            [By.ID, 'ss']
        )
        search_field.clear()
        search_field.send_keys(place_to_go)
        first_result = self.find_element(
            [By.CSS_SELECTOR, 'Li[data-i="0']
        )
        first_result.click()

    def click_search(self):
        search_button = self.find_element(
            By.CSS_SELECTOR, 'button[type="submit]'
        )
        search_button.click()

    def select_date(self, check_in_date, check_out_date):
        check_in_element = self.find_element(
            By.CSS_SELECTOR, f'td[date-date="{check_in_date}"]'
        )
        check_in_element.click()
        check_out_element = self.find_element(
            By.CSS_SELECTOR, f'td[date-date="{check_out_date}"]'
        )
        check_out_element.click()

    def select_adult(self, count=1):
        selection_element = self.find_element(
            By.ID, 'xp__guests__toggle'
        )
        selection_element.click()
        while True:
            decrease_adults_element = self.find_element(
                By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]'
            )
            decrease_adults_element.click()
            adults_value_element = self.find_element(
                By.ID, 'group_adults'
            )
            adults_value = adults_value_element.get_attribute(
                'value'
            )
            if int(adults_value) == 1:
                break

        increase_button_element = self.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Increase number of adults"]'
        )
        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.find_element(
            By.CSS_SELECTOR, 'button[type="submit]'
        )
        search_button.click()

    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(5)
        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_element(
            By.ID, 'hotellist_inner'
        )
        report = BookingReport(hotel_boxes)
        print(report.pull_deal_boxes.get_attributes())


