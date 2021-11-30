from django import forms
from django.contrib.auth.models import User
from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.ProfileUser
        fields = '__all__'
        exclude = ('user',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='Senha',
        # help_text='Sua senha precisa ter no mínimo 6 caracteres'
    )

    password_confirmation = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='Confirmação de senha',
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'password', 'password_confirmation')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_message = {}

        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_confirmation_data = cleaned.get('password_confirmation')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'Email já existe'
        error_msg_password_match = 'As senhas não conferem'
        error_msg_password = 'Sua senha precisa ter no mínimo 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório'

        if self.user:
            if user_db:
                if user_data != user_db.username:
                    validation_error_message['username'] = error_msg_user_exists
            if email_db:
                if email_data != email_db.email:
                    validation_error_message['email'] = error_msg_email_exists
            if password_data:
                if password_data != password_confirmation_data:
                    validation_error_message['password'] = error_msg_password_match
                if len(password_data) < 6:
                    validation_error_message['password_confirmation'] = error_msg_password
        else:
            if  user_db:
                validation_error_message['username'] = error_msg_user_exists
            if email_db:
                validation_error_message['email'] = error_msg_email_exists
            if not password_data:
                validation_error_message['password'] = error_msg_required_field
            if not password_confirmation_data:
                validation_error_message['password'] = error_msg_required_field
            if password_data != password_confirmation_data:
                validation_error_message['password'] = error_msg_password_match
            if len(password_data) < 6:
                validation_error_message['password_confirmation'] = error_msg_password

        if validation_error_message:
            raise (forms.ValidationError(validation_error_message))
