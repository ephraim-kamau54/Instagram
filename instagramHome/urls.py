from django.urls import path
from . import views

urlpatterns = [
    path('Phome', views.home, name='instagramHome-home'),
    path('Pabout/', views.about, name='instagramHome-about'),
    path('new_post/', views.add_post, name='add_post'),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path('<int:pk>',views.like, name='likes'),
    # path('register/', views.user_views.register, name='register'),
]