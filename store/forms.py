from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'address']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 010 1234 5678',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Delivery address',
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        digits = phone.replace(' ', '').replace('-', '').replace('+', '')
        if not digits.isdigit() or len(digits) < 8:
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone
