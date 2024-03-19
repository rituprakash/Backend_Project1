from django.urls import path
from . import views
urlpatterns = [
    path('signup',views.signup,name='signup_api'),
    path('login', views.login, name='login_api'),
    path('addmedicine', views.add_medicine, name='addMedicine_api'),
    path('listmedicine', views.medicines_list, name='listmedicineapi'),
    path('api/search/', views.SearchAPIView.as_view() ,name = 'search_api'),
    path('<int:pk>/editmedicine', views.edit_medicine, name='editmedicineapi'),
    path('<int:pk>/deleteproduct', views.delete_medicine, name='deletemedicineapi'),
]

    