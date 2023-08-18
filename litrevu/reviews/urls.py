from django.urls import path
from reviews import views as re_views

urlpatterns = [
    path('', re_views.IndexView.as_view(), name='feed'),
    path('reviews/user-posts/<int:user_id>', re_views.TicketListView.as_view(),
         name='user-posts'),
    path('reviews/ticket/<int:pk>', re_views.TicketDetailView.as_view(),
         name='ticket-detail'),
    path('reviews/review/<int:pk>', re_views.ReviewDetailView.as_view(),
         name='review-detail'),
    path('reviews/ticket/create/', re_views.TicketCreateView.as_view(),
         name='create-ticket'),
    path('reviews/ticket/<int:pk>/change', re_views.TicketUpdateView.as_view(),
         name='update-ticket'),
    path('reviews/ticket/<int:pk>/delete', re_views.TicketDeleteView.as_view(),
         name='delete-ticket'),
    path('reviews/review/create', re_views.ReviewCreateView.as_view(),
         name='create-review'),
]
