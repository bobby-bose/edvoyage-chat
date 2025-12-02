from django.db import models


class UserSimple(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.email


class Conversation(models.Model):
    user_a = models.ForeignKey(UserSimple, related_name='conversations_a', on_delete=models.CASCADE)
    user_b = models.ForeignKey(UserSimple, related_name='conversations_b', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_a.email} <> {self.user_b.email}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(UserSimple, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.email}: {self.text[:20]}"
