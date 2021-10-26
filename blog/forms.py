from .models import Ticket, Review
from django.forms import ModelForm


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

class AnswerForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]