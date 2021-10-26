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
        if 'specific-ticket' in request.POST:
            id_ticket = request.POST.get('specific-ticket')
            ticket = models.Ticket.objects.get(pk=id_ticket)
            return render(request, 'blog/answer.html', context={'ticket': ticket, 'form': form})
        if 'answer' in request.POST:
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
def review(request):
    context = {}
    return render(request, 'blog/review.html', context=context)


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
