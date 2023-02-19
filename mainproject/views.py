from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serilaizers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import jwt as JWT_
from django.db import IntegrityError
from JK.settings import SIMPLE_JWT
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.


class AuthorizateView(TokenObtainPairView):
    """Дефолтная авторизация через jwt """
    serializer_class = AuthorizateSerializer
    

class RegistrationView(generics.GenericAPIView):
    """Кастомная регистрация """
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerilizer
    def post(self, request):
        

        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(iin=serializer.data['iin'],email=serializer.data['email'])
        if user.exists():
            return Response({"error":"Пользователь уже существует в системе"},status=status.HTTP_400_BAD_REQUEST)

        else:
            new_user = User.objects.create_user(
                        iin = request.data["iin"],
                        first_name = request.data["first_name"],
                        last_name = request.data["last_name"],
                        password = request.data["password"],
                        email = request.data["email"],
                        )

            refresh = RefreshToken.for_user(new_user)
            return Response(
                    {
                    'user':serializer.data, 
                    'is_superuser':new_user.is_superuser,   
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    },
                    status=status.HTTP_201_CREATED)


class ProfileView(generics.GenericAPIView):
    serializer_class=UserSerilizer
    permission_classes = (AllowAny,)
    def get(self,request):
   

        queryset = self.get_queryset()
        serializer = UserSerilizer(queryset, many=True)

        return Response(serializer.data)

    def get_queryset(self):
        
        return User.objects.all()



class Filter_Data_User(generics.ListAPIView):


    queryset=User.objects.all()
    serializer_class = UserSerilizer
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['is_superuser',]


class BooksView(generics.GenericAPIView):
    serializer_class=BooksSerilizers
    permission_classes = (AllowAny,)
    def get(self,request):
   

        queryset = self.get_queryset()
        serializer = BooksSerilizers(queryset, many=True)

        return Response(serializer.data)

    def get_queryset(self):
        
        return Books.objects.all()

class AuthChecking(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        refresh_token_get = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
        jwt=JWT_.decode(
            refresh_token_get,
            SIMPLE_JWT['SIGNING_KEY'],
        algorithms = [SIMPLE_JWT['ALGORITHM']],
            )
        users =User.objects.get(id=jwt['user_id'])
 
        return Response(
                    {
                    'user':UserSerilizer(users).data, 
                    'is_superuser':users.is_superuser,   
                    },status=status.HTTP_200_OK)




class FilterBooks(generics.ListAPIView):
    """List of all books"""
    permission_classes = [AllowAny,]
    queryset = Books.objects.all()
    serializer_class = BooksSerilizers
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = {
      'age':['gte', 'lte', 'exact', 'gt', 'lt','range'],
      'date_add':['gte', 'lte', 'exact', 'gt', 'lt','range'],

  }

  
class BookAdd(generics.GenericAPIView):
    serializer_class = ManagerSerilizer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_book = Manager.objects.filter(book = Books.objects.get(id = request.data['book']))  
        if Books.objects.get(id = request.data['book']).count != 0:
            if (is_book.exists()):
                if(is_book.first().passed):
                    Bookscount =Books.objects.get(id = request.data['book'])
                    Bookscount.count = Bookscount.count - 1 
                    Bookscount.save()
                
                    data_object = Manager.objects.create(
                                user = User.objects.get(id = request.data['user']),
                                book = Books.objects.get(id = request.data['book']),
                                Date_end = request.data['Date_end']
                                )
                    return Response(ManagerSerilizerData(data_object).data,status=status.HTTP_201_CREATED)
                if(not is_book.first().passed):
                    return Response(status=status.HTTP_409_CONFLICT)
            Bookscount =Books.objects.get(id = request.data['book'])
            Bookscount.count = Bookscount.count - 1 
            Bookscount.save()        
            data_object = Manager.objects.create(
                                    user = User.objects.get(id = request.data['user']),
                                    book = Books.objects.get(id = request.data['book']),
                                    Date_end = request.data['Date_end']
                                    )
            return Response(ManagerSerilizerData(data_object).data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_410_GONE)


class DeleteUser(generics.GenericAPIView):
    serializer_class=UserDeleteSerilizer
    permission_classes = (IsAuthenticated,)
    def delete(self, request,pk, *args, **kwargs):
        user=User.objects.filter(id=pk)
        user.delete()
        return Response(status=status.HTTP_200_OK)



class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerilizer

    def get(self,request,pk):
        try:
            queryset = self.get_queryset(pk)
        except ObjectDoesNotExist:
            return Response([{"error":"Токого пользователя не существует"},])
        serializer = UserSerilizer(queryset)

        return Response(serializer.data)

    def get_queryset(self,pk):
        
        return User.objects.get(id=pk)



class BooksUserInfor(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserDeleteSerilizer

    def post(self,request):

        
        user=User.objects.get(id=request.data['id'])
        
        books = Manager.objects.filter(user = user)



        return Response( ManagerSerilizerData(books, many=True).data,status=status.HTTP_200_OK)


class PassedUserData(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserDeleteSerilizer

    def post(self,request):


        user=User.objects.get(id=request.data['id'])
        
        passedCount = Manager.objects.filter(user =  user ,passed = True).count()
        noPassedCount =  Manager.objects.filter(user =  user ,passed = False).count()
        allMnagaerCount = Manager.objects.all().count()
        data ={
            'passedCount':passedCount,
            'noPassedCount':noPassedCount,
            'allMnagaerCount':allMnagaerCount,
        }


        return Response(data ,status=status.HTTP_200_OK)


class BooksSearchView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerilizers
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


class BooksAdd(generics.GenericAPIView):
    serializer_class = BooksSerilizers
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        check = Books.objects.filter(name = request.data['name'])
  
        if not check.exists():
            book = Books.objects.create(
            name = request.data['name'],
            age = request.data['age'],
            photo = request.data['photo'],
            count = request.data['count']
        )
            return Response(BooksSerilizers(book).data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_409_CONFLICT)

        


class BooksUser(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request,pk, *args, **kwargs):
        user=Books.objects.filter(id=pk)
        user.delete()
        return Response(status=status.HTTP_200_OK)



class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerilizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['iin','first_name','last_name',]




class BooksPassedTrue(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDeleteSerilizer

    def post(self,request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        books=Manager.objects.get(id=request.data['id'])
        books.passed = True
        books.save() 
        book_count= Books.objects.get(id = books.book.id)
        book_count.count =  books.book.count + 1
        book_count.save()


        return Response(status=status.HTTP_200_OK)

from django.utils import timezone
class BeLate(generics.GenericAPIView):
    serializer_class=ManagerSerilizerBeLate
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        
        print(timezone.datetime.now())
        queryset = self.get_queryset()
        serializer = ManagerSerilizerBeLate(queryset, many=True)

        return Response(serializer.data)

    def get_queryset(self):
        
        return Manager.objects.filter(Date_end__lte = timezone.datetime.now(),passed = False)




class AnalisticCount(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        
        print(timezone.datetime.now())
        count_BeLate = Manager.objects.filter(Date_end__lte = timezone.datetime.now(),passed = False).count() 
        count = Manager.objects.filter(passed = False).count()
        procents = count_BeLate * 100 / count
    
  
        return Response({'type':'кешіккендер проценттік көріністе','value':procents},status=status.HTTP_200_OK)


        

class UserBeLateSearchView(generics.ListAPIView):
    queryset = Manager.objects.filter(Date_end__lte = timezone.datetime.now(),passed = False)
    serializer_class = ManagerSerilizerBeLate
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__iin','user__first_name','user__last_name',]




class NewsView(generics.GenericAPIView):
    serializer_class=NewsSerilizer
    permission_classes = (AllowAny,)
    def get(self,request):
   

        queryset = self.get_queryset()
        serializer = NewsSerilizer(queryset, many=True)

        return Response(serializer.data)

    def get_queryset(self):
        
        return News.objects.all()
