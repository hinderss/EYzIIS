from django.db.models.functions import Lower
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import WordForm, SearchForm
from .models import UploadedFile, Word
from .utils import extract_text_from_docx, extract_text_with_styles, analyze_text
from alalyzer import analyzer


def index(request):
    if not request.session.session_key:
        request.session.create()
    files = UploadedFile.objects.filter(session_key=request.session.session_key).order_by("-uploaded_at")
    return render(
        request,
        "index.html",
        {"files": files, "form": WordForm(), "search": SearchForm()}
    )


def upload(request):
    if request.method == 'POST' and request.FILES.get('document'):
        uploaded_file = request.FILES['document']
        file_instance = UploadedFile.objects.create(
            name=uploaded_file.name,
            file=uploaded_file,
            session_key=request.session.session_key
        )
        return redirect("analyze_list", file_id=file_instance.id)
    return redirect(reverse('index'))


def analyze_list(request, file_id):
    if not request.session.session_key:
        request.session.create()

    file = get_object_or_404(UploadedFile, id=file_id, session_key=request.session.session_key)
    text = extract_text_from_docx(file.file.path)
    words = Word.objects.filter(file=file)
    if not words:
        words = analyze_text(text, file)
    words = words.distinct().order_by(Lower("lemma"))
    words = {word.lemma: word for word in words}.values()

    return words_view(request, words, template="analyze.html", file=file)


def words_view(request, words, template="words.html", **kwargs):
    return render(
        request,
        template,
        {
            "words": words,
            "form": WordForm(),
            "search": SearchForm(),
            **kwargs,
        }
    )


def generate(request, word_id):
    if not request.session.session_key:
        request.session.create()

    word = get_object_or_404(Word, id=word_id)
    return render(
        request,
        "generate.html",
        {"word": word, "form": WordForm(), "search": SearchForm()}
    )


def document_view(request, file_id):
    if not request.session.session_key:
        request.session.create()
    file = get_object_or_404(UploadedFile, id=file_id, session_key=request.session.session_key)
    if not file:
        return render(request, "document_view.html", {"file": file, "document_words": []})
    text = extract_text_with_styles(file.file)
    return render(
        request,
        "document_view.html",
        {
            "file": file,
            "document_text": text,
            "form": WordForm(),
            "search": SearchForm()
        }
    )


def generate_wordform(request):
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            word_base = form.cleaned_data["word_base"]
            part_of_speech = form.cleaned_data["part_of_speech"]
            feature = form.cleaned_data["feature"]
            word = Word.objects.filter(lemma=word_base, pos=part_of_speech, tag=feature).first()
            if not word:
                inflect = analyzer.get_inflected_form(word_base, feature, part_of_speech)
                lexeme = analyzer.analyze(inflect)

                word = Word.objects.create(
                    word=inflect,
                    lemma=lexeme.lemma,
                    pos=lexeme.pos,
                    tag=lexeme.tag,
                    suffixes=[{
                        "inflection": inflection,
                        "suffix": suffix,
                        "tag": tag,
                        "explained": analyzer.explain_tag(tag),
                    } for inflection, suffix, tag in lexeme.possible_suffixes],
                )
            return redirect("generate", word.id)
        return redirect("index")


def search_wordform(request):
    words = Word.objects.all()
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            pos = form.cleaned_data["pos"]
            tag = form.cleaned_data["tag"]

            if query:
                words = words.filter(lemma__icontains=query)
            if pos:
                words = words.filter(pos=pos)
            if tag:
                words = words.filter(tag=tag)
            words = words.distinct().order_by(Lower("lemma"))
            words = {word.lemma: word for word in words}.values()
            return words_view(request, words, template="search.html", name=f"{query}, {pos}, {tag}")
    return redirect("index")


@require_POST
def delete_word(request, word_id):
    if not request.session.session_key:
        request.session.create()

    word = get_object_or_404(Word, id=word_id)
    file_id = word.file.id
    word.delete()
    return redirect("analyze_list", file_id=file_id)
