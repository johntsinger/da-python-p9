from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q, Case, When
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from reviews.forms import TicketForm
from reviews.models import Ticket, Review


class TicketBaseView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = Ticket
    fields = ('title', 'description', 'image')
    success_url = reverse_lazy('feed')


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'reviews/feed.html'

    def get_queryset(self):
        tickets = Ticket.objects.filter(
            # current user tickets
            Q(user=self.request.user)
            # tickets from users followed by the current user
            | Q(user_id__in=self.request.user.following.values_list(
                "followed_user"))
            # tickets answered by users followed by current user
            | Q(review__user__id__in=self.request.user.following.values_list(
                "followed_user"))
        ).annotate(
            # annotate date = ticket time_created if no review for this
            # ticket else review__time_created
            date=Case(
                When(review__isnull=False, then="review__time_created"),
                default="time_created"
            )
        ).order_by("-date")  # sort by reverse (-) date from annotate

        return tickets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('Context IndexView', context)

        return context


class UserPostView(TicketBaseView, ListView):
    template_name = 'reviews/feed.html'

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['user_id'])
        tickets = (
            user.ticket_set.all()
            | Ticket.objects.filter(review__user=user)
        ).annotate(
            date=Case(
                When(review__isnull=False, then="review__time_created"),
                default="time_created"
            )
        ).order_by("-date")

        return tickets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)

        return context


class TicketDetailView(TicketBaseView, DetailView):
    template_name = 'reviews/ticket_detail.html'


class TicketCreateView(TicketBaseView, CreateView):
    template_name = 'reviews/ticket_create.html'
    success_message = 'Your ticket has been successfully created !'

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class TicketUpdateView(TicketBaseView, UpdateView):
    template_name = 'reviews/ticket_change.html'
    success_message = 'Your ticket has been successfully updated !'


class TicketDeleteView(TicketBaseView, DeleteView):
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(
            self.request,
            'Your ticket has been sucessfully deleted !'
        )

        return response


class ReviewBaseView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = Review
    fields = ('headline', 'body', 'rating')
    success_url = reverse_lazy('feed')


class ReviewCreateView(ReviewBaseView, CreateView):
    template_name = 'reviews/review_create.html'
    success_url = reverse_lazy('feed')
    success_message = 'Your review has been successfully created !'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = None
        if self.kwargs:
            ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])
        context['ticket_form'] = TicketForm(
            instance=ticket
        )

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        ticket_form = TicketForm(request.POST, request.FILES)

        if form.is_valid() and ticket_form.is_valid():
            return self.form_valid(form, ticket_form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, form2):
        if not self.kwargs:
            ticket = form2.save(commit=False)
            ticket.user = self.request.user
            ticket.save()
        else:
            ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])

        review = form.save(commit=False)
        review.ticket_id = ticket.id
        review.user = self.request.user
        review.save()

        return super().form_valid(form)


class ReviewUpdateView(ReviewBaseView, UpdateView):
    template_name = 'reviews/review_change.html'
    success_message = 'Your review has been successfully updated !'
