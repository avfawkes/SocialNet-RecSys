# SocialNet-RecSys
Рекомендательная система постов для ленты социальной сети / RecSys for a social network feed

![image](https://github.com/avfawkes/SocialNet-RecSys/assets/65026452/4442ec94-7e74-4326-a70b-f47a558d6944)

Контентная рекомендательная система постов для ленты социальной сети. При регистрации пользователи заполняют данные своего профиля. Так же платформа обладает лентой, которую пользователи могут листать и просматривать случайные записи случайных сообществ. Если пост нравится, можно поддержать автора и поставить like. Все действия пользователей сохраняются, каждая их активность, связанная с просмотром постов, записывается в базу. Реализованный RESP API сервис позволяет рекомендовать пользователю посты. Доступен endpoint для сравнения рекомендаций модели со случайными для проведения AB эксперимента.
 - [app](https://github.com/avfawkes/SocialNet-RecSys/tree/main/app) - собственно код приложения
 - [data](https://github.com/avfawkes/SocialNet-RecSys/tree/main/data) - структура таблиц БД и сэмплы данных
   - `user_data` - пользователи и их признаки 163205 записей
   - `post_text_df` - тексты постов и их категория 7023 записей
   - `feed_data` - журнал взаимодействия пользователей с постами и информация о лайках. 76892800 записей
 - [train](https://github.com/avfawkes/SocialNet-RecSys/tree/main/train) - ноутбук обучения модели. Также можно посмотреть на [Kaggle](https://www.kaggle.com/avfawkes/socialnet-recsys)

## Технологии/ Technology stack
<!--
![Python](https://img.shields.io/badge/Python-blue?logo=python&logoColor=%23ffd845&color=%233f7daf)
![Pandas](https://img.shields.io/badge/Pandas-%23150458?logo=pandas)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-blue?logo=SQLAlchemy&logoColor=black&color=%23d71f00)
![CatBoost](https://img.shields.io/badge/CatBoost-%23ffcc00)
![Scipy](https://img.shields.io/badge/Scipy-white?logo=scipy&labelColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-white?logo=fastapi)
-->
![Python](https://img.shields.io/badge/Python-%233f7daf?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-%23f37726?logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-%23150458?logo=pandas&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-blue?logo=SQLAlchemy&logoColor=white&color=%23d71f00)
![CatBoost](https://img.shields.io/badge/CatBoost-%23ffcc00)
![Scipy](https://img.shields.io/badge/Scipy-%230054a6?logo=scipy&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-%23009485?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-%231D63ED?logo=docker&logoColor=white)

## Попробовать/ Try it
![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=http%3A%2F%2Fars.fvds.ru%3A5000%2Fhealthcheck&query=%24.status&style=for-the-badge&logo=fastapi&label=Service%20Healthcheck&link=http%3A%2F%2Fars.fvds.ru%3A5000%2Fhealthcheck&link=http%3A%2F%2Fars.fvds.ru%3A5000%2Fhealthcheck)  
Попробовать сервис можно здесь [Service API](http://ars.fvds.ru:5000/docs)

## Скачать данные/ Data download endpoints
Данные в формате csv  
[user_data](http://ars.fvds.ru:5000/download/user_data) - 11.25 Mb  
[post_text_df](http://ars.fvds.ru:5000/download/post_text_df) - 9.2 Mb  
[post_text_df](http://ars.fvds.ru:5000/download/feed_data) - 2.68 Gb    

## Развернуть приложение/ Deploy
1. Клонировать или загрузить репозиторий
   
    ```
    git clone --depth 1 'https://github.com/avfawkes/SocialNet-RecSys.git' && rm -rf SocialNet-RecSys/.git
    ```
    ```
    curl -L "https://github.com/avfawkes/SocialNet-RecSys/archive/main.tar.gz" | tar -xzf -
    ```
2. Переименовать `db_creds_template.yaml` в `db_creds.yaml` указав реквизиты доступа к БД
3. Запустить
    ```
    sudo docker compose up
    ```
