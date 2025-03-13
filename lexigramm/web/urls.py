from django.urls import path
from .views import index, upload, analyze_list, document_view, generate_wordform, generate, delete_word, search_wordform

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload, name='upload'),
    path('analyze/<uuid:file_id>/', analyze_list, name='analyze_list'),
    path('document/<uuid:file_id>/', document_view, name='document_view'),
    path('generate_wordform/', generate_wordform, name='generate_wordform'),
    path('search_wordform/', search_wordform, name='search_wordform'),
    path('generate/<uuid:word_id>/', generate, name='generate'),
    path("delete_word/<uuid:word_id>/", delete_word, name="delete_word"),
]