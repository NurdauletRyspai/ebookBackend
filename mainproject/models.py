from django.db import models
from django.conf import settings 
from django.contrib.auth.models import (
	AbstractBaseUser, PermissionsMixin
)

from datetime import datetime, timedelta

from .Manager import UserManager






class User(AbstractBaseUser, PermissionsMixin):
    
    # Каждому пользователю нужен понятный человеку уникальный идентификатор,
    # который мы можем использовать для предоставления User в пользовательском
    # интерфейсе. Мы так же проиндексируем этот столбец в базе данных для
    # повышения скорости поиска в дальнейшем.
    iin = models.IntegerField(db_index=True, verbose_name='ИИН', unique=True)
    first_name=models.CharField(db_index=True,verbose_name='Аты',max_length=150)
    last_name=models.CharField(db_index=True,verbose_name='Тегі',max_length=150)
    email=models.EmailField(db_index=True,verbose_name='Электрондық пошта', unique=True)
    date_register = models.DateTimeField(auto_now_add=True , verbose_name="Тіркелген уақыты")
        
    # Когда пользователь более не желает пользоваться нашей системой, он может
    # захотеть удалить свой аккаунт. Для нас это проблема, так как собираемые
    # нами данные очень ценны, и мы не хотим их удалять :) Мы просто предложим
    # пользователям способ деактивировать учетку вместо ее полного удаления.
    # Таким образом, они не будут отображаться на сайте, но мы все еще сможем
    # далее анализировать информацию.
    is_active = models.BooleanField(default=True)

    # Этот флаг определяет, кто может войти в административную часть нашего
    # сайта. Для большинства пользователей это флаг будет ложным.
    is_staff = models.BooleanField(default=False,verbose_name='Персонал')

    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)

    # Дополнительный поля, необходимые Django
    # при указании кастомной модели пользователя.

    # Свойство iin сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'iin'
    REQUIRED_FIELDS = ['email','first_name','last_name',]

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова Author.token, вместо
        iin._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать iin.
        """
        return self.iin

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.iin

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
    
    class Meta:
        ordering = ['id']
        verbose_name='қолданушы'
        verbose_name_plural='Қолданушылар'

    def __str__(self):
        return "{}".format(self.iin)


class Books(models.Model):
    name = models.CharField(verbose_name="Кітап аты",max_length=255)
    age = models.IntegerField(verbose_name="Нешінші жылғы кітап",default=2023)
    photo = models.ImageField(verbose_name="Кітап фотосы")
    date_add = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(verbose_name="Кітап саны",default=1)
    
    def __str__(self):
        return (f"{self.name}")
    class Meta:
        ordering = ['-id']
        verbose_name='кітап'
        verbose_name_plural='Кітаптар'


class Manager(models.Model):
    user = models.ForeignKey(User,verbose_name='Қолданушы', on_delete=models.CASCADE)
    book = models.ForeignKey(Books,verbose_name='Кітап', on_delete=models.CASCADE)
    Date_start = models.DateTimeField(auto_now_add=True , verbose_name="Алған уақыты")
    Date_end = models.DateTimeField(verbose_name="Қайтару уақыты")
    commoner = models.BooleanField(verbose_name="Кешігу(болса)",default=False)
    commoner_time = models.DateTimeField(verbose_name="Кешігу уақыты(болса)",null=True,blank=True)
    passed = models.BooleanField(verbose_name="Тапсырды",default=False)

    def __str__(self):
        return (f"{self.user}")
    class Meta:
        ordering = ['-id']
        verbose_name='менеджер'
        verbose_name_plural='менеджер'
    
   

class News(models.Model):
    name = models.CharField(verbose_name="Жаңалық аты",max_length=255,unique=True)
    image =  models.ImageField(verbose_name="Жаңалық фотосы")
    descriptionNews = models.TextField(verbose_name="Жаңалық сипаттамасы")

    def __str__(self):
        return (f"{self.name}")
    class Meta:
        ordering = ['-id']
        verbose_name='жаңалық'
        verbose_name_plural='Жаңалықтар'
    