import time

import cv2 as cv
import numpy as np
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options

report_step = 0


def initialize_appium_driver():
    desired_caps = {
        'platformName': 'Android',
        'appium: automationName': 'uiautomator2',
    }

    appium_server_url = 'http://localhost:4723'

    # Converts capabilities to AppiumOptions instance
    capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)
    driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)
    return driver


def add_screen_to_report(image, screen, search_result, img, click):
    global report_step
    h, w = image.shape
    (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(search_result)
    location = maxLoc
    botr = (location[0] + w, location[1] + h)
    tap_loc = (location[0] + w / 2, location[1] + h / 2)
    cv.rectangle(screen, location, botr, 255, 10)
    cv.rectangle(screen, location, botr, 0, 5)
    report_step += 1
    if click:
        cv.imwrite("report_screens/Step " + str(report_step) + ". CLICK on " + img + ".png", screen)
    else:
        cv.imwrite("report_screens/Step " + str(report_step) + ". Finding " + img+".png", screen)
    return tap_loc


def smart_wait_by_image(appium_driver, img, timeout=20, click=False):
    t_end = time.time() + timeout
    image = cv.imread('tests/res/'+img+'.png', 0)
    assert image is not None, "file 1 could not be read"
    while time.time() < t_end:
        appium_driver.save_screenshot("tests/screen.png")
        screen = cv.imread('tests/screen.png', 0)
        assert screen is not None, "file 2 could not be read"
        search_result = cv.matchTemplate(screen, image, cv.TM_CCOEFF_NORMED)
        threshold = 0.90
        loc = np.where(search_result >= threshold)
        if len(loc[0]) > 0:
            tap_loc = add_screen_to_report(image, screen, search_result, img, click)
            if click:
                appium_driver.tap([tap_loc], 300)
            return search_result
        else:
            time.sleep(0.2)
    return None


def smart_wait_by_image_with_condition(appium_driver, img, condition, timeout=20, click=False):
    t_end = time.time() + timeout
    image = cv.imread('tests/res/'+img+'.png', 0)
    assert image is not None, "file 1 could not be read"
    cond = cv.imread('tests/res/' + condition + '.png', 0)
    assert cond is not None, "file 1 could not be read"
    while time.time() < t_end:
        appium_driver.save_screenshot("tests/screen.png")
        screen = cv.imread('tests/screen.png', 0)
        assert screen is not None, "file 2 could not be read"
        search_result = cv.matchTemplate(screen, image, cv.TM_CCOEFF_NORMED)
        cond_result = cv.matchTemplate(screen, cond, cv.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(search_result >= threshold)
        loc_cond = np.where(cond_result >= threshold)
        if len(loc[0]) > 0:
            tap_loc = add_screen_to_report(image, screen, search_result, img, click)
            if click:
                appium_driver.tap([tap_loc], 300)
            return search_result
        else:
            time.sleep(0.2)
        if len(loc_cond[0]) > 0:
            add_screen_to_report(cond, screen, search_result, condition, click)
            return cond_result
        else:
            time.sleep(0.2)
    return None


def clear_report():
    report_path = 'report_screens'
    for root, dirs, files in os.walk(report_path):
        for file in files:
            if file.endswith('.png'):
                os.remove(os.path.join(root, file))




