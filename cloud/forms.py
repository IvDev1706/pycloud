from django import forms
from .models import Directory

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
    type = forms.CharField(label="",widget=forms.HiddenInput(),initial="dir")
    
class FileForm(forms.Form):
    #campos del formulario
    file = forms.FileField(label="Seleccionar archivo:",required=True,allow_empty_file=False)
    type = forms.CharField(label="",widget=forms.HiddenInput(),initial="file")
    
class DropDirectoryForm(forms.Form):
    #campos del formulario
    type = forms.CharField(label="",widget=forms.HiddenInput(),initial="rm-dir")
    
class DropFileForm(forms.Form):
    #campos del formulario
    type = forms.CharField(label="",widget=forms.HiddenInput(),initial="rm-file")
    
class UpdateFileForm(forms.Form):
    #campos del formulario
    name = forms.CharField(label="Nombre del archivo:",strip=True,max_length=50,widget=forms.TextInput(attrs={'required':True,'class':'inpt'}))
    dir = forms.ModelChoiceField(label="Carpeta contenedora:",queryset=Directory.objects.none(),required=True,empty_label="-- seleccione carpeta --")
    type = forms.CharField(label="",widget=forms.HiddenInput(),initial="up-file")
    #sobreescribir init
    def __init__(self, *args, **kargs):
        #extraer el id
        id = kargs.pop("user_id",None)
        #instancia de padre
        super().__init__(*args,**kargs)
        
        #si existe el id. obtener carpetas
        if not id:
            return
        
        #guardar el queryset
        self.fields['dir'].queryset = Directory.objects.filter(user=id)