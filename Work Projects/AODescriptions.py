# Anthony D'Alessandro | EDS
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import UnexpectedAlertPresentException
from pynput.keyboard import Controller
from pynput.keyboard import Key

driver = webdriver.Firefox()
kb = Controller()


def login(username, password, volume):
    driver.set_context('chrome')
    # JavaScript for changing 'security.tls.version.min' = 1
    script = (
        "var prefs = Components.classes['@mozilla.org/preferences-service;1'].getService(Components.interfaces.nsIPrefBranch);"
        "prefs.setIntPref('security.tls.version.min', 1);")
    # Execute JavaScript to change FireFox TLS setting
    driver.execute_script(script, 1)
    driver.set_context('content')

    # Connect to TIL
    driver.get('https://10.222.224.135/')
    driver.maximize_window()

    # Click 'Accept Agreement'
    driver.find_element(by=By.XPATH,
                        value='/html/body/table/tbody/tr[7]/td[2]/table/tbody/tr/td[1]/form/input[2]').click()

    # Login
    driver.find_element(by=By.XPATH, value='/html/body/form/table/tbody/tr[2]/td[2]/input[5]').send_keys(username)
    driver.find_element(by=By.XPATH, value='/html/body/form/table/tbody/tr[2]/td[2]/input[6]').send_keys(password)
    driver.find_element(by=By.XPATH, value='/html/body/form/table/tbody/tr[2]/td[2]/input[7]').click()

    # Try calling the navigateQA method
    try:
        navigateVolume(volume)
    # If the UnexpectedAlertPresentException is encountered, alert the user that their login information was incorrect
    except UnexpectedAlertPresentException as ex:
        print("\nIncorrect Username or Password!\nRe-Enter Username and Password\n")
        # Take new username as input
        newUsername = input("Enter TIL Username: ")
        # Take new password as input
        newPassword = input("Enter TIL Password: ")
        # Call login method with new credentials
        login(newUsername, newPassword, volume)


def navigateVolume(volume):
    # Click TIL
    driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[1]/td[1]/form/input[1]').click()

    # Select Volumes Dropdown --> EDS
    driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[1]/td/table/tbody/tr/td[4]/select/option[4]').click()

    # Get list of option elements from Volumes Dropdown
    options = driver.find_elements(by=By.TAG_NAME, value='option')
    # Cast max Volume value to integer
    maxValue = int(options[0].get_attribute("value"))
    # Cast min Volume value to integer
    minValue = int(options[len(options) - 1].get_attribute("value"))
    # Declare boolean to control while loop
    flag = False
    while not flag:
        # Check if the user-provided Volume number is less than the min or larger than the max
        if (int(volume) < minValue or int(volume) > maxValue):
            # If so, alert user that the Volume number is invalid and take a new value as input
            print("\nInvalid Volume Number\nPlease enter a valid Volume")
            volume = input("Enter EDS Volume Number: ")
        else:
            # If the Volume value is valid, set the boolean value to True so the while loop does not continue
            flag = True

    # Select EDS Volume
    select = Select(driver.find_element(by=By.XPATH, value='/html/body/form/table[1]/tbody/tr[2]/td[2]/select'))
    select.select_by_value(str(volume))


def inputAODescriptions(filePath):
    bags = {}
    with open(filePath, newline='') as csvFile:
        reader = csv.reader(csvFile)
        data = list(reader)
    # Turn CSV data into dictionary where each key corresponds with the respective 'ECTM' number
    for element in data:
        bags[element[0]] = element

    table = driver.find_element(by=By.XPATH, value='/html/body/form/table[2]/tbody/tr[3]/td[3]/table')
    # Get first 'ECTM' HTML row element
    firstElementRow = driver.find_element(by=By.XPATH, value='/html/body/form/table[2]/tbody/tr[3]/td[3]/table/tbody/tr[4]').find_elements(by=By.TAG_NAME, value='td')
    # Get first 'ECTM' number
    firstElement = firstElementRow[1].text
    # Get last 'ECTM' HTML row element
    lastElementRow = driver.find_element(by=By.XPATH,value='/html/body/form/table[2]/tbody/tr[3]/td[3]/table/tbody/tr[last()]').find_elements(by=By.TAG_NAME, value='td')
    # Get last 'ECTM' number
    lastElement = lastElementRow[1].text
    # Remove 'ECTM' from first and last bag names leaving just the numbers
    firstNum = int(firstElement.replace('ECTM', ''))
    lastNum = int(lastElement.replace('ECTM', ''))
    volumeRange = lastNum - firstNum

    for i in range(volumeRange):
        # Store current 'ECTM' element
        currentElement = driver.find_element(by=By.XPATH, value='/html/body/form/table[2]/tbody/tr[3]/td[3]/table/tbody/tr[' + str(4 + i) + ']/td[2]/a')
        # Store current 'ECTM' value
        currentBag = currentElement.text
        # Click current 'ECTM' element
        currentElement.click()
        # Click "Edit" button
        driver.find_element(by=By.XPATH, value='/html/body/table[1]/tbody/tr[2]/td[2]/form/input[1]').click()
        # Store description of current bag from CSV
        currentDescription = bags[currentBag][2]
        # Clear Long Description text box
        driver.find_element(by=By.XPATH,
                            value='/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[10]/td/textarea').clear()
        # Enter description of current bag AO into Long Description text box
        driver.find_element(by=By.XPATH,
                            value='/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[10]/td/textarea').send_keys(
            currentDescription)
        # Click save
        driver.find_element(by=By.XPATH, value='/html/body/table[1]/tbody/tr[2]/td[2]/form/input[2]').click()
        # Press enter
        kb.press(Key.enter)
        # Click "EATM" link
        eatmLink = WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[6]/td[2]/a')))
        eatmLink.click()
        # Click "Edit" button
        driver.find_element(by=By.XPATH, value='/html/body/table[1]/tbody/tr[2]/td[2]/form/input[1]').click()
        # Clear Long Description text box
        driver.find_element(by=By.XPATH,
                            value='/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[7]/td/textarea').clear()
        # Enter description of current bag AO into Long Description text box
        driver.find_element(by=By.XPATH,
                            value='/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[7]/td/textarea').send_keys(
            currentDescription)
        if bags[currentBag][3] != "":
            # Make sure Non-Threat Description text box is cleared
            driver.find_element(by=By.XPATH,
                                value='/html/body/table[2]/tbody/tr[2]/td[3]/table/tbody/tr[12]/td/textarea').clear()
            # Store TMI/IDC Number of current bag from CSV
            currentThreat = bags[currentBag][3]
            # Clear Threat Description text box
            driver.find_element(by=By.XPATH,
                                value='/html/body/table[2]/tbody/tr[2]/td[3]/table/tbody/tr[7]/td/textarea').clear()
            # Enter description of current bag AO into Threat Description text box
            driver.find_element(by=By.XPATH,
                                value='/html/body/table[2]/tbody/tr[2]/td[3]/table/tbody/tr[7]/td/textarea').send_keys(
                currentDescription)
            # Clear Item ID text box
            driver.find_element(by=By.XPATH,
                                value='/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[2]/input').clear()
            # Enter TMI/IDC Number into Item ID text box
            driver.find_element(by=By.XPATH,
                                value='/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[2]/input').send_keys(
                currentThreat)
            # Click save
            driver.find_element(by=By.XPATH, value='/html/body/table[1]/tbody/tr[2]/td[2]/form/input[2]').click()
            # Press enter
            kb.press(Key.enter)

        else:
            # Make sure Threat Description text box is cleared
            driver.find_element(by=By.XPATH,
                                value='/html/body/table[2]/tbody/tr[2]/td[3]/table/tbody/tr[7]/td/textarea').clear()
            # Clear Non-Threat Description text box
            driver.find_element(by=By.XPATH,
                                value='/html/body/table[2]/tbody/tr[2]/td[3]/table/tbody/tr[12]/td/textarea').clear()
            # Enter description of current bag AO into Non-Threat Description text box
            driver.find_element(by=By.XPATH,
                                value='/html/body/table[2]/tbody/tr[2]/td[3]/table/tbody/tr[12]/td/textarea').send_keys(
                currentDescription)
            # Click save
            driver.find_element(by=By.XPATH, value='/html/body/table[1]/tbody/tr[2]/td[2]/form/input[2]').click()
            # Press enter
            kb.press(Key.enter)

        try:
            # Click back
            backLink = WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, '/html/body/table[1]/tbody/tr[2]/td[2]/form/input[6]')))
            backLink.click()
        except UnexpectedAlertPresentException as ex:
            print("Invalid threat number!")
            # Press enter
            kb.press(Key.enter)
            # Click save
            driver.find_element(by=By.XPATH, value='/html/body/table[1]/tbody/tr[2]/td[2]/form/input[2]').click()
            # Press enter
            kb.press(Key.enter)
            # Click back
            backLink = WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, '/html/body/table[1]/tbody/tr[2]/td[2]/form/input[6]')))
            backLink.click()

        # C:\Users\TSA\Desktop\144Test.csv
        # "C:\Users\TSA\Desktop\144Test.csv"


def main():
    username = input("Please enter TIL Username: ")
    password = input("Please enter TIL Password: ")
    volume = input("Please enter Volume Number: ")
    login(username, password, volume)

    csvPath = input("Enter file path for CSV File: ")
    csvPath = csvPath.replace('"', "")
    inputAODescriptions(csvPath)


if __name__ == '__main__':
    main()
