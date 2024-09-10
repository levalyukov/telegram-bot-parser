from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from config import config

def get_schedule(group:str):
    options = webdriver.ChromeOptions()             # ← Browser settings
    options.add_argument("--headless")              # ← The argument of the option. In this case, all manipulations will occur without opening the browser itself
    driver = webdriver.Chrome(options = options)    # ← Setting the browser for all site manipulations
    driver.get(config['url'])                       # ← Getting a url from the config

    input_contaienr = driver.find_element(By.ID, 'select2-id_listgroups-container')   # ↰ — In order to enter the 'group' variable, you need to click on the input field 
    input_contaienr.click()                                                           # ↲  
    search_input = driver.find_element(By.CLASS_NAME, 'select2-search__field')        # ← The input field where you need to enter the 'group' variable
    search_input.send_keys(str(group))                                                # ← Entering the 'group' variable in the search field
    result = driver.find_element(By.CLASS_NAME, 'select2-results__option')      # ↰ — Finding a suitable study group by the variable 'group'
    result.click()                                                              # ↲ 
    get_shedule = driver.find_element(By.ID, 'id_submitbutton')                 # ↰ — Getting the full schedule of the specified study group
    get_shedule.click()                                                         # ↲ 

    # ↓

    shedule = driver.find_element(By.CLASS_NAME, 'urk_shedule')             # ↰ — 
    all_lessons = shedule.find_elements(By.CLASS_NAME, 'urk_sheduleblock')  # ↲
    timedate_system = datetime.today().strftime('%d.%m.%Y')                 # ← Getting the date of the system
    found_lessons = False                                                   # ← The variable responsible for finding activities
    
    # ↓

    result = []                                                             # ← The main array to which we will add information from the site
    for lessons in all_lessons: 
        lesson_data_details = lessons.find_element(By.CLASS_NAME, 'urk_sheduledate')
        target_data = lesson_data_details.text.split(" ", 1)[1]
        if str(target_data) == str(timedate_system):                        # ← If the date of the system and the date of the pair match, then we continue the cycle
            found_lessons = True
            lesson = lessons.find_elements(By.CLASS_NAME, 'urk_lessonblock')    # ← 
            result.append(f"*Учебная группа*: {group}")
            result.append(f"*Дата*: {target_data}")
            for content in lesson:
                name = content.find_element(By.CLASS_NAME, 'urk_lessondescription')     # ← Lesson name
                study_couple = " ".join(get_study_couple(content))                      # ← Getting the serial number of the student couple
                lesson_time = " - ".join(get_lesson_time(content))                      # ← Getting a student couple's time
                result.append(f"\n{name.text}\n{study_couple}: {lesson_time}")          # ← Writing the result to an array

    driver.quit()
    if found_lessons:   # ← If the lessons are found, then we pass an array with the final result
        print("\n".join(result))
        return "\n".join(result)
    else:               # ← If there are still no lessons, it shows that there is no class schedule for today
        print(f"Учебная группа: {group}\nДата: {timedate_system}\n\nНа сегодняшний день расписания нет.")
        return f"*Учебная группа*: {group}\n*Дата*: {timedate_system}\n\nНа сегодняшний день расписания нет."

def get_lesson_time(container):    # Getting the time of a specific student couple
    timewindow = container.find_element(By.CLASS_NAME, 'urk_timewindow')
    timewindow_info = timewindow.find_elements(By.CLASS_NAME, 'urk_timewindowinfo')
    last_two = timewindow_info[-2:]
    lesson_time = [element.text for element in last_two]
    return lesson_time

def get_study_couple(container):    # Getting the number of the student couple
    timewindow = container.find_element(By.CLASS_NAME, 'urk_timewindow')
    timewindow_infos = timewindow.find_elements(By.CLASS_NAME, 'urk_timewindowinfo')
    last_two = timewindow_infos[:1]
    study_couple = [element.text for element in last_two]
    return study_couple