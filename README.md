# Publishing-comics-on-Vkontakte

Publishing-comics-on-Vkontakte - это публикация комиксов во Вконтакте

### Как установить

Нужно создать файл .env и занести в него следующие данные: клиент ID и access токен.

Получить access токен нужно будет по даннной ссылке: https://oauth.vk.com/authorize?client_id=7777777&scope=photos,groups,wall,offline&display=page&response_type=token&v=5.131&state=123456 .

(В ссылке надо будет указать свой клиент ID)

[Получить клиент ID можно после ригистрации приложения](https://vk.com/editapp?act=create)

Пример файла .env
```
CLIENT_ID=[ваш клиент ID]
ACCESS_TOKEN=[ваш access токен]
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Пример работы скрипта в случае штатной ситуации:
Скрипт main.py публикует комикс.
Для запуска скрипта напишите в терминале: 
```
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
