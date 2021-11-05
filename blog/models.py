from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


class Ticket(models.Model):
    title = models.CharField('titre', max_length=128)
    description = models.TextField('description', max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField('image', null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return self.title
    
    IMAGE_MAX_SIZE = (500, 500)

    def resize_image(self):
        try:
            image = Image.open(self.image)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.image.path)
        except ValueError:
            pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name="review")
    rating = models.PositiveSmallIntegerField('note', validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField('en-tête', max_length=128)
    body = models.TextField('contenu', max_length=8192, blank=True)
    time_created = models.DateTimeField('date de publication', auto_now_add=True)

    class Meta:
        verbose_name = "Critique"
        verbose_name_plural = "Critiques"

    def __str__(self):
        return self.headline


class UserFollows(models.Model):
    followed_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Abonnés',  related_name="Abonnés", on_delete=models.CASCADE)
    follows = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Abonnements', related_name="Abonnements", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('followed_by', 'follows', )
        verbose_name = "Relation Utilisateur"
        verbose_name_plural = "Relations Utilisateurs"
    
    def __str__(self):
        return ' %s suit %s ' % (self.followed_by, self.follows)

    
