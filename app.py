from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# driver = webdriver.PhantomJS('vendor/phantomjs/bin/phantomjs')
driver = webdriver.Chrome('vendor/chromedriver')
final_dict={}
final_output = []

#driver.implicitly_wait(10)
#driver.maximize_window()

driver.get("http://norfolkair.norfolk.gov/norfolkairmobile/")

def back():
    global driver
    driver.execute_script("window.history.go(-1)")

def getMenuOptions():
    global driver
    menu = driver.find_elements_by_class_name("selectbtn")
    # print("Content of Menu:")
    # for item in menu:
    #     print(item.get_property("value"))
    return menu

def search():
    global driver
    search_field = driver.find_element_by_id("ctl00_MainContent_txtadd")
    search_field.clear()
    search_field.send_keys("400 granby street")
    search_field.send_keys(Keys.RETURN)

def openMenuOption(menu,index):
    #print(menu)
    #print(index)
    temp = menu[index].get_property("value")
    menu[index].click()
    return temp


def getTableContents():
    global driver
    table_items = driver.find_elements_by_tag_name("td")
    return table_items

def parseContent(tableContents):
    hyperlinkFields = ["Website","Recycling Dates"]
    output_list = []
    for field in tableContents:
        link = field.find_elements_by_tag_name("a")
        if len(link)>0 and output_list[-1] in hyperlinkFields:
            for item in link:
                output_list.append(item.get_attribute('href'))
        else:
            output_list.append(field.text)
    return output_list

def populateDictWithMenu(menu):
    dict={}
    for item in menu:
        dict[item.get_property("value")]=[]
    return dict


def walkMenu():
    #TODO: Skips building permits. len(menu) should be for loop
    menu = getMenuOptions()
    global final_dict
    global final_output
    for i in range(0,len(menu)-1):
        openedMenu = openMenuOption(menu, i)
        if i == 0:
            getRealEstateData()
        else:
            #print(menu)
            #print(final_dict)
            pageContents = getTableContents()
            #print(pageContents)
            final_output = parseContent(pageContents)
            final_dict[openedMenu] = final_output
            back()
            #Up or lower the time if you're receiving index errors
        time.sleep(1)
        #driver.save_screenshot('screenie.png')
        menu = getMenuOptions()

def getRealEstateData():
    """
    Called from the Main Menu to traverse the Real Estate Data SubMenu
    """
    global final_dict
    global final_output
    time.sleep(1)
    menu = getMenuOptions()
    #print(menu)
    for i in range(0,len(menu)):
        print("i: "+ str(i)+" len(menu): "+str(len(menu)))
        #print(menu)
        #print(final_dict)
        openedMenu = openMenuOption(menu, i)
        pageContents = getTableContents()
        print(pageContents)
        final_output = parseContent(pageContents)
        final_dict[openedMenu] = final_output
        back()
        #Up or lower the time if you're receiving index errors
        time.sleep(1)
        #driver.save_screenshot('screenie.png')
        menu = getMenuOptions()
    back()

def main():
    global driver
    global final_output
    global final_dict
    search()
    #menu = getMenuOptions()
    walkMenu()
    print("\nContent of Table")
    print(final_output)
    print("Final Dict Contents:")
    print(final_dict)
    driver.quit()

main()