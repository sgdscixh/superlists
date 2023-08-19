"""Module for functional tests."""
import unittest
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    """Test new visitor"""

    def setUp(self):  # unittest 会在每个测试方法之前运行 setUp
        self.browser = webdriver.Firefox()

    def tearDown(self):  # unittest 会在每个测试方法之后运行 tearDown
        self.browser.quit()

    # unittest 会运行所有以 test_ 开头的方法
    def test_can_start_a_list_and_retrieve_it_later(self):
        """test can start a list and retrieve it later"""
        # online to-do list
        self.browser.get("http://localhost:8000")

        # page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_elements("tag name", "h1")
        self.assertIn("To-Do", header_text)

        ## 应用邀请她输入一个代办事项
        inputbox = self.browser.find_element("id", "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        ## 她在一个文本框中输入了"Buy peacock feathers"
        ## 她的爱好是使用假蝇做饵钓鱼

        inputbox.send_keys("Buy peacock feathers")

        ## 她按回车键后,页面更新了
        ## 代办事项表格中显示了"1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element("id", "id_list_table")
        rows = table.find_elements("tag name", "tr")
        self.assertTrue(any(row.text == "1: Buy peacock feathers" for row in rows))

        ## 页面中又显示了一个文本框,可以输入其他的代办事项
        ## 她输入了"Use peacock feathers to make a fly"
        ## 她做事很有条理

        self.fail("Finish the test!")
        ## 页面再次更新,她的清单中显示了这两个代办事项

        ## 她想知道这个网站是否会记住她的清单
        ## 她看到网站为她生成了一个唯一的URL
        ## 而且页面中有一些文字解说这个功能

        ## 她访问那个URL,发现她的代办事项列表还在

        ## 她很满意,去睡觉了


if __name__ == "__main__":
    unittest.main(warnings="ignore")
