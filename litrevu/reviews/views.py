from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q, Case, When
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    ModelFormMixin
)
from django.urls import reverse_lazy
from reviews.forms import (
    TicketForm,
    ReviewForm,
    SubscriptionFrom,
)
from reviews.models import Ticket, Review, UserFollows


class IndexView(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'reviews/feed.html'

    def get_queryset(self):
        tickets = Ticket.objects.filter(
            # current user tickets
            Q(user=self.request.user)
            # current user reviews
            | Q(review__user=self.request.user)
            # tickets from users followed by the current user
            | Q(user_id__in=self.request.user.following.values_list(
                "followed_user", flat=True))
            # tickets answered by users followed by current user
            | Q(review__user__id__in=self.request.user.following.values_list(
                "followed_user", flat=True))
        ).annotate(
            # annotate date = ticket time_created if no review for this
            # ticket else review__time_created
            date=Case(
                When(review__isnull=False, then="review__time_created"),
                default="time_created"
            )
        ).order_by("-date")  # sort by reverse (-) date from annotate

        return tickets


class UserPostView(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'reviews/feed.html'

    def get_queryset(self):
        User = get_user_model()
        user = User.objects.get(id=self.kwargs['pk'])
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
        """Add followed_user_pk to context to check if current user
        follows the user related to the user-posts page and
        user_post to get the user of the user-post page"""
        context = super().get_context_data(**kwargs)
        followed_user_pk = self.request.user.following.values_list(
            'followed_user',
            flat=True
        )
        context['followed_user_pk'] = followed_user_pk
        User = get_user_model()
        context['user_post'] = User.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        """On post create UserFollows"""
        user_follow = UserFollows.objects.create(
            user=self.request.user,
            followed_user_id=self.kwargs['pk']
        )
        messages.success(
            request,
            f'You are now follow user {user_follow.followed_user}'
        )
        return self.get(request, *args, **kwargs)


class TicketBaseView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = Ticket
    fields = ('title', 'description', 'image')
    success_url = reverse_lazy('feed')


class TicketDetailView(TicketBaseView, DetailView):
    template_name = 'reviews/ticket_detail.html'


class TicketCreateView(TicketBaseView, CreateView):
    template_name = 'reviews/ticket_create.html'
    success_message = 'Your ticket has been successfully created !'

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs:
            context['form'] = TicketForm(
                self.request.POST or None,
                instance=Ticket.objects.get(pk=self.kwargs['pk'])
            )
        else:
            context['form_media'] = TicketForm(
                self.request.POST or None,
            )

        return context
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = None
        if self.kwargs:
            instance = Ticket.objects.get(pk=self.kwargs['pk'])
        context['form'] = TicketForm(
            self.request.POST or None,
            self.request.FILES or None,
            instance=instance
        )
        if 'page' in self.request.GET:
            context['page'] = self.request.GET['page']
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = None
        messages.error(
            self.request,
            "Please correct the errors below !")
        # get previous_url senf by input hidden in form
        # and pass it to render_to_response to use it when the
        # page reload
        if 'previous_url' in self.request.POST:
            previous_url = self.request.POST['previous_url']
        return self.render_to_response(
            self.get_context_data(
                form=form,
                previous_url=previous_url,
            ),
        )


class TicketUpdateView(TicketBaseView, UpdateView):
    template_name = 'reviews/ticket_change.html'
    success_message = 'Your ticket has been successfully updated !'

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in kwargs:
            context['form'] = TicketForm(
                self.request.POST or None,
                instance=Ticket.objects.get(pk=self.kwargs['pk']),
            )
        else:
            # pass another for to context so that it can be used in
            # the model to load its form.media,
            # as the other form's media is curiously empty
            context['form_media'] = TicketForm()

        if 'page' in self.request.GET:
            context['page'] = self.request.GET['page']

        return context
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TicketForm(
            self.request.POST or None,
            self.request.FILES or None,
            instance=Ticket.objects.get(pk=self.kwargs['pk'])
        )
        if 'page' in self.request.GET:
            context['page'] = self.request.GET['page']

        return context

    def get_success_url(self):
        ticket = self.get_object()
        if 'page' in self.request.GET:
            self.success_url += (
                f'?page={self.request.GET["page"]}#ticket{ticket.id}'
            )
        return str(self.success_url)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please correct the errors below !")
        if 'previous_url' in self.request.POST:
            previous_url = self.request.POST['previous_url']
        return self.render_to_response(
            self.get_context_data(
                form=form,
                previous_url=previous_url,
            ),
        )


class TicketDeleteView(TicketBaseView, DeleteView):
    def form_valid(self, form):
        messages.warning(
            self.request,
            'Your ticket has been sucessfully deleted !'
        )
        return super().form_valid(form)


class ReviewBaseView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = Review
    fields = ('headline', 'body', 'rating')
    success_url = reverse_lazy('feed')


class ReviewCreateView(ReviewBaseView, CreateView):
    template_name = 'reviews/review_create.html'
    success_message = 'Your review has been successfully created !'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = None
        if self.kwargs:
            ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])
            context['ticket'] = ticket

        context['ticket_form'] = TicketForm(
            self.request.POST or None,
            self.request.FILES or None,
            instance=ticket
        )

        context['form'] = ReviewForm(
            self.request.POST or None
        )

        return context

    def post(self, request, *args, **kwargs):
        """Dispatch form_valid method depending if ticket is created or not
        else return form_invalid"""
        form = self.get_form(ReviewForm)
        ticket_form = None
        if not self.kwargs:
            ticket_form = self.get_form(TicketForm)

        if not self.kwargs and (form.is_valid() and ticket_form.is_valid()):
            return self.form_valid(form, ticket_form)
        elif self.kwargs and form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, form2=None):
        """Create ticket if no ticket else get it then create review"""
        if form2:
            ticket = form2.save(commit=False)
            ticket.user = self.request.user
            ticket.save()
            ticket_id = ticket.id
        else:
            ticket_id = self.kwargs['pk']

        review = form.save(commit=False)
        review.ticket_id = ticket_id
        review.user = self.request.user
        review.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = None
        messages.error(
            self.request,
            "Please correct the errors below !")
        if 'previous_url' in self.request.POST:
            previous_url = self.request.POST['previous_url']
        return self.render_to_response(
            self.get_context_data(
                form=form,
                previous_url=previous_url,
            ),
        )


class ReviewUpdateView(ReviewBaseView, UpdateView):
    template_name = 'reviews/review_change.html'
    success_message = 'Your review has been successfully updated !'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm(
            self.request.POST or None,
            instance=Review.objects.get(pk=self.kwargs['pk'])
        )
        context['ticket'] = get_object_or_404(Review, pk=self.kwargs['pk']).ticket
        # pass the pagination
        if 'page' in self.request.GET:
            context['page'] = self.request.GET['page']

        return context

    def get_success_url(self):
        review = self.get_object()
        if 'page' in self.request.GET:
            self.success_url += (
                f'?page={self.request.GET["page"]}#ticket{review.ticket.id}'
            )
        return str(self.success_url)


class ReviewDeleteView(ReviewBaseView, DeleteView):
    def form_valid(self, form):
        messages.warning(
            self.request,
            'Your review has been sucessfully deleted !'
        )
        return super().form_valid(form)


class SubscriptionBaseView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = UserFollows
    form_class = SubscriptionFrom
    success_url = reverse_lazy('subscriptions')


class SubscriptionView(SubscriptionBaseView, ListView, ModelFormMixin):
    template_name = 'reviews/subscriptions.html'
    success_message = 'You are now follow user %(username)s'

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return super().get(self, request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        followed_user = form.cleaned_data['username']
        form.instance.followed_user = followed_user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.object = self.form
            return self.form_valid(self.form)

        return self.get(request, *args, **kwargs)


class UserfollowDeleteView(SubscriptionBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.warning(
            self.request,
            f'You no longer follow {self.object.followed_user}'
        )
        return self.delete(request, *args, **kwargs)
