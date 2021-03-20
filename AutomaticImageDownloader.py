from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
import time
from os import path
import os
from urllib import request

search_word = "페트"  # 검색어를 정한다.
folder_name = "PET"  # image를 저장할 folder 이름을 정한다.
browser = webdriver.Edge("msedgedriver.exe")  # 사용할 browser에 맞게 driver를 선언한다.

with browser as driver:  # edge driver를 with문 안에서 사용한다.
    wait = WebDriverWait(driver, 10)  # 허용 응답 시간이 10초인 WebDriverWait 객체를 선언한다.
    driver.get(f"https://www.google.co.kr/imghp?hl=ko&ogbl")  # 검색할 site의 url를 지정한다.

    search_banner = driver.find_element(By.NAME, "q")  # 검색 banner를 찾는다.
    key_combination = search_word + Keys.RETURN  # 검색어와 RETURN key를 조합한다.
    search_banner.send_keys(key_combination)  # 검색 banner에 key 조합을 입력한다.

    '''
    last_height = driver.execute_script("return document.body.scrollHeight")  # 현재 page의 총 scroll 높이를 저장한다.
    while True:  # 더 이상 image가 나오지 않을 때까지 반복한다.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 현재 page의 바닥까지 scroll한다.
        time.sleep(1)  # browser의 응답을 위해 대기한다.
        new_height = driver.execute_script("return document.body.scrollHeight")  # 현재 page의 바뀐 총 Scroll 높이를 저장한다.
        
        if new_height == last_height:  # 더 이상 scoll할 높이가 없을 경우 수행한다.
            try:  # click할 '결과 더 보기'가 존재하지 않으면 예외가 발생한다.
                locator = (By.CSS_SELECTOR, ".mye4qd")  # 요소를 CSS_SELECTOR로 찾기 위해 준비한다.
                presence = expected_conditions.presence_of_element_located(locator)  # 해당 요소의 존재를 확인한다.
                more_button = wait.until(presence)  # '결과 더 보기'를 찾을 때까지 기다리고 반환한다.
                more_button.click()  # '결과 더 보기' button을 click한다.
            except Exception as e:  # 예외 발생 시 수행한다.
                print(e)  # 예외 massage를 출력한다.
                break  # while문을 빠져 나간다.
        
        last_height = new_height  # scroll을 계속 수행하기 위해 마지막 last_height를 갱신한다.
    '''

    if not path.isdir(folder_name):  # image를 저장할 folder가 없을 경우 수행한다.
        os.mkdir(folder_name)  # image를 저장할 folder를 생성한다.

    count = 1  # image 이름의 시작 번호를 지정한다.
    locator = (By.CSS_SELECTOR, ".Q4LuWd")  # 요소를 CSS_SELECTOR로 찾기 위해 준비한다.
    presence = expected_conditions.presence_of_all_elements_located(locator)  # 해당 요소의 존재를 확인한다.
    thumbnails = wait.until(presence)  # thumbnail 요소를 찾을 때까지 기다리고 반환한다.
    for thumbnail in thumbnails:  # 찾아낸 전체 thumbnail에 대해 반복한다.
        try:
            thumbnail.click()  # thumbnail을 click한다.
            time.sleep(0.3)  # browser의 응답을 위해 대기한다.
            locator = (By.CSS_SELECTOR, ".BIB1wf > "
                                        "c-wiz > "
                                        "div > "
                                        "div > "
                                        "div > "
                                        "div > "
                                        "div > "
                                        "a > "
                                        "img")  # 요소를 CSS_SELECTOR로 찾기 위해 준비한다.
            presence = expected_conditions.presence_of_element_located(locator)  # 해당 요소의 존재를 확인한다.
            image = wait.until(presence)  # image 요소를 찾을 때까지 기다리고 반환한다.
            img_url = image.get_attribute("src")  # 현재 image의 src를 저장한다.

            img_path = f"{folder_name}/{folder_name}_{count}.jpg"  # image를 저장할 경로를 저장한다.
            while path.isfile(img_path):  # 이미 존재하는 file 이름이라면 반복한다.
                count += 1  # image 번호를 1 증가시킨다.
                img_path = f"{folder_name}/{folder_name}_{count}.jpg"  # image 경로를 수정한다.
            print(img_url)

            request.urlretrieve(img_url, img_path)  # image를 해당 경로에 저장한다.
        except Exception as e:  # 예외 발생 시 수행한다.
            input(e)  # 예외 massage를 출력한다.
