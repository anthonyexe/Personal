# Anthony D'Alessandro | EDS
import os
import time
import cv2
import csv
import pytesseract
import pygetwindow
from pynput.keyboard import Controller
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException

driver = webdriver.Firefox()
action = ActionChains(driver)
# Keyboard controller
kb = Controller()
# Create global empty string to hold volume
volume = ''
# Create dictionary to hold lists of any missing images for each machine that corresponds to ECTM numbers
missingImages = {}
# Create list of bags
bags = []
# Pytesseract config
custom_config = r'--oem 3 --psm 6'
# Pytesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\TSA\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def createFolders(volume):
    # Declare list of machine names
    machines = ['', 'CT80', '9400', '9800', '6700', 'Analogic', 'CTiX']
    for machine in machines:
        # Use empty string to identify first value and check if the Volume folder exists yet
        if machine == '' and not os.path.exists('C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume ' + volume):
            # If the Volume folder does not exist yet, create it
            os.makedirs(r'C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume ' + volume)
        # Check if the subsequent machine folders exist inside the volume folder yet
        elif not os.path.exists('C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume ' + volume + '\\' + machine):
            # If any of the machine folders do not exist yet, create them
            os.makedirs(r'C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume ' + volume + '\\' + machine)


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
        navigateQA(volume)
    # If the UnexpectedAlertPresentException is encountered, alert the user that their login information was incorrect
    except UnexpectedAlertPresentException as ex:
        print("\nIncorrect Username or Password!\nRe-Enter Username and Password\n")
        # Take new username as input
        newUsername = input("Enter TIL Username: ")
        # Take new password as input
        newPassword = input("Enter TIL Password: ")
        # Call login method with new credentials
        login(newUsername, newPassword, volume)

def navigateQA(volume):
    # Click TIL
    driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[1]/td[1]/form/input[1]').click()

    # Click QA Dropdown --> EDS
    driver.find_element(by=By.XPATH,
                        value='/html/body/table/tbody/tr[1]/td/table/tbody/tr/td[5]/select/option[6]').click()

    # Click CAI QA
    driver.find_element(by=By.XPATH, value='/html/body/table[1]/tbody/tr[2]/td[2]/input[3]').click()
    # Get list of option elements from CAI QA Dropdown
    options = driver.find_elements(by=By.TAG_NAME, value='option')
    # Cast max Volume value to integer
    maxValue = int(options[0].get_attribute("value"))
    # Cast min Volume value to integer
    minValue = int(options[len(options) - 1].get_attribute("value"))
    # Declare boolean to control while loop
    flag = False
    while not flag:
        # Check if the user-provided Volume number is less than the min or larger than the max
        if(int(volume) < minValue or int(volume) > maxValue):
            # If so, alert user that the Volume number is invalid and take a new value as input
            print("\nInvalid Volume Number\nPlease enter a valid Volume")
            volume = input("Enter EDS Volume Number: ")
        else:
            # If the Volume value is valid, set the boolean value to True so the while loop does not continue
            flag = True

    # Select EDS Volume
    select = Select(driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[1]/td[2]/form/b/b/select'))
    select.select_by_value(str(volume))

    # Set active window to TIL (Firefox)
    # pygetwindow.getWindowsWithTitle('QA EDS Deliverable — Mozilla Firefox')[0]


def returnData(dataFunction, value):
    if value != "":
        value = dataFunction(value)
    else:
        value = 0

    return value


def ct80MachineData():
    ct80BagCategory = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[8]/td[1]/table/tbody/tr[3]/td[2]').text
    ct80CTValue = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[8]/td[1]/table/tbody/tr[5]/td[2]').text
    ct80CTValue = returnData(float, ct80CTValue)
    ct80ZValue = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[8]/td[1]/table/tbody/tr[6]/td[2]').text
    ct80ZValue = returnData(float, ct80ZValue)
    ct80Mass = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[8]/td[1]/table/tbody/tr[7]/td[2]').text
    ct80Mass = returnData(float, ct80Mass)
    ct80Density = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[8]/td[1]/table/tbody/tr[8]/td[2]').text
    ct80Density = returnData(float, ct80Density)
    ct80Alarms = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[8]/td[1]/table/tbody/tr[9]/td[2]').text
    ct80Alarms = returnData(int, ct80Alarms)
    ct80Ancillary = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[8]/td[1]/table/tbody/tr[11]/td[2]').text
    ct80Ancillary = returnData(int, ct80Ancillary)
    ct80File = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[8]/td[1]/table/tbody/tr[12]/td[2]').text
    ct80File = returnData(int, ct80File)
    ct80Data = [ct80BagCategory, ct80CTValue, ct80ZValue, ct80Mass, ct80Density, ct80Alarms + ct80Ancillary, ct80File]

    return ct80Data


def _9400MachineData():
    _9400BagCategory = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[16]/td[1]/table/tbody/tr[3]/td[2]').text
    _9400CTValue = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[16]/td[1]/table/tbody/tr[5]/td[2]').text
    _9400CTValue = returnData(int, _9400CTValue)
    _9400Mass = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[16]/td[1]/table/tbody/tr[6]/td[2]').text
    _9400Mass = returnData(int, _9400Mass)
    _9400Density = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[16]/td[1]/table/tbody/tr[7]/td[2]').text
    _9400Density = returnData(float, _9400Density)
    _9400Alarms = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[16]/td[1]/table/tbody/tr[8]/td[2]').text
    _9400Alarms = returnData(int, _9400Alarms)
    _9400Ancillary = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[16]/td[1]/table/tbody/tr[10]/td[2]').text
    _9400Ancillary = returnData(int, _9400Ancillary)
    _9400File = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[16]/td[1]/table/tbody/tr[11]/td[2]').text
    _9400File = returnData(int, _9400File)
    _9400Data = [_9400BagCategory, _9400CTValue, _9400Mass, _9400Density, _9400Alarms + _9400Ancillary, _9400File]

    return _9400Data


def _9800MachineData():
    _9800BagCategory = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[21]/td[1]/table/tbody/tr[3]/td[2]').text
    _9800CTValue = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[21]/td[1]/table/tbody/tr[5]/td[2]').text
    _9800CTValue = returnData(int, _9800CTValue)
    _9800Mass = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[21]/td[1]/table/tbody/tr[6]/td[2]').text
    _9800Mass = returnData(int, _9800Mass)
    _9800Density = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[21]/td[1]/table/tbody/tr[7]/td[2]').text
    _9800Density = returnData(float, _9800Density)
    _9800Alarms = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[21]/td[1]/table/tbody/tr[8]/td[2]').text
    _9800Alarms = returnData(int, _9800Alarms)
    _9800Ancillary = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[21]/td[1]/table/tbody/tr[10]/td[2]').text
    _9800Ancillary = returnData(int, _9800Ancillary)
    _9800File = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[21]/td[1]/table/tbody/tr[11]/td[2]').text
    _9800File = returnData(int, _9800File)
    _9800Data = [_9800BagCategory, _9800CTValue, _9800Mass, _9800Density, _9800Alarms + _9800Ancillary, _9800File]

    return _9800Data

def _6700MachineData():
    _6700BagCategory = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[26]/td[1]/table/tbody/tr[3]/td[2]').text
    _6700CTValue = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[26]/td[1]/table/tbody/tr[5]/td[2]').text
    _6700CTValue = returnData(float, _6700CTValue)
    _6700Mass = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[26]/td[1]/table/tbody/tr[6]/td[2]').text
    _6700Mass = returnData(float, _6700Mass)
    _6700Alarms = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[26]/td[1]/table/tbody/tr[7]/td[2]').text
    _6700Alarms = returnData(int, _6700Alarms)
    _6700Ancillary = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[26]/td[1]/table/tbody/tr[9]/td[2]').text
    _6700Ancillary = returnData(int, _6700Ancillary)
    _6700File = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[26]/td[1]/table/tbody/tr[10]/td[2]').text
    _6700File = returnData(int, _6700File)
    _6700Data = [_6700BagCategory, _6700CTValue, _6700Mass, _6700Alarms + _6700Ancillary, _6700File]

    return _6700Data


def analogicMachineData():
    analogicFile = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[31]/td[1]/table/tbody/tr[11]/td[2]').text
    analogicFile = returnData(int, analogicFile)
    analogicData = [analogicFile]

    return analogicData


def CTiXMachineData():
    CTiXAlarms = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[36]/td[1]/table/tbody/tr[8]/td[2]').text
    CTiXAlarms = returnData(int, CTiXAlarms)
    CTiXAncillary = driver.find_element(by=By.XPATH, value='/html/body/table[4]/tbody/tr[36]/td[1]/table/tbody/tr[10]/td[2]').text
    CTiXAncillary = returnData(int, CTiXAncillary)
    CTiXData = [CTiXAlarms + CTiXAncillary]

    return CTiXData


def extractScreenshots(element, currentBag, machine):
    # Store window handles
    window = driver.window_handles
    # Store HTML element of machine image
    htmlElement = driver.find_element(by=By.XPATH, value=element)
    # Scroll to machine image
    driver.execute_script("arguments[0].scrollIntoView();", htmlElement)
    # Right click on machine image
    action.context_click(driver.find_element(by=By.XPATH, value=element)).perform()
    # Press 'i' to open image in new tab
    kb.press('i')
    # Store window handles
    windows = driver.window_handles
    # Switch to new tab
    driver.switch_to.window(windows[1])
    # File path for current volume, machine, and bag
    path = "C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume " + volume + "\\" + machine + "\\" + currentBag + ".png"
    try:
        # Retrieve image element using
        img = WebDriverWait(driver, 2).until(
            expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/img")))
        # Pause program for 1 second to allow webpage to fully load image
        time.sleep(1)
        # Take screenshot and save it to proper path
        img.screenshot(path)
    except TimeoutException as ex:
        print("\n" + currentBag + " screenshot for " + machine + " missing")
        print("TimeoutException has been thrown")
        # If missingImages dictionary does not already contain currentBag as a key, add currentBag and corresponding
        # machine as the key and list respectively
        if currentBag not in missingImages.keys():
            missingImages[currentBag] = [machine]
        else:
            # If missingImages does contain currentBag as a key, append current machine to existing list
            missingImages[currentBag].append(machine)

    finally:
        # Close current window
        driver.close()
    # Switch back to main window before continuing
    driver.switch_to.window(window[0])


def extractAll():
    # Create dictionary of dictionaries to hold machine data where keys of outer dictionary correspond to ECTM numbers
    machineData = defaultdict(dict)
    # Create table element of all ECTMs
    table = driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[2]/td[2]/table')
    # Counter for loop control
    count = 0
    # Loop through table
    for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
        # Skip first 4 rows
        if count == 4:
            # Store current row (5th row) of website table
            currentRow = row.find_elements(by=By.TAG_NAME, value='td')
            # Click link to first ECTM in the Volume
            currentRow[0].click()
            # Store current ECTM
            currentBag = driver.find_element(by=By.XPATH, value='/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]/b/a').text
            # Add current bag to list of bags
            bags.append(currentBag)

            # Call ct80MachineData method to extract & store machine data
            ct80Data = ct80MachineData()
            # Add ct80MachineData to dictionary of all machine data
            machineData[currentBag]["CT80"] = ct80Data
            ct80Element = '/html/body/table[4]/tbody/tr[10]/td[2]/img'
            extractScreenshots(ct80Element, currentBag, 'CT80')

            _9400Data = _9400MachineData()
            machineData[currentBag]["9400"] = _9400Data
            _9400Element = '/html/body/table[4]/tbody/tr[18]/td/img'
            extractScreenshots(_9400Element, currentBag, '9400')

            _9800Data = _9800MachineData()
            machineData[currentBag]["9800"] = _9800Data
            _9800Element = '/html/body/table[4]/tbody/tr[23]/td/img'
            extractScreenshots(_9800Element, currentBag, '9800')

            _6700Data = _6700MachineData()
            machineData[currentBag]["6700"] = _6700Data
            _6700Element = '/html/body/table[4]/tbody/tr[28]/td/img'
            extractScreenshots(_6700Element, currentBag, '6700')

            analogicData = analogicMachineData()
            machineData[currentBag]["Analogic"] = analogicData
            analogicElement = '/html/body/table[4]/tbody/tr[33]/td/img'
            extractScreenshots(analogicElement, currentBag, 'Analogic')

            CTiXData = CTiXMachineData()
            machineData[currentBag]["CTiX"] = CTiXData
            CTiXElement = '/html/body/table[4]/tbody/tr[38]/td/img'
            extractScreenshots(CTiXElement, currentBag, 'CTiX')

        if count > 4:
            # Click next QA CAI
            driver.find_element(by=By.XPATH, value='/html/body/table[1]/tbody/tr[2]/td/form/input[2]').click()
            # Store current ECTM
            currentBag = driver.find_element(by=By.XPATH, value='/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]/b/a').text
            # Add current bag to list of bags
            bags.append(currentBag)

            # Call ct80MachineData method to store extract & store machine data
            ct80Data = ct80MachineData()
            # Add ct80MachineData to dictionary of all machine data
            machineData[currentBag]["CT80"] = ct80Data
            ct80Element = '/html/body/table[4]/tbody/tr[10]/td[2]/img'
            extractScreenshots(ct80Element, currentBag, 'CT80')

            _9400Data = _9400MachineData()
            machineData[currentBag]["9400"] = _9400Data
            _9400Element = '/html/body/table[4]/tbody/tr[18]/td/img'
            extractScreenshots(_9400Element, currentBag, '9400')

            _9800Data = _9800MachineData()
            machineData[currentBag]["9800"] = _9800Data
            _9800Element = '/html/body/table[4]/tbody/tr[23]/td/img'
            extractScreenshots(_9800Element, currentBag, '9800')

            _6700Data = _6700MachineData()
            machineData[currentBag]["6700"] = _6700Data
            _6700Element = '/html/body/table[4]/tbody/tr[28]/td/img'
            extractScreenshots(_6700Element, currentBag, '6700')

            analogicData = analogicMachineData()
            machineData[currentBag]["Analogic"] = analogicData
            analogicElement = '/html/body/table[4]/tbody/tr[33]/td/img'
            extractScreenshots(analogicElement, currentBag, 'Analogic')

            CTiXData = CTiXMachineData()
            machineData[currentBag]["CTiX"] = CTiXData
            CTiXElement = '/html/body/table[4]/tbody/tr[38]/td/img'
            extractScreenshots(CTiXElement, currentBag, 'CTiX')

        count += 1

    return machineData


def extractMachine():
    # Create dictionary of dictionaries to hold machine data where keys of outer dictionary correspond to ECTM numbers
    machineData = defaultdict(dict)
    # Create table element of all ECTMs
    table = driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[2]/td[2]/table')
    # Counter for loop control
    count = 0
    # Loop through table
    for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
        # Skip first 4 rows
        if count == 4:
            # Store current row (5th row) of website table
            currentRow = row.find_elements(by=By.TAG_NAME, value='td')
            # Click link to first ECTM in the Volume
            currentRow[0].click()
            # Store current ECTM
            currentBag = driver.find_element(by=By.XPATH,
                                             value='/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]/b/a').text
            # Add current bag to list of bags
            bags.append(currentBag)

            # Call ct80MachineData method to extract & store machine data
            ct80Data = ct80MachineData()
            # Add ct80MachineData to dictionary of all machine data
            machineData[currentBag]["CT80"] = ct80Data
            # ct80Element = '/html/body/table[4]/tbody/tr[10]/td[2]/img'
            # extractScreenshots(ct80Element, currentBag, 'CT80')

            _9400Data = _9400MachineData()
            machineData[currentBag]["9400"] = _9400Data
            # _9400Element = '/html/body/table[4]/tbody/tr[18]/td/img'
            # extractScreenshots(_9400Element, currentBag, '9400')

            _9800Data = _9800MachineData()
            machineData[currentBag]["9800"] = _9800Data
            # _9800Element = '/html/body/table[4]/tbody/tr[23]/td/img'
            # extractScreenshots(_9800Element, currentBag, '9800')

            _6700Data = _6700MachineData()
            machineData[currentBag]["6700"] = _6700Data
            # _6700Element = '/html/body/table[4]/tbody/tr[28]/td/img'
            # extractScreenshots(_6700Element, currentBag, '6700')

            analogicData = analogicMachineData()
            machineData[currentBag]["Analogic"] = analogicData
            # analogicElement = '/html/body/table[4]/tbody/tr[33]/td/img'
            # extractScreenshots(analogicElement, currentBag, 'Analogic')

            CTiXData = CTiXMachineData()
            machineData[currentBag]["CTiX"] = CTiXData
            # CTiXElement = '/html/body/table[4]/tbody/tr[38]/td/img'
            # extractScreenshots(CTiXElement, currentBag, 'CTiX')

        if count > 4:
            # Click next QA CAI
            driver.find_element(by=By.XPATH, value='/html/body/table[1]/tbody/tr[2]/td/form/input[2]').click()
            # Store current ECTM
            currentBag = driver.find_element(by=By.XPATH,
                                             value='/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]/b/a').text
            # Add current bag to list of bags
            bags.append(currentBag)

            # Call ct80MachineData method to store extract & store machine data
            ct80Data = ct80MachineData()
            # Add ct80MachineData to dictionary of all machine data
            machineData[currentBag]["CT80"] = ct80Data
            # ct80Element = '/html/body/table[4]/tbody/tr[10]/td[2]/img'
            # extractScreenshots(ct80Element, currentBag, 'CT80')

            _9400Data = _9400MachineData()
            machineData[currentBag]["9400"] = _9400Data
            # _9400Element = '/html/body/table[4]/tbody/tr[18]/td/img'
            # extractScreenshots(_9400Element, currentBag, '9400')

            _9800Data = _9800MachineData()
            machineData[currentBag]["9800"] = _9800Data
            # _9800Element = '/html/body/table[4]/tbody/tr[23]/td/img'
            # extractScreenshots(_9800Element, currentBag, '9800')

            _6700Data = _6700MachineData()
            machineData[currentBag]["6700"] = _6700Data
            # _6700Element = '/html/body/table[4]/tbody/tr[28]/td/img'
            # extractScreenshots(_6700Element, currentBag, '6700')

            analogicData = analogicMachineData()
            machineData[currentBag]["Analogic"] = analogicData
            # analogicElement = '/html/body/table[4]/tbody/tr[33]/td/img'
            # extractScreenshots(analogicElement, currentBag, 'Analogic')

            CTiXData = CTiXMachineData()
            machineData[currentBag]["CTiX"] = CTiXData
            # CTiXElement = '/html/body/table[4]/tbody/tr[38]/td/img'
            # extractScreenshots(CTiXElement, currentBag, 'CTiX')

        count += 1

    return machineData


def ct80OCR(imagePath):
    img = cv2.imread(imagePath)
    data = []

    cropped_image1 = img[90:110, 380:450]  # Bag category
    cropped_image2 = img[90:110, 900:952]  # CT Value
    cropped_image3 = img[90:110, 542:575]  # Z Value
    cropped_image4 = img[90:110, 650:700]  # Mass
    cropped_image5 = img[90:110, 797:825]  # Density
    cropped_image6 = img[90:108, 260:275]  # Threat count
    cropped_image7 = img[978:994, 1638:1694]  # File name

    images = [cropped_image1, cropped_image2, cropped_image3, cropped_image4, cropped_image5, cropped_image6,
              cropped_image7]

    for i in range(len(images)):
        currentImage = images[i]
        invertedResized = cv2.bitwise_not(cv2.resize(currentImage, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC))
        bw = cv2.threshold(invertedResized, 85, 255, cv2.THRESH_BINARY)[1]
        text = pytesseract.image_to_string(bw, config="--oem 3 --psm 6 -c tessedit_char_whitelist=.0123456789")
        if i == 0:
            categoryText = pytesseract.image_to_string(bw, config=custom_config)
            categoryText = categoryText.replace("\n", "")
            categoryText = categoryText.upper()
            data.append(categoryText)
        elif i == 2:
            invertedResized2 = cv2.bitwise_not(cv2.resize(currentImage, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC))
            bw2 = cv2.threshold(invertedResized2, 50, 255, cv2.THRESH_BINARY)[1]
            text = pytesseract.image_to_string(bw2, config="--oem 3 --psm 6 -c tessedit_char_whitelist=.0123456789")
            text = text.replace("|", "1").replace(" ", "").replace("\n", "").replace(".", "")
            text = text[0] + '.' + text[1:len(text)]
            # text = text.replace("|", "1").replace(" ", "").replace("\n", "")
            # if text[0] != '7' or text[1] != '.':
                # invertedResized2 = cv2.bitwise_not(cv2.resize(currentImage, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC))
                # bw2 = cv2.threshold(invertedResized2, 50, 255, cv2.THRESH_BINARY)[1]
                # text = pytesseract.image_to_string(bw2, config="--oem 3 --psm 6 -c tessedit_char_whitelist=.0123456789")
                # text = text.replace("|", "1").replace(" ", "").replace("\n", "").replace(".", "")
                # text = text[0] + '.' + text[1:len(text) - 1]

            data.append(float(text))
        elif i == 5 or i == 6:
            text = text.replace("|", "1").replace(" ", "")
            data.append(int(text))
        else:
            text = text.replace("|", "1").replace(" ", "").replace("\n", "")
            data.append(float(text))

    return data


def _9400OCR(imagePath):
    img = cv2.imread(imagePath)
    data = []

    cropped_image1 = img[402:420, 1075:1142]  # Bag category
    cropped_image2 = img[368:386, 1088:1133]  # CT Value
    cropped_image3 = img[436:451, 1081:1112]  # Mass
    cropped_image4 = img[470:485, 1075:1105]  # Density
    cropped_image5 = img[457:471, 875:896]  # Threat count
    cropped_image6 = img[522:537, 850:921]  # File name

    images = [cropped_image1, cropped_image2, cropped_image3, cropped_image4, cropped_image5, cropped_image6]

    for i in range(len(images)):
        # Store image at index 'i'
        currentImage = images[i]
        # Resize image using INTER_CUBIC interpolation (3x3)
        resized = cv2.resize(currentImage, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        # Change image to black and white with min threshold of 150
        bw = cv2.threshold(resized, 150, 255, cv2.THRESH_BINARY)[1]
        # Extract text/numeric values from image
        text = pytesseract.image_to_string(bw, config=custom_config)
        # i = 0 corresponds to Bag Category image
        if i == 0:
            # Remove any occurrences of '\n'
            text = text.replace("\n", "")
            text = text.upper()
            # Append text to data list
            data.append(text)
        # i = 3 corresponds with density value which is a float format; append to data list
        elif i == 3:
            # Pytesseract confuses '7' with '?' sometimes; this fixes that error
            text = text.replace("?", "7").replace("\n", "")
            data.append(float(text))
        # All other values of i have an integer format; append to data list
        else:
            # Pytesseract confuses '7' with '?' sometimes; this fixes that error
            text = text.replace("?", "7").replace("\n", "")
            data.append(int(text))

    return data


def _9800OCR(imagePath):
    img = cv2.imread(imagePath)
    data = []

    cropped_image1 = img[315:335, 1055:1145]  # Bag category
    cropped_image2 = img[389:406, 1065:1102]  # CT Value
    cropped_image3 = img[336:350, 1064:1097]  # LongMass
    cropped_image4 = img[355:371, 1064:1095]  # Density
    cropped_image5 = img[516:532, 889:902]  # Threat count
    cropped_image6 = img[752:764, 534:575]  # File name

    images = [cropped_image1, cropped_image2, cropped_image3, cropped_image4, cropped_image5, cropped_image6]

    for i in range(len(images)):
        # Store image at index 'i'
        currentImage = images[i]
        # Resize image using INTER_CUBIC interpolation (3x3)
        resized = cv2.resize(currentImage, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        # Change image to black and white with min threshold of 160
        bw = cv2.threshold(resized, 170, 255, cv2.THRESH_BINARY)[1]
        # Extract text/numeric values from image
        text = pytesseract.image_to_string(bw, config=custom_config)
        # i = 0 corresponds to Bag Category image
        if i == 0:
            text = text.replace("\n", "")
            text = text.upper()
            data.append(text)
            # i = 2 corresponds to Mass which is an int format; append to data list
        elif i == 2:
            if text == '':
                data.append(0)
            else:
                text = text.replace(" ", "").replace("\n", "")
                print(text + "!")
                nonChar = False
                for j in text:
                    if not j.isdigit():
                        nonChar = True

                if nonChar:
                    cropped_image = img[336:351, 1064:1092]
                    resized2 = cv2.resize(cropped_image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
                    bw2 = cv2.threshold(resized2, 170, 255, cv2.THRESH_BINARY)[1]
                    text = pytesseract.image_to_string(bw2, config=custom_config)
                    # cv2.imshow('image', bw2)
                    # cv2.waitKey()
                    print(text)
                    data.append(int(text))
                else:
                    # cv2.imshow('image', bw)
                    # cv2.waitKey()
                    print(text)
                    data.append(int(text))
        # i = 3 corresponds with density value which is a float format; append to data list
        elif i == 3:
            if text == '':
                data.append(0)
            else:
                text = text.replace("]", "1").replace("\n", "").replace(".", "")
                text = text[0] + '.' + text[1:len(text)]
                data.append(float(text))
        # i = 5 corresponds with file name which is normally an int; append to data list,
        # otherwise, append a 0
        elif i == 5:
            if text == '':
                data.append(0)
            else:
                data.append(int(text))
        # All other values of i have an integer format; append to data list
        else:
            data.append(int(text))

    return data


def _6700OCR(imagePath):
    img = cv2.imread(imagePath)
    data = []
    cropped_image1 = img[192:205, 35:98]  # Bag category 1
    cropped_image2 = img[205:218, 35:98]  # Bag category 2
    cropped_image3 = img[218:231, 35:98]  # Bag category 3
    cropped_image4 = img[231:244, 35:98]  # Bag category 4
    cropped_image5 = img[244:257, 35:98]  # Bag category 5
    cropped_image6 = img[257:270, 35:98]  # Bag category 6
    cropped_image7 = img[1025:1051, 733:824]  # CT Value
    cropped_image8 = img[1027:1051, 538:680]  # Mass
    cropped_image9 = img[108:122, 60:75]  # Threat count
    cropped_image10 = img[345:360, 1618:1689]  # File name
    images = [cropped_image1, cropped_image2, cropped_image3, cropped_image4, cropped_image5,
              cropped_image6, cropped_image7, cropped_image8, cropped_image9, cropped_image10]

    for i in range(len(images)):
        # Store image at index 'i'
        currentImage = images[i]
        text = ""
        # i = 0 corresponds to Bag Category image
        if i >= 0 and i < 6:
            # Resize image using INTER_CUBIC interpolation (3x3)
            resized = cv2.resize(currentImage, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
            # Threshold set lower (min of 10) to only extract bolder text
            bw = cv2.threshold(resized, 10, 255, cv2.THRESH_BINARY)[1]
            # Extract text from image
            text = pytesseract.image_to_string(bw, config=custom_config)
            # Remove any occurrences of '\n', periods, or spaces
            text = text.replace("\n", "").replace(" ", "").replace(".", "")
            if text != '':
                resized2 = cv2.resize(currentImage, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
                bw2 = cv2.threshold(resized2, 80, 255, cv2.THRESH_BINARY)[1]
                text2 = pytesseract.image_to_string(bw2, config=custom_config)
                text2 = text2.replace("F", "E").replace("\n", "").replace(" ", "").replace(".", "")
                text2 = text2.upper()
                if text2 == "BALK":
                    text2 = "BULK"
                # Add text to list
                data.append(text2)
        else:
            # Resize image using INTER_CUBIC interpolation (3x3)
            resized = cv2.resize(currentImage, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
            # Threshold set higher (min of 170) for numeric values for optimal text extraction performance
            bw = cv2.threshold(resized, 170, 255, cv2.THRESH_BINARY)[1]
            # Extract text/numbers from image
            text = pytesseract.image_to_string(bw, config=custom_config)
            # i = 1 or i = 2 corresponds to CT Value and Mass which depending on the dimensions of the image,
            # will sometimes have unwanted characters included in the text extraction. Therefore, the text
            # requires filtering to solely focus on the numeric values and decimals
            if i == 6 or i == 7:
                filteredText = ""
                for j in text:
                    if j == '.' or j.isdigit():
                        # If the current character in the text is a decimal or numeric value, append to
                        # filteredText variable
                        filteredText = filteredText + j
                try:
                    if isinstance(float(filteredText), float):
                        # Append filteredText to data list
                        data.append(float(filteredText))
                except ValueError:
                    # Append 0 to data list if text is not a float value
                    data.append(0)
            # For all other values, simply append the integer values of the text to the data list
            else:
                data.append(int(text))

    return data


def analogicOCR(imagePath):
    img = cv2.imread(imagePath)
    data = []
    cropped_image = img[39:63, 370:424]  # File Name
    # Resize image using INTER_CUBIC interpolation (3x3)
    resized = cv2.resize(cropped_image, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)
    # Change image to black and white with min threshold of 200
    bw = cv2.threshold(resized, 230, 255, cv2.THRESH_BINARY)[1]
    # Extract text/numeric values from image
    text = pytesseract.image_to_string(bw, config=custom_config)
    # Remove any occurrences of " " and "\n"
    text = text.replace(" ", "").replace("\n", "").replace("|", "1").replace("O", "0").replace("]", "1").replace("/", "7")
    # Pytesseract adds an extra character to the end of the string sometimes; in the case that text is
    # longer than 4 characters, remove the end character until the length is equal to 4
    while len(text) > 4:
        text = text[:-1]
    # Append text to data list
    data.append(int(text))

    return data


def CTiXOCR(imagePath):
    img = cv2.imread(imagePath)
    data = []
    cropped_image = img[973:1057, 360:373]  # Alarm Count
    # Resize image using INTER_CUBIC interpolation (3x3)
    resized = cv2.resize(cropped_image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    # Change image to black and white with min threshold of 150
    bw = cv2.threshold(resized, 150, 255, cv2.THRESH_BINARY)[1]
    # Extract text/numeric values from image
    text = pytesseract.image_to_string(bw, config=custom_config)
    # Split text into a list by "\n" occurrences
    texts = text.split("\n")
    # List now holds values of alarms from image; find total number by taking the max of the list
    maxValue = int(max(texts))
    # Append the maxValue (total number of alarms) to data list
    data.append(maxValue)

    return data


def imageProcessComparison():
    global bags
    machineData = extractMachine()
    # machineData = extractAll()
    imageData = defaultdict(dict)
    results = defaultdict(dict)
    # Test Print
    # ----------------------------------------
    for keys,values in machineData.items():
        print(keys)
        print(values)
    # ----------------------------------------
    for bag in bags:
        print(bag)

        ct80FilePath = "C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume " + volume + "\\CT80\\" + bag + ".png"
        _9400FilePath = "C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume " + volume + "\\9400\\" + bag + ".png"
        _9800FilePath = "C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume " + volume + "\\9800\\" + bag + ".png"
        _6700FilePath = "C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume " + volume + "\\6700\\" + bag + ".png"
        analogicFilePath = "C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume " + volume + "\\Analogic\\" + bag + ".png"
        CTiXFilePath = "C:\\Users\\TSA\\PycharmProjects\\OCR\\Volume " + volume + "\\CTiX\\" + bag + ".png"

        if os.path.exists(ct80FilePath):
            CT80Data = ct80OCR(ct80FilePath)
            imageData[bag]["CT80"] = CT80Data
        if os.path.exists(_9400FilePath):
            _9400Data = _9400OCR(_9400FilePath)
            imageData[bag]["9400"] = _9400Data
        if os.path.exists(_9800FilePath):
            _9800Data = _9800OCR(_9800FilePath)
            imageData[bag]["9800"] = _9800Data
        if os.path.exists(_6700FilePath):
            _6700Data = _6700OCR(_6700FilePath)
            imageData[bag]["6700"] = _6700Data
        if os.path.exists(analogicFilePath):
            analogicData = analogicOCR(analogicFilePath)
            imageData[bag]["Analogic"] = analogicData
        # Temp else
        else:
            if bag not in missingImages.keys():
                missingImages[bag] = ["Analogic"]
            else:
                missingImages[bag].append("Analogic")
        if os.path.exists(CTiXFilePath):
            CTiXData = CTiXOCR(CTiXFilePath)
            imageData[bag]["CTiX"] = CTiXData
        # Temp else
        else:
            if bag not in missingImages.keys():
                missingImages[bag] = ["CTiX"]
            else:
                missingImages[bag].append("CTiX")

        ct80Bool, _9400Bool, _9800Bool, _6700Bool, AnalogicBool, CTiXBool = (True,)*6
        # Check if current bag with corresponding machine is missing
        if bag in missingImages:
            if "CT80" in missingImages[bag]:
                results[bag]["CT80"] = ["Missing Image!"]
                ct80Bool = False
            if "9400" in missingImages[bag]:
                results[bag]["9400"] = ["Missing Image!"]
                _9400Bool = False
            if "9800" in missingImages[bag]:
                results[bag]["9800"] = ["Missing Image!"]
                _9800Bool = False
            if "6700" in missingImages[bag]:
                results[bag]["6700"] = ["Missing Image!"]
                _6700Bool = False
            if "Analogic" in missingImages[bag]:
                results[bag]["Analogic"] = ["Missing Image!"]
                AnalogicBool = False
            if "CTiX" in missingImages[bag]:
                results[bag]["CTiX"] = ["Missing Image!"]
                CTiXBool = False

        CT80DataFields = ["Bag Category", "CT Value", "Z Value", "Mass", "Density", "Alarm Count", "File Name"]
        _94009800DataFields = ["Bag Category", "CT Value", "Mass", "Density", "Alarm Count", "File Name"]
        _6700DataFields = ["Bag Category", "CT Value", "Mass", "Alarm Count", "File Name"]
        if ct80Bool:
            results[bag]["CT80"] = []
            for i in range(len(machineData[bag]["CT80"])):
                if machineData[bag]["CT80"][i] != imageData[bag]["CT80"][i]:
                    results[bag]["CT80"].append("" + CT80DataFields[i] + " does not match!")
                else:
                    results[bag]["CT80"].append("")
        if _9400Bool:
            results[bag]["9400"] = []
            for i in range(len(machineData[bag]["9400"])):
                if machineData[bag]["9400"][i] != imageData[bag]["9400"][i]:
                    results[bag]["9400"].append("" + _94009800DataFields[i] + " does not match!")
                else:
                    results[bag]["9400"].append("")
        if _9800Bool:
            results[bag]["9800"] = []
            for i in range(len(machineData[bag]["9800"])):
                if machineData[bag]["9800"][i] != imageData[bag]["9800"][i]:
                    results[bag]["9800"].append("" + _94009800DataFields[i] + " does not match!")
                else:
                    results[bag]["9800"].append("")
        if _6700Bool:
            results[bag]["6700"] = []
            for i in range(len(machineData[bag]["6700"])):
                if machineData[bag]["6700"][i] != imageData[bag]["6700"][i]:
                    results[bag]["6700"].append("" + _6700DataFields[i] + " does not match!")
                else:
                    results[bag]["6700"].append("")
        if AnalogicBool:
            results[bag]["Analogic"] = []
            for i in range(len(machineData[bag]["Analogic"])):
                if machineData[bag]["Analogic"][i] != imageData[bag]["Analogic"][i]:
                    results[bag]["Analogic"].append("File name does not match!")
                else:
                    results[bag]["Analogic"].append("")
        if CTiXBool:
            results[bag]["CTiX"] = []
            for i in range(len(machineData[bag]["CTiX"])):
                if machineData[bag]["CTiX"][i] != imageData[bag]["CTiX"][i]:
                    results[bag]["CTiX"].append("Alarm count does not match!")
                else:
                    results[bag]["CTiX"].append("")

    # Test Print
    # ----------------------------------------
    for keys, values in imageData.items():
        print(keys)
        print(values)
    # ----------------------------------------
    return results


def checkIndex(list, index):
    result = True
    try:
        list[index]
    except IndexError:
        result = False

    if result:
        return str(list[index])
    else:
        return ""


def outputCSV(results):
    global bags
    with open('Volume ' + volume + ' QA Results.csv', 'w', newline='') as csvfile:
        fields = ["", "", "CT80", "9400", "9800", "6700", "Analogic", "CTiX"]
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        regWriter = csv.writer(csvfile)
        writer.writeheader()

        for bag in bags:
            list1 = [bag, "Bag Category", checkIndex(results[bag]["CT80"], 0), checkIndex(results[bag]["9400"], 0),
                     checkIndex(results[bag]["9800"], 0), checkIndex(results[bag]["6700"], 0), "N/A", "N/A"]
            list2 = ["", "CT Value", checkIndex(results[bag]["CT80"], 1), checkIndex(results[bag]["9400"], 1),
                     checkIndex(results[bag]["9800"], 1), checkIndex(results[bag]["6700"], 1), "N/A", "N/A"]
            list3 = ["", "Z Value", checkIndex(results[bag]["CT80"], 2), "N/A", "N/A", "N/A", "N/A", "N/A",]
            list4 = ["", "Mass", checkIndex(results[bag]["CT80"], 3), checkIndex(results[bag]["9400"], 2),
                     checkIndex(results[bag]["9800"], 2), checkIndex(results[bag]["6700"], 2), "N/A", "N/A"]
            list5 = ["", "Density", checkIndex(results[bag]["CT80"], 4), checkIndex(results[bag]["9400"], 3),
                     checkIndex(results[bag]["9800"], 3), "N/A", "N/A", "N/A"]
            list6 = ["", "Alarm Count", checkIndex(results[bag]["CT80"], 5), checkIndex(results[bag]["9400"], 4),
                     checkIndex(results[bag]["9800"], 4), checkIndex(results[bag]["6700"], 3), "N/A",
                     checkIndex(results[bag]["CTiX"], 0)]
            list7 = ["", "File Name", checkIndex(results[bag]["CT80"], 6), checkIndex(results[bag]["9400"], 5),
                     checkIndex(results[bag]["9800"], 5), checkIndex(results[bag]["6700"], 4),
                     checkIndex(results[bag]["Analogic"], 0), "N/A"]
            regWriter.writerow(list1)
            regWriter.writerow(list2)
            regWriter.writerow(list3)
            regWriter.writerow(list4)
            regWriter.writerow(list5)
            regWriter.writerow(list6)
            regWriter.writerow(list7)
            print(list1)
            print(list2)
            print(list3)
            print(list4)
            print(list5)
            print(list6)
            print(list7)

        csvfile.close()


def quickTest():
    return 0


def main():
    global volume

    username = input("Enter TIL Username: ")
    password = input("Enter TIL Password: ")
    volume = input("Enter EDS Volume Number: ")

    createFolders(volume)

    login(username, password, volume)
    
    results = imageProcessComparison()

    for keys,values in results.items():
        print(keys)
        print(values)

    outputCSV(results)

if __name__ == '__main__':
    main()
