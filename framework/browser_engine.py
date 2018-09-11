# -*- coding:utf-8 -*-

import os.path
from configparser import ConfigParser
from selenium import webdriver
from framework.logger import Logger

logger = Logger(logger="BrowserEngine").getlog()


class BrowserEngine(object):
    dir = os.path.dirname(os.path.abspath('.'))  # 注意相对路径获取方法
    chrome_driver_path = dir + '/tools/chromedriver'
    firefox_driver_path = dir + '/tools/geckodriver2'
    ie_driver_path = dir + '/tools/IEDriverServer.exe'

    def __init__(self, driver):
        self.driver = driver

        # read the browser type from config.ini file, return the driver

    def open_browser(self, driver):
        # 读取配置配件
        config = ConfigParser()
        file_path = os.path.dirname(os.path.abspath('.')) + '/config/config.ini'
        config.read(file_path)

        # 获取配置文件属性
        browser = config.get("browserType", "browserName")
        logger.info("You had select %s browser." % browser)
        url = config.get("testServer", "URL")
        logger.info("The test server url is: %s" % url)

        if browser == "Firefox":
            options = webdriver.FirefoxOptions()
            options.set_headless('-headless')
            driver = webdriver.Firefox(executable_path=self.firefox_driver_path,
									  # firefox_profile="/Users/buxiangjie/FirefoxProfiles",
									  # firefox_options=options,
                                      )
            logger.info("Starting firefox-headless browser.")
        elif browser == "ff":
            driver = webdriver.Firefox(executable_path=self.firefox_driver_path,
                                       #firefox_profile="/Users/buxiangjie/FirefoxProfiles",
                                       )

        elif browser == "Chrome":
            driver = webdriver.Chrome(executable_path="/Users/buxiangjie/Downloads/chromedriver")
            logger.info("Starting Chrome browser.")
        elif browser == "IE":
            driver = webdriver.Ie(self.ie_driver_path)
            logger.info("Starting IE browser.")

        driver.get(url)
        logger.info("Open url: %s" % url)
        driver.maximize_window()
        logger.info("Maximize the current window.")
        return driver

    def quit_browser(self):
        logger.info("Now, Close and quit the browser.")
        self.driver.quit()