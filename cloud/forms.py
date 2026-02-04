from django import forms

#login de la pagina
class LoginForm(forms.Form):
    #campos del formulario
    name = forms.CharField(label="Nombre de usuario:",strip=True,max_length=15,widget=forms.TextInput(attrs={'required':True,'class':'inpt'}))
    password = forms.CharField(label="Contraseña:",strip=True,max_length=10,widget=forms.PasswordInput(attrs={'required':True,'class':'inpt'}))
    
#signup de la pagina
class SignUpForm(forms.Form):
    #campos del formulario
    name = forms.CharField(label="Nombre de usuario:",strip=True,max_length=15,widget=forms.TextInput(attrs={'required':True,'class':'inpt','placeholder':'john doe'}))
    password = forms.CharField(label="Contraseña:",strip=True,max_length=10,widget=forms.PasswordInput(attrs={'required':True,'class':'inpt','placeholder':'a password'}))
    email = forms.EmailField(label="Correo electronico",max_length=35,widget=forms.EmailInput(attrs={'required':True,'class':'inpt','placeholder':'jdoe@example.com'}))

class DirectoryForm(forms.Form):
    #campos del formulario
    name = forms.CharField(label="Nombre de la carpeta:",strip=True,max_length=20,widget=forms.TextInput(attrs={'required':True,'class':'inpt','placeholder':'example'}))