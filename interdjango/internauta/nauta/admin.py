from django.contrib import admin
from .models import Text, Dictionary, Word, Grammar, Language, Underline, Category

# Register your models here.

admin.site.register(Text)
admin.site.register(Dictionary)
admin.site.register(Word)
admin.site.register(Grammar)
admin.site.register(Language)
admin.site.register(Underline)
admin.site.register(Category)