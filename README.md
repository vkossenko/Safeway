# Safeway

  Auto add Just4U offers to safeway card.
Main idea to use it - create rule in Outlook and on arriving email from Safeway this script will verify 
if there any new offers available, add them to account, mark email as read, move to specified folder.
  Make life easier if long time did not log in to Just4U account. Sometimes there hundreds offers and 
manually clicking is boring... Web browser Chrome.

Sample for bat file to execute in rule:

  start /B pythonw your_file_location\SafewayJust4u.py -lg "your_email" -ps "your_password"

In case of using executable:

  your_file_location\SafewayJust4u.exe -lg "your_email" -ps "your_password"
