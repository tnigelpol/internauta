from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse
#Ti prende automaticamente l'utente
User = settings.AUTH_USER_MODEL
# Create your models here.

class Category (models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    
    def __str__(self):
        return self.name

class Word (models.Model):
    sentence = models.CharField(primary_key=True, max_length=250)
    language = models.ForeignKey("Language", on_delete=models.PROTECT)

    def __str__(self):
        return self.sentence

class Dictionary (models.Model):
    word = models.ForeignKey(Word, on_delete=models.PROTECT, related_name="Original")
    synonym = models.TextField(blank=True, null=True)
    translation = models.ForeignKey(Word, on_delete=models.PROTECT)
    grammar = models.CharField(blank=True, null=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    #la FK prende la fonte dall'autore che l'ha inserita
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.creator) + ' (' + str(self.word) + ', ' + str(self.translation) + ')'


class TextQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(author__username__iexact=username)
    def feed(self, user):
        profiles_exist = user.following.exists() 
        #profiles = user.following.all()
        followed_ids = []
        if profiles_exist:
            followed_ids = user.following.values_list("user__id", flat=True)
        print("followed", followed_ids)
        return self.filter(
            Q(user__id__in=followed_ids) |
            Q(user=user)
        ).distinct().order_by("-timestamp")

class TextManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TextQuerySet(self.model, using=self._db)
    def feed(self, user):
        return self.get_queryset().feed(user)


class Text(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(blank=False, null=False, max_length=50)
    subtitle = models.CharField(blank=False, null=True, max_length=50)
    author = models.CharField(blank=False, null=False, max_length=50)
    text = models.TextField(blank=False, null=False)
    reference = models.ManyToManyField(Dictionary, related_name="words", blank=True)
    underlines= models.ManyToManyField("Underline", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    objects = TextManager()
    chapter = models.CharField(null=True, max_length=1000)
    firstchapter= models.BooleanField()
    nocopy = models.BooleanField()
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def view_count(self):
        return TextView.objects.filter(text=self).count()

class TextView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.ForeignKey('Text', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('view', kwargs={
            'id': self.id
        })


class Language(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)
    
    def __str__(self):
        return self.name

class Grammar(models.Model):
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    typology = models.CharField(blank=False, null=False, max_length=50)

    def __str__(self):
        return self.typology

class Underline(models.Model):
    gram = models.ForeignKey(Grammar, on_delete=models.PROTECT)
    ref = models.ForeignKey(Word, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Underline(' + str(self.gram) + ', ' + str(self.ref) + ')'