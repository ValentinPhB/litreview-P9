from django.contrib import admin
from blog.models import Ticket
from .models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import Group

class TicketInLine(admin.TabularInline):
    model = Ticket
    readonly_field = ('time_created',)
    can_delete = False
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [TicketInLine, ]


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
