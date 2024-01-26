# SocialNet-RecSys
Рекомендательная система постов для ленты социальной сети / RecSys for a social network feed

![image](https://github.com/avfawkes/SocialNet-RecSys/assets/65026452/4442ec94-7e74-4326-a70b-f47a558d6944)

## Оглавление/ Table of contents
 - [Цель проекта](#Цель-проекта/-Project-focus)
 - [Этапы проекта](#Этапы-проекта/-Project-stages)
 - [В планах](#В-планах/-Backlog)
 - [Технологии](#Технологии/-Technology-stack)
 - [Структура репозитория](#Структура-репозитория/-Repo-navigation)
 - [Попробовать](#Попробовать/-Try-it)
 - [Скачать данные](#Скачать-данные/-Data-download-endpoints)
 - [Развернуть приложение](#Развернуть-приложение/-Deploy)
 - [Поддержка](#Поддержка/-Support)

### Цель проекта/ Project focus
Создание контентной рекомендательной системы постов для ленты социальной сети. При регистрации пользователи заполняют данные своего профиля. Так же платформа обладает лентой, которую пользователи могут листать и просматривать случайные записи случайных сообществ. Если пост нравится, можно поддержать автора и поставить like. Все действия пользователей сохраняются, каждая их активность, связанная с просмотром постов, записывается в базу.  
Реализованный RESP API сервис позволяет рекомендовать пользователю посты. Доступен endpoint для сравнения рекомендаций модели со случайными для проведения AB эксперимента.

### Этапы проекта/ Project stages
- Реализация подключения к PostgreSQL базе и загрузка данных. Изначально планировалось загружать чанками, т.к. Pandas при выполнении SQL запроса требует [в 4 раза больше памяти](https://pythonspeed.com/articles/pandas-sql-chunking/) чем размер данных и одна из таблиц достаточно большая. Но в итоге её полностью загружать не пришлось и решение упростил. Также создал FastAPI сервис и эндпоинт для получения рекомендаций, который будет принимает параметры `id` и `limit` и возвращать топ `limit` рекомендованных постов для пользователя с указанным `id`.
- Создание бэйзлайн модели для рекомендации постов на основании числовых и категориальных признаков. Обработка признаков, кодирование, эксперименты с разными "деревянными" моделями Sklearn. Остановился на CatBoost, т.к. он дал лучший AUC.
- Улучшение модели с помощью обработки текста постов. Векторизовал текст энкодером трансформера BERT и добавлял эмбеддинги как числовые признаки. Также пробовал признак расстояния до центра кластера этих эмбеддингов. Но в итоге CatBoost опять же справился лучше с обработкой текста. Насколько я смог разобраться, подход также в векторизации и генерации признаков на основе LDA, KNN.
- Добавил эндпоинт для проведения АБ эксперимента между рекомендациями случайными и модели. Пользователи солятся по id с помощью MD5. Получил контрольную и тестовую группу, с помощью биномиального теста убедился, что разбиение соответствует требуемому. Метрика "число лайков на пользователя" распределена логнормально, поэтому применил критерий Манна-Уитни-Уилкоксона, показавший статистически значимое различие между группами.

### В планах/ Backlog
- Попробовать разные параметры токенизации текста катбуст (лемматизация, stop слова)
- Попробовать векторы энкодера BERT в embeding features CatBoost
- Попробовать архитектуры DL комбинирующие контентный подход и факторизацию
- ...

---

### Технологии/ Technology stack
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

### Структура репозитория/ Repo navigation 
 - [app](https://github.com/avfawkes/SocialNet-RecSys/tree/main/app) - собственно код приложения
 - [data](https://github.com/avfawkes/SocialNet-RecSys/tree/main/data) - структура таблиц БД и сэмплы данных
   - `user_data` - пользователи и их признаки 163205 записей
   - `post_text_df` - тексты постов и их категория 7023 записей
   - `feed_data` - журнал взаимодействия пользователей с постами и информация о лайках. 76892800 записей
 - [train](https://github.com/avfawkes/SocialNet-RecSys/tree/main/train) - ноутбук обучения модели. Также можно посмотреть на [Kaggle](https://www.kaggle.com/avfawkes/socialnet-recsys)

### Попробовать/ Try it
![Service Healthcheck](https://img.shields.io/badge/dynamic/json?url=http%3A%2F%2Fars.fvds.ru%3A5000%2Fhealthcheck&query=%24.status&style=for-the-badge&logo=fastapi&label=Service%20Healthcheck&link=http%3A%2F%2Fars.fvds.ru%3A5000%2Fhealthcheck&link=http%3A%2F%2Fars.fvds.ru%3A5000%2Fhealthcheck)  
Попробовать сервис можно здесь [`Service API`](http://ars.fvds.ru:5000/docs)

### Скачать данные/ Data download endpoints
Данные в формате csv  
[user_data](http://ars.fvds.ru:5000/download/user_data) - 11.25 Mb  
[post_text_df](http://ars.fvds.ru:5000/download/post_text_df) - 9.2 Mb  
[post_text_df](http://ars.fvds.ru:5000/download/feed_data) - 2.68 Gb    

### Развернуть приложение/ Deploy
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

### Поддержка/ Support
Если у вас возникли сложности или вопросы, создайте [`обсуждение`](https://github.com/avfawkes/SocialNet-RecSys/issues/new/choose) в данном репозитории
