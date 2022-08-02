﻿## Веб API приложение с данными Книг и Авторами

### Отображает данные с Авторами по ссылке: /authors/
#### Отображает следующие данные: ['id', 'name', 'last_name', 'birth_year']
#### Возможна фильтрация по имени автора
* URL: authors/?name=имя_автора

### Отображает данные с Книгами по ссылке: /books/
#### Отображает следующие данные: ['id', 'author', 'name', 'isbn', 'release_year', 'page_count']
#### Возможна фильтрация по названию и id_автора:
* URL: /books/?name="название_книги"&author=id_автора
#### Возможна фильтрация по количеству страниц:
* URL: /books/?equally=50 - точное значение "50"
* URL: /books/?min=50 - больше "50"
* URL: /books/?max=50 - меньше "50"
#### Документация доступна по ссылке:
* URL: /swagger

