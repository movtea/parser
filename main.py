from bs4 import BeautifulSoup
import sqlite3 as sql
import requests

import pandas as ps
import streamlit as sl

def create_db():
    data_base = sql.connect('data_html_parser.db')
    with data_base:
        query = data_base.cursor()
        query.execute('CREATE TABLE IF NOT EXISTS data_from_html '
                        '(id        int PRIMARY KEY, '
                        'name       VARCHAR(127), '
                        'age        int,'
                        'duration   VARCHAR(127), '
                        'city       VARCHAR(63), '
                        'desc       VARCHAR(8182), '
                        'link       VARCHAR(255));'
        )
        query.execute('DELETE FROM data_from_html;')
        query.close()
    return data_base

def write_in_db(array, data_base):
    with data_base:
        query = data_base.cursor()
        query.execute("INSERT INTO data_from_html (name, age, duration, city, desc, link) VALUES ('" + str(array[0]) + "', '" + str(array[1]) + "', '" + str(array[2]) + "', '" + str(array[3]) + "', '" + str(array[4]) + "', '" + str(array[5]) + "');")
        query.close()

def collect_link(target, target_age):
    print("Выполняется поиск в " + str(target_age ))
    target_site = requests.get(target)

    if target_site.status_code != 200:
        print("Ошибка открытия сайта: ", target_site.status_code)
        quit()

    target_html = BeautifulSoup(target_site.content, 'html.parser')
    
    links_age = []
    zero = 0

    if target_age == 2025:
        li_html = target_html.find('li', 'active').findAll('a')
        for target in li_html:
            if target.text == str(target_age) + ' год':
                page_age = li_html[zero]['href']
                print("Определенная начальная страница - " + str(page_age))
            zero += 1
    else:
        target_site = requests.get(target + str(age) + ".html")
        target_html = BeautifulSoup(target_site.content, 'html.parser')

    for link in target_html.select(r'h3 > a'):
        links_age.append(link['href'])
    
    return links_age

def formater(target_site):
    return target_site.find(attrs={'class': 'duration'}).text.strip().replace("\n", "").replace("\t", "").replace("\r", "").split("|")

def parser(link, age):
    parsing = requests.get(link)
    target_site = BeautifulSoup(parsing.content, "html.parser")

    query_name = target_site.find("h1").text.strip().replace("'", "`")
    query_age = age
    query_duration, query_city = formater(target_site)
    query_desc = target_site.find("div", "convention_inner_text").text.strip().replace("'", "`")
    query_link = target_site.find("a", "btn btn-link")["href"]

    return [query_name, query_age, query_duration, query_city, query_desc, query_link]

if __name__ == '__main__':
    sl.title("Парсер группы ...")
    sl.write("Программа для сбора и записи данных с предложенного сайта! "
    "Ниже будет представлена таблица данных, записанная из файла базы данных по пути ./data_html_parser.db")

    anime = 'https://anime-conventions.ru/catalogue/'
    n_ages = 5
    ages = []

    for i in range(n_ages):
        ages.append(2025 - i)
    data_base = create_db()
    for age in ages:  
        link_age = collect_link(anime, age)
        for link in link_age:
            write_in_db(parser(str(link), age), data_base)
    
    print("Поиск окончен")
    sl.write(ps.read_sql("SELECT name as 'Название мероприятия', "
                                "age as 'Год проведения', "
                                "duration as 'Продолжительность', "
                                "city as 'Город проведения', "
                                "desc as 'Описание', "
                                "link as 'Ссылка на мероприятие' "
                                "FROM data_from_html", data_base))