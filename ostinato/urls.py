from django.urls import path
from . import views

urlpatterns = [
    path('', views.index ),
    path('register', views.register),
    path('home', views.home),
    path('login', views.login),
    path('logout', views.logout),
    path('user_profile/<int:id>', views.favorites),
    path('comment/<int:post_id>', views.post_comment),
    path('post_message', views.create_post),
    path('delete_comment/<int:id>', views.delete_comment),
    path('delete_post/<int:id>', views.delete_post),
    path('like/<int:id>', views.add_likes),
    path('edit/<int:user_id>', views.edit),
    path('update/<int:user_id>', views.update),
    path('avatar', views.avatar),
    path('upload', views.upload),
    path('delete_image/<int:id>', views.delete_image),
    path('set_picture/<int:id>', views.set_picture),
]