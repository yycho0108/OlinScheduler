# getCourseInfo.py : scrape course Info from Olin Website
import sys
import time
import pickle
from urllib.request import urlretrieve
import subprocess
from selenium import webdriver

def reachSite(userName, password, target="2016;SP"):
    driver = webdriver.Firefox();
    driver.implicitly_wait(3);
    driver.get("https://my.olin.edu/ICS/My_StAR/Registration_AddDrop.jnz");
    #time.sleep(2);
    driver.find_element_by_name("userName").send_keys(userName);
    driver.find_element_by_name("password").send_keys(password);
    driver.find_element_by_name("btnLogin").click();
    #time.sleep(2);
    term = driver.find_element_by_id("pg0_V_ddlTerm");
    webdriver.support.select.Select(term).select_by_value(target);
    #time.sleep(2);
    driver.find_element_by_id("pg0_V_tabSearch_btnSearch").click();
    #time.sleep(2);
    driver.find_element_by_id("pg0_V_lnkShowAll").click();
    time.sleep(2);
    return driver;
def scrapeInfo(driver):
    driver.implicitly_wait(0); #by now, all info should be loaded
    record = [];
    for tr in driver.find_elements_by_tag_name("tr"):
        entries = tr.find_elements_by_tag_name("td");
        if(len(entries) == 12):
            content = [];
            for entry in entries:
                subentryList = [];
                subNodes = entry.find_elements_by_xpath(".//li");
                if(len(subNodes) != 0): #is a list
                    for subNode in subNodes:
                        subentryList.append(subNode.text);
                    content.append(subentryList);
                else:
                    content.append(entry.text);
            d = {
                "code" : content[1],
                "title" : content[2],
                "instructor" : content[5],
                "openSpots" : content[6],
                "status" : content[7],
                "meetingPattern" : content[8],
                "credit" : content[9],
            };
            record.append(d);
    return record;
def getCourseInfo(userName,password,target):
    driver = reachSite(userName,password,target);
    record = scrapeInfo(driver);
    with open('courseInfo.dat', 'wb') as out:
        pickle.dump(record,out);
        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Invalid # of arguments");
    elif len(sys.argv) == 3:
        getCourseInfo(sys.argv[1], sys.argv[2]);
    elif len(sys.argv) == 4:
        getCourseInfo(sys.argv[1],sys.argv[2],sys.argv[3]);
