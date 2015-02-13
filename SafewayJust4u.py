__author__ = 'Vasiliy'
# auto add items to safeway card

from selenium import webdriver
import selenium.webdriver.common.by
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
from selenium.webdriver.common.keys import Keys
from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS
from sys import exit
import psutil

def params():
    """Import parameters from command line"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-lg', '--loginname', required=True, dest='user',
                        help='Enter email')
    parser.add_argument('-ps', '--password', required=True, dest='password',
                        help='Enter password')
    args = parser.parse_args()
    username = args.user
    password = args.password

    pathlink = "https://www.safeway.com/ShopStores/OSSO-Login.page?goto=http%3A%2F%2Fwww.safeway.com%2F"

    return username, password, pathlink

APPNAME = 'chromedriver.exe'

def kill_chromedriver():
    for proc in psutil.process_iter():
        name = str(proc.name)
        print name
        if name == APPNAME:
            proc.kill()

class singlescript:
    """ Limits script to single instance """

    def __init__(self):
        self.mutexname = "scriptmutex_{D0E858DF-985E-4907-B7FB-8D732C3FC3B9}"
        self.mutex = CreateMutex(None, False, self.mutexname)
        self.lasterror = GetLastError()

    def alreadyrunning(self):
        return (self.lasterror == ERROR_ALREADY_EXISTS)

    def __del__(self):
        if self.mutex:
            CloseHandle(self.mutex)

class ACCOUNT:
    def __init__(self, username, password, path):

        self.username = username
        self.password = password
        self.driver = None
        self.path = path

    def login(self):
        for i in xrange(3):
            try:
                self.driver = DRIVER()
                if self.driver:
                    break
            except Exception, mess:
                print str(mess)
                time.sleep(1)
        if not self.driver:
            self.driver.implicitly_wait(30)

        # Navigate to initial web page
        base_url = self.path
        self.driver.get(base_url)
        self.driver.maximize_window()

        # Verify that only single instance script is running
        try:
            checksingle = singlescript()
            if checksingle.alreadyrunning():
                print "Script already running, quit this instance"
                self.quit()
                kill_chromedriver()
                exit(0)
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

        # Find menu
        print "Find menu Just4U on page"
        try:
            getmenu = self.driver.findlinkbyhref("/ShopStores/Offers-Landing-IMG.page")
            if getmenu:
                self.driver.myclick(getmenu)
                sleep(2)
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

        # Move to coupon center page
        print "Going to coupon page"
        try:
            getcoupon = self.driver.findlinkbyimg("/CMS/assets/media/LandingPages/NewCTAButtons/J4U_LP_CouponCenterPod_01.jpg")
            if getcoupon:
                self.driver.myclick(getcoupon)
                sleep(15)
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

        # Clear username box and enter new
        try:
            print "Find userid input"
            inputelement = self.driver.findbyid("userId")
            if inputelement.is_displayed() and inputelement.is_enabled():
                self.driver.mysendtext(inputelement, self.username)
                sleep(2)
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

        # Clear password box and enter new
        try:
            print "Find password input"
            inputelement = self.driver.findbyid("password")
            if inputelement.is_displayed() and inputelement.is_enabled():
                self.driver.mysendtext(inputelement, self.password)
                sleep(1)
                self.driver.mysendkey(inputelement, Keys.ENTER)
                sleep(2)
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

        try:
            print "Select show all offers on one page"
            getall = self.driver.findselectbyid("j4u-items-per-page")
            if getall:
                sleep(10)
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

        try:
            print "Check if any adds up"
            addsoff = self.driver.findlinkbyclass("btuw-neverwarn")
            if addsoff:
                self.driver.myclick(addsoff)
            else:
                print "No adds found"
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

        getadd = self.driver.findspanclassaddclick("lt-button-primary-add")
        if len(getadd) != 0:
            print "Added to card: " + str(len(getadd)) + " offers"
        else:
            print "Nothing to add: " + str(len(getadd)) + " offers available"

        getoffers = self.driver.findbyid("headerMyCardCount")
        if len(getoffers.text) != 0:
            print "Total offers on Safeway card currently = %s" % str(getoffers.text[1:4])

        return self.driver

    def quit(self):
        try:
            self.driver.quit()
            self = None
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

class DRIVER(webdriver.Chrome):
    def __init__(self):
        webdriver.Chrome.__init__(self)
        pass

    def findbyid(self, idname, waittime=60):
        # Find element by ID
        print("*** Function findbyid started. id = %s" % str(idname))
        try:
            wait = WebDriverWait(self, waittime)
            element = wait.until(EC.element_to_be_clickable((selenium.webdriver.common.by.By.ID, idname)))
            if element:
                print "*** Element " + str(idname) + " is found. Return Element"
                return element
            else:
                print "*** Element " + str(idname) + " is NOT found. Return None"
                return False

        except Exception, mess:
            print (">>> Exception: %s" % str(mess))
            return False

    def mysendtext(self, element, text):
        # Send text to element
        print "*** Function mysendtext started."
        try:
            element.clear()
            element.send_keys(text)
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

    def myclick(self, element):
        # Click element
        print "*** Function myclick started."
        try:
            element.click()
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

    def mysendkey(self, element, key):
        # Send KEY to element
        print "*** Function mysendkey started"
        try:
            element.send_keys(key)
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

    def findlinkclick(self, link):
        # Find link and tries to click it
        print "Function findlinkclick started"
        try:
            wait = WebDriverWait(self, 10)
            linklink = wait.until(EC.element_to_be_clickable(DRIVER.find_element_by_partial_link_text(link)))
            if linklink.is_displayed() and linklink.is_enabled():
                linklink.click()
                return True
        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

    def findlinkbyhref(self, name):
        # Find link by HREF attribute and click it
        print "*** Function findlinkbyhref started, href = %s" % str(name)
        try:
            alllink = self.find_elements_by_tag_name('a')
            i = 0
            while i < len(alllink):
                try:
                    if str(alllink[i].get_attribute('href')).find(name) > -1:
                        return alllink[i]
                except:
                    pass
                i += 1

        except Exception, mess:
            print (">>> Exception: %s" % str(mess))
            return False

    def findlinkbyimg(self, name):
        # Find link by image attribute and click it
        print "*** Function findlinkbyimg started link image = %s" % str(name)
        try:
            alllink = self.find_elements_by_tag_name('img')
            i = 0
            while i < len(alllink):
                try:
                    if str(alllink[i].get_attribute('src')).find(name) > -1:
                        return alllink[i]
                except:
                    pass
                i += 1
            time.sleep(1)

        except Exception, mess:
            print (">>> Exception: %s" % str(mess))
            return False

    def findlinkbytext(self, text):
        # Find link by text attribute and click it
        print "*** Function findlinkbytext started, link text = %s" % str(text)
        try:
            alllink = self.find_elements_by_tag_name('a')
            i = 0
            while i < len(alllink):
                try:
                    if str(alllink[i].get_attribute('text')).find(text) > -1:
                        return alllink[i]
                except:
                    pass
                i += 1
            time.sleep(1)

        except Exception, mess:
            print (">>> Exception: %s" % str(mess))
            return False

    def findlinkbyclass(self, name):
        # Find link by class name and click it
        print "*** Function findlinkbyclass started, class name = %s" % str(name)
        try:
            alllink = self.find_elements_by_tag_name('a')
            i = 0
            while i < len(alllink):
                try:
                    if str(alllink[i].get_attribute('class')).find(name) > -1:
                        return alllink[i]
                except:
                    pass
                i += 1
            time.sleep(1)

        except Exception, mess:
            print (">>> Exception: %s" % str(mess))
            return False

    def findspanclassaddclick(self, name):
        # Find button by span text and click it
        print "*** Function findspanclassaddclick started"
        try:
            allSpans = self.find_elements_by_tag_name('span')
            total = []
            i = 0
            while i < len(allSpans):
                try:
                    if allSpans[i].get_attribute('class').find(name) > -1 and str(allSpans[i].text) == "Add" and \
                            allSpans[i].is_displayed() and allSpans[i].is_enabled():
                        allSpans[i].click()
                        total.append(allSpans[i])
                except:
                    pass
                i += 1
            time.sleep(1)
            return total

        except Exception, mess:
            print (">>> Exception: %s" % str(mess))

    def findselectbyid(self, name):
        # Find select attribute by ID and click it
        print "*** Function findselectbyid started"
        try:
                allSpans = self.find_elements_by_tag_name('select')
                i = 0
                while i < len(allSpans):
                    try:
                        if allSpans[i].get_attribute('id').find(name) > -1 and allSpans[i].is_displayed() and \
                                allSpans[i].is_enabled():
                            allSpans[i].click()
                            try:
                                if str(allSpans[i].get_attribute('value')) == "-1":
                                    allSpans[i].click()
                                    return True
                            except:
                                pass
                    except:
                        pass
                    i += 1
                time.sleep(1)

        except Exception, mess:
            print (">>> Exception: %s" % str(mess))
        return True

def safeway_login():
    """
    Login User
    """
    username = (params()[0])
    password = (params()[1])
    pathlink = (params()[2])

    try:
        userlogin = ACCOUNT(username, password, params()[2])
        if userlogin:
            print "We login to: " + pathlink
            result = userlogin.login()
            if result:
                print ("Adding coupons to Safeway Card was successful")
                result.close()
                kill_chromedriver()
        else:
            print ("Login to Safeway failed:")

    except Exception, mess:
        print (">>> Exception: %s" % str(mess))

safeway_login()