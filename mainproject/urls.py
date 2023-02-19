from django.urls import path

from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # auth
    path('api/v1/login/', AuthorizateView.as_view(), name='token_obtain_pair'),
    path('api/v1/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/register/', RegistrationView.as_view()),
    path('api/v1/user/all/', ProfileView.as_view()),
    path('api/v1/filter/user/', Filter_Data_User.as_view()),
    path('api/v1/filter/books/', FilterBooks.as_view()),
    path('api/v1/books/all/', BooksView.as_view()),
    path('api/v1/user/check/', AuthChecking.as_view()),
    path('api/v1/books/user/add', BookAdd.as_view()),
    
    
    
    path('api/v1/user/delete/<int:pk>',DeleteUser.as_view()),
    path('api/v1/user/detail/<int:pk>',UserDetail.as_view()),
    path('api/v1/user/books/detail',BooksUserInfor.as_view()),
    path('api/v1/user/books/analis/passed',PassedUserData.as_view()),
    path('api/v1/user/books/search/',BooksSearchView.as_view()),

    path('api/v1/books/add/',BooksAdd.as_view()),
    path('api/v1/books/detail/<int:pk>',BooksUser.as_view()),
    path('api/v1/user/search/',UserSearchView.as_view()),
    path('api/v1/books/passed/',BooksPassedTrue.as_view()),
    path('api/v1/user/be_late/',BeLate.as_view()),
    path('api/v1/user/books/analic/',AnalisticCount.as_view()),
    path('api/v1/user/books/beLate/search/',UserBeLateSearchView.as_view()),
    path('api/v1/news/all/',NewsView.as_view())


    


]