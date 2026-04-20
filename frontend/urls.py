from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Link
    path('', views.index, name='index'),
    path('popup-callback/', views.popup_callback, name='popup-callback'),

    # Users
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),

    # Songs
    path('songs/', views.SongListView.as_view(), name='song-list'),
    path('songs/create/', views.SongCreateView.as_view(), name='song-create'),
    path('songs/<int:pk>/update/', views.SongUpdateView.as_view(), name='song-update'),
    path('songs/<int:pk>/delete/', views.SongDeleteView.as_view(), name='song-delete'),



    # Shares
    path('shares/', views.ShareLinkListView.as_view(), name='sharelink-list'),
    path('shares/create/', views.ShareLinkCreateView.as_view(), name='sharelink-create'),
    path('shares/<int:pk>/update/', views.ShareLinkUpdateView.as_view(), name='sharelink-update'),
    path('shares/<int:pk>/delete/', views.ShareLinkDeleteView.as_view(), name='sharelink-delete'),
]
