from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest
from .forms import *
from .models import *
from datetime import date
from PyCloud.settings import CLOUD_DIR
import os

# Create your views here.
class LoginView(View):
    #atributos de la vista
    template = "loginTemplate.html"
    context = {'title':"login",'form':None,'error':""}
    #cuando se realizan peticiones get
    def get(self, request:HttpRequest):
        #logica de vista
        id = request.session.get("user_id")
        
        #cerrar la sesion
        if id:
           request.session.flush()
           
        #configuracion del contexto
        if self.context != "":
            self.context['error'] = ""
        self.context['form'] = LoginForm()
        #logica de vista
        return render(request,self.template,self.context)
    #cuando se realizan peticiones post
    def post(self, request:HttpRequest):
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
        #logica de vista
        id = request.session.get("user_id")
        
        #cerrar la sesion
        if id:
           request.session.flush()
        
        #configuracion del contexto
        if self.context != '':
            self.context['error'] = ''
        self.context['form'] = SignUpForm()
        #logica de vista
        return render(request,self.template,self.context)
    #cuando se realizan peticiones post
    def post(self, request:HttpRequest):
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
                #crear directorio raiz
                dir = Directory.objects.create(name=f"user{user.pk}",hierarchy=f"user{user.pk}/",level=0,user=user)
                #crear fisicamente el directorio fisico
                os.mkdir(CLOUD_DIR+dir.name,mode=0o775)
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
    context = {'title':"myunit",'user':{},'stats':{}, 'recent': None}
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
        
        #obtener estadisticas de la nube
        files = File.objects.filter(dir=f"user{id}")
        dirs = Directory.objects.filter(user=id)
        self.context['stats']['files'] = files.count()
        self.context['stats']['dirs'] = dirs.count()
        self.context['stats']['mem'] = 0
        
        #contar archivos y memoria de subdirectorios
        if dirs.count():
            for dir in dirs:
                files = File.objects.filter(dir=dir.name)
                self.context['stats']['files'] += files.count()
                for file in files:
                    self.context['stats']['mem'] += file.size
        
        #si existen archivos, obtener los mas recientes
        if self.context['stats']['files']:
            dt = date()
            #obtener files
            self.context['recent'] = File.objects.filter(date__year=dt.year,date__month=dt.month).order_by("-date")[:10]
                
        #retornar la plantilla
        return render(request,self.template,self.context)
    #cuando se realiza peticion post
    def post(self,request:HttpRequest):
        #retornar la plantilla
        return redirect("/")
    
class DirectoryView(View):
    #atributos de la vista
    template = "dir.html"
    context = {'title':'dirctory','user':{}}
    #cuando se realiza peticiones get
    def get(self,request:HttpRequest,dir:str):
        #obtener el id
        id = request.session.get("user_id")
        
        #verificar el login
        if not id:
            return redirect("/")
        
        #guardar info de usuario
        self.context['user']['id'] = id
        self.context['user']['name'] = request.session.get("user_name")
        self.context['user']['mail'] = request.session.get("user_mail")
        
        #formularios de accion
        self.context['dirform'] = DirectoryForm()
        
        #definir el dirname
        try:
            #obtener directorio si existe
            dr = Directory.objects.get(name=dir,user=User.objects.get(id=id))
            self.context['dirname'] = dr.name
            
            #obtener la jerarquia
            self.context['crumbs'] = [dir for dir in dr.hierarchy.split("/") if dir != ""]
            
            #obtener directorios internos
            self.context['innerdirs'] = Directory.objects.filter(hierarchy__icontains=dr.hierarchy,level=dr.level+1)
            
            #obtener archivos del directorio
            self.context['dirfiles'] = File.objects.filter(dir=dir)
        except Directory.DoesNotExist:
            #mostrar raiz
            self.context['dirname'] = f"user{id}"
            
            #obtener archivos del directorio
            self.context['dirfiles'] = File.objects.filter(dir=f"user{id}")
        
        #retornar vista
        return render(request,self.template,self.context)
        
    #cuando se realizan peticiones post
    def post(self,request:HttpRequest,dir:str):        
        #verificrar que el directorio exista
        try:
            #obtener el directorio
            dr = Directory.objects.get(name=dir)
            
            #obtener nuevo directorio
            dform = DirectoryForm(request.POST)
            
            if dform.is_valid():
                #nombre de la nueva carpeta
                name = dform.cleaned_data['name']
                #creamos el directorio en la bd
                Directory.objects.create(name=name,hierarchy=dr.hierarchy+name+"/",level=dr.level+1,user=User.objects.get(id=self.context['user']['id']))
                #creamos el directorio fisicamente
                os.mkdir(CLOUD_DIR+dr.hierarchy+name)
                #refrescar directorios
                self.context['innerdirs'] = Directory.objects.filter(hierarchy__icontains=dr.hierarchy,level=dr.level+1)
        except Directory.DoesNotExist:
            return render(request,self.template,self.context)
        except Exception:
            return render(request,self.template,self.context)
        
        #retornar vista
        return render(request,self.template,self.context)