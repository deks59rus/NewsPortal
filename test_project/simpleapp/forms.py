from django import forms
from .models import Product
from django.core.exceptions import ValidationError
class ProductForm(forms.ModelForm):

    description = forms.CharField(min_length=20)
    class Meta:
       model = Product
       #fields = '__all__'
       fields = [
           'name',
           'description',
           'quantity',
           'category',
           'price',]

    def clean(self):
       cleaned_data = super().clean()
       description = cleaned_data.get("description")
       name = cleaned_data.get("name")
       if name == description:
           raise ValidationError({
               "description": "Описание не должно быть идентично названию."})
       return cleaned_data
    """
    Выбирайте соответствующий способ валидации данных, исходя из задачи.
    Если можно обойтись переопределением поля формы forms.CharField(min_length=20),
    лучше воспользоваться им. Если требуется проверить одно поле сложным образом, создайте для этого метод clean_fieldname.
    В случае необходимости использования нескольких полей одновременно воспользуйтесь методом clean.
    """