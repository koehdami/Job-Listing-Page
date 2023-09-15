from django import forms

contactInputClass = "w-100 border border-2 border-dark rounded px-2 py-1"

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': contactInputClass}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': contactInputClass}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': contactInputClass}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': contactInputClass}))
    context = forms.CharField(widget=forms.Textarea(attrs={'class': contactInputClass, 'rows':'20'}), required=True)
    checkboxAGB = forms.CheckboxInput()
