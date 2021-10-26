from django.contrib import admin
from blog.models import Ticket, Review
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


class TicketInLine(admin.TabularInline):
    model = Ticket
    fieldsets = [
        (None, {'fields': ['title', 'description', 'image']})]
    extra = 0


class ReviewInLine(admin.TabularInline):
    model = Review
    fieldsets = [
        (None, {'fields': ['headline', 'body', 'ticket']})]
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ReviewInLine, TicketInLine, ]


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# don't show groups
admin.site.unregister(Group)
