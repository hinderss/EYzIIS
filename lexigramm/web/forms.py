from django import forms

PARTS_OF_SPEECH = [
    ('VERB', 'Глагол'),
    ('NOUN', 'Существительное'),
    ('ADJ', 'Прилагательное'),
    ('ADV', 'Наречие'),
]

FEATURES_BY_POS = {
    'VERB': [
        ('VBD', 'Прошедшее время'),
        ('VBZ', '3-е лицо единственного числа настоящего времени'),
        ('VBG', 'Герундий/причастие настоящего времени'),
        ('VBN', 'Причастие прошедшего времени'),
        ('VB', 'Базовая форма'),
    ],
    'NOUN': [
        ('NN', 'Единственное число'),
        ('NNS', 'Множественное число'),
        ('NNP', 'Имя собственное, единственное число'),
        ('NNPS', 'Имя собственное, множественное число'),
    ],
    'ADJ': [
        ('JJ', 'Прилагательное'),
        ('JJR', 'Сравнительная степень'),
        ('JJS', 'Превосходная степень'),
    ],
    'ADV': [
        ('RB', 'Наречие'),
        ('RBR', 'Сравнительная степень'),
        ('RBS', 'Превосходная степень'),
    ],
}


class WordForm(forms.Form):
    word_base = forms.CharField(label="Основа слова", max_length=100)
    part_of_speech = forms.ChoiceField(label="Часть речи", choices=PARTS_OF_SPEECH)
    feature = forms.ChoiceField(label="Характеристика", choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'part_of_speech' in self.data:
            pos = self.data['part_of_speech']
            self.fields['feature'].choices = FEATURES_BY_POS.get(pos, [])


class SearchForm(forms.Form):
    query = forms.CharField(label="Запрос", max_length=100, required=False)
    pos = forms.ChoiceField(label="Часть речи", choices=[("", "")] + PARTS_OF_SPEECH, required=False)
    tag = forms.ChoiceField(label="Характеристика", choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'pos' in self.data:
            pos = self.data['pos']
            self.fields['tag'].choices = [(None, "")] + FEATURES_BY_POS.get(pos, [])
