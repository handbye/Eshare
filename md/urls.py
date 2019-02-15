from django.urls import  path
from md import views

app_name = 'md'

urlpatterns=[
    path('<name>/',views.mdtoHtml,name='md'),
]
