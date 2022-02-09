from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.http import is_safe_url
from django.http import HttpResponse, JsonResponse, Http404
from django.conf import settings
from django.db.models import Count, Q

from .forms import TextForm
from .models import Text, Word, Dictionary, Language, Grammar, Underline, Category, TextView
from .serializers import DictionarySerializer, TextSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# Create your views here.

def index(request):
    object_list = Text.objects.filter(firstchapter=True, nocopy=True)[:3]
    latest = Text.objects.order_by('-timestamp')
    page = Paginator(latest, 3)

    # if request.method == "POST":
    #     email = request.POST["email"]
    #     new_signup = Signup()
    #     new_signup.email = email
    #     new_signup.save()

    context = {
        'object_list': object_list,
        'page': page
    }
    return render(request, 'index.html', context)

def search(request):
    texty_searchy = Text.objects.all()
    query = request.GET.get('q')
    
    if query:
        texty_searchy = texty_searchy.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(id__icontains=query)
        ).distinct()
    context = {
        'texty_searchy': texty_searchy
    }
    return render(request, 'pages/search_results.html', context)

def get_category_count():
    queryset = Text.objects.values('categories__name').annotate(Count('categories__name'))
    return queryset

def feed(request):
    category_count = get_category_count()
    most_recent = Text.objects.order_by('-timestamp')[:3]
    text_list = Text.objects.filter(firstchapter=True)
    paginator = Paginator(text_list, 9)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    
    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
        'text_list': text_list,
    }
    return render(request, 'feed.html', context)

def update(request, text_id, *args, **kwargs):
    title = 'Update'
    text = get_object_or_404(Text, id=text_id)
    form = TextForm(
        request.POST or None,
        request.FILES or None,
        instance=text)
    user = request.user
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = user
            form.save()
            return redirect('/feed')
    context = {
        'title': title,
        'form': form,
        'btn_label': 'Inserisci',
        'text_id': text_id
    }
    return render(request, "pages/text_update.html", context)


def text_create_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        user=None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TextForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            return redirect('/feed')
    context = { 'form': form,
                'btn_label': 'Inserisci',
                'title': 'Inserimento testo'
    }
    return render(request, 'pages/forms.html', context)

@api_view(['GET'])
def text_visualize_view(request, text_id, *args, **kwargs):
    qs = Text.objects.filter(id = text_id)
    if not qs.exists():
            return Response({}, status=404)
    obj = qs.first()
    serializer = TextSerializer(obj)
    ds = obj.reference.all()
    i = 0
    dd = {}
    for d in ds:
        dd[str(i)] = {
            'word': d.word.sentence,
            'translation': d.translation.sentence,
            'synonym' : d.synonym,
            'grammar' : d.grammar
        }
        i+=1
    us = obj.underlines.all()
    i = 0
    uu = {}
    for u in us:
        uu[str(i)] = {
            'word': u.ref.sentence,
            'grammar': u.gram.typology
        }
        
        i+=1
    data = serializer.data
    data['reference'] = dd
    data['underlines'] = uu
    return Response(data, status=200)
    
# def text_view(request, text_id, *args, **kwargs):
#     context = {
#         'text_id': text_id,
#     }
#     return render(request, 'pages/visualize.html', context)

def text_view(request, text_id, *args, **kwargs):
    most_recent = Text.objects.order_by('-timestamp')[:3]
    text = get_object_or_404(Text, id=text_id)

    if request.user.is_authenticated:
        TextView.objects.get_or_create(user=request.user, text=text)

    context = {
        'text_id': text_id,
        'text': text,
        'most_recent': most_recent
    }
    return render(request, 'pages/visualize.html', context)



@api_view(['POST'])
def add_entry_view(request, *args, **kwargs):
    user = request.user
    d1= None
    if not user.is_authenticated:
        user=None
        if request.is_ajax():
            return Response({}, status=401)
        return redirect(settings.LOGIN_URL)
    data = request.data or None
    if(data):
        qs = Language.objects.filter(name = data['original'])
        if not qs.exists():
            orig = Language(name=data['original'])
            orig.save()
        else:
            orig = qs.first()
            
        qs = Language.objects.filter(name = data['translated'])
        if not qs.exists():
            trans = Language(name=data['translated'])
            trans.save()
        else:
            trans = qs.first()


        qs = Word.objects.filter(sentence=data['word'])
        if not qs.exists():
            w = Word(sentence=data['word'], language=orig)
            w.save()
        else:
            w = qs.first()
        
        qs = Word.objects.filter(sentence=data['translation'])
        if not qs.exists():
            t = Word(sentence=data['translation'], language=trans)
            t.save()
        else:
            t = qs.first()
        
        qs = Dictionary.objects.filter(word=w, translation=t)
        if not qs.exists():
            d = Dictionary(word=w, translation=t, synonym=data['synonym'], grammar=data['grammar'], creator=user)
            d.save()
        else:
            d = qs.first()
            if d.synonym is None and data['synonym'] is not None:
                d.synonym = data['synonym']
                d.save()
            if d.synonym != data['synonym']:
                d1 = Dictionary(word=w, translation=t, synonym=data['synonym'], grammar=data['grammar'], creator=user)
                d1.save()
        qs = Text.objects.filter(id=int(data['id']))
        if not qs.exists():
            return Response({'message': 'Not found!'}, status=404)
        else:
            text = qs.first()
            text.reference.add(d if d1 is None else d1)
            text.save()
            return Response({'message': 'great success!'}, status=200)

    return Response({'message': 'great failure!'}, status=503)

def text_edit_view(request, text_id, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        user=None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    context = { 'text_id': text_id}
    qs = Text.objects.filter(id=text_id)
    
    if qs.exists():
        return render(request, 'pages/edit.html', context)
    else:
        context = {'message': 'the text selected does not exists'}
        return render(request, 'pages/error.html', context)


def find_word(word, translatedLanguage):
    result = []
    qs = Dictionary.objects.filter(word=word) 
    if not qs.exists(): 
        qs = Dictionary.objects.filter(translation=word)
        if not qs.exists():
            return None
        for d in qs:
            if d.word.language == translatedLanguage:
                result.append(d)
        if len(result) == 0:
            return None
        else:
            maximum = 0
            index = -1
            i = 0
            for entry in result:
                n = entry.words.count()
                if n > maximum:
                    maximum = n
                    index = i
                i += 1
            data = {
                'original': result[index].translation.sentence,
                'translated': result[index].word.sentence,
                'synonym':  result[index].synonym,
            }
            return data
    for d in qs:
        if d.translation.language == translatedLanguage:
            result.append(d)
        if len(result) == 0:
            return None
        else:
            maximum = 0
            index = -1
            i = 0
            for entry in result:
                n = entry.words.count()
                if n > maximum:
                    maximum = n
                    index = i
                i += 1
            data = {
                'original': result[index].word.sentence,
                'translated':  result[index].translation.sentence,
                'synonym':  result[index].synonym,
            }
            return data
    return None

@api_view(['GET'])
def retrieve_grammars_view(request, lang, *args, **kwargs):
    qs = Grammar.objects.filter(language__name=lang)
    results = {}
    if not qs.exists():
        return Response({'message': 'Language not found!'}, status=404)
    else:
        i = 0
        
        for g in qs:
            results[str(i)] = g.typology
            i += 1
        return Response(results, status=200)
    return Response({'message': 'Server Error'}, status=500)

@api_view(['POST'])
def retrieve_word_view(request, *args, **kwargs):
    data = request.data or None
    if(data):
        qs = Language.objects.filter(name=data['original'])
        if not qs.exists():
                return Response({})
        orig_lang = qs.first()
        qs = Language.objects.filter(name=data['translated'])
        if not qs.exists():
                return Response({})
        trans_lang = qs.first()
        qs = Word.objects.filter(sentence = data['word'], language=orig_lang)
        if not qs.exists():
                return Response({})
        obj = qs.first()
        ret_data = find_word(obj, trans_lang)
        if ret_data is not None:
            return Response(ret_data, status=200)
        else:
            return Response({}, status=404)
                
    else:
        return Response({}, status=404)
        
@api_view(['POST'])
def add_underline_view(request, *args, **kwargs):
    data = request.data or None
    if data:
        qs = Text.objects.filter(id=data['text_id'])
        if not qs.exists():
            return Response({}, status=404)
        t = qs.first()
        qs = Grammar.objects.filter(typology=data['typology'])
        if not qs.exists():
            return Response({}, status=404)
        g = qs.first()
        qs = Word.objects.filter(sentence=data['word'])
        if not qs.exists():
            w = Word(sentence=data['word'], language=g.language)
            w.save()
        else:
            w = qs.first()
        qs = Underline.objects.filter(gram=g, ref=w)
        if not qs.exists():
            undies = Underline(gram=g, ref=w)
            undies.save()
        else:
            undies = qs.first()
        t.underlines.add(undies)
        return Response({'message': 'great success!'}, status=200)
    else:
        return Response({'message': 'great failure!'}, status=500)


def homepage_view(request, *args, **kwargs):
    # context = { 'text_id': text_id}
    return render(request, 'home.html')

def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = TextSerializer(paginated_qs, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def user_feed_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return Response({}, status=401)
    qs = Text.objects.feed(user)
    if not qs.exists():
            return Response({}, status=404)
    return get_paginated_queryset_response(qs, request)
    

@api_view(['GET'])
def global_feed_view(request, *args, **kwargs):
    qs=Text.objects.all()
    if not qs.exists():
            return Response({}, status=404)
    return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
def text_delete(request, text_id):
    text_to_delete = Text.objects.filter(id = text_id)[0]
    user = request.user
    if not user.is_authenticated:
        return Response({"message" : "you are not authenticated"}, status=401)
    if text_to_delete is None:
        return Response({"message" : "this post does not exists"}, status=404)
    if text_to_delete.user == user:
        obj = text_to_delete.delete()
    else:
        return Response({"message" : "this is not your post to delete"}, status=404)
    return redirect("/feed")

@api_view(['GET'])
def words_delete(request, text_id, orig, transl, syn):
    words_to_delete = Text.objects.filter(id = text_id)[0]
    user = request.user
    if not user.is_authenticated:
        return Response({"message" : "you are not authenticated"}, status=401)
    if words_to_delete is None:
        return Response({"message" : "this post does not exists"}, status=404)
    if words_to_delete.user == user:
        obj = words_to_delete.delete()
    else:
        return Response({"message" : "this is not your post to delete"}, status=404)
    return redirect("/feed")
