from itertools import chain
from django.db.models import CharField, Value

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from . import forms
from . import models


@login_required
def home(request):
    form = forms.AnswerForm()

    tickets = models.Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = models.Review.objects.all()
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    posts = sorted(
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True)
    context = {'posts': posts}
    if request.method == 'POST':
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>')
        if 'specific-ticket' in request.POST:
            print('herereererereererr')
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
def post(request):
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
        if 'adjust_ticket' in request.POST:
            id_ticket = request.POST.get('adjust_ticket')
            ticket = models.Ticket.objects.get(pk=id_ticket)
            return render(request, 'blog/adjust_ticket.html', context={'ticket': ticket, 'adjust_ticket_form': adjust_ticket_form})
        elif 'adjust_review' in request.POST:
            id_review = request.POST.get('adjust_review')
            review = models.Review.objects.get(pk=id_review)
            return render(request, 'blog/adjust_review.html', context={'review': review, 'adjust_review_form': adjust_review_form})

        elif 'delete_ticket' in request.POST:
            id_ticket = request.POST.get('delete_ticket')
            ticket = models.Ticket.objects.get(pk=id_ticket)
            if hasattr(ticket, 'review') :
                review = models.Review.objects.get(ticket=ticket)
                review.delete()
                ticket.delete()
                messages.add_message(request, messages.SUCCESS, 'Votre demande et sa critique associée ont été supprimées.')
            else:
                ticket.delete()
                messages.add_message(request, messages.SUCCESS, 'Votre demande a été supprimée.')
            return redirect('post')
        elif 'delete_review' in request.POST:
            id_review = request.POST.get('delete_review')
            review = models.Review.objects.get(pk=id_review)
            review.delete()
            messages.add_message(request, messages.SUCCESS, 'Votre Critique a été supprimée.')
            return redirect('post')

        elif 'adjust_review_validate' in request.POST:
            print('innnnnnnnnnnnnnnnnnnnnnnnnnnnn')
            adjust_review_form = forms.AnswerForm(request.POST, prefix="adjust_review_form")
            print(adjust_review_form)
            if adjust_review_form.is_valid():
                print('VALIDDDDDDDDDDDDDDDDDDDDD')
                id_review = request.POST.get('review_to_pass')
                review = models.Review.objects.get(pk=id_review)
                review.save(commit=False)
                print(review.headline)
                print(review.body)
                print(review.rating)
                messages.add_message(request, messages.SUCCESS, 'Votre critique a bien été modifiée.')
                redirect('post')

        elif 'adjust_ticket_validate' in request.POST:
            adjust_ticket_form = forms.TicketForm(request.POST, request.FILES)
            if adjust_ticket_form.is_valid():
                id_ticket = request.POST.get('ticket_to_pass')
                ticket = models.Ticket.objects.get(pk=id_ticket)
                ticket.title = request.POST.get('')
                ticket.description = request.POST.get('')
                ticket.image = request.FILES.get('')
                if hasattr(ticket, 'review') :
                    review = models.Review.objects.get(ticket=ticket)
                    review.delete()
                    messages.add_message(request, messages.SUCCESS, 'Votre demande a bien été modifiée par conséquent, sa critique associée a été supprimée.')
                else:
                    messages.add_message(request, messages.SUCCESS, 'Votre demande a bien été modifiée.')


    return render(request, 'blog/post.html', context=context)


@login_required
def review(request):
    ticket_form = forms.TicketForm(prefix="ticket_form")
    answer_form = forms.AnswerForm(prefix="answer_form")
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES, prefix="ticket_form")
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
