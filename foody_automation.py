import base64
import time
import constants
import config

from common import get_chrome_browser, wait_browser_load_by_selector, wait_loader_disappeared


class NowAutomation:
    def __init__(self, headless, merchant_url=None):
        if merchant_url is None:
            merchant_url = 'https://www.now.vn/ho-chi-minh/com-trua-bento-now-station-ton-that-tung/'

        self.browser = get_chrome_browser(headless)
        self.wait_timeout = 20
        self.delay_between_action = 5

        self.email = config.EMAIL
        self.password = base64.decodestring(config.ENCODED_PASSWORD)

        self.url_login = 'https://www.now.vn/account/login'
        self.url_merchant = merchant_url
        self.url_history = 'https://www.now.vn/lich-su-dat-mon/'

    def default_sleep(self):
        time.sleep(self.delay_between_action)

    def get(self, url):
        self.default_sleep()
        self.browser.get(url)

    def skip_modal_blocker_in_merchant(self):
        try:
            btn = self.browser.find_element_by_css_selector(constants.NOW_DISMISS_MERCHANT_BTN_SELECTOR)
            btn.click()
        except Exception:
            pass

    def do_login(self):
        self.get(self.url_login)
        wait_browser_load_by_selector(self.browser, self.wait_timeout, constants.NOW_LOGIN_EMAIL_SELECTOR)

        email_input = self.browser.find_element_by_css_selector(constants.NOW_LOGIN_EMAIL_SELECTOR)
        password_input = self.browser.find_element_by_css_selector(constants.NOW_LOGIN_PASSWORD_SELECTOR)
        login_btn = self.browser.find_element_by_css_selector(constants.NOW_LOGIN_BTN_SELECTOR)

        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        login_btn.click()

    def get_order_link(self):
        self.get(self.url_merchant)
        wait_browser_load_by_selector(self.browser, self.wait_timeout, constants.NOW_GROUP_ORDER_LINK_SELECTOR)

        self.skip_modal_blocker_in_merchant()

        group_order_btn = self.browser.find_element_by_css_selector(constants.NOW_GROUP_ORDER_BTN_SELECTOR)
        group_order_link_text = self.browser.find_element_by_css_selector(constants.NOW_GROUP_ORDER_LINK_SELECTOR)

        group_order_btn.click()
        time.sleep(0.5)
        return group_order_link_text.get_attribute('value')

    def save_screenshot_of_detail_order(self, filepath):
        self.get(self.url_merchant)
        wait_browser_load_by_selector(self.browser, self.wait_timeout, constants.NOW_GROUP_ORDER_DETAIL_BTN_SELECTOR)

        self.skip_modal_blocker_in_merchant()

        group_order_detail_btn = self.browser.find_element_by_css_selector(
            constants.NOW_GROUP_ORDER_DETAIL_BTN_SELECTOR)
        group_order_detail_btn.click()

        self.default_sleep()

        self.browser.find_element_by_css_selector(constants.NOW_GROUP_ORDER_DETAIL_MODAL_SELECTOR).screenshot(filepath)

    def get_card_item_list_text(self):
        self.get(self.url_merchant)
        wait_browser_load_by_selector(self.browser, self.wait_timeout, constants.NOW_GROUP_ORDER_BTN_SELECTOR)

        return self.browser.find_element_by_class_name('now-order-card-group').text

    def get_last_bill(self):
        # go to history
        self.get(self.url_history)
        wait_browser_load_by_selector(self.browser, self.wait_timeout, constants.NOW_HISTORY_FROM_DATE_INPUT_SELECTOR)

        # filter from first day of last month till now
        from_date_input = self.browser.find_element_by_css_selector(constants.NOW_HISTORY_FROM_DATE_INPUT_SELECTOR)
        search_btn = self.browser.find_element_by_css_selector(constants.NOW_HISTORY_SEARCH_BTN_SELECTOR)

        # select from-date and to-date is today
        from_date_input.click()
        time.sleep(0.5)
        self.browser.find_element_by_css_selector(constants.NOW_HISTORY_FROM_DATE_TODAY_VALUE_SELECTOR).click()
        time.sleep(0.5)

        # search for today bill
        search_btn.click()
        wait_loader_disappeared(self.browser, self.wait_timeout)

        try:
            # click on bill
            first_order_link = self.browser.find_element_by_css_selector(
                constants.NOW_HISTORY_FIRST_ORDER_DETAIL_LINK_SELECTOR)
            first_order_link.click()
            wait_loader_disappeared(self.browser, self.wait_timeout)

            usernames = [e.text for e in self.browser.find_elements_by_css_selector(
                'div.history-table-scroll > div.history-table-row > div.history-table-cell.history-table-col1')]
            dishnames = [e.text for e in self.browser.find_elements_by_css_selector(
                'div.history-table-scroll > div.history-table-row > div.history-table-cell.history-table-col2')]
            finalprices = [e.text for e in self.browser.find_elements_by_css_selector(
                'div.history-table-scroll > div.history-table-row > div.history-table-cell.history-table-col7')]

            return [{
                'username': usernames[i],
                'dish': dishnames[i],
                'price': finalprices[i],
            } for i in xrange(len(usernames))]
        except Exception:
            return []

    def __del__(self):
        self.browser.close()


if __name__ == '__main__':
    now = NowAutomation(headless=False)

    now.do_login()
    l = now.get_last_bill()
    for e in l:
        print(u'name: {}, dish: {}, price: {}'.format(e['username'], e['dish'], e['price']))
