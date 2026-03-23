from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Link
    path('', views.index, name='index'),

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

    # Libraries
    path('libraries/', views.LibraryListView.as_view(), name='library-list'),
    path('libraries/create/', views.LibraryCreateView.as_view(), name='library-create'),
    path('libraries/<int:pk>/update/', views.LibraryUpdateView.as_view(), name='library-update'),
    path('libraries/<int:pk>/delete/', views.LibraryDeleteView.as_view(), name='library-delete'),

    # LibraryEntries
    path('entries/', views.LibraryEntryListView.as_view(), name='libraryentry-list'),
    path('entries/create/', views.LibraryEntryCreateView.as_view(), name='libraryentry-create'),
    path('entries/<int:pk>/update/', views.LibraryEntryUpdateView.as_view(), name='libraryentry-update'),
    path('entries/<int:pk>/delete/', views.LibraryEntryDeleteView.as_view(), name='libraryentry-delete'),

    # Shares
    path('shares/', views.ShareLinkListView.as_view(), name='sharelink-list'),
    path('shares/create/', views.ShareLinkCreateView.as_view(), name='sharelink-create'),
    path('shares/<int:pk>/update/', views.ShareLinkUpdateView.as_view(), name='sharelink-update'),
    path('shares/<int:pk>/delete/', views.ShareLinkDeleteView.as_view(), name='sharelink-delete'),
]
