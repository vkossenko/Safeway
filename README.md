# Safeway

  Auto add Just4U offers to safeway card.
Main idea to use it - create rule in Outlook and on arriving email from Safeway this script will verify 
if there any new offers available, add them to account, mark email as read, move to specified folder.
  Make life easier if long time did not log in to Just4U account. Sometimes there hundreds offers and 
manually clicking is boring...As a result of script execution you will get an email with statistics about added/total offers from different category. Web browser Chrome. You may need download chromedriver.exe in order to run this script and add path to chromedriver.exe to your system path variable. Download latest from here:
  https://sites.google.com/a/chromium.org/chromedriver/downloads

Sample for bat file to execute in rule:

  start /B pythonw your_file_location\SafewayJust4u.py -lg "your_email" -ps "your_password" -emailps "your email_account password"

In case of using executable:

  your_file_location\SafewayJust4u.exe -lg "your_email" -ps "your_password" -emailps "your email_account password"
