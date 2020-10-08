from django.db import models
#sto importando settings.py
from django.conf import settings

#Ti prende automaticamente l'utente
User = settings.AUTH_USER_MODEL
# Create your models here.
class Word (models.Model):
    sentence = models.CharField(primary_key = True, max_length=250)
    language = models.ForeignKey("Language", on_delete=models.PROTECT)

class Dictionary (models.Model):
    word = models.ForeignKey(Word, on_delete=models.PROTECT, related_name="Original")
    synonym = models.TextField(blank=True, null=True)
    translation = models.ForeignKey(Word, on_delete=models.PROTECT)
    grammar = models.CharField(blank=True, null=True, max_length=50)
    #la FK prende la fonte dall'autore che l'ha inserita
    creator = models.ForeignKey(User, on_delete=models.PROTECT)

class Text (models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(blank=False, null=False, max_length=50)
    subtitle = models.CharField(blank=False, null=True, max_length=50)
    author = models.CharField(blank=False, null=False, max_length=50)
    text = models.TextField(blank=False, null=False)
    reference = models.ManyToManyField(Dictionary, related_name="words", blank=True)
    underlines= models.ManyToManyField("Underline", blank=True)

class Language(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)

class Grammar(models.Model):
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    typology = models.CharField(blank=False, null=False, max_length=50)

class Underline(models.Model):
    gram = models.ForeignKey(Grammar, on_delete=models.PROTECT)
    ref = models.ForeignKey(Word, on_delete=models.PROTECT)