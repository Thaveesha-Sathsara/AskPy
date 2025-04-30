from django.db import models

class ConversationPair(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question} → {self.answer}"


class UnknownQuestion(models.Model):
    question = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    
    
class SimplifierMapping(models.Model):
    keyword = models.CharField(max_length=255, unique=True)
    replacement = models.TextField()

    def __str__(self):
        return self.keyword

