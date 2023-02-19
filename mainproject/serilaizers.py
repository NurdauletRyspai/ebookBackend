from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist




#Author model 

class UserSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = 'id','first_name','last_name','iin','email','is_superuser','date_register',


class RegisterSerilizer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
        label="Пароль"

    )
    class Meta:
        model = User
        fields = 'first_name','password','last_name','iin','email',

class LogoutSerilizers(serializers.Serializer):
    refresh_token = serializers.CharField(
        write_only=True,
        label="Refresh токен"

    )


class AuthorizateSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
        label="Пароль"

    )
    iin = serializers.IntegerField(

        write_only=True,
        label="ИИН"

    )
    class Meta:

        fields = 'password','iin',

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = UserSerilizer(User.objects.get(iin= user.iin)).data
       
        return data




class BooksSerilizers(serializers.ModelSerializer):
    
    class Meta:
        model = Books
        fields = '__all__'


class ManagerSerilizer(serializers.Serializer):
    user = serializers.IntegerField(

        write_only=True,
        label="ID Пользователя"

    )
    book =  serializers.IntegerField(

        write_only=True,
        label="ID Книги"

    )

    Date_end = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M",  
        write_only=True,
        label=" когда должен вернуть книгу")

    class Meta:
        
        fiels = 'user','book','Date_end',


class ManagerSerilizerData(serializers.ModelSerializer):
    book = BooksSerilizers()
    class Meta:
        model = Manager
        fields = '__all__'


class UserDeleteSerilizer(serializers.Serializer):
    id = serializers.IntegerField(        
        write_only=True,
        label="ID Пользователя"
        )

    class Meta:
        fields = 'id',


class ManagerSerilizerBeLate(serializers.ModelSerializer):
    user = UserSerilizer()
    book = BooksSerilizers()

    class Meta:
        model = Manager
        fields = '__all__'


class NewsSerilizer(serializers.ModelSerializer):
    class Meta:
        models = News
        fields = '__all__'