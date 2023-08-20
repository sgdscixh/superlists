"""Module for functional tests."""
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By

from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
    """_summary_

    Args:
        LiveServerTestCase (_type_): liver server url
    """

    def setUp(self):  # unittest 会在每个测试方法之前运行 setUp
        self.browser = webdriver.Firefox()

    def tearDown(self):  # unittest 会在每个测试方法之后运行 tearDown
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """check for row in list table"""

        table = self.browser.find_element("id", "id_list_table")
        rows = table.find_elements("tag name", "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_retrieve_it_later(self):
        """test mutiple user"""

        # online to-do app
        self.browser.get(self.live_server_url)

        # page title and header mention to-do lists
        headers = self.browser.find_elements(By.TAG_NAME, "h1")
        header_texts = [header.text for header in headers]
        self.assertTrue(any("To-Do" in text for text in header_texts))

        # 应用邀请她输入一个代办事项
        inputbox = self.browser.find_element("id", "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # 她在一个文本框中输入了"Buy peacock feathers"
        # 她的爱好是使用假蝇做饵钓鱼

        inputbox.send_keys("Buy peacock feathers")

        # 她按回车键后,页面更新了
        # 代办事项表格中显示了"1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)
        table = self.browser.find_element("id", "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "td")
        self.assertTrue(any("1: Buy peacock feathers" in row.text for row in rows))

        # 页面中又显示了一个文本框,可以输入其他的代办事项
        # 她输入了"Use peacock feathers to make a fly"
        # 她做事很有条理
        inputbox = self.browser.find_element("id", "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)
        # 页面再次更新,她的清单中显示了这两个代办事项
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")
        # 她想知道这个网站是否会记住她的清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 她访问那个URL,发现她的代办事项列表还在

        # 她很满意,去睡觉了
