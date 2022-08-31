from django.urls import path
from . import views

urlpatterns = [

    path('book/<int:bookID>', views.book, name='book'),
    path('filter/<str:category>', views.filterCategory, name='filterCategory'),
    path('search/<str:searchBy>', views.searchAjax, name='searchAjax'),
    path('search/<str:searchValue>/<str:searchBy>', views.searchAjax, name='searchAjax'),
    path('HomePage/', views.search, name='search'),
    path('', views.search, name='search'),
    path('signup/', views.signUp, name='signUp'),
    path('signin/', views.signIn, name='signIn'),
    path('logout/', views.user_logout, name='logout'),
    path('addBook/', views.addBook, name='addBook'),
    path('userInfo/', views.userinfo, name='userinfo'),
    path('borrow/<int:id>,', views.borrow, name='borrow'),
    path('returnBook/<int:id>,', views.returnBook, name='return'),
    path('extend/<int:id>,', views.extend, name='extend'),

]
