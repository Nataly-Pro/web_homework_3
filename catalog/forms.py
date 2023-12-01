from django import forms
from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('create_date', 'last_mod_date', 'is_published',)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in words:
            if word in cleaned_data.lower().strip():
                raise forms.ValidationError('Нельзя указывать запрещённые продукты')
        return cleaned_data

    def clean_text(self):
        cleaned_data = self.cleaned_data['text']
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in words:
            if word in cleaned_data.lower().strip():
                raise forms.ValidationError('Нельзя указывать запрещённые продукты')
        return cleaned_data


class ModeratorProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('text', 'category', 'is_published',)


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'

