from django.urls import path, re_path
from . import views

urlpatterns = [
   path('put/', views.put),
   path('content/<int:id>/', views.content, name='box'),
   path('content/<int:id>/next/', views.next_content),
   path('content/<int:id>/comment/', views.comment),
   path('content/<int:id>/<int:id2>/comment2/', views.comment2),
   path('content/<int:id>/delete/<int:id2>/', views.com_del),
   path('<int:id>/ad_delete/', views.ad_box_del),
   path('<int:id>/delete/', views.box_del),
   path('content/<int:id>/delete2/<int:id2>/', views.com_del2),
   path('search/school/',views.search_school),
]