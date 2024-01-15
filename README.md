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

## Try it

Попробовать сервис можно здесь [Service API](http://ars.fvds.ru:5000/docs)

## Data download endpoints
Данные в формате csv  
[user_data](http://ars.fvds.ru:5000/download/user_data) - 11.25 Mb  
[post_text_df](http://ars.fvds.ru:5000/download/post_text_df) - 9.2 Mb  
[post_text_df](http://ars.fvds.ru:5000/download/feed_data) - 2.68 Gb    

## Deploy
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
