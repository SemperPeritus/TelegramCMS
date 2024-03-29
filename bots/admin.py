import telegram
from django import forms
from django.contrib import admin

from bots.models import Bot, Channel, Message

# Global configs
admin.site.empty_value_display = '???'


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


class ChannelAdminForm(forms.ModelForm):
    def clean(self):
        try:
            bot_model = self.cleaned_data.get('bot')
            token = bot_model.token
            bot = telegram.Bot(token=token)
            print(bot.get_me())
            print(self.cleaned_data.get('username'))
            bot.get_chat(self.cleaned_data.get('username'))
        except telegram.TelegramError:
            raise forms.ValidationError("Can't connect to the channel using the bot")

        return self.cleaned_data


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('title', 'username', 'bot')
    fields = ('username', 'bot')
    form = ChannelAdminForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'channel', 'image_tag', 'send_time')
    fields = ('channel', 'text', 'image', 'image_tag', 'send_time')
    readonly_fields = ('image_tag',)
