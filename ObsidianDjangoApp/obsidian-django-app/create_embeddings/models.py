# create_embeddings/models.py

from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    uploadPDF = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title