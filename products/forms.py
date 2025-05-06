import re
from .models import Product, Category
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Vacancy, Comment


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['full_name', 'phone_number', 'about']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя и фамилию'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Расскажите о себе'}),
        }

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if not re.match(r'^[А-ЯЁа-яёA-Za-z\s-]+$', full_name):
            raise forms.ValidationError("Имя и фамилия могут содержать только буквы и пробелы.")
        return full_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not re.match(r'^\+?\d{11}$', phone_number):
            raise forms.ValidationError("Введите корректный номер телефона (от 11 цифр).")
        return phone_number


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'cat', 'discount', 'image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
