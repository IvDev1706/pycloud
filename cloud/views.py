from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .models import *

# Create your views here.
class LoginView(View):
    #atributos de la vista
    template = "login.html"
    #cuando se realizan peticiones get
    def get(self, request):
        #logica de vista
        return render(request,self.template,{'form':LoginForm(),'error':''})
    #cuando se realizan peticiones post
    def post(self, request):
        #logica de vista
        id = request.session.get('user_id')
        
        #cerrar la sesion
        if id:
           request.session.flush()
        
        #obtener el formulario
        form = LoginForm(request.POST)
        
        #validar formulario
        if form.is_valid():
            #obtener los datos ingresados
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            #verificamos que exista en la bd
            try:
                #pedir informacion de la bd
                user = User.objects.get(name=name,password=password)
                #guardar el id en la request
                request.session['user_id'] = user.pk
                #redirigir
                return redirect(f'myunit/')
            except User.DoesNotExist:
                #retornamos el mensaje de error
                return render(request,self.template,{'form':LoginForm(),'error':'Acceso invalido, usuario o contraseña incorrecto'})