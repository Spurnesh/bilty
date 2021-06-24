from .models import Role, NosName, Bilty, User
from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

# User = get_user_model()


class NosNameForm(forms.ModelForm):
    class Meta:
        model = NosName
        fields = '__all__'
        exclude = ['status']


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        exclude = ['status']


NosNameFormSet = inlineformset_factory(Role, NosName,
                                            form=NosNameForm, extra=1)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email',  'password', 'confirm_password', 'phone', 'address']

    def clean(self):
        # data from the form is fetched using super function
        super(UserForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        # conditions to be met for the username

        if not password == confirm_password:
            self._errors['password'] = self.error_class([
                'password and confirm password not matched'])
        return self.cleaned_data


class BiltyForm(forms.ModelForm):

    class Meta:
        model = Bilty
        fields = '__all__'