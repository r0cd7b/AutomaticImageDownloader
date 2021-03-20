from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
from os import path
import os
import time
import requests

browser = webdriver.Edge("msedgedriver.exe")  # 사용할 browser에 맞게 driver를 선언한다.
search_word = "페트"  # 검색어를 정한다.
folder_name = "PET"  # image를 저장할 folder 이름을 정한다.

with browser as driver:  # edge driver를 with문 안에서 사용한다.
    wait = WebDriverWait(driver, 1)  # 허용 응답 시간이 10초인 WebDriverWait 객체를 선언한다.
    driver.get(f"https://www.google.co.kr/imghp?hl=ko&ogbl")  # 검색할 site의 url를 지정한다.

    search_banner = driver.find_element(By.NAME, "q")  # 검색 banner를 찾는다.
    key_combination = search_word + Keys.RETURN  # 검색어와 RETURN key를 조합한다.
    search_banner.send_keys(key_combination)  # 검색 banner에 key 조합을 입력한다.

    if not path.isdir(folder_name):  # image를 저장할 folder가 없을 경우 수행한다.
        os.mkdir(folder_name)  # image를 저장할 folder를 생성한다.

    attempts = 0  # '관련 검색어'를 제외한 image 항목을 찾기 위해 시도 횟수를 센다.
    element_number = 1  # 검색된 요소 번호를 센다.
    image_number = 1  # image 이름의 시작 번호를 지정한다.
    while attempts < 2:  # '관련 검색어'는 건너뛰고 이후에도 image 항목이 없다면 중단한다.
        selector = f"#islrg > div.islrc > div:nth-child({element_number}) > a.wXeWr.islib.nfEiy.mM5pbd > " \
                   f"div.bRMDJf.islir > img"  # selector를 설정한다.
        locator = (By.CSS_SELECTOR, selector)  # 요소를 CSS_SELECTOR로 찾기 위해 준비한다.
        conditions = expected_conditions.presence_of_element_located(locator)  # 해당 요소의 존재를 확인한다.
        try:  # 해당 요소 번호의 image가 없을 경우 예외가 발생한다.
            thumbnail = wait.until(conditions, "It is not an element or an image.")  # thumbnail 요소를 찾을 때까지 기다리고 반환한다.
            attempts = 0  # 요소가 존재하므로 시도 횟수를 0으로 초기화한다.
        except Exception as e:  # 예외가 발생할 경우 수행한다.
            print(e)  # error message를 출력한다.
            element_number += 1  # 요소 번호를 1 증가시킨다.
            attempts += 1  # 시도 횟수를 1 증가시킨다.
            continue  # 이후 code는 건너 뛴다.

        action = ActionChains(driver)  # driver가 수행할 action을 초기화한다.
        move = action.move_to_element(thumbnail)  # 해당 thumbnail 항목까지 이동하는 작업을 선언한다.
        move.perform()  # 이동 작업을 수행한다.
        thumbnail.click()  # 해당 thumbnail을 click한다.

        locator = (By.CSS_SELECTOR,
                   "#Sva75c > div > div > div.pxAole > div.tvh9oe.BIB1wf > c-wiz > div > div.OUZ5W > div.zjoqD > "
                   "div > div.v4dQwb > a > img")  # 요소를 CSS_SELECTOR로 찾기 위해 준비한다.
        conditions = expected_conditions.presence_of_element_located(locator)  # 해당 요소의 존재를 확인한다.
        image = wait.until(conditions)  # image 요소를 찾을 때까지 기다리고 반환한다.
        time.sleep(0.3)  # browser가 src 값을 갱신할 수 있게 기다린다.
        img_url = image.get_attribute("src")  # 현재 image의 src를 저장한다.
        print(img_url)  # 찾아낸 image의 url을 출력한다.

        img_path = f"{folder_name}/{folder_name}_{image_number}.jpg"  # image의 경로를 저장한다.
        while path.isfile(img_path):  # 이미 존재하는 file 이름이라면 반복한다.
            image_number += 1  # image 번호를 1 증가시킨다.
            img_path = f"{folder_name}/{folder_name}_{image_number}.jpg"  # image 경로를 갱신한다.

        result = requests.get(img_url, headers={'User-Agent': 'Edge/89.0.774.57'})  # request 과정에서 필요한 정보를 설정한다.
        with open(img_path, 'wb') as f:  # image를 file로 처리한다.
            f.write(result.content)  # image를 file로 저장한다.

        element_number += 1  # 요소 번호를 1 증가시킨다.
