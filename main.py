from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from config import config

def get_shedule(group:str):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options = options)
    driver.get(config['url'])

    container = driver.find_element(By.ID, 'select2-id_listgroups-container')
    container.click()
    search = driver.find_element(By.CLASS_NAME, 'select2-search__field')
    search.send_keys(str(group))
    result = driver.find_element(By.CLASS_NAME, 'select2-results__option')
    result.click()
    get_shedule = driver.find_element(By.ID, 'id_submitbutton')
    get_shedule.click()

    shedule = driver.find_element(By.CLASS_NAME, 'urk_shedule')
    lessons = shedule.find_elements(By.CLASS_NAME, 'urk_sheduleblock')
    timedate_system = datetime.today().strftime('%d.%m.%Y')
    found_lessons = False

    result = []
    result.append(f"Учебная группа: {group}")
    for lesson in lessons:
        lesson_data_details = lesson.find_element(By.CLASS_NAME, 'urk_sheduledate')
        target_data = lesson_data_details.text.split(" ", 1)[1]
        if str(target_data) == str(timedate_system):
            found_lessons = True
            lesson_block = lesson.find_elements(By.CLASS_NAME, 'urk_lessonblock')
            result.append(f"Дата: {target_data}")
            for block in lesson_block:
                caption = block.find_element(By.CLASS_NAME, 'urk_lessondescription')
                lesson_text = f"\n{caption.text}"
                study_couple = " ".join(get_study_couple(block))
                lesson_time = " - ".join(get_lesson_time(block))
                result.append(f"{lesson_text}\n{study_couple}: {lesson_time}")

    driver.quit()
    
    if found_lessons:
        return "\n".join(result)
    else:
        return "На сегодняшний день расписания нет."

def get_lesson_time(container):
    timewindow = container.find_element(By.CLASS_NAME, 'urk_timewindow')
    timewindow_info = timewindow.find_elements(By.CLASS_NAME, 'urk_timewindowinfo')
    last_two = timewindow_info[-2:]
    lesson_time = [element.text for element in last_two]
    return lesson_time

def get_study_couple(container):
    timewindow = container.find_element(By.CLASS_NAME, 'urk_timewindow')
    timewindow_infos = timewindow.find_elements(By.CLASS_NAME, 'urk_timewindowinfo')
    last_two = timewindow_infos[:1]
    study_couple = [element.text for element in last_two]
    return study_couple

print(get_shedule(110))