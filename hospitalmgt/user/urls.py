from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('log_in', views.log_in, name = 'log_in'),
    path('signout', views.signout, name = 'signout'),

    
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),   
    path('receptionist_dashboard', views.receptionist_dashboard, name='receptionist_dashboard'), 
    path('billing_Staf_dashboard', views.billing_Staf_dashboard, name='billing_Staf_dashboard'), 




    # user
    
    path('create-user/', views.create_user, name='create_user'), 
    path('user-list/', views.user_list, name='user_list'),
    path('delet_user/<int:user_id>/',views.delete_user,name='delete_user'), 
    path('edit_user/<int:id>/', views.edit_user, name='edit_user'),
    



    # doctor
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('doctor-list/', views.doctor_list, name='doctor_list'),
    path('edit_doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('delete-doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),


    # billing

    path('add_billing_record/<int:patient_id>/', views.add_billing_record, name='add_billing_record'),
    path('update_billing_record/<int:billing_record_id>/', views.update_billing_record, name='update_billing_record'),
    path('delete_billing_record/<int:billing_record_id>/', views.delete_billing_record, name='delete_billing_record'),
    path('patient_billing_history/<int:patient_id>/', views.get_patient_billing_history, name='patient_billing_history'),
    path('search_billing_records/', views.search_billing_records, name='search_billing_records'),


   
]  

