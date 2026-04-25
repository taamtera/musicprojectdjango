from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Link
    path('', views.index, name='index'),
    path('popup-callback/', views.popup_callback, name='popup-callback'),
    path('dev-login/', views.dev_login, name='dev-login'),
    
    # Audio serving with range request support
    path('media/songs/<str:filename>', views.serve_audio, name='serve-audio'),

    # Users
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<str:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('users/<str:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),

    # Songs
    path('songs/', views.SongListView.as_view(), name='song-list'),
    path('songs/create/', views.SongCreateView.as_view(), name='song-create'),
    path('songs/<str:pk>/update/', views.SongUpdateView.as_view(), name='song-update'),
    path('songs/<str:pk>/delete/', views.SongDeleteView.as_view(), name='song-delete'),
    path('songs/callback/<str:token>/', views.SongCallbackView.as_view(), name='song-callback'),

    # Shares
    path('shares/', views.ShareLinkListView.as_view(), name='sharelink-list'),
    path('shares/create/', views.ShareLinkCreateView.as_view(), name='sharelink-create'),
    path('shares/<str:pk>/update/', views.ShareLinkUpdateView.as_view(), name='sharelink-update'),
    path('shares/<str:pk>/delete/', views.ShareLinkDeleteView.as_view(), name='sharelink-delete'),
]
