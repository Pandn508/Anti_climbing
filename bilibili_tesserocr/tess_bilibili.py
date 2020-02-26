import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chaojiying import Chaojiying_Client

EMAIL = '***'
PASSWORD = '***'

CHAOJIYING_USERNAME = '****'
CHAOJIYING_PASSWORD = '****'
CHAOJIYING_SOFT_ID = ***
CHAOJIYING_KIND = ***

class CrackBilibili():
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = Chaojiying_Client(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)

    def __del__(self):
        self.browser.close()

    def open(self):
        '''打开网页输入用户名密码'''
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def get_bilibili_button(self):
        '''获取登录按钮'''
        button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-login')))
        return button

    def get_bilibili_element(self):
        '''获取验证图片对象'''
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_img')))
        return element

    def get_position(self):
        '''获取验证码位置'''
        element = self.get_bilibili_element()
        time.sleep(2)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y']-50, location['y'] + size['height']-10, location['x'], location[
            'x'] + size['width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        '''获取网页截图'''
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_bilibili_image(self, name = 'captcha.png'):
        '''获取验证码图片'''
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_points(self, captcha_result):
        '''解析识别结果'''
        groups = captcha_result.get('pic_str').split('|')
        print(groups)
        locations = [[int(number) for number in group.split(',')] for group in groups]
        for i in locations:
            i[1] = i[1] - 15
        return locations

    def touch_click_words(self, locations):
        '''点击验证图片'''
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_bilibili_element(), location[0],
                                                                   location[1]).click().perform()
            time.sleep(1)

    def touch_click_verify(self):
        '''点击验证按钮'''
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_commit_tip')))
        button.click()
        time.sleep(10)
        print('success')

    # def login(self):
    #     submit = self.wait.until(EC.element_to_be_clickable((By)))

    def crack(self):
        time.sleep(5)
        self.open()
        button = self.get_bilibili_button()
        button.click()

        image = self.get_bilibili_image()
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')

        result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print(result)
        locations = self.get_points(result)
        self.touch_click_words(locations)
        self.touch_click_verify()

    #     faild = self.wait.until(
    #         EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_result_tip'), '验证失败'))
    #     print(faild)
    #
    #     if faild:
    #         time.sleep(5)
    #         self.relogin()
    #     else:
    #         print('success')
    #
    # def relogin(self):
    #     image = self.get_bilibili_image()
    #     bytes_array = BytesIO()
    #     image.save(bytes_array, format='PNG')
    #
    #     result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
    #     print(result)
    #     locations = self.get_points(result)
    #     self.touch_click_words(locations)
    #     self.touch_click_verify()
    #
    #     faild = self.wait.until(
    #         EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_result_tip'), '验证失败'))
    #     print(faild)
    #
    #     if faild:
    #         time.sleep(5)
    #         self.relogin()
    #     else:
    #         print('success')

if __name__ == '__main__':
    crack = CrackBilibili()
    crack.crack()




























