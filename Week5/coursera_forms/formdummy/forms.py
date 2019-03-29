from django import forms


class DummyForm(forms.Form):
    text = forms.CharField(label='Отзыв', min_length=3, max_length=10)
    grade = forms.IntegerField(label='Оценка', min_value=1, max_value=100)
    image = forms.FileField(label='Фотография', required=False)

    def clean_text(self):
        if 'abc' not in self.cleaned_data['text']:
            raise forms.ValidationError('Вы не о том пишете')


class ProductForm(forms.Form):
    uid = forms.CharField(label='Идентификатор', max_length=10)
    title = forms.CharField(label='Наименование', max_length=100)
    price = forms.DecimalField(
      label='Цена', max_value=10000, decimal_places=2, required=False
    )