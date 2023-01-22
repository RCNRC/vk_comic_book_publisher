# vk_comic_book_publisher

Программа, при запуске постящая в группу ВК случайный комикс с сайта [xkcd](https://xkcd.com/).

# Требования к использованию

Требуется [Python](https://www.python.org/downloads/) версии 3.7 или выше и установленный [pip](https://pip.pypa.io/en/stable/getting-started/). Для установки необходимых зависимостей используйте команду:  
- Для Unix/macOs:
```commandline
python -m pip install -r requirements.txt
```
- Для Windows:
```commandline
py -m pip download --destination-directory DIR -r requirements.txt
```

# Установка и подготовка

1. Скачать репозиторий.
2. Создать файл `.env` в корне репозитория.
3. Зарегистрроваться в [ВК](https://vk.com).
4. Создать группу ВК, на [этой](https://vk.com/groups?tab=admin) странице.
5. Поместить в файл `.env` строку `VK_GROUP_ID=id_группы`, где вместо строчки `id_группы` поместить свой ID группы, который можно узнать [здесь](https://regvk.com/id/).
6. Создать приложение standalone ВК приложение [здесь](https://vk.com/dev). На вкладке настроек приложеня взять ID приложения для дальнейшей аутентификации.
7. Используюя ID приложения получить ключ доступа по (этой)[https://dev.vk.com/api/access-token/implicit-flow-user] инструкции для приложения, выдав соответствующие разрешения для приложения.
8. Поместить в файл `.env` строку `VK_APP_API_ACCESS_TOKEN=ключ_доступа`, где вместо строчки `ключ_доступа` поместить свой ключ доступа.

# Использование

Запустить как Python3 скрипт.

## publish.py

При запуске публекует рандомное изображение в группу. Ничего не выводит в терминал.

## comics_download.py

При запуске скачивает в папку `images` случайный комикс. Ничего не выводит в терминал.