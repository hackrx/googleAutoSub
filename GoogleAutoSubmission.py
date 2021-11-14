
from selenium import webdriver


EMAIL = "testemail@gmail.com"
PASSWORD = "8888888"
GOOGLEFORMLINK = "https://forms.gle/kndFRgEDFJ22HwyG7"
# file upload feature is not available, it requires google signin, and in that case it will fail.
data = {
    "UID": "18BCSxxxx",
    "NAME": "RAJAT GOYAL",
    "UNIVERSITY": "CHANDIGARH UNIVERSITY",
    "GMAIL": "ABSC@GMAIL.COM",
    "MAIL": "testgmail@COM",
    "MOBILE": "4567xxxxxx",
    "DOB": "2xxxx",
    "SKYPE": "ASDFADS@SYKPEID",
    "BACKLOG": 0,
    "12": "98.2",
    "10": "90",
    "SKILLS": "FULL STACK WEB AND MOBILE DEVELOPMENT",
    "SEMESTER": 7,
    "SGPA": 8,
    "CGPA": 8,
    "SHORT": "this is a short ans",
    "LONG": "this is a long ans",
    "COUNTRY": "INDIA"

}


def printRestPendingTitle(pendingTitles):
    for i in range(len(pendingTitles)):
        print(pendingTitles[i].text)


def takeInput():
    tGOOGLEFORMLINK = input("Please enter google form link")
    if len(tGOOGLEFORMLINK) == 0:
        print("Procedding with test google form")
        return GOOGLEFORMLINK
    if ("forms.gle" in tGOOGLEFORMLINK or "docs.google.com" in tGOOGLEFORMLINK):
        print("Opening browser")
        return tGOOGLEFORMLINK
    else:
        print("Please enter valid google form link.")
        exit()
        return


GOOGLEFORMLINK = takeInput()
option = webdriver.ChromeOptions()
option.add_argument("-incognito")
option.add_experimental_option("excludeSwitches", ['enable-automation'])
option.add_argument("--disable-popup-blocking")
# option.add_argument("--headless") Use this and the following option to run Headless
# option.add_argument("disable-gpu")


browser = webdriver.Chrome(executable_path="./chromedriver",
                           options=option)
browser.delete_all_cookies()

# google login if needed:
# browser.get(
#     "https://accounts.google.com/signin/v2/identifier?elo=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")


def submitForm(allButtons):
    # need to find submit button, from all buttons in the form
    for i in range(len(allButtons)):
        if allButtons[i].text == "Submit":
            allButtons[i].click()
            return


def googleLogin():
    browser.get("https://www.gmail.com")
    browser.find_element_by_name("identifier").send_keys(EMAIL)
    browser.find_element_by_xpath(
        "//*[@id='identifierNext']/div/button/span").click()
    browser.implicitly_wait(5)
    browser.find_element_by_name("password").send_keys(PASSWORD)

    browser.find_element_by_xpath(
        "//*[@id='passwordNext']/div/button/span").click()


def handleTexInputField(inputFields, titlesHeading):
    leftTitles = 0
    intialTitleHeadingCount = len(titlesHeading)
    filledOnes = 0
    pushedTitleIndex = []
    dataKeys = data.keys()
    for elementIndex in range(0, len(inputFields)):
        title = titlesHeading[elementIndex].text.upper()
        print(title)
        for key in data:
            if key in title:
                print(data[key])
                print("Yes found a value")
                inputFields[elementIndex].send_keys(data[key])
                filledOnes = filledOnes + 1
                pushedTitleIndex.append(elementIndex)
    # remove indexes from titlesHeading which we have already inserted
    for i in sorted(pushedTitleIndex, reverse=True):
        del titlesHeading[i]

    return {"leftTitles": intialTitleHeadingCount - filledOnes, "titlesHeading": titlesHeading}


browser.get(GOOGLEFORMLINK)
if "accounts.google" in browser.current_url:
    print("This google form requires, google authentication, and we don't support it yet. Please fill it manually")
    browser.close()
    exit()
# now check if it is redirected to google login

# Use the following snippets to get elements by their class names

textboxes = browser.find_elements_by_class_name(
    "quantumWizTextinputPaperinputInput")

textAreaBoxes = browser.find_elements_by_css_selector(
    ".quantumWizTextinputPapertextareaInput.exportTextarea")

titlesHeading = browser.find_elements_by_css_selector(
    ".freebirdFormviewerComponentsQuestionBaseTitle.exportItemTitle.freebirdCustomFont")
radiobuttons = browser.find_elements_by_class_name(
    "docssharedWizToggleLabeledLabelWrapper")
checkboxes = browser.find_elements_by_class_name(
    "quantumWizTogglePapercheckboxInnerBox")

allButtons = browser.find_elements_by_css_selector(
    ".appsMaterialWizButtonPaperbuttonLabel.quantumWizButtonPaperbuttonLabel.exportLabel")

submitbutton = browser.find_element_by_class_name(
    "appsMaterialWizButtonPaperbuttonContent")

# Use the following snippets to get elements by their XPath
# otherboxes = browser.find_element_by_xpath("<Paste the XPath here>")

# textboxes[0].
print("total titles ${len(textboxes)}")
print(len(textboxes))
print("heading total")
print(len(titlesHeading))
if len(titlesHeading) == 0:
    print("There are no textinput fields questions")
else:
    print(titlesHeading[0].text)
    result = handleTexInputField(textboxes, titlesHeading)
    leftTitles = int(result["leftTitles"])
    titlesHeading = result["titlesHeading"]

# NOW CHECK if we have more titles, if yes then check for other input fields
# paragraphs
if leftTitles > 0:
    result = handleTexInputField(textAreaBoxes, titlesHeading)
    # print("Please consider adding these left values in data, to enable auto submit")

titlesHeading = result["titlesHeading"]

# for i in range(len(titlesHeading)):
#     print(titlesHeading[i].text)

if len(titlesHeading) == 0:
    print("Going to submit the forum")
    submitForm(allButtons)
    print("going to close browser")
    browser.close()
else:
    print("Please enter the rest details manually")
    printRestPendingTitle(titlesHeading)
    print("Please submit the form manually")
