# Телеграм бот для создания QR-кодов о вакцинации
_Важно: этот инструмент был сделан исключительно в целях саморазвлечения, и при любом его использовании всю ответственность несет пользователь, разраб не при делах_

## Как запустить:
1. Создаем три переменные окружения - `DJANGO_GOS_DEBUG`, `DJANGO_GOS_SECRET_KEY`, и `TG_TOKEN_GOS`. Первая может быть 1 или 0 (лучше поставьте ноль), вторая — сделайте кучей рандомных символов, третья — токен от вашего бота в телеге.
2. В терминале прописываем `pip install -r requirements.txt`, дальше `python manage.py makemigrations`, `python manage.py migrate` и `python manage.py collectstatic`
3. В файле `gosusligi_copy/settings.py` также ставим наш `HOSTNAME` на тот домен, который вы купите. Ну или не купили, а воспользовались нжроком например.
4. Теперь, *в теории*, все готово. Чтобы запустить бота, пишем `python run_pooling.py`, а сайт - `python manage.py runserver 0.0.0.0:80`. НО

Будет много проблем. Во-первых, генерируемые коды не будут работать, т.к. у вас будет сайт стоять на http а не https. Во-вторых, на сайте не будут появляться все картинки (например картинка русского языка), т.к. статичные файлы не обрабатываются никем. Для этого нужно поставить сайт на nginx, а для этого чекайте классный туториал [здесь](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04) (часть с дб скипаете).

Там считается что вы ставите бота на линукс, но я надеюсь вы так и делаете, ибо иначе бог вам в помощь (не, ну конечно есть несколько способ это обойти, но для этого нужно немного пострадать, можете мне написать ради такого).


## Автор и важные упоминания
Автор - я, [VeryBigSad](https://github.com/verybigsad). Но также очень много было взято с [этого](https://github.com/ohld/django-telegram-bot) шаблона, который сделал замечательный и прекрасный [ohld](https://github.com/ohld).

## Добавлять код:
Я был бы рад увидеть пул реквесты, но тогда убедитесь, что:
1. у вас не говнокод (дада двойные стандарты они такие)
2. все в целом

Еще прошу осознавать, что этот бот вообще будет не актуален когда правительство снимет необходимость QR кодов когда ходишь в рестораны.


## лицензия
лицензии нет, делайте что хотите, но если будете делать что-то на основе этого бота то дайте мне кредит плиз
