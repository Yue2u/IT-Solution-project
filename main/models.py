from django.db import models


class Text(models.Model):
    text = models.CharField(max_length=50, blank=False, null=False)
    get_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Text '{self.text}'"
