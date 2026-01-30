from django import forms

#login de la pagina
class LoginForm(forms.Form):
    #campos del formulario
    name = forms.CharField(label="Nombre de usuario:",strip=True,max_length=15,widget=forms.TextInput(attrs={'required':True,'class':'inpt'}))
    password = forms.CharField(label="Contraseña:",strip=True,max_length=10,widget=forms.PasswordInput(attrs={'required':True,'class':'inpt'}))