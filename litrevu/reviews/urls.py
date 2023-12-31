from django.urls import path
from reviews import views as re_views

urlpatterns = [
    path('', re_views.IndexView.as_view(), name='feed'),
    path('reviews/user-posts/<int:pk>', re_views.UserPostView.as_view(),
         name='user-posts'),
    path('reviews/ticket/<int:pk>', re_views.TicketDetailView.as_view(),
         name='ticket-detail'),
    path('reviews/ticket/create/', re_views.TicketCreateView.as_view(),
         name='create-ticket'),
    path('reviews/ticket/<int:pk>/change', re_views.TicketUpdateView.as_view(),
         name='change-ticket'),
    path('reviews/ticket/<int:pk>/delete', re_views.TicketDeleteView.as_view(),
         name='delete-ticket'),
    path('reviews/review/create', re_views.ReviewCreateView.as_view(),
         name='create-review'),
    # to create review for an existing ticket
    path('reviews/review/create/<int:pk>', re_views.ReviewCreateView.as_view(),
         name='create-review'),
    path('reviews/review/<int:pk>/change', re_views.ReviewUpdateView.as_view(),
         name='change-review'),
    path('reviews/review/<int:pk>/delete', re_views.ReviewDeleteView.as_view(),
         name='delete-review'),
    path('reviews/subscriptions/', re_views.SubscriptionView.as_view(),
         name='subscriptions'),
    path('reviews/subscriptions/<int:pk>/delete',
         re_views.UserfollowDeleteView.as_view(),
         name='delete-userfollow')
]
