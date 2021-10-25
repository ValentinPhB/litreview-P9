from .models import Ticket, Review, UserFollows
from django.forms import ModelForm, Form


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

class AnswerForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]