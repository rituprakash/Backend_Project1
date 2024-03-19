

from django.urls import path
from .views import signup_page, login_page, user_logout, medicines_list, edit_medicine,  delete_medicine, add_medicine, home

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_page, name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', user_logout, name='logout'), 
    path('medicines/', medicines_list, name='medicines_list'),
    path('add_medicine/', add_medicine, name='add_medicine'),
    path('add_medicine/<int:medicine_id>/', add_medicine, name='edit_existing_medicine'),
    path('edit_medicine/<int:medicine_id>/', edit_medicine, name='edit_medicine'),
    path('delete_medicine/<int:medicine_id>/', delete_medicine, name='delete_medicine'),
    path('signup/login/', login_page, name='login'),
   

   
]
