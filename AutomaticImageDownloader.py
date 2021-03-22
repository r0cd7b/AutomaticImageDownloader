"""
** 사전 조건 **
1. 아래 모듈 중 없는 모듈을 설치한다. (pip install 명령어로 설치 가능하다.)
2. 자신의 컴퓨터에 설치된 브라우저 중 사용할 브라우저의 버전을 확인한다.
3. 브라우저 버전에 맞는 드라이버 파일을 다운로드한다.
4. 드라이버 파일을 이 py 파일과 같은 경로에 둔다.
5. browser = webdriver.Edge("msedgedriver.exe") -> 'Edge' 부분을 드라이버 종류에 맞게 아래 예시에서 참고하여 수정한다.
    ex) 엣지: Edge, 크롬: Chrome, 파이어폭스: Firefox, 인터넷 익스플로러: Ie, 오페라: Opera, 사파리: Safari
6. browser = webdriver.Edge("msedgedriver.exe") -> 'msedgedriver.exe' 부분을 드라이버 파일 이름으로 수정한다.
7. folder_name = "PET" -> 'PET' 부분을 저장할 폴더 이름으로 수정한다. (생성될 폴더 경로는 이 py 파일과 동일 경로상의 Images 폴더이다.)
8. search_word = "페트" -> '페트' 부분을 원하는 검색어로 수정한다.
"""
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from os import path
from urllib import request

search_word = "종이팩"  # 검색어를 정한다.
file_name = "carton"  # 저장할 이미지 파일의 이름을 정한다.
browser = webdriver.Edge("msedgedriver.exe")  # 드라이버를 선언한다.

with browser as driver:  # 드라이버를 with문으로 처리한다.
    driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")  # 드라이버에 페이지 주소를 연결한다.
    driver.find_element(By.NAME, 'q').send_keys(search_word + Keys.RETURN)  # 검색 배너를 찾고 검색어를 입력한다.

    os.makedirs(f"Images/{file_name}", exist_ok=True)  # 이미지를 저장할 폴더가 있는지 확인하고 생성한다.

    wait = WebDriverWait(driver, 1)  # 드라이버가 동작할 때 최대 응답 대기 시간을 설정한다.
    element_number = 1  # 검색된 결과 요소의 시작 번호를 설정한다.
    image_number = 1  # 처리할 이미지의 시작 번호를 정한다.
    file_number = 1  # 저장할 이미지 파일 이름의 시작 번호를 지정한다.
    while True:  # 더 이상의 검색 결과가 없을 때까지 수행한다.
        try:  # "결과 더보기" 요소가 없을 경우 예외가 발생한다.

            try:  # 검색된 결과 요소가 더 이상 없을 경우 예외가 발생한다.
                result_locator = (By.CSS_SELECTOR, f"#islrg > div.islrc > div:nth-child({element_number})")
                # 결과 요소를 찾을 locator를 설정한다.
                result_presence = expected_conditions.presence_of_element_located(result_locator)
                # 해당 요소가 존재하는지 확인하고 값을 반환한다.
                result_element = wait.until(result_presence, "There are no more search results.")  # 찾은 요소를 반환한다.
                ActionChains(driver).move_to_element(result_element).perform()  # 검색 결과를 계속해서 불러오기 위해 해당 요소로 화면을 이동한다.

            except Exception as e:  # 예외를 처리한다.
                print(e)  # 예외 메시지를 출력한다.
                more_results_selector = "#islmp > div > div > div > div > div.qvfT1 > div.YstHxe > input"
                # "결과 더보기" 요소를 찾을 selector를 설정한다.
                more_results_locator = (By.CSS_SELECTOR, more_results_selector)  # selector를 locator로 지정한다.
                more_results_presence = expected_conditions.presence_of_element_located(more_results_locator)
                # 해당 요소가 존재하는지 확인하고 값을 반환한다.
                more_results_element = wait.until(more_results_presence, '''There is no "More results".''')
                # 찾은 요소를 반환한다.
                ActionChains(driver).move_to_element(more_results_element).perform()  # "결과 더보기" 요소로 화면을 이동한다.
                more_results_element.click()  # 찾은 "결과 더보기"를 클릭한다.

        except Exception as e:  # 예외를 처리한다.
            print(e)  # 예외 메시지를 출력한다.
            print("All of the searched images have been saved.")  # 모든 이미지를 저장했음을 알린다.
            break  # 프로그램을 종료한다.

        if result_element.get_attribute("class") == "isv-r PNCib MSM1fd BUooTd":  # 해당 결과 요소가 이미지가 맞을 경우 수행한다.
            while path.isfile(f"Images/{file_name}/{file_name}_{file_number}.jpg"):  # 중복되는 파일 이름이 있는지 검사한다.
                file_number += 1  # 중복된다면 파일 이름에 적용할 번호를 1 증가시킨다.

            image_selector = f"#islrg > div.islrc > div:nth-child({element_number}) > a.wXeWr.islib.nfEiy.mM5pbd > " \
                             f"div.bRMDJf.islir > img "  # 이미지를 찾을 selector를 설정한다.
            image_locator = (By.CSS_SELECTOR, image_selector)  # selector를 locator로 지정한다.
            image_presence = expected_conditions.presence_of_element_located(image_locator)
            # 해당 요소가 존재하는지 확인하고 값을 반환한다.
            image_element = wait.until(image_presence)  # 찾은 요소를 반환한다.
            image_url = image_element.get_attribute("src")  # 찾은 이미지의 src 값을 반환한다.

            with request.urlopen(image_url) as f:  # 이미지 url을 with문으로 처리한다.
                image = f.read()  # 이미지를 읽고 보관한다.
            with open(f"Images/{file_name}/{file_name}_{file_number}.jpg", "wb") as f:  # 이미지 파일을 with문으로 처리한다.
                f.write(image)  # 이미지를 파일로 저장한다.

            print(image_number, image_url)  # 처리된 이미지의 번호와 url을 출력한다.
            image_number += 1  # 처리된 이미지의 번호를 증가시킨다.

        element_number += 1  # 찾을 결과 요소 번호를 1 증가시킨다.
