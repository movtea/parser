from bs4 import BeautifulSoup
from selenium import webdriver
import requests

if __name__ == '__main__':
    r = requests.get('https://anime-conventions.ru/catalogue/')
    # Создаем объект BeautifulSoup путем разбора содержимого
    soup = BeautifulSoup(r.content, "html.parser")
    # Найдите все элементы с классом "post-title" и заголовком "h2"
    postTitles = soup.find("li", "active").findAll("a")
    # Пройдитесь по списку всех заголовков постов
    k = 0
    for i in postTitles:
        if i.text == "2025 год":
            # print(postTitle.text.strip())
            print(postTitles[k]['href'])
        k += 1
    # for i in soup.select(r'h3 > a'):
    #     print(i['href'])

    w = requests.get('https://anime-conventions.ru/convention/manukefest-winter-2025-c2187.html')
    ss = BeautifulSoup(w.content, "html.parser")
    arr = [
        ss.find(attrs={'class': 'duration'}).text.strip(),
        #ss.find('div', 'convention_container'),
        ss.find("h1").text.strip(),
        ss.find("div", "convention_inner_text").text.strip()
    ]

    for i in arr:
        print(i)
