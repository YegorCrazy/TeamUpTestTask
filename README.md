Это - небольшой сервис, хранящий результаты тестов IQ и EQ, написанный на Django (ссылка на [задание](https://docs.google.com/document/d/1nGKb9hiPk8kvRwyGI7tcwvv8B1NK2XcWuI-bkDI2-v0/edit)). В репозитории хранится файл spec.yaml со спецификацией API на OpenAPI.

**Запуск**

После клонирования репозитория необходимо выполнить следующие команды (необходимы Python и Poetry):

```
poetry shell
poetry install
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0
```

**Запуск тестов**

```
python3 manage.py test
```

**Примеры использования API**

Считаем, что сервис слушает на localhost:8000.

1) Создание нового теста:
   
   ```
   curl --request POST \
     --url http://localhost:8000/tests/create/ \
     --header 'Content-Type: application/json' \
     --data '{}'
   ```
   
   Пример ответа:
   
   ```
   {
   	"test_login": "vkrQYwawTy"
   }
   ```
2. Ввод результатов теста IQ:
   
   ```
   curl --request POST \
     --url http://localhost:8000/tests/add_result/iq/ \
     --header 'Content-Type: application/json' \
     --data '{
   	"test_login": "vkrQYwawTy",
   	"points": 29
   }'
   ```
   
   Пример ответа:
   
   ```
   {
   	"test_login": "vkrQYwawTy",
   	"test_result": {
   		"points": 29,
   		"answer_datetime": "2023-06-09T17:23:41.527Z"
   	}
   }
   ```

3. Ввод результатов теста EQ:
   
   ```
   curl --request POST \
     --url http://localhost:8000/tests/add_result/eq/ \
     --header 'Content-Type: application/json' \
     --data '{
   	"test_login": "vkrQYwawTy",
   	"answer": "аббвд"
   }'
   ```
   
   Пример ответа:
   
   ```
   {
   	"test_login": "vkrQYwawTy",
   	"test_result": {
   		"answer": "аббвд",
   		"answer_datetime": "2023-06-09T17:24:18.200Z"
   	}
   }
   ```

4. Получение результатов тестов:
   
   ```
   curl --request GET \
     --url http://localhost:8000/tests/get_result/vkrQYwawTy/
   ```
   
   Пример ответа:
   
   ```
   {
       "test_login": "vkrQYwawTy",
       "test_result": {
           "answer": "аббвд",
           "answer_datetime": "2023-06-09T17:24:18.200Z"
       }
   }
   ```
