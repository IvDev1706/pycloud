from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest
from .forms import *
from .models import *

# Create your views here.
class LoginView(View):
    #atributos de la vista
    template = "loginTemplate.html"
    context = {'title':"login",'form':None,'error':""}
    #cuando se realizan peticiones get
    def get(self, request:HttpRequest):
        #configuracion del contexto
        if self.context != "":
            self.context['error'] = ""
        self.context['form'] = LoginForm()
        #logica de vista
        return render(request,self.template,self.context)
    #cuando se realizan peticiones post
    def post(self, request:HttpRequest):
        #logica de vista
        id = request.session.get("user_id")
        
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
                request.session['user_name'] = user.name
                request.session['user_mail'] = user.email
                #redirigir
                return redirect("/myunit")
            except User.DoesNotExist:
                #actualizacion del contexto
                self.context['form'] = LoginForm()
                self.context['error'] = "Acceso invalido, usuario o contraseña incorrecto"
                #retornamos el mensaje de error
                return render(request,self.template,self.context)

class SignUpView(View):
    #atributos de la vista
    template = 'loginTemplate.html'
    context = {'title':"signup",'form':None,'error':""}
    #cuando se realizan peticiones get
    def get(self, request:HttpRequest):
        #configuracion del contexto
        if self.context != '':
            self.context['error'] = ''
        self.context['form'] = SignUpForm()
        #logica de vista
        return render(request,self.template,self.context)
    #cuando se realizan peticiones post
    def post(self, request:HttpRequest):
        #logica de vista
        id = request.session.get("user_id")
        
        #cerrar la sesion
        if id:
           request.session.flush()
        
        #obtener el formulario
        form = SignUpForm(request.POST)
        
        #validar formulario
        if form.is_valid():
            #obtener los datos ingresados
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            #verificamos que exista en la bd
            try:
                #pedir informacion de la bd
                user = User.objects.create(name=name,password=password,email=email)
                #validar insercion
                if not user:
                    raise Exception("Error al registrar usuario!!")
                #redirigir
                return redirect("/")
            except Exception as e:
                #actualizacion del contexto
                self.context['form'] = SignUpForm()
                self.context['error'] = e
                #retornamos el mensaje de error
                return render(request,self.template,self.context)
            
class UnitView(View):
    #atributos de la vista
    template = "unit.html"
    context = {'title':"myunit",'user':{}}
    #cuando se realiza peticion get
    def get(self,request:HttpRequest):
        #obtener el id
        id = request.session.get("user_id")
        
        #verificar el login
        if not id:
            return redirect("/")
        
        #guardar info de usuario
        self.context['user']['id'] = id
        self.context['user']['name'] = request.session.get("user_name")
        self.context['user']['mail'] = request.session.get("user_mail")
        
        #retornar la plantilla
        return render(request,self.template,self.context)
    #cuando se realiza peticion post
    def post(self,request:HttpRequest):
        #retornar la plantilla
        return render(request,self.template)