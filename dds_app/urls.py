from django.urls import path
from . import views

urlpatterns = [
    path('', views.DDSListView.as_view(), name='dds_list'),
    path('create/', views.DDSRecordCreateView.as_view(), name='dds_create'),
    path('update/<int:pk>/', views.DDSRecordUpdateView.as_view(), name='dds_update'),
    path('delete/<int:pk>/', views.DDSRecordDeleteView.as_view(), name='dds_delete'),
    path('manage/', views.manage_refs, name='manage_refs'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]
