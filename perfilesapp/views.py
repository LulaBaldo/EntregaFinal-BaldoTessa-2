from re import L
from django.shortcuts import render, redirect
from perfilesapp.models import *
from perfilesapp.forms import *
from .models import *
from .forms import *
from django.db.models import Q 
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def inicio(request):
    if request.user.is_authenticated: 
        try:
            avatar= Avatar.objects.get(usuario=request.user)
            url= avatar.imagen.url
        except:
            url= "/media/avatar/generic.png" 
        return render(request, "perfilesapp/inicio.html", {"url":url} ) 


    return render(request, "perfilesapp/inicio.html") 



def login_request(request):
    
    if request.method == "POST":
        
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("inicio")
            else:
                return redirect("login")
        else:
            return redirect("login")
            
    form = AuthenticationForm()
    
    return render(request, "perfilesapp/login.html", {"form":form})

def register_request(request):
    
    if request.method == "POST":
        
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('pasword1')
            
            form.save()
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("inicio")
            else:
                return redirect("login")
            
    
        return render(request, "perfilesapp/register.html", {"form":form})
    
    form = UserRegisterForm()
    
    return render(request, "perfilesapp/register.html", {"form":form})

def logout_request(request):
    logout(request)
    return redirect("inicio")


@login_required
def editar_perfil(request):

    user=request.user

    if request.method == "POST":      
        form = UserEditForm(request.POST)

        if form.is_valid():

            info = form.cleaned_data
            user.email= info["email"]
            user.first_name= info["first_name"]
            user.last_name= info["last_name"]
            user.password1= info["password1"]
            user.password2= info["password1"]
            user.save()

            return redirect("inicio")

        return render(request, "perfilesapp/editar_perfil.html", {"form":form} )

    else:
        form = UserEditForm(initial= {"email":user.email, "first_name":user.first_name, "last_name":user.last_name} )


    return render(request, "perfilesapp/editar_perfil.html", {"form":form} )

@login_required
def formulario_avatar(request):

    if request.method == "POST":
        form= AvatarForm(request.POST, request.FILES)

        if form.is_valid():

            user= User.objects.get(username=request.user)
            avatar= Avatar(usuario=user, imagen=form.cleaned_data["imagen"])
            avatar.save()
  #          avatar= Avatar()
   #         avatar.usuario= request.user
   #         avatar.imagen= form.cleaned_data["imagen"]
    #        avatar.save()

            return redirect("inicio")
    else:
            form= AvatarForm()
        
    return render(request, "perfilesapp/formulario_avatar.html", {"form": form})


def socios(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            socios = Socios.objects.filter( Q(nombre__icontains=search) | Q(apellido__icontains=search)).values()
            return render(request,"perfilesapp/socios.html", {"socios": socios, "search":True, "busqueda":search})

    socios = Socios.objects.all()
    return render(request, "perfilesapp/socios.html", {"socios": socios} )

def tienda(request):
    tiendaactividades = TiendaActividad.objects.all()
    tiendaobjetos = TiendaObjetos.objects.all()
    return render(request, "perfilesapp/tienda.html", {"tiendaactividades": tiendaactividades, "tiendaobjetos": tiendaobjetos})

def objetos(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            tiendaobjetos = TiendaObjetos.objects.filter( Q(producto__icontains=search) ).values()
            return render(request,"perfilesapp/objetos.html", {"tiendaobjetos": tiendaobjetos, "search":True, "busqueda":search})


    tiendaobjetos = TiendaObjetos.objects.all()
    return render(request, "perfilesapp/objetos.html", {"tiendaobjetos": tiendaobjetos})    

@staff_member_required
def crear_objeto(request):

    if request.method == "POST":
        formulario=ObjetoFormulario(request.POST, request.FILES)
        
        if formulario.is_valid():
            info_objeto=formulario.cleaned_data
            objeto= TiendaObjetos()
            objeto.producto = info_objeto["producto"]
            objeto.descripcion = info_objeto["descripcion"]
            objeto.precio = info_objeto["precio"]
            objeto.imagen = info_objeto["imagen"]
            objeto.save()
            return redirect("objetos")
        
        else:
            print("Error en el formulario")
            return redirect("crear_objeto")
    
    else:
        formulariovacio=ObjetoFormulario()
        return render(request, "perfilesapp/formulario_objeto.html", {"form":formulariovacio})

def buscar_objeto(request):

    if request.method == "POST":

        info_objeto = request.POST["objetos"]
        
        tiendaobjetos = TiendaObjetos.objects.filter(producto__icontains=info_objeto).values()
        

        return render(request,"perfilesapp/buscar_objeto.html",{"tiendaobjetos": tiendaobjetos})

    else: # get y otros

        tiendaobjetos =  []  
        
        return render(request,"perfilesapp/buscar_objeto.html",{"tiendaobjetos": tiendaobjetos})

@staff_member_required
def eliminar_objeto(request, objeto_id):
    objetos = TiendaObjetos.objects.get(id=objeto_id)
    objetos.delete()
    
    return redirect("objetos")

@staff_member_required
def editar_objeto(request, objeto_id):
    objeto = TiendaObjetos.objects.get(id=objeto_id)
    
    if request.method == "POST":
    
        formulario = ObjetoFormulario(request.POST, request.FILES or None)
        if formulario.is_valid():
            info_objeto = formulario.cleaned_data
            objeto.producto = info_objeto["producto"]
            objeto.descripcion = info_objeto["descripcion"]
            objeto.precio = info_objeto["precio"]
            objeto.imagen = info_objeto["imagen"]
            objeto.save()
            return redirect ("objetos")
    
     #get
    formulario_vacio = ObjetoFormulario(
        initial={
            "producto":objeto.producto,
            "descripcion": objeto.descripcion,
            "precio": objeto.precio,
            "imagen": objeto.imagen
        })
    

    return render(request, "perfilesapp/editar_objeto.html", {"form":formulario_vacio})    
        

def municipal(request):
    return render(request, "perfilesapp/municipal.html")

def cro(request):
    return render(request, "perfilesapp/cro.html")

def cursos(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            cursos = TiendaActividad.objects.filter( Q(actividad__icontains=search) | Q(profesor__icontains=search)).values()
            return render(request,"perfilesapp/cursos.html", {"cursos": cursos, "search":True, "busqueda":search})


    cursos = TiendaActividad.objects.all()
    return render(request, "perfilesapp/cursos.html", {"cursos": cursos})    

@staff_member_required
def crear_curso(request):
    if request.method == "GET":
        formulariovacio=CursoFormulario()
        return render(request, "perfilesapp/formulario_curso.html", {"form":formulariovacio})  
    
    elif request.method == "POST":
        formulario=CursoFormulario(request.POST, request.FILES)    
        
        if formulario.is_valid():
            info_curso=formulario.cleaned_data
            
            curso= TiendaActividad(actividad=info_curso["actividad"], profesor=info_curso["profesor"], dias=info_curso["dias"], turno=info_curso["turno"], precio=info_curso["precio"], imagen=info_curso["imagen"] )
            curso.save()
            return redirect("cursos")
        else:
             return redirect("cursos")
    else:
        return render(request, "perfilesapp/formulario_cursos.html", {})


def buscar_curso(request):

    if request.method == "POST":

        info_curso = request.POST["cursos"]
        
        tiendaactividades = TiendaActividad.objects.filter(actividad__icontains=info_curso).values()
        

        return render(request,"perfilesapp/buscar_curso.html",{"tiendaactividades":tiendaactividades})

    else: # get y otros

        tiendaactividades =  []  #Curso.objects.all()
        
        return render(request,"perfilesapp/buscar_curso.html",{"tiendaactividades":tiendaactividades})

@staff_member_required  
def eliminar_curso(request, curso_id):
    cursos = TiendaActividad.objects.get(id=curso_id)
    cursos.delete()
    
    return redirect("cursos")

@staff_member_required
def editar_curso(request, curso_id):
    cursos = TiendaActividad.objects.get(id=curso_id)
    
    if request.method == "POST":
    
        formulario = CursoFormulario(request.POST, request.FILES or None, curso_id)
        if formulario.is_valid():

            info_curso = formulario.cleaned_data
            cursos.actividad = info_curso["actividad"]
            cursos.profesor = info_curso["profesor"]
            cursos.dias = info_curso["dias"]
            cursos.turno = info_curso["turno"]
            cursos.precio = info_curso["precio"]
                
            if request.FILES:
                cursos.imagen = request.FILES["imagen"]
                cursos.save()
            return redirect ("cursos")

    
    #get
    formulario_vacio = CursoFormulario(initial={"actividad":cursos.actividad,
                                              "profesor":cursos.profesor,
                                              "dias": cursos.dias,
                                              "turno":cursos.turno,
                                              "precio":cursos.precio,
                                              "imagen": cursos.imagen})
   
    return render(request, "perfilesapp/editar_curso.html", {"form":formulario_vacio})     

def nosotros(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            profesores = Profesor.objects.filter( Q(nombreprofesor__icontains=search) | Q(apellidoprofesor__icontains=search)).values()
            return render(request,"perfilesapp/nosotros.html", {"profesores": profesores, "search":True, "busqueda":search})


    profesores = Profesor.objects.all()
    return render(request, "perfilesapp/nosotros.html", {"profesores": profesores})

def blog(request):
    blogs= Blog.objects.all()

    return render(request, "perfilesapp/blog.html", {"blogs": blogs})

@staff_member_required
def crear_blog(request):

    if request.method == "GET":
        formulariovacio=BlogForm()
        return render(request, "perfilesapp/formulario_blog.html", {"form":formulariovacio})

    elif request.method == "POST":

        formulario=BlogForm(request.POST, request.FILES)

        if formulario.is_valid():

            info_blog=formulario.cleaned_data

            blog=Blog(titulo=info_blog["titulo"], subtitulo=info_blog["subtitulo"], texto=info_blog["texto"], imagen=info_blog["imagen"], autor=info_blog["autor"], fecha=info_blog["fecha"])
            blog.save()
            return redirect("blog")
        else:
             return redirect("blog")
        
    else:
        return render(request, "perfilesapp/formulario_blog.html")

@staff_member_required 
def eliminar_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    
    return redirect("blog")

@staff_member_required
def editar_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    
    if request.method == "POST":
    
        formulario = BlogForm(request.POST, request.FILES)
        if formulario.is_valid():
            info_blog = formulario.cleaned_data
            blog.titulo = info_blog["titulo"]
            blog.subtitulo = info_blog["subtitulo"]
            blog.texto = info_blog["texto"]
            blog.imagen = info_blog["imagen"]
            blog.autor = info_blog["autor"]
            blog.fecha = info_blog["fecha"]
            blog.save()
        
            return redirect ("blog")
        
    
    #get
    formulario_vacio = BlogForm(initial={"titulo":blog.titulo, 
                                              "subtitulo":blog.subtitulo,
                                              "texto":blog.texto,
                                              "imagen": blog.imagen,
                                              "autor":blog.autor,
                                              "fecha":blog.fecha,
                                              })
    
    return render(request, "perfilesapp/editar_blog.html", {"form":formulario_vacio}) 
 
def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)   
    return render(request, "perfilesapp/blog_detail.html", {"blog": blog})

def buscar_blog(request):

    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            blog = Blog.objects.filter( Q(titulo__icontains=search) | Q(autor__icontains=search)).values()
            return render(request,"perfilesapp/blog.html", {"blog": blog, "search":True, "busqueda":search})

    blog = Blog.objects.all()
    return render(request, "perfilesapp/blog.html", {"blog": blog} )



def profesores(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            profesores = Profesor.objects.filter( Q(nombreprofesor__icontains=search) | Q(apellidoprofesor__icontains=search)).values()
            return render(request,"perfilesapp/profesores.html", {"profesores": profesores, "search":True, "busqueda":search})


    profesores = Profesor.objects.all()
    return render(request, "perfilesapp/profesores.html", {"profesores": profesores} )


@staff_member_required
def crear_profesor(request):

    if request.method == "GET":
        formulariovacio=ProfesorFormulario()
        return render(request, "perfilesapp/formulario_profe.html", {"form":formulariovacio})

    elif request.method == "POST":

        formulario=ProfesorFormulario(request.POST)

        if formulario.is_valid():

            info_profe=formulario.cleaned_data

            profesores=Profesor(nombreprofesor=info_profe["nombreprofesor"], apellidoprofesor=info_profe["apellidoprofesor"], edadprofesor=info_profe["edadprofesor"], emailprofesor=info_profe["emailprofesor"])
            profesores.save()
            return redirect("profesores")
        else:
             return redirect("profesores")
        
    else:
        return render(request, "perfilesapp/formulario_profe.html")

def buscar_profesor(request):

    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            profesor = Profesor.objects.filter( Q(nombreprofesor__icontains=search) | Q(apellidoprofesor__icontains=search)).values()
            return render(request,"perfilesapp/profesores.html", {"profesor": profesor, "search":True, "busqueda":search})

    profesor = Profesor.objects.all()
    return render(request, "perfilesapp/profesores.html", {"profesor": profesor} )

@staff_member_required 
def eliminar_profesor(request, profesor_id):
    profesor = Profesor.objects.get(id=profesor_id)
    profesor.delete()
    
    return redirect("profesores")

@staff_member_required
def editar_profesor(request, profesor_id):
    profesor = Profesor.objects.get(id=profesor_id)
    
    if request.method == "POST":
    
        formulario = ProfesorFormulario(request.POST)
        if formulario.is_valid():
            info_profesor = formulario.cleaned_data
            profesor.nombreprofesor = info_profesor["nombreprofesor"]
            profesor.apellidoprofesor = info_profesor["apellidoprofesor"]
            profesor.edadprofesor = info_profesor["edadprofesor"]
            profesor.emailprofesor = info_profesor["emailprofesor"]
            profesor.save()
        
            return redirect ("profesores")
        
    
    #get
    formulario_vacio = ProfesorFormulario(initial={"nombreprofesor":profesor.nombreprofesor,
                                              "apellidoprofesor":profesor.apellidoprofesor,
                                              "edadprofesor": profesor.edadprofesor,
                                              "emailprofesor":profesor.emailprofesor})
    
    return render(request, "perfilesapp/editar_profesor.html", {"form":formulario_vacio})    
 
 
@staff_member_required     
def crear_socio(request):
    if request.method == "GET":
        formulariovacio=SocioFormulario()
        return render(request, "perfilesapp/formulario_socio.html", {"form":formulariovacio})  
    
    elif request.method == "POST":
        formulario=SocioFormulario(request.POST)    
        
        if formulario.is_valid():
            info_socio=formulario.cleaned_data
            
            socio= Socios(nombre=info_socio["nombre"], apellido=info_socio["apellido"], edad=info_socio["edad"], fechanacimiento=info_socio["fechanacimiento"], email=info_socio["email"] )
            socio.save()
            return redirect("socios")
        else:
             return redirect("socios")
    else:
        return render(request, "perfilesapp/formulario_socio.html", {})

@login_required
def buscar_socio(request):

    if request.method == "POST":

        info_socio = request.POST["socios"]
        
        socio = Socios.objects.filter(nombre=info_socio).values()
        

        return render(request,"perfilesapp/buscar_socio.html",{"socios":socio})

    else: # get y otros

        socio =  []  #Curso.objects.all()
        
        return render(request,"perfilesapp/buscar_socio.html",{"socios":socio})

@staff_member_required
def eliminar_socio(request, socio_id):
    socios = Socios.objects.get(id=socio_id)
    socios.delete()
    
    return redirect("socios")

@staff_member_required
def editar_socio(request, socio_id):
    socio = Socios.objects.get(id=socio_id)
    
    if request.method == "POST":
    
        formulario = SocioFormulario(request.POST)
        if formulario.is_valid():
            info_socio = formulario.cleaned_data
            socio.nombre = info_socio["nombre"]
            socio.apellido = info_socio["apellido"]
            socio.edad = info_socio["edad"]
            socio.email = info_socio["email"]
            socio.fechanacimiento = info_socio["fechanacimiento"]
            socio.save()
        
            return redirect ("socios")
        
    
    #get
    formulario_vacio = SocioFormulario(initial={"nombre":socio.nombre,
                                              "apellido":socio.apellido,
                                              "edad": socio.edad,
                                              "email":socio.email,
                                              "fechanacimiento":socio.fechanacimiento})
    
    return render(request, "perfilesapp/editar_socio.html", {"form":formulario_vacio})    
        

 



  

