from django.urls import path

from . import views


urlpatterns = [

path('records/',views.get_records),

path('records/create/',views.create_record),

path('records/update/<int:id>/',views.update_record),

path('records/delete/<int:id>/',views.delete_record),

path('summary/',views.summary),
path('check-role/',views.check_role),
path('test/', views.api_test_page),
path('add/', views.add_record_page),
path('', views.api_home),

]