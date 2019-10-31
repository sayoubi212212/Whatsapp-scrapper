from PageCrawler import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Consts import *
from Env import *
from datetime import datetime
import threading
from threading import Lock
from SoundPlayer import *


class WhatsappPageCrawler(PageCrawler):

    def __init__(self, url, contact):
        super().__init__(url)
        self.updater_thread = None  # this will contain the auto fetching thread
        self.working_dir = BASE_WORKING_DIR + r"/Whatsapp/"
        self.contact = contact
        self.auto_update = False
        self.lock = Lock()

        # init notification sound player
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.sp = SoundPlayer(dir_path + NOTIFICATION_SOUND)

        Env.createFolder(self.working_dir)

    def startAutolFetch(self, interval):
        # start auto fetching data
        if not self.lock.locked():
            self.lock.acquire()
            if not self.auto_update and not self.updater_thread:
                self.updater_thread = threading.Thread(target=self.__fetchWithInterval, args=(interval,))
                self.auto_update = True
                self.updater_thread.start()
        else:
            raise RuntimeError("Auto fetch is already started")

    def stopAutolFetch(self):
        # stop the auto fetch, if started

        self.auto_update = False
        self.updater_thread = None
        self.lock.acquire()  # wait for the fetching thread to end and release the lock
        self.lock.release()

    def __fetchWithInterval(self, interval):
        # returns a dictionary of a time fetched and status keys

        driver = self.initDriver()
        file_name = self.working_dir + self.contact + ".pickle"
        prev_status = False  # will be indication to play notification sound

        while self.auto_update:

            status = self.checkStatusOfContact(driver, self.contact)
            data = (datetime.now(), status)
            Env.appendToPickle(file_name, data)

            if status and not prev_status:   # if the user was offline, and than logged in to be online
                self.sp.play()  # play notification sound
                print("playing")
            prev_status = status

            time_to_sleep = interval
            while self.auto_update and time_to_sleep > 0:  # to ensure faster reaction to stop the auto update
                time.sleep(1)  # sleep for a second, then check if you need to stop
                time_to_sleep -= 1

        driver.quit()
        self.lock.release()

    def initDriver(self):
        # init a chrome driver to connect whatsapp web, then click on the requested contact

        options = webdriver.ChromeOptions();
        options.add_argument(r"user-data-dir={}".format(CHROME_COOKIES_PATH))  # use an existing chrome data, with whatsapp web cookies
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        try:
            # search the contact in the search box
            wait_for_search_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, r"//input")))
            input_element = driver.find_elements(By.XPATH, r"//input")[0]
            input_element.send_keys(self.contact)
            input_element.send_keys(Keys.ENTER)

            wait_for_contact = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r"//span[text()='{}']".format(self.contact))))
            time.sleep(3)
            driver.find_elements(By.XPATH, r"//span[text()='{}']".format(self.contact))[0].click() # click on the contact name to enter conversation

            return driver

        except:
            driver.quit()
            raise RuntimeError("could not initialize driver properly")

    def checkStatusOfContact(self, driver, contact):
        # checks whether the contact appears as online in the current driver state

        try:
            # if the user is connected, a span that contains the word "online" exists
            WebDriverWait(driver, 0).until(EC.presence_of_element_located((By.XPATH, r"//span[text()='{}']".format("online"))))
            status = True
        except:
            status = False

        return status

