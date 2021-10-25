
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from . import forms
from . import models

@login_required
def home(request):
    tickets = models.Ticket.objects.all().order_by('-id')
    reviews = models.Review.objects.all()
    context = {'tickets': tickets,
                'reviews' : reviews}
    if request.method == 'POST':
            id_ticket = request.POST.get('specific-ticket')
            answer(request, id_ticket)
            ticket = models.Ticket.objects.get(pk=id_ticket)
            return render(request, 'blog/answer.html', context={'ticket': ticket})
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
    return render(request, 'blog/ticket.html', context={'form' : form})

@login_required
def review(request):
    context = {}
    return render(request, 'blog/review.html', context=context)

@login_required
def answer(request, id_ticket):
    form = forms.AnswerForm()
    if request.method == 'POST':
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            print('>>>>>>>>>>>>>>>>>>>>>>>> 6')
            print(review.ticket)
            print(review.rating)
            print(review.user)
            print(review.headline)
            print(review.body)
            print(review.time_created)
    return render(request, 'blog/answer.html', context={'form' : form, 'ticket' : id_ticket})
