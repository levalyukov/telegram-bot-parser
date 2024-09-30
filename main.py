from playwright.async_api import async_playwright
from datetime import datetime, timedelta
from config import config
import asyncio

async def get_schedule(group: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(config['url'])

        await page.click(".select2-selection__rendered")
        await page.wait_for_timeout(100)
        await page.click(".select2-search__field")
        await page.wait_for_timeout(100)
        await page.fill(".select2-search__field", group)
        await page.wait_for_timeout(100)
        await page.click(".select2-results__option")
        await page.wait_for_timeout(100)
        await page.click("#id_submitbutton")
        await page.wait_for_timeout(100)

        shedule = page.locator(".urk_shedule")
        shedule_blocks = shedule.locator(".urk_sheduleblock")
        all_lessons = await shedule_blocks.count()
        timedate = datetime.today().strftime('%d.%m.%Y') 

        shedule_visible = await shedule.is_visible()
        shedule_count = await shedule.count()

        if shedule_count > 0 and shedule_visible:
            result = []
            found_lessons = False
            result.append(f"*Учебная группа*: {group}")
            result.append(f"*Дата*: {timedate}")
            for lesson in range(all_lessons):
                lesson_block = shedule_blocks.nth(lesson)
                lesson_date = lesson_block.locator(".urk_sheduledate")
                dates = await lesson_date.count()
                for time in range(dates):
                    time_lesson = lesson_date.nth(time)
                    content = await time_lesson.text_content()
                    target = content.split()[1].strip()
                    if str(target) == str(timedate):
                        target_lessons = lesson_block.locator(".urk_lessonblock")
                        count = await target_lessons.count()
                        for content in range(count):
                            found_lessons = True
                            count_description = lesson_block.locator(".urk_lessondescription")
                            nth_description = count_description.nth(content)
                            result_description = await nth_description.text_content()
                            target_description = result_description.replace('\n', ' ').strip()

                            target_lesson_date = target_lessons.locator(".urk_timewindow")
                            nth_target_lesson_date = target_lesson_date.nth(content)
                            lesson_time_coupe = nth_target_lesson_date.locator(".urk_timewindowinfo").nth(0)
                            lesson_time_start = nth_target_lesson_date.locator(".urk_timewindowinfo").nth(1)
                            lesson_time_end = nth_target_lesson_date.locator(".urk_timewindowinfo").nth(2)

                            target_time_coupe = await lesson_time_coupe.text_content()
                            target_time_start = await lesson_time_start.text_content()
                            target_time_end = await lesson_time_end.text_content()

                            formatted_output = f"\n{target_description}\n{target_time_coupe}: {target_time_start} - {target_time_end}"
                            result.append(formatted_output)

        if found_lessons:
            await browser.close()
            return "\n".join(result)
        else:
            result.clear()
            await browser.close()
            return f"*Учебная группа*: {group}\n*Дата*: {timedate}\n\nНа сегодняшний день расписания нет."
        
async def get_schedule_tomorrow(group:str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(config['url'])
        await page.click(".select2-selection__rendered")
        await page.wait_for_timeout(100)
        await page.click(".select2-search__field")
        await page.wait_for_timeout(100)
        await page.fill(".select2-search__field", group)
        await page.wait_for_timeout(100)
        await page.click(".select2-results__option")
        await page.wait_for_timeout(100)
        await page.click("#id_submitbutton")
        await page.wait_for_timeout(100)

        shedule = page.locator(".urk_shedule")
        shedule_blocks = shedule.locator(".urk_sheduleblock")
        all_lessons = await shedule_blocks.count()
        timedate_day = datetime.today().strftime('%d.%m.%Y') 
        target_date = add_one_day(timedate_day)

        shedule_visible = await shedule.is_visible()
        shedule_count = await shedule.count()

        if shedule_count > 0 and shedule_visible:
            result = []
            found_lessons = False
            result.append(f"*Учебная группа*: {group}")
            result.append(f"*Дата*: {target_date}")
            for lesson in range(all_lessons):
                lesson_block = shedule_blocks.nth(lesson)
                lesson_date = lesson_block.locator(".urk_sheduledate")
                dates = await lesson_date.count()
                for time in range(dates):
                    time_lesson = lesson_date.nth(time)
                    content = await time_lesson.text_content()
                    target = content.split()[1].strip()
                    if str(target) == str(target_date):
                        target_lessons = lesson_block.locator(".urk_lessonblock")
                        count = await target_lessons.count()
                        for content in range(count):
                            found_lessons = True
                            count_description = lesson_block.locator(".urk_lessondescription")
                            nth_description = count_description.nth(content)
                            result_description = await nth_description.text_content()
                            target_description = result_description.replace('\n', ' ').strip()

                            target_lesson_date = target_lessons.locator(".urk_timewindow")
                            nth_target_lesson_date = target_lesson_date.nth(content)
                            lesson_time_coupe = nth_target_lesson_date.locator(".urk_timewindowinfo").nth(0)
                            lesson_time_start = nth_target_lesson_date.locator(".urk_timewindowinfo").nth(1)
                            lesson_time_end = nth_target_lesson_date.locator(".urk_timewindowinfo").nth(2)

                            target_time_coupe = await lesson_time_coupe.text_content()
                            target_time_start = await lesson_time_start.text_content()
                            target_time_end = await lesson_time_end.text_content()

                            formatted_output = f"\n{target_description}\n{target_time_coupe}: {target_time_start} - {target_time_end}"
                            result.append(formatted_output)

        if found_lessons:
            await browser.close()
            return "\n".join(result)
        else:
            result.clear()
            await browser.close()
            return f"*Учебная группа*: {group}\n*Дата*: {target_date}\n\nРасписание отсутствует."
        
async def add_one_day(date_string: str) -> str:
    date_obj = datetime.strptime(date_string, "%d.%m.%Y")
    next_day = date_obj + timedelta(days=1)
    return next_day.strftime("%d.%m.%Y")
