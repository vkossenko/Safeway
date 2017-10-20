__author__ = 'Vasiliy'
# auto add items to safeway card

# from win32com.server.exception import Exception
from selenium import webdriver
import selenium.webdriver.common.by
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from win32event import CreateMutex
# from win32api import CloseHandle, GetLastError
# from winerror import ERROR_ALREADY_EXISTS
from sys import exit
import psutil
import os
# import logging
# import smtplib
# from email.mime.text import MIMEText
import glob


def params():
    """Import parameters from command line"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-lg', '--loginname', required = True, dest = 'user',
                        help = 'Enter email')
    parser.add_argument('-ps', '--password', required = True, dest = 'password',
                        help = 'Enter password')
    parser.add_argument('-emailps', '--emailpassword', required = False, dest = 'emailpassword',
                        help = 'Enter email password')

    args = parser.parse_args()
    username = args.user
    password = args.password
    emailps = args.emailpassword
    pathlink = "https://www.safeway.com/"

    return username, password, pathlink, emailps

# def set_logging(name = "", path = "", level = "INFO"):
#     """Set logging tools"""
# 
#     # global logger
#     logger = logging.getLogger(name)
# 
#     numeric_level = getattr(logging, level.upper(), None)
#     logger.setLevel(numeric_level)
# 
#     #log to file
#     if not path:
#         path = os.path.curdir
#     else:
#         try:
#             os.makedirs(path)
#         except:
#             pass
#     formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
#     log = os.path.join(path, "%s_%s.log" % (name, time.strftime("%m%d%y_%H%M%S")))
#     fh = logging.FileHandler(log, "w")
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)
# 
#     #log to stdout
#     ch = logging.StreamHandler()
#     ch.setFormatter(formatter)
#     logger.addHandler(ch)
#     return logger

def cleanup_log():
    """ clean existing log files from working dir"""
    try:
        print("Clean up old log files")
        log_name = glob.glob("Just4you*.log")
        i = 0
        while i < len(log_name):
            filepath = os.getcwd() + "\\" + str(log_name[i])
            print("Completed")
            os.remove(filepath)
        i += 1
    except:
        pass
    else:
        print("We do not have old log files in directory\r\n")


# logger = set_logging("Just4you")


# def email_results(msg):
#     """ email results"""
#     sender = (params()[0])
#     receiver = (params()[0])
#     passw = (params()[3])
# 
#     message = MIMEText(msg)
#     message['Subject'] = "SMTP_SSL email with results from Just4you script"
#     message['From'] = sender
#     message['To'] = receiver
# 
#     try:
#         try:
#             print ("\r\nCreate SMTP_SSL object")
#             smtpObj = smtplib.SMTP_SSL ('outbound.att.net', 465)
# 
#         except Exception as mess:
#             print ("Error on SMTP object creation: " + str(mess))
# 
#         try:
#             print ("Secure login to outgoing mail server")
#             smtpObj.login(sender, passw)
#         except Exception as mess:
#             print ("Error on login: " + str(mess))
# 
#         try:
#             print ("Attempt send email")
#             smtpObj.sendmail(sender, receiver, message.as_string())
#         except Exception as mess:
#             print ("Error on send email: " + str(mess))
#         print ("Close instance")
#         smtpObj.quit()
# 
#         print ("\r\nEmail with results successfully sent")
#     except Exception as mess:
#         print ("Error: unable to send email %s") % str(mess)


def kill_chromedriver():
    for proc in psutil.process_iter():
        name = str(proc.name).encode('ascii', 'ignore')
        if name.__contains__('chromedriver'):
            proc.kill()

# class SINGLESCRIPT:
#     """ Limits number of running scripts to single instance """
# 
#     def __init__(self):
#         self.mutexname = "scriptmutex_{D0E858DF-985E-4907-B7FB-8D732C3FC3B9}"
#         self.mutex = CreateMutex(None, False, self.mutexname)
#         self.lasterror = GetLastError()
# 
#     def alreadyrunning(self):
#         return (self.lasterror == ERROR_ALREADY_EXISTS)
# 
#     def __del__(self):
#         if self.mutex:
#             CloseHandle(self.mutex)

class ACCOUNT:
    def __init__(self, username, password, path):
        self.username = username
        self.password = password
        self.driver = None
        self.path = path

    def login(self):
        for i in range(3):
            try:
                self.driver = DRIVER()
                if self.driver:
                    break
            except Exception as mess:
                print (mess)
                time.sleep(1)
            i += 1
        if not self.driver:
            self.driver.implicitly_wait(30)

        # Navigate to initial web page
        base_url = self.path
        self.driver.get(base_url)
        self.driver.maximize_window()

#         # Verify that only single instance script is running
#         try:
#             checksingle = SINGLESCRIPT()
#             if checksingle.alreadyrunning():
#                 print ("Script already running, quit this instance")
#                 self.quit()
#                 kill_chromedriver()
#                 exit(0)
#         except Exception as mess:
#             print (">>> Exception: %s" % str(mess))

        # Find menu
        print ("Find menu Just4U on page")
        try:
            signin = self.driver.findbyid("Offers-Landing-IMG_img_link_2")
            if signin:
                self.driver.myclick(signin)
                sleep(2)
            else:
                print ("Can't find menu Just4U")
        except Exception as mess:
            print (">>> Exception: %s" % str(mess))
            
        print ("Find Sign In on page")
        try:
            signin1 = self.driver.findbyid("globalui_signin_text2")
            if signin:
                self.driver.myclick(signin1)
                sleep(2)
            else:
                print ("Can't find menu Sign In")
        except Exception as mess:
            print (">>> Exception: %s" % str(mess))            

        # Clear username box and enter new
        try:
            print ("Find userid input")
            inputelement = self.driver.findbyid("input-email")
            if inputelement.is_displayed() and inputelement.is_enabled():
                self.driver.mysendtext(inputelement, self.username)
                sleep(2)
        except Exception as mess:
            print (">>> Exception: %s" % str(mess))

        # Clear password box and enter new
        try:
            print ("Find password input")
            inputelement = self.driver.findbyid("password-password")
            if inputelement.is_displayed() and inputelement.is_enabled():
                self.driver.mysendtext(inputelement, self.password)
                sleep(1)
                self.driver.mysendkey(inputelement, Keys.ENTER)
                sleep(2)
        except Exception as mess:
            print (">>> Exception: %s" % str(mess))

        # Check if change store dialog up, dismiss it
        sayno = self.driver.findbyid("ssAdvancedDialogLeftButton")
        if sayno:
            self.driver.myclick(sayno)

        # Find menu
        print ("Find menu Just4U on page")
      
        sleep(5)
        #scroll to bottom page to make all add visible
        get_height = self.driver.execute_script("return document.body.scrollHeight")
        get_screen_size = self.driver.get_window_size()
        screen_y = get_screen_size["height"]
        current_y = 0
        current_offers = self.driver.findbyid("headerMyListCount")
#         logger.info("Current offers on Safeway card currently = {0}".format(current_offers.text))
        
        #TODO: add good logic here ==========
        offers_found = self.driver.findspanclassaddclick("Add")
        if len(offers_found) > 0:
            self.driver.findspanclassaddclick("Add")
            cmd = "window.scrollTo(0, {0});".format(current_y + screen_y*2)
            self.driver.execute_script(cmd)
            current_y = self.driver.execute_script("return window.pageYOffset;")
            while len(self.driver.findspanclassaddclick("Add")) != 0:
                self.driver.findspanclassaddclick("Add")
                cmd = "window.scrollTo(0, {0});".format(current_y + screen_y*2)
                self.driver.execute_script(cmd)
                current_y = self.driver.execute_script("return window.pageYOffset;")
                get_height = self.driver.execute_script("return document.body.scrollHeight")
                if current_y > get_height - get_screen_size["height"] < get_height:
                    break                
        else:          
            while len(self.driver.findspanclassaddclick("Add")) == 0:
                if  len(self.driver.findspanclassaddclick("Add")) != 0:
                    sleep(3)
                    self.driver.findspanclassaddclick("Add")
                    cmd = "window.scrollTo(0, {0});".format(current_y + screen_y*2)
                    self.driver.execute_script(cmd)
                else:
                    cmd = "window.scrollTo(0, {0});".format(current_y + screen_y*2)
                    self.driver.execute_script(cmd)
                    sleep(3)
                    self.driver.findspanclassaddclick("Add")
                    current_y = self.driver.execute_script("return window.pageYOffset;")
                    get_height = self.driver.execute_script("return document.body.scrollHeight")
                    if current_y > get_height - get_screen_size["height"] < get_height:
                        break

        getoffers = self.driver.findbyid("headerMyListCount")
        if len(getoffers.text) != 0:
#             logger.info("Total offers on Safeway card currently = %s" % str(getoffers.text))
            print ("Total offers on Safeway card currently = %s" % str(getoffers.text))
            
#         logger.info("Added {0} offers".format(int(getoffers.text) - int(current_offers.text)))

        getgasrewards = self.driver.find_element_by_id("headerRewardsAvailable")
        if len(getgasrewards.text) != "0":
#             logger.info("Total Gas Rewards on Safeway card available = %s" % str(getgasrewards.text))
            print ("Total Gas Rewards on Safeway card available = %s" % str(getgasrewards.text))
        else:
#             logger.info("Total Gas Rewards on Safeway card available = %s" % str(getgasrewards.text))
            print ("Total Gas Rewards on Safeway card available = %s" % str(getgasrewards.text))
        return self.driver

    def quit(self):
        try:
            self.driver.quit()
            self = None
        except Exception as mess:
            print (">>> Exception: %s" % str(mess))

class DRIVER(webdriver.Chrome):
    def __init__(self):
        """ initialize with Chrome options(arguments):
        --start-maximized
        --no-sandbox
        disable-infobars
        disable-web-security
        password_manager_enabled: False
        """
        chrome_options = Options()
        # disable infobar popup for clean screenshot
        chrome_options.add_argument("disable-infobars")
        # chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument("disable-web-security")
        # docker do not allow run Chrome sandbox, disable it
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        
        webdriver.Chrome.__init__(self, chrome_options = chrome_options)
        pass

    def findbyid(self, idname, waittime = 60):
        # Find element by ID
        print("*** Function findbyid started. id = %s" % str(idname))
        try:
            wait = WebDriverWait(self, waittime)
            element = wait.until(EC.element_to_be_clickable((selenium.webdriver.common.by.By.ID, idname)))
            if element:
                print ("*** Element " + str(idname) + " is found. Return Element")
                return element
            else:
                print ("*** Element " + str(idname) + " is NOT found. Return None")
                return False

        except Exception as mess:
            print (">>> Exception: %s" % str(mess))
            return False

    def mysendtext(self, element, text):
        # Send text to element
        print ("*** Function mysendtext started.")
        try:
            element.clear()
            element.send_keys(text)
        except Exception as mess:
            print (">>> Exception: %s" % str(mess))

    def myclick(self, element):
        # Click element
        print ("*** Function myclick started.")
        try:
            element.click()
        except Exception as mess:
            print (">>> Exception: %s" % str(mess))

    def mysendkey(self, element, key):
        # Send KEY to element
        print ("*** Function mysendkey started")
        try:
            element.send_keys(key)
        except Exception as mess:
            print (">>> Exception: %s" % str(mess))

    def findlinkclick(self, link):
        # Find link and tries to click it
        print ("Function findlinkclick started")
        try:
            wait = WebDriverWait(self, 10)
            linklink = wait.until(EC.element_to_be_clickable(DRIVER.find_element_by_partial_link_text(link)))
            if linklink.is_displayed() and linklink.is_enabled():
                linklink.click()
                return True
        except Exception as mess:
            print (">>> Exception: %s" % str(mess))

    def findlinksbyhref(self, name):
        # Find link by HREF attribute and click it
        print ("*** Function findlinksbyhref started, href = %s" % str(name))
        try:
            alllink = self.find_elements_by_tag_name('a')
            i = 0
            while i < len(alllink):
                try:
                    if str(alllink[i].get_attribute('href')).find(name) == name:
                        print (alllink[i].get_attribute('href'))
                        return alllink[i]
                except:
                    pass
                i += 1

        except Exception as mess:
            print (">>> Exception: %s" % str(mess))
            return False

    def findlinkbyimg(self, name):
        # Find link by image attribute and click it
        print ("*** Function findlinkbyimg started link image = %s" % str(name))
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

        except Exception as mess:
            print (">>> Exception: %s" % str(mess))
            return False

    def findlinksbytext(self, text):
        # Find link by text attribute and click it
        print ("*** Function findlinksbytext started, link text = %s" % str(text))
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

        except Exception as mess:
            print (">>> Exception: %s" % str(mess))
            return False

    def findlinksbyclass(self, name):
        # Find link by class name and click it
        print ("*** Function findlinksbyclass started, class name = %s" % str(name))
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

        except Exception as mess:
            print (">>> Exception: %s" % str(mess))
            return False

    def findspanclassaddclick(self, txt):
        # Find button by span text and click it
        print ("*** Function findspanclassaddclick started")
        try:
            allSpans = self.find_elements_by_class_name('lt-add-offer-gallery')
            total = []
            i = 0
            while i < len(allSpans):
                try:
                    if allSpans[i].text == txt:#and allSpans[i].is_displayed() and allSpans[i].is_enabled():
                        allSpans[i].click()
                        total.append(allSpans[i])
                        sleep(1)
                except:
                    pass
                i += 1
            time.sleep(1)
            return total

        except Exception as mess:
            print (">>> Exception: %s" % str(mess))

    def findselectbyid(self, name):
        # Find select attribute by ID and click it
        print ("*** Function findselectbyid started")
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

        except Exception as mess:
            print (">>> Exception: %s" % str(mess))
        return True

def safeway_login():
    """
    Login User
    """
    username = (params()[0])
    password = (params()[1])
    pathlink = (params()[2])
    emailps = (params()[3])

    try:
        userlogin = ACCOUNT(username, password, pathlink)
        if userlogin:
            print ("We login to: " + pathlink)
            result = userlogin.login()
            if result:
                print ("\r\nAdding coupons to Safeway Card was successful")
                result.close()

            # open log file for reading , read, email  result with statistics
            if emailps:
                log_name = glob.glob("Just4you*.log")
                filepath = os.getcwd() + "\\" + str(log_name[0])
                msg = open(filepath, "r")
                content = msg.read()
                msg.close()
                email_results(content)

        else:
            print ("Login to Safeway failed:")

    except Exception as mess:
        print (">>> Exception: %s" % str(mess))
        

cleanup_log()
safeway_login()
