# FS_Test_task_1
## Первое тестовое задание Focus Start 2020

Напишите web-сервис на python, у которого будет html страничка с кнопкой upload mp3.
Web-сервис должен преобразовать аудиозапись в изображение её частотного спектра и
показать на странице. Можете использовать любой ваш любимый python веб-фреймворк.
Если не знаете за что браться, можете посмотреть:
a. Python Flask Tutorial https://www.youtube.com/watch?v=MwZwr5Tvyxo
b. Uploading Files http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
c. Discrete Fourier transform:
https://librosa.github.io/librosa/generated/librosa.core.stft.html?highlight=stft

## Заметки по выполнению задания

+ Любимый фреймворк отсутствует, раньше пробовал только Django. Разворачивать Django
ради такого маленького приложения посчитал нецелесообразным, Flask показался более 
приемлемым. Использовал его.
+ На тестовом сервере flask приложение работает хорошо, ручное тестирование прошло без 
ошибок. Попытался сделать deploy на Heroku, пока не смог победить установку ffmpeg на
их сервер, то есть приложение запускается и ломается при попытке загрузить файл. 
