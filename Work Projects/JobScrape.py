import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()

jobs = {}
ignoreTerms = ["Staff", "Manager", "Senior", "Sr", "Sr.", "Stf", "Supervisor", "Supv"]


def checkElement(xpath):
    try:
        driver.find_element(By.XPATH, value=xpath)
    except NoSuchElementException:
        return False
    return True


def checkClickable(xpath):
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return True
    except TimeoutException:
        return False

def leidosScrape():
    driver.get("https://careers.leidos.com/search/jobs?q=")
    driver.maximize_window()

    driver.find_element(By.XPATH, value='/html/body/div[3]/div[5]/div[2]/div/div/div/section[1]/div[2]/div/div[1]/div/section/div[2]/div[1]/div[1]/button').click()
    driver.find_element(By.XPATH, value='/html/body/div[3]/div[5]/div[2]/div/div/div/section[1]/div[2]/div/div[1]/div/section/div[2]/div[1]/div[2]/div[2]/div[1]/a/span[1]').click()


def lockheedScrape():
    global ignoreTerms
    driver.get('https://www.lockheedmartinjobs.com/search-jobs')
    driver.maximize_window()
    driver.find_element(By.XPATH, value='//*[@id="region-toggle"]').click()
    driver.find_element(By.XPATH, value='//*[@id="region-filter-28"]').click()
    if checkElement('//*[@id="ccpa-alert"]'):
        driver.find_element(By.XPATH, value='//*[@id="ccpa-button"]').click()

    jobTitles = []
    nextButtonXpath = '/html/body/div[3]/main/div/div/section[2]/section/section/div[2]/a[2]'

    while checkElement(nextButtonXpath):
        time.sleep(1)
        jobList = driver.find_element(By.XPATH, value='/html/body/div[3]/main/div/div/section[2]/section/ul')
        jobListItems = jobList.find_elements(By.TAG_NAME, 'li')
        currentJobTitles = driver.find_elements(By.CLASS_NAME, value='job-title')
        currentJobIDs = driver.find_elements(By.CLASS_NAME, value='job-id')
        for i in range(len(currentJobTitles)):
            title = currentJobTitles[i].get_attribute('innerHTML')
            id = currentJobIDs[i].get_attribute('innerHTML')
            linkElement = jobListItems[i].find_element(By.TAG_NAME, 'a')
            link = linkElement.get_attribute('href')
            jobTuple = (title, id, link)
            jobTitles.append(jobTuple)

        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, nextButtonXpath))).click()
        except TimeoutException:
            break


    for title in jobTitles[:]:
        for term in ignoreTerms:
            if term in title[0]:
                jobTitles.remove(title)
                break

    for title in jobTitles:
        print(title[0] + " : " + title[1])
        print(title[2])


def main():
    lockheedScrape()


if __name__ == "__main__":
    main()