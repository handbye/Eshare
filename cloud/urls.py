from django.urls import  path
from cloud import views

app_name = 'cloud'

urlpatterns=[
    path('',views.index,name='index'),
    path('data/',views.datatables,name='data'),
]