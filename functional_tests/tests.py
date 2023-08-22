"""Module for functional tests."""
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from django.test import LiveServerTestCase

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """_summary_

    Args:
        LiveServerTestCase (_type_): liver server url
    """

    def setUp(self):  # unittest 会在每个测试方法之前运行 setUp
        self.browser = webdriver.Firefox()

    def tearDown(self):  # unittest 会在每个测试方法之后运行 tearDown
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text: str):
        """check for row in list table"""

        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element("id", "id_list_table")
                rows = table.find_elements("tag name", "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as error:
                if time.time() - start_time > MAX_WAIT:
                    raise error
                time.sleep(0.5)

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

        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # 页面中又显示了一个文本框,可以输入其他的代办事项
        # 她输入了"Use peacock feathers to make a fly"
        # 她做事很有条理
        inputbox = self.browser.find_element("id", "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新,她的清单中显示了这两个代办事项
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")
        # 她想知道这个网站是否会记住她的清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 她访问那个URL,发现她的代办事项列表还在

        # 她很满意,去睡觉了

    def test_mutiple_users_can_start_lists_at_different_urls(self):
        """mutiple users can start lists at different urls"""

        # 伊迪丝新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # 她注意到清单有个唯一的URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # 现在一名叫作弗朗西斯的新用户访问了网站

        ## 我们使用一个新浏览器会话
        ## 确保伊迪丝的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 弗朗西斯访问首页
        # 页面中看不到伊迪丝的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # 弗朗西斯输入一个新待办事项,新建一个清单
        # 他不像伊迪丝那样兴趣盎然
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # 弗朗西斯获得了他的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 这个页面还是没有伊迪丝的清单
        page_text = self.browser.find_elements(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # 两人都很满意,去睡觉了
        self.fail("Finish the test!")
