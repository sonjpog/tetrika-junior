#  Тестовые задания для онлайн-школы Тетрика

##  Task1

Реализация декоратора @strict . Декоратор проверяет соответствие типов переданных в вызов функции аргументов типам аргументов, объявленным в прототипе функции.

### Пример работы:

```yaml
@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(1, 2))      # Выведет 3
print(sum_two(1, 2.4))    # Вызовет TypeError: Argument 'b' must be of type int, not float
```



##  Task2

Скрипт, который парсит список всех животных из википедии (https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту) и записывать в файл в формате beasts.csv количество животных на каждую букву алфавита.

###  Как запустить и проверить:

1. Установите зависимости: 


```yaml
pip install requests beautifulsoup4
```

2. Запустите скрипт: 

```yaml
python3 task2.py
```

3. Можно посмотреть созданный файл в папке проекта или вызвать командой: 

```yaml
cat beasts.csv
```



##  Task3

Реализация функции ```appearance```, которая получает на вход словарь с интервалами и возвращает время общего присутствия ученика и учителя на уроке (в секундах).