from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, FileResponse
from .forms import *
from .models import *
from .utils import *
from datetime import date
import os, shutil

# Create your views here.
class LoginView(View):
    #atributos de la vista
    template = "loginTemplate.html"
    context = {'title':"login",'form':None}
    #cuando se realizan peticiones get
    def get(self, request:HttpRequest):
        #logica de vista
        id = request.session.get("user_id")
        
        #cerrar la sesion
        if id:
           request.session.flush()
           
        #configuracion del contexto
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
                #retornamos el mensaje de error
                return render(request,ERRORTEMPLATE,INVALIDLOGIN,status=INVALIDLOGIN['code'])

class SignUpView(View):
    #atributos de la vista
    template = 'loginTemplate.html'
    context = {'title':"signup",'form':None}
    #cuando se realizan peticiones get
    def get(self, request:HttpRequest):
        #logica de vista
        id = request.session.get("user_id")
        
        #cerrar la sesion
        if id:
           request.session.flush()
        
        #configuracion del contexto
        self.context['form'] = SignUpForm()
        #logica de vista
        return render(request,self.template,self.context)
    #cuando se realizan peticiones post
    def post(self, request:HttpRequest):
        #obtener el formulario
        form = SignUpForm(request.POST)
        
        #validar formulario
        if not form.is_valid():
            return
        
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
        except Exception:
            #actualizacion del contexto
            self.context['form'] = SignUpForm()
            #retornamos el mensaje de error
            return render(request,ERRORTEMPLATE,INTERNALERROR,status=INTERNALERROR['code'])

class UnitView(View):
    #atributos de la vista
    template = "unit.html"
    context = {'title':"myunit",'caption':"Mi unidad",'user':{},'stats':{}, 'recent': None}
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
        files = File.objects.filter(dir=Directory.objects.get(name=f"user{id}").pk)
        dirs = Directory.objects.filter(user=id)
        self.context['stats']['files'] = 0
        self.context['stats']['dirs'] = dirs.count()
        self.context['stats']['mem'] = 0
        
        #contar archivos y memoria de subdirectorios
        if dirs.count():
            for dir in dirs:
                files = File.objects.filter(dir=dir.pk)
                self.context['stats']['files'] += files.count()
                for file in files:
                    self.context['stats']['mem'] += file.size
        self.context['stats']['mem'] /= 1000000
        
        #si existen archivos, obtener los mas recientes
        if self.context['stats']['files']:
            dt = date.today()
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
    context = {'title':"dirctory",'user':{}}
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
        self.context['fileform'] = FileForm()
        self.context['rmdirform'] = DropDirectoryForm()
        self.context['rmfileform'] = DropFileForm()
        
        #definir el dirname
        try:
            #obtener directorio si existe
            dr = Directory.objects.get(name=dir,user=User.objects.get(id=id).pk)
            self.context['caption'] = dr.name
            
            #obtener la jerarquia
            self.context['crumbs'] = [dir for dir in dr.hierarchy.split("/") if dir != ""]
            
            #obtener directorios internos
            self.context['innerdirs'] = Directory.objects.filter(hierarchy__icontains=dr.hierarchy,level=dr.level+1)
            
            #obtener archivos del directorio
            self.context['dirfiles'] = File.objects.filter(dir=dr.pk)
            
            #retornar vista
            return render(request,self.template,self.context)
        except Directory.DoesNotExist:
            return render(request,ERRORTEMPLATE,NOTFOUNDDIR)
        
    #cuando se realizan peticiones post
    def post(self,request:HttpRequest,dir:str):        
        #verificrar que el directorio exista
        try:
            #obtener el directorio
            dr = Directory.objects.get(name=dir,user=User.objects.get(id=self.context['user']['id']).pk)
            
            #obtener el tipo
            type = request.POST.get("type")
            
            #manejar los formularios
            if type == "dir":
                self.handle_dir(request,dr)
            elif type == "file":
                self.handle_file(request,dr)
            elif type == "rm-dir":
                if self.handle_rmdir(request,dr):
                    #redirigir a un directorio superior
                    hr = [d for d in dr.hierarchy.split("/") if d != ""]
                    return redirect(f"/dir/{hr[len(hr)-2]}")
                else:
                    #se intento eliminar la raiz
                    raise Exception()
            elif type == "up-dir":
                if self.handle_update(request,dr):
                    #redirigir a carpeta actualizada
                    return redirect(f"/dir/{dr.name}")
                else:
                    #se intento modificar la raiz
                    raise Exception()
            #retornar vista
            return render(request,self.template,self.context)
        except Directory.DoesNotExist:
            return render(request,ERRORTEMPLATE,NOTFOUNDDIR,status=NOTFOUNDDIR['code'])
        except Exception:
            return render(request,ERRORTEMPLATE,INTERNALERROR,status=INTERNALERROR['code'])
    
    def handle_dir(self,request:HttpRequest,dr:Directory):
        #obtener nuevo directorio
        dform = DirectoryForm(request.POST)
        
        #validar el formulario
        if not dform.is_valid():
            return 
        
        #nombre de la nueva carpeta
        name = dform.cleaned_data['name']
        #creamos el directorio en la bd
        Directory.objects.create(name=name,hierarchy=dr.hierarchy+name+"/",level=dr.level+1,user=User.objects.get(id=self.context['user']['id']))
        #creamos el directorio fisicamente
        os.mkdir(CLOUD_DIR+dr.hierarchy+name)
        #refrescar directorios
        self.context['innerdirs'] = Directory.objects.filter(hierarchy__icontains=dr.hierarchy,level=dr.level+1)
    
    def handle_file(self,request:HttpRequest,dr:Directory):
        #obtener nuevo directorio
        fform = FileForm(request.POST, request.FILES)
        
        #validar el formulario
        if not fform.is_valid():
            return
        
        #obtener el archivo
        file = request.FILES['file']
        
        #guardar en bd
        File.objects.create(name=file.name,size=file.size,date=date.today().strftime("%Y-%m-%d"),dir=dr)
        
        #guardar fisicamente
        with open(CLOUD_DIR+dr.hierarchy+file.name,"wb+") as destination:
            #escribir chunks de datos
            for chunk in file.chunks():
                destination.write(chunk)
            #cerrar el archivo
            destination.close()
            del destination
        
        #refrescar los archivos
        self.context['dirfiles'] = File.objects.filter(dir=dr.pk)
    
    def handle_rmdir(self,request:HttpRequest,dr:Directory):
        #obtener datos del formulario
        rdform = DropDirectoryForm(request.POST)
        
        #validar formulario
        if not rdform.is_valid() or dr.name.find("user") != -1:
            return False
        
        #obtener directorios internos
        dirs = Directory.objects.filter(hierarchy__icontains=dr.name)
        
        #eliminar directorios
        for dir in dirs:
            dir.delete() #elimina archivos por cascadeo
            
        #eliminar fisicamente
        shutil.rmtree(CLOUD_DIR+dr.hierarchy[:-1])
        
        #redirigir
        return True
    
    def handle_update(self,request:HttpRequest,dr:Directory):
        #obtener datos del formulario
        updirform = UpdateDirectoryForm(request.POST)
        
        #verificar si es valido
        if not updirform.is_valid() or dr.name.find("user") != -1:
            return False
        
        #obtener el nombre
        old_name = dr.name
        old_hierarchy = dr.hierarchy
        
        #si no cambio nada
        if old_name == updirform.cleaned_data['name']:
            return True
        
        #actualizar en bd (nombre y jerarquia)
        dr.name = updirform.cleaned_data['name']
        dr.hierarchy = dr.hierarchy.replace(old_name,dr.name)
        #guardar
        dr.save()
        #actualizar jerarquias
        dirs = [dir for dir in Directory.objects.filter(hierarchy__icontains=old_name) if dir.pk != dr.pk]
        for dir in dirs:
            dir.hierarchy = dir.hierarchy.replace(old_name,dr.name)
            dir.save()
        #renombrar fisicamente
        os.rename(CLOUD_DIR+old_hierarchy,CLOUD_DIR+dr.hierarchy)
        
        return True
        
class FileView(View):
    #cuando se realizen peticiones get
    def get(self, request:HttpRequest, file:str):
        #obtener el id
        id = request.session.get("user_id")
        
        #verificar el login
        if not id:
            return redirect("/")
        
        #validar el archivo
        try:
            #obtener el archivo
            fl = File.objects.get(name=file)
            
            #obtener la ruta
            path = Directory.objects.get(name=fl.dir.name).hierarchy + fl.name
            
            handler = open("rb+",CLOUD_DIR+path)
            
            #retornar el archivo
            return FileResponse(handler,as_attachment=True,filename=os.path.basename(path))
        except File.DoesNotExist:
            return render(request,ERRORTEMPLATE,NOTFOUNDFILE,status=NOTFOUNDFILE['code'])
        
    def post(self, request:HttpRequest, file:str):
        #validar existenia del archivo
        try:
            #obtener el archivo
            fl = File.objects.get(name=file)
            
            #obtener la accion
            type = request.POST.get("type")
            
            #segun el tipo
            if type == "rm-file":
                #eliminar el archivo de la bd
                fl.delete()
                #eliminar fisicamente el archivo
                os.remove(CLOUD_DIR+fl.dir.hierarchy+file)
            elif type == "up-file":
                self.handle_update(request,fl)
            return redirect(f"/dir/{fl.dir.name}")
        except File.DoesNotExist:
            return render(request,ERRORTEMPLATE,NOTFOUNDFILE,status=NOTFOUNDFILE['code'])
        except Exception as e:
            return render(request,ERRORTEMPLATE,INTERNALERROR,status=INTERNALERROR['code'])
        
    def handle_update(self,request:HttpRequest,fl:File):
        #obtener informacion del formulario
        upform = UpdateFileForm(request.POST,user_id=request.session.get("user_id"))
        
        #validar formulario
        if not upform.is_valid():
            return
        
        #guardar previos
        old_dir = fl.dir
        old_name = fl.name
        
        #si no cambio nada
        if old_name == upform.cleaned_data['name'] and old_dir.pk == upform.cleaned_data['dir'].pk:
            return
        
        #actualizar nombre
        if old_name != upform.cleaned_data['name']:
            #primero en la bd
            fl.name = upform.cleaned_data['name']
            #guardar
            fl.save()
            #renombrar fisicamente
            os.rename(CLOUD_DIR+old_dir.hierarchy+old_name,CLOUD_DIR+old_dir.hierarchy+fl.name)
        
        #actualizar el directorio
        if old_dir.pk != upform.cleaned_data['dir'].pk:
            #primero en la bd
            fl.dir = upform.cleaned_data['dir']
            #guardar
            fl.save()
            #mover fisicamente
            shutil.move(CLOUD_DIR+old_dir.hierarchy+fl.name,CLOUD_DIR+fl.dir.hierarchy+fl.name)

class UpdateFileView(View):
    #atributos de clase
    template = "update.html"
    context = {'user':{}}
    #metodo get para vista
    def get(self, request:HttpRequest, file:str):
        #obtener el id
        id = request.session.get("user_id")
        
        #verificar el login
        if not id:
            return redirect("/")
        
        #manejo de error
        try:
            #obtener archivo
            fl = File.objects.get(name=file)
            
            #añadir nombre de archivo
            self.context['dofname'] = file
            self.context['type'] = "file"
            
            #formulario de actualizacion
            self.context['form'] = UpdateFileForm(user_id=id,initial={'name':fl.name,'dir':fl.dir})
            
            #guardar info de usuario
            self.context['user']['id'] = id
            self.context['user']['name'] = request.session.get("user_name")
            self.context['user']['mail'] = request.session.get("user_mail")
            
            return render(request,self.template,self.context)
        except File.DoesNotExist:
            return render(request,ERRORTEMPLATE,NOTFOUNDFILE,status=NOTFOUNDFILE['code'])
        
    #cuando se realiza peticion post
    def post(self,request:HttpRequest):
        #retornar la plantilla
        return redirect("/")

class UpdateDirectoryView(View):
    #atributos de clase
    template = "update.html"
    context = {'user':{}}
    #metodo get para vista
    def get(self, request:HttpRequest, dir:str):
        #obtener el id
        id = request.session.get("user_id")
        
        #verificar el login
        if not id:
            return redirect("/")
        
        #manejo de error
        try:
            #obtener archivo
            dr = Directory.objects.get(name=dir)
            
            #añadir nombre de archivo
            self.context['dofname'] = dir
            self.context['type'] = "dir"
            
            #formulario de actualizacion
            self.context['form'] = UpdateDirectoryForm(initial={'name':dr.name})
            
            #guardar info de usuario
            self.context['user']['id'] = id
            self.context['user']['name'] = request.session.get("user_name")
            self.context['user']['mail'] = request.session.get("user_mail")
            
            return render(request,self.template,self.context)
        except File.DoesNotExist:
            return render(request,ERRORTEMPLATE,NOTFOUNDDIR,status=NOTFOUNDDIR['code'])
        
    #cuando se realiza peticion post
    def post(self,request:HttpRequest):
        #retornar la plantilla
        return redirect("/")