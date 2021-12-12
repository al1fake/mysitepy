# mysitepy
Проект представляет из себя сайт для статей.

В проекте присутствуют модели Question(хранит в себе текст статьи, описание, картинку и дату создания) 
и Comment(хранит в себе адрес на статью, имя написавшего, текст комментария, и айди написавшего пользователя).

Регистрация реализована через стандарные средства Django.

Доступ к сайту можно получить при запуске проекта локально или перейдя по ссылке http://al1fake.pythonanywhere.com/polls/.
Доступ к API сайта можно получить по ссылке https://al1fake.pythonanywhere.com/api/comments/ (доступ только залогиненым пользователям, через API можно удалять комментарии которые 
вы создали)
