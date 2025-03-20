from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import subprocess
import time


chrome_options = webdriver.ChromeOptions()
# Change the directory to existing Google Chrome profile
chrome_options.add_argument("--user-data-dir=/Users/{USERNAME}/Library/Application Support/Google/Chrome")  
chrome_options.add_argument("--profile-directory=Profile 1") 


# prevent the system from going to sleep (delete the following line if you don't want that to happen)
caffeinate_process = subprocess.Popen(["caffeinate", "-dims"])

driver = webdriver.Chrome(options=chrome_options)
# Change the link to the Pollev Poll you want to automate
driver.get("https://pollev.com/") 

time.sleep(5)

last_question_text = None

def get_question_title():
    try:
        question_element = driver.find_element(By.CLASS_NAME, "component-response-header__title")
        return question_element.text.strip()
    except Exception as e:
        print("Error retrieving question title:", e)
        return None


def handle_mcq():
    global last_question_text
    try:
        question_text = get_question_title()
        if question_text and question_text != last_question_text:
            options = driver.find_elements(By.CLASS_NAME, "component-response-multiple-choice__option__vote")
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] New Question Detected: {question_text}")

            if options:
                options[0].click() # Change the default option that you want to select for MCQ questions (currently selecting the first option)
                last_question_text = question_text
    except Exception as e:
        print("Error handling MCQ:", e)
        
        
def handle_open_ended():
    global last_question_text
    try:
        question_text = get_question_title()
        if question_text and question_text != last_question_text:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] New Question Detected: {question_text}")

            answer_box = driver.find_element(By.NAME, "response")
            answer_text = "I am not too sure."  # Change the default text that you want to input into open-ended questions
            answer_box.send_keys(answer_text)
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            print("Open-ended Answer Submitted!")
            last_question_text = question_text
    except Exception as e:
        print("Error handling Open-Ended question:", e)


def detect_question_type():
    try:
        question_type_handlers = {
            "MCQ": handle_mcq,
            "OpenEnded": handle_open_ended
        }

        if driver.find_elements(By.CLASS_NAME, "component-response-multiple-choice__option__vote"):
            question_type = "MCQ"
        elif driver.find_elements(By.CLASS_NAME, "component-response-open-ended__input"):
            question_type = "OpenEnded"
        else:
            print("No new question detected.")
            return

        question_type_handlers.get(question_type, lambda: print("Unknown question type"))()

    except Exception as e:
        print("Error detecting question type:", e)


while True:
    detect_question_type()
    time.sleep(2) # Change the interval time between question detections (in seconds)






