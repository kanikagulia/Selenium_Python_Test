# **********************************************************************************
# 
# Created By        : Kanika Gulia
# Date              : 15-Jan-2021
# Summary           : Below code submits user inputs in a web form and verfies the submitted details.
#                     Also verifies the Address in Google Maps. (Optional Step 6 Done)
# Python Version    : 3.9.1
# IDE               : Visual Studio Code
# 
# ***********************************************************************************

# Importing required modules
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import datetime
import re


# ***************************** STEP 5 **************************************************
# ******************** Function for printing Issue Format *******************************

# ******************** VERIIFICATION FUNCTION DEFINITION  *******************************
# Verifies 2 values and prints a formatted Issue message in case of mismatch
# Function Arguments: 
# arg_userInput - the value entered by user on Registration form 
# arg_AppActual - The value displayed on Employee Details Page
# arg_field - The field to be verified, it is used only as Issue Text in reporting
def my_Validation(arg_userInput,arg_AppActual,arg_field):
    try:
        assert arg_userInput == arg_AppActual
    except AssertionError:
        print("\na. Issue Heading: ", arg_field , " MISMATCH\nb. Issue Description: ", arg_field ," on Employee Details Page does NOT match with its value entered on Registration Form\nc. Expected Behaviour: Expected value from User Input Form is '", arg_userInput, "' but Actual value from Employee Details Page is '", arg_AppActual, "'\n")


# ***************************** STEP 1 **************************************************
# ************************ Go to Employee Registration Page *****************************
# Launch Chrome
ChromeDriverPath = "C:\\Program Files (x86)\\chromedriver.exe"      #Update it to use on your PC
driver = webdriver.Chrome(ChromeDriverPath)
URL1 = "https://rpmsoftware.com/hiring/2020/integration-test/form-edit.html"
URL2 = "https://rpmsoftware.com/hiring/2020/integration-test/form.html"


# Open the Registration Web Form and maximize window
driver.get(URL1)
driver.maximize_window()

# ***************************** STEP 2 **************************************************
# ************************** Enter Details **********************************************
# Defining Input Variables / User Inputs
var_EmployeeName = "Isabel Britt"
var_Summary = "This is a test Employee Summary."
var_Department = "Management"
var_Salary = "$50,000.00"
var_Address_Lat = "34.833850°"
var_Address_Long = "106.748580°"
var_WorkLocation = "Headquarters"
var_DOJ = "Jan 4, 2018"
var_IsActive = "Yes"
var_Cubicle_Length = "47"       # Change Dropdown from mm to inch
var_Cubicle_Width = "21"        # Change Dropdown from mm to inch
var_Cubicle_Color = "Brown"
list_Car1 = ["Ford", "Taurus", "2018", "SEL", "Black", "TEST-0001"] 
list_Car2 = ["Ford", "F150", "2015", "XLT", "Red", "Test-0002"]

# Filling Registration Form using User Input values (Input variables)
driver.find_element_by_id("FL:_ctl0:_ctl3").send_keys(var_EmployeeName)
driver.find_element_by_id("FL:_ctl1:_ctl4").send_keys(var_Summary)
Select(driver.find_element_by_id('FL:_ctl3:_ctl3')).select_by_visible_text(var_Department)
driver.find_element_by_id("FL:_ctl4:_ctl3").send_keys(var_Salary)
driver.find_element_by_id("FL_latTxt_5").send_keys(var_Address_Lat)
driver.find_element_by_id("FL_longTxt_5").send_keys(var_Address_Long)
Select(driver.find_element_by_id('FL:_ctl6:_ctl3')).select_by_visible_text(var_WorkLocation)    #Dropdown

# Enter Date of Joining - Format change from MMM dd, yyyy to MM/dd/yyyy
var_DOJ = var_DOJ.replace(',','')
var_DOJ_new = datetime.datetime.strptime(var_DOJ,'%b %d %Y').strftime('%m/%d/%Y')
# Enter the value of Date 
driver.find_element_by_id("FL:_ctl8:_ctl3").send_keys(var_DOJ_new)

# Radio Button Is Active Selected as Yes
if var_IsActive == "Yes":
    driver.find_element_by_id("FL__ctl3_9").click()     # Select Yes Radio Button
else:
    driver.find_element_by_id("FL__ctl5_9").click()  # Select No Radio Button


# Enter Cubicle Details - Length, Width and Color
driver.find_element_by_xpath('/html/body/div/div/div[15]/span[2]/div/table/tbody/tr[2]/td[2]/div/div/div/span/input').send_keys(var_Cubicle_Length)
driver.find_element_by_xpath('/html/body/div/div/div[15]/span[2]/div/table/tbody/tr[2]/td[3]/div/div/div/span/input').send_keys(var_Cubicle_Width)
driver.find_element_by_xpath('/html/body/div/div/div[15]/span[2]/div/table/tbody/tr[2]/td[4]/div/div/div/input').send_keys(var_Cubicle_Color)

# Change dropdown from mm to inch
Select(driver.find_element_by_xpath('/html/body/div/div/div[15]/span[2]/div/table/tbody/tr[2]/td[2]/div/div/div/span/select')).select_by_visible_text("in")
Select(driver.find_element_by_xpath('/html/body/div/div/div[15]/span[2]/div/table/tbody/tr[2]/td[3]/div/div/div/span/select')).select_by_visible_text("in")

# Enter Car Details for Car 1 using loop on column count
car_columncount = len(driver.find_elements_by_xpath('''//*[@id="Table500_15:Container"]/table/tbody/tr[2]/td'''))
for i in range(car_columncount - 1):
    driver.find_element_by_xpath("/html/body/div/div/div[16]/span[2]/div/table/tbody/tr[2]/td["+str(i+2)+"]/div/div/div/input").send_keys(list_Car1[i])

# Enter Car Details for Car 2 using loop on column count
for j in range(car_columncount - 1):
    driver.find_element_by_xpath("/html/body/div/div/div[16]/span[2]/div/table/tbody/tr[3]/td["+str(j+2)+"]/div/div/div/input").send_keys(list_Car2[j])




# ***************************** STEP 3 **************************************************
# ******************** Submit & Validate User Navigated *********************************

# Click on Submit button
driver.find_element_by_xpath('//*[@id="FormEditPanel"]/div[18]/button').click()

#Fetch the URL from Application at Run time
URL_current = driver.current_url

# Verify User navigated to URL2 (Employee Details Page)
# Navigation Fails, Exit the Test Script using assert
# Using If to print SUCCESS Message
if URL_current == URL2:
    print("\nPASS - User successfully navigated to Page after submitting the details\n")
else:
    assert URL_current == URL2, "FAIL - User NOT navigated to Employee Details Page, Exit the code"




# ***************************** STEP 4 **************************************************
# ***************** Validate Data Displayed with entered Step 2 data ********************
# ***************** Report Issue in desired format for mismatches, using function ********

# Verify Employee name
my_Validation(var_EmployeeName, str(driver.find_element_by_id('Field.500_1:ValueContainer').text.strip()), "Employee name")

# Verify Summary
app_Summary = driver.find_element_by_xpath('/html/body/div/div[2]/div[4]/span[2]').text.strip()
try:
    assert var_Summary in app_Summary
except AssertionError:
    print("\nIssue Heading: Summary MISMATCH\nIssue Description: Summary on Employee Details Page does NOT match with its value entered on Registration Form\nExpected Behaviour: Expected value from User Input Form is '", var_Summary, "' but Actual value from Employee Details Page is '", app_Summary , "'\n")

# Verify Department
my_Validation(var_Department, str(driver.find_element_by_id('Field.500_7:ValueContainer').text.strip()), "Department")

# Verify Salary
my_Validation(var_Salary, str(driver.find_element_by_id('Field.500_6:ValueContainer').text.strip()), "Salary")

# Verify Address - Latitude and Longitude
a = driver.find_element_by_id('Field.500_25:ValueContainer').text.strip()   #Fetch Address from Application
# From the Address, Seperate the Latitude and Longitude in a list 
a = a.replace(',', '')
b = a.split(' ')    # b is now a list 
# Type Casting - Converting to string
b[0] = str(b[0])
b[1] = str(b[1])

# Verify Address Latitude
my_Validation(var_Address_Lat, b[0], "Address Latitude")

# Verify Address Longitude
my_Validation(var_Address_Long, b[1], "Address Longitude")

# Verify Work Location
my_Validation(var_WorkLocation, driver.find_element_by_id('Field.500_8:ValueContainer').text.strip(), "Work Location")

# Verify Date of Joining
my_Validation(var_DOJ, str(driver.find_element_by_id('Field.500_3:ValueContainer').text.strip()), "Date of Joining")

# Verify Is Employee still Active
my_Validation(var_IsActive, driver.find_element_by_id('Field.500_4:ValueContainer').text.strip(), "Employee still Active")


# Verify Employee Cubicle Needs
# Verify Length
my_Validation(var_Cubicle_Length, str(driver.find_element_by_xpath('/html/body/div/div[2]/div[16]/span[2]/div[1]/table/tbody/tr[2]/td[2]/div/div/div').text.replace('in','')), "Employee Cubicle Length")

# Verify Width
my_Validation(var_Cubicle_Width, str(driver.find_element_by_xpath('/html/body/div/div[2]/div[16]/span[2]/div[1]/table/tbody/tr[2]/td[3]/div/div/div').text.replace('in','')), "Employee Cubicle Width")

# Verify Color
my_Validation(var_Cubicle_Color, str(driver.find_element_by_xpath('/html/body/div/div[2]/div[16]/span[2]/div[1]/table/tbody/tr[2]/td[4]/div/div/div').text), "Employee Cubicle Color")


# *************** Verify Car Details of Car 1 ******************
# Verify details of each columns of Car 1
car_columncount_emp_page = len(driver.find_elements_by_xpath('''//*[@id="Table500_15:Container"]/table/tbody/tr[2]/td'''))
for k in range(car_columncount_emp_page - 1):
    my_Validation(str(list_Car1[k]), str(driver.find_element_by_xpath("/html/body/div/div[2]/div[17]/span[2]/div[1]/table/tbody/tr[2]/td["+str(k+2)+"]/div/div/div").text), "Car 1 Detail")


# *************** Verify Car Details of Car 2 ******************
# Verify details of each columns of Car 2 
for m in range(car_columncount_emp_page - 1):
    my_Validation(str(list_Car2[m]), str(driver.find_element_by_xpath("/html/body/div/div[2]/div[17]/span[2]/div[1]/table/tbody/tr[3]/td["+str(m+2)+"]/div/div/div").text), "Car 2 Detail")




# ***************************** STEP 6 **************************************************
# ****************** Verify Header, Address Format, Google Maps Address *****************

# Verify Employee Name displayed as HEADER on Employee Details Page
# Fetch text of the Header element of Page by using Xpath containing <h1> tag
# Using IF to print SUCCESS Message and else uses assert to print Issue mismatch
if driver.find_element_by_xpath('/html/body/div/h1').text == var_EmployeeName:
    print("\nPASS: HEADER : The Employee name is displayed as Header on the Employee page: SUCCESS\n")
else:
    my_Validation(var_EmployeeName, driver.find_element_by_xpath('/html/body/div/h1').text, "HEADER")


# Verify Address Format as  xxx.xxxxxx °, xxx.xxxxxx°
exptd_addr_format = "xxx.xxxxxx°, xxx.xxxxxx°"
# Fetch address appearing on Application
address_app = driver.find_element_by_id('Field.500_25:ValueContainer').text.strip()
address_app = address_app.replace(' Map', '') # Removing Map from address, to get only latitude and longitude
# Replace all characters in address with x
address_app = str(re.sub('[0-9]', 'x', address_app))

# Comparing Expected Format with Actual address format 
# Using IF to print SUCCESS Message and else uses assert to print Issue mismatch
if exptd_addr_format == address_app:
    print("\nSUCCESS: VERIFIED: Address field has data in Expected format xxx.xxxxxx°, xxx.xxxxxx°\n")
else:
    my_Validation(exptd_addr_format, address_app, "ADDRESS FORMAT")


# Verify address field has link Map, taking user to respective location on Google Maps
MapLink = driver.find_element_by_link_text("Map")
MapLink.click()

# wait for 3 seconds if new tab takes time to open
time.sleep(4)

# New Tab opens - Fetch Window Handles
allTabs = driver.window_handles

# Iterate through the open tabs and verify Google Maps opens in second tab
for tab in allTabs:
    driver.switch_to_window(tab)  
    if tab in allTabs[1]:
        if 'Google Maps' in str(driver.title):
            print("\nSUCCESS - Google Maps opens\n")  
            # Fetch Address from Google Maps Application Page          
            GoogleMapAddress = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2').text
        else:
            print("\nFAIL: Google Map NOT open\n")

# Verify correct address is shown in Google maps - GoogleMapAddress matches with input address
var_Full_Address = var_Address_Lat + ", " + var_Address_Long       ## These are input variables
var_Full_Address = var_Full_Address.replace('°', '')  # This is input address

# Compare Google Map address with input address
# Using IF to print SUCCESS Message
if str(GoogleMapAddress) == str(var_Full_Address):
    print("\nSUCCESS: Correct address in Google Maps. Map Link takes the user to correct location in Google Maps\n")
else:
    my_Validation(str(var_Full_Address), str(GoogleMapAddress), "Google Map Address")



# Close the Application
driver.quit()
