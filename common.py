# coding=utf-8
import re
from datetime import date, timedelta

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def get_chrome_browser(headless=True):
    ops = Options()
    ops.headless = headless

    browser = Chrome(options=ops)
    return browser


def wait_browser_load_by_selector(browser, timeout, css_selector):
    WebDriverWait(browser, timeout).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    wait_loader_disappeared(browser, timeout)


def wait_loader_disappeared(browser, timeout):
    WebDriverWait(browser, timeout).until_not(
        expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'loading-center'))
    )


def get_first_of_last_month():
    d = date.today()
    d = d.replace(day=1)
    lm = d - timedelta(days=1)
    return lm.replace(day=1)


class CartItem:
    def __init__(self, name):
        self.name = name
        self.number_of_dishes = 0
        self.dish_names = []

    def add_dish(self, dish_name):
        self.dish_names.append(dish_name)

    def __unicode__(self):
        return u':white_check_mark: *{name}* - {num_dishes} món {note}\n{list}'.format(
            name=self.name,
            note=u':jenkins_triggered: *CHANGE YOUR NAME PLEASE*!!!' if 'foodee' in self.name.lower() else u'',
            num_dishes=self.number_of_dishes,
            list=u'\n'.join([u'- {}'.format(unicode(d)) for d in self.dish_names])
        )


def beautify_cart_items_text(text):
    # remove price tag
    text = re.sub(u'([0-9]+\,0+đ)', '', text)

    this_line_is_username = True
    this_line_is_num_of_dishes = False
    num_dishes = 0
    cur_item = None
    items = list()

    for line in text.splitlines():
        line = line.strip()

        # skip empty line
        if not line:
            continue

        if this_line_is_username:
            cur_item = CartItem(line)
            this_line_is_username = False
            this_line_is_num_of_dishes = True
        elif this_line_is_num_of_dishes:
            num_dishes = int(line.split(' ')[0])
            cur_item.number_of_dishes = num_dishes
            this_line_is_num_of_dishes = False
        # this line is item
        else:
            cur_item.add_dish(line)
            num_dishes -= 1
            if num_dishes == 0:
                if cur_item:
                    items.append(cur_item)
                this_line_is_username = True

    str = u'\n\n'.join([unicode(i) for i in items])
    return str if str else u':question:'


if __name__ == '__main__':
    t = u"""Hà Vĩnh Đạt
11 món
1 Mì gà quay xá xíu (OB)
35,000 đ
1 Cơm chiên gà xối mỡ (BLT)
38,000 đ
1 Tokbokki (OB)
35,000 đ
1 Bạch tuộc cay phô mai (size L) + kèm bánh mì (OB)
70,000 đ
1 Nui pate trứng (OB)
30,000 đ
1 Nui xào gà bơ tỏi (OB)
35,000 đ
1 Combo đùi gà xá xíu (2 đùi +1 bánh mì) (OB)
55,000 đ
1 Bánh canh cá lóc (OB)
35,000 đ
2 Mì xào gà quay tiêu (OB)
70,000 đ
2 Mì xào gà xá xíu (OB)
70,000 đ
1 Bánh canh đầu cá lóc (OB)
45,000 đ
Doge Benjamin
1 món
1 Cơm chiên gà xối mỡ (BLT)
38,000 đ"""
    t = beautify_cart_items_text(t)
    print(t)
