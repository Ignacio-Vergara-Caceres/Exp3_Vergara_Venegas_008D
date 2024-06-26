from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Categoria, Producto, Boleta, detalle_boleta
from .forms import ProductoForm, RegistroUserForm, ActualizarPerfilForm
from django.contrib.auth.models import User
from jardinesVecinosApp.compras import Carrito

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')
def acercaDe(request):
    return render(request, 'acercaDe.html')
def feriados(request):
    return render(request, 'feriados.html')
def filtrar(request):
    return render(request, 'filtrar.html')
def productos(request):
    return render(request, 'productos.html')
def crear(request):
    return render(request, 'crear.html')


@login_required
def productos(request):
    productos = Producto.objects.all()              #similar a select * from Producto
    return render(request, 'productos.html', {'productos':productos})

def crear(request):
    if request.method=='POST':
        productoform = ProductoForm(request.POST, request.FILES)
        if productoform.is_valid():
            productoform.save()         #similar en función al insert into
            return redirect ('productos')
    else:
        productoform=ProductoForm()
    return render(request, 'crear.html',{'productoform':productoform})

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)   #realiza busquedas especificas por atributo pk
    return render (request, 'detalleProducto.html', {'producto':producto})

def modificar(request, id):
    producto = Producto.objects.get(idProducto=id)
    datos={
        'forModificar': ProductoForm(instance=producto),     #crea un obj de tipo formulario
        'producto':  producto
    }
    if request.method=='POST':
        formulario= ProductoForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()               #actualiza la información del obj.
            return redirect('productos')
    return render(request, 'modificar.html', datos)


def eliminar(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    if request.method=='POST':
        if 'elimina' in request.POST:       #botón cuyo name es elimina en html para confirmar
            producto.delete()               #elimina el objeto despues de confirmar
            return redirect ('productos')
        else:
            return redirect ('detalle', idProducto=id)
    return render (request, 'eliminar.html', {'producto': producto})

def cerrar(request):
    logout(request)
    return redirect('inicio')

def registro(request):
    data={
        'form':RegistroUserForm()
    }
    if request.method=='POST':
        formulario = RegistroUserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],
                                password=formulario.cleaned_data["password1"])
            login(request,user)
            return redirect('inicio')
        data["form"]=formulario
    return render(request, 'registration/registro.html',data)

def modificarPerfil(request, username):
    usuario = get_object_or_404(User, username=username)

    if request.method == 'POST':
        formulario = ActualizarPerfilForm(request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            return redirect('modificarPerfil', username=usuario.username)
        else:
            print(formulario.errors)  # Imprime los errores del formulario en la consola
    else:
        formulario = ActualizarPerfilForm(instance=usuario)

    return render(request, 'modificarPerfil.html', {'form': formulario, 'user': usuario})

def agregar_producto(request,id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(idProducto=id)
    carrito_compra.agregar(producto=producto)
    return redirect('tienda')

def eliminar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(idProducto=id)
    carrito_compra.eliminar(producto=producto)
    return redirect('tienda')

def restar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(idProducto=id)
    carrito_compra.restar(producto=producto)
    return redirect('tienda')

def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect('tienda')    

def tienda(request):
    productos = Producto.objects.all()
    return render(request, 'tienda.html', {'productos': productos})


def generarBoleta(request):
    precio_total=0
    for key, value in request.session['carrito'].items():
        precio_total = precio_total + int(value['precio']) * int(value['cantidad'])

    boleta = Boleta(total = precio_total)
    boleta.save()

    productos = []
    for key, value in request.session['carrito'].items():
            producto = Producto.objects.get(idProducto=value['producto_id'])
            cant = value['cantidad']
            subtotal = cant * int(value['precio'])
            detalle = detalle_boleta(idBoleta = boleta, id_producto = producto, cantidad = cant, subtotal = subtotal)
            detalle.save()
            productos.append(detalle)
    datos={
        'productos':productos,
        'fecha':boleta.fechaCompra,
        'total': boleta.total
    }
    request.session['boleta'] = boleta.idBoleta
    carrito = Carrito(request)
    carrito.limpiar()
    return render(request, 'detallecarrito.html',datos)