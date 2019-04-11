from django.db import models

# Create your models here.
class Prompt(models.Model):
    text = models.CharField(max_length = 65536)

    def __str__(self):
        return self.text

class StudentResponse(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    submit_date = models.DateTimeField('date submitted')
    response_text = models.CharField(max_length = 65536)

    def __str__(self):
        return self.response_text
