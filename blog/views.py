from itertools import chain
from django.db.models import CharField, Value
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from . import forms, models
from authentication.models import User

@login_required
def home(request):
    """
    Home view, shows tickets and reviews [::-1]. Manage AnswerForm if users want to submit and answer to tickets.
    """
    form = forms.AnswerForm()

    my_tickets = models.Ticket.objects.filter(user=request.user)
    my_tickets_a = my_tickets.annotate(content_type=Value('TICKET', CharField()))

    my_reviews = models.Review.objects.filter(user=request.user)
    my_reviews_a = my_reviews.annotate(content_type=Value('REVIEW', CharField()))

    reviews_to_me = [obj.user.id for obj in models.Review.objects.all() if obj.ticket.user == request.user]
    reviews_to_me_a = (models.Review.objects.filter(user__in=reviews_to_me).annotate(content_type=Value('REVIEW', CharField())))

    follows_users = [obj.follows.id for obj in models.UserFollows.objects.filter(
        followed_by=request.user)]

    follows_tickets_a = (models.Ticket.objects.filter(
        user__in=follows_users).annotate(content_type=Value('TICKET', CharField())))

    follows_reviews_a = (models.Review.objects.filter(
        user__in=follows_users).annotate(content_type=Value('REVIEW', CharField())))
    
    posts = sorted(
        list(set(chain(my_tickets_a, my_reviews_a, reviews_to_me_a, follows_tickets_a, follows_reviews_a))),
        key=lambda post: post.time_created, 
        reverse=True)

    context = {'posts': posts}

    if request.method == 'POST':
        if 'specific-ticket' in request.POST:
            id_ticket = request.POST.get('specific-ticket')
            ticket = models.Ticket.objects.get(pk=id_ticket)
            return render(request, 'blog/answer.html', context={'ticket': ticket, 'form': form})

        elif 'answer' in request.POST:
            form = forms.AnswerForm(request.POST)
            id_ticket = request.POST.get('ticket_to_pass')
            ticket = models.Ticket.objects.get(pk=id_ticket)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.ticket = ticket
                answer.user = request.user
                answer.save()
                messages.add_message(request, messages.SUCCESS, 'Votre critique a bien été publiée')
                return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'blog/home.html', context=context)


@login_required
def ticket(request):
    """
    Manage TicketForm is users want to submit tickets.
    """
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Votre demande a bien été publiée')
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'blog/ticket.html', context={'form': form})


@login_required
def review(request):
    """
    Manage ReviewForm is users want to submit tickets.
    """
    ticket_form = forms.TicketForm(prefix="ticket_form")
    answer_form = forms.AnswerForm(prefix="answer_form")
    if request.method == 'POST':
        ticket_form = forms.TicketForm(
            request.POST, request.FILES, prefix="ticket_form")
        answer_form = forms.AnswerForm(request.POST, prefix="answer_form")
        if ticket_form.is_valid() and answer_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            answer = answer_form.save(commit=False)
            answer.ticket = ticket
            answer.user = request.user
            answer.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Votre critique a bien été publiée')
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'blog/review.html', context={'ticket_form': ticket_form, 'answer_form': answer_form})


@login_required
def post(request):
    """
    Display posts [::-1] of current user logged and manage Adjust|Delete functionalities.
    """
    adjust_ticket_form = forms.TicketForm(prefix="adjust_ticket_form")
    adjust_review_form = forms.AnswerForm(prefix="adjust_review_form")
    tickets = models.Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = models.Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    posts = sorted(
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True)
    context = {'posts': posts}

    if request.method == 'POST':

        # Ticket adjust or delete
        # Adjust ticket 
        if 'adjust_ticket' in request.POST:
            id_ticket = request.POST.get('adjust_ticket')
            ticket = models.Ticket.objects.get(pk=id_ticket)
            return render(request, 'blog/adjust_ticket.html', context={'ticket': ticket, 'adjust_ticket_form': adjust_ticket_form})
        
        elif 'adjust_ticket_validate' in request.POST:
            adjust_ticket_form = forms.TicketForm(request.POST, request.FILES, prefix='adjust_ticket_form')
            id_ticket = request.POST.get('ticket_to_pass')
            ticket = models.Ticket.objects.get(pk=id_ticket)
            if adjust_ticket_form.is_valid():
                ticket.title = adjust_ticket_form.cleaned_data['title']
                ticket.description = adjust_ticket_form.cleaned_data['description']
                if adjust_ticket_form.cleaned_data['image']:
                    ticket.image = adjust_ticket_form.cleaned_data['image']
                if hasattr(ticket, 'review'):
                    review = models.Review.objects.get(ticket=ticket)
                    review.delete()
                    messages.add_message(
                        request, messages.SUCCESS, 'Votre demande a bien été modifiée par conséquent, sa critique associée a été supprimée.')
                else:
                    messages.add_message(
                        request, messages.SUCCESS, 'Votre demande a bien été modifiée.')
                ticket.save()
                ticket.refresh_from_db()
                return redirect('post')
            return render(request, 'blog/adjust_ticket.html', context={'ticket': ticket, 'adjust_ticket_form': adjust_ticket_form})

        # Delete ticket
        elif 'delete_ticket' in request.POST:
            id_ticket = request.POST.get('delete_ticket')
            ticket = models.Ticket.objects.get(pk=id_ticket)
            if hasattr(ticket, 'review'):
                review = models.Review.objects.get(ticket=ticket)
                review.delete()
                ticket.delete()
                messages.add_message(
                    request, messages.SUCCESS, 'Votre demande et sa critique associée ont été supprimées.')
            else:
                ticket.delete()
                messages.add_message(
                    request, messages.SUCCESS, 'Votre demande a été supprimée.')
            return redirect('post')

        # Review adjust or delete
        # Adjust review
        elif 'adjust_review' in request.POST:
            id_review = request.POST.get('adjust_review')
            review = models.Review.objects.get(pk=id_review)
            return render(request, 'blog/adjust_review.html', context={'review': review, 'adjust_review_form': adjust_review_form})
        
        elif 'adjust_review_validate' in request.POST:
            adjust_review_form = forms.AnswerForm(
                request.POST, prefix="adjust_review_form")
            id_review = request.POST.get('review_to_pass')
            review = models.Review.objects.get(pk=id_review)
            if adjust_review_form.is_valid():
                review.rating = adjust_review_form.cleaned_data['rating']
                review.headline = adjust_review_form.cleaned_data['headline']
                review.body = adjust_review_form.cleaned_data['body']
                review.save()
                review.refresh_from_db()
                messages.add_message(
                    request, messages.SUCCESS, 'Votre critique a bien été modifiée.')
                return redirect('post')
            return render(request, 'blog/adjust_review.html', context={'review': review, 'adjust_review_form': adjust_review_form})

        # Delete review 
        elif 'delete_review' in request.POST:
            id_review = request.POST.get('delete_review')
            review = models.Review.objects.get(pk=id_review)
            review.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Votre Critique a été supprimée.')
            return redirect('post')   

    return render(request, 'blog/post.html', context=context)


@login_required
def follow(request):
    follows = models.UserFollows.objects.filter(followed_by=request.user)
    followed_by = models.UserFollows.objects.filter(follows=request.user)
    # Add relation
    if request.method == 'POST':
        if 'user_string' in request.POST:
            user_string = request.POST.get('user_string')
            try :
                user_followed = User.objects.get(username=user_string)
                instance = models.UserFollows.objects.create(followed_by=request.user, follows=user_followed)
                messages.add_message(
                    request, messages.SUCCESS, "Utilisateur ajouté à votre liste d'abonnement.")
            except (ObjectDoesNotExist, IntegrityError):
                messages.add_message(
                    request, messages.ERROR, "Veuillez vérifier l'orthographe de votre entrée, cet utilisateur est peut être déja suivi.")
                return redirect('follow')
        # Delete relation 
        elif 'specific_user' in request.POST:
            id_instance = request.POST['specific_user']
            follow_instance = models.UserFollows.objects.get(id=id_instance)
            follow_instance.delete()
            return redirect('follow')
    return render(request, 'blog/follow.html', context={ 'follows' : follows, 'followed_by' : followed_by, })