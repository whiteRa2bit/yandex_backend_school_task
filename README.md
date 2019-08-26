# yandex_backend_school_task
Task for applying at Yandex Backend School

Интернет-магазин подарков хочет запустить акцию в разных регионах. Чтобы стратегия продаж была эффективной, необходимо произвести анализ рынка. У магазина есть поставщик, регулярно присылающий выгрузки данных с информацией о жителях. Проанализировав их, можно выявить спрос на подарки в разных городах у жителей разных возрастных групп по месяцам. Ваша задача - разработать на python REST API сервис, который сохраняет переданные ему наборы данных (выгрузки от поставщика) c жителями, позволяет их просматривать, редактировать информацию об отдельных жителях, а также производить анализ возрастов жителей по городам и анализировать спрос на подарки в разных месяцах для указанного набора данных. Должна быть реализована возможность загрузить несколько независимых наборов данных с разными идентификаторами, независимо друг от друга изменять и анализировать их.


To run project:
1) sudo apt-get install postgresql postgresql-contrib
2) sudo -u postgres createuser --superuser name_of_user
3) sudo -u name_of_user createdb name_of_database
4) pip install virtualenv
5) virtualenv env
6) source env/bin/activate
7) export APP_SETTINGS="config.DevelopmentConfig"
8) export DATABASE_URL="postgresql:///name_of_database"
9) python manage.py db init
10) python manage.py db migrate
11) python manage.py db upgrade
12) python manage.py runserver
