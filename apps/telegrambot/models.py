from django.db import models

# Create your models here.
class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(unique = True)
    username = models.CharField(max_length=100, blank = True)

class Message(models.Model) :
    user = models.ForeignKey(TelegramUser, on_delete = models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)