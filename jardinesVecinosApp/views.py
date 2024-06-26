from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Categoria, Producto, Boleta, detalle_boleta
from .forms import ProductoForm, RegistroUserForm, ActualizarPerfilForm
from django.contrib.auth.models import User
from jardinesVecinosApp.compras import Carrito
from django.contrib import messages


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
    producto = get_object_or_404(Producto, idProducto=id)
    original_id = producto.idProducto

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():
            nuevo_producto = formulario.save(commit=False)
            nuevo_id = formulario.cleaned_data['idProducto']  # Obtener el nuevo ID desde formulario

            if nuevo_id != original_id:
                # Guardar el nuevo producto con el nuevo ID
                nuevo_producto.idProducto = nuevo_id
                nuevo_producto.save()

                # Eliminar el producto original después de guardar el nuevo producto
                Producto.objects.filter(idProducto=original_id).delete()
            else:
                # Si no hay cambio en la llave primaria, simplemente se guarda
                nuevo_producto.save()

            return redirect('productos')

    datos = {
        'forModificar': ProductoForm(instance=producto),
        'producto': producto
    }

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
    try:
        precio_total = 0
        carrito = request.session.get('carrito', {})
        productos = []

        # Verificar si el carrito está vacío
        if not carrito:
            raise ValueError("No se ha agregado nada al carrito")

        # Validar el stock de todos los productos antes de procesar la boleta
        for key, value in carrito.items():
            producto = get_object_or_404(Producto, idProducto=value['producto_id'])
            cant = value['cantidad']

            if cant > producto.stock:
                raise ValueError(f"No hay suficiente stock para {producto.nombre}. Cantidad disponible: {producto.stock}")

            subtotal = cant * int(value['precio'])
            precio_total += subtotal

            # Crear el detalle de la boleta
            detalle = detalle_boleta(idBoleta=None, id_producto=producto, cantidad=cant, subtotal=subtotal)
            productos.append(detalle)

        # Guardar la boleta
        boleta = Boleta(total=precio_total)
        boleta.save()

        # Guardar los detalles de la boleta
        for detalle in productos:
            detalle.idBoleta = boleta
            detalle.save()

            # Actualizar el stock del producto
            producto = detalle.id_producto
            producto.stock -= detalle.cantidad
            producto.save()

        # Limpiar el carrito después de completar la boleta
        request.session['boleta'] = boleta.idBoleta
        carrito.clear()

        datos = {
            'productos': productos,
            'fecha': boleta.fechaCompra,
            'total': boleta.total
        }

        return render(request, 'detallecarrito.html', datos)

    except ValueError as e:
        # Manejar el error de stock insuficiente con mensaje flash
        error_message = str(e)
        messages.error(request, error_message)
        return redirect('tienda')  # Redirigir a la página principal de la tienda