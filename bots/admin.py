import telegram
from django import forms
from django.contrib import admin

from bots.models import Bot


class BotAdminForm(forms.ModelForm):
    def clean(self):
        try:
            token = self.cleaned_data.get('token')
            telegram.Bot(token=token).get_me()
        except telegram.TelegramError:
            raise forms.ValidationError("Can't connect connect to the bot")

        return self.cleaned_data


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'username')
    fields = ('token',)
    form = BotAdminForm

    def save_model(self, request, obj, form, change):
        bot = telegram.Bot(token=obj.token)

        bot_info = bot.get_me()

        obj.id = bot_info['id']
        obj.name = bot_info['first_name']
        obj.username = bot_info['username']

        super().save_model(request, obj, form, change)
