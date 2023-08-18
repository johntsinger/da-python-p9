from itertools import chain
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, CharField, Value
from reviews.forms import TicketForm
from reviews.models import Ticket, Review


class TicketBaseView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = Ticket
    fields = ('title', 'description', 'image')
    success_url = reverse_lazy('feed')


class IndexView(ListView):
    template_name = 'reviews/feed.html'

    def get_queryset(self):
        tickets = Ticket.objects.filter(
            Q(user=self.request.user)
            | Q(user_id__in=self.request.user.following.values_list(
                "followed_user"))
        )
        return tickets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = self.get_queryset()

        print(context)
        return context


class TicketListView(TicketBaseView, ListView):
    template_name = 'reviews/feed.html'

    def get_queryset(self):
        if self.kwargs:
            return Ticket.objects.filter(user_id=self.kwargs['user_id'])
        else:
            return Ticket.objects.all()


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_form'] = TicketForm()

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        ticket_form = TicketForm(request.POST, request.FILES)
        if form.is_valid() and ticket_form.is_valid():
            return self.form_valid(form, ticket_form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, form2):
        t = form2.save(commit=False)
        t.user = self.request.user
        t.save()

        review = form.save(commit=False)
        review.ticket_id = t.id
        review.user = self.request.user
        review.save()

        return super().form_valid(form)


class ReviewDetailView(ReviewBaseView, DetailView):
    template_name = 'reviews/ticket_detail.html'
