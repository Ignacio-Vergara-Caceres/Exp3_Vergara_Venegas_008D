/* Funciones Registro */

jQuery(function(){ 
    jQuery("#datosRegistro").validate({ 
        rules:{
            nombre:{
                required: true
            },
            correo:{
                required: true,
                email:true
            },
            telefono:{
                required:true,
                number:true
            },
            contra:{
                required:true
            },
            confirm:{
                required:true,
                equalTo:"#contra"
            },
        }        
    })

    jQuery("#botonRegistrar").on("click", function(event) {
        event.preventDefault();

        if (jQuery("#datosRegistro").valid()) {
            alert("Usuario creado con éxito");
            window.location.href = inicioUrl;
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var botonCancelar = document.getElementById("Cancelar");
    botonCancelar.addEventListener("click", function(event) {
        event.preventDefault();
        window.location.href = inicioUrl;
    });
});

function Develarcontraseña() {
    let contraseñaing = document.getElementById('contra');
    if (contraseñaing.type == 'password') {
        contraseñaing.type = 'text';
    } else {
        contraseñaing.type = 'password';
    }
}

function Develarcontraseña2() {
    let contraseñaing = document.getElementById('confirm');
    if (contraseñaing.type == 'password') {
        contraseñaing.type = 'text';
    } else {
        contraseñaing.type = 'password';
    }
}
