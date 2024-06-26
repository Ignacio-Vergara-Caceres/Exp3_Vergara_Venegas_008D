function develarContraseña() {
    let contraseñaing = document.getElementById("id_password");
    if (contraseñaing.type === 'password') {
        contraseñaing.type = 'text';
    } else {
        contraseñaing.type = 'password';
    }
}

function cambiarCaptcha() {
    let imagenCaptcha = document.getElementById('imagencaptcha');
    let cambioIMG = Math.floor(Math.random() * 3) + 1;
    imagenCaptcha.src = staticUrl + "imagenesCaptcha/captcha" + cambioIMG + ".png"; //Acá se utiliza la variable global staticUrl
} 

function obtenerNombreDeImagen(urlImagen) {
    let partesURL = urlImagen.split("/");     // Separa la URL en "/"
    let nombreArchivo = partesURL[partesURL.length - 1];    // Obtiene la última parte de la URL 
    return nombreArchivo;
}



function validarCaptcha() {
    let textoCaptcha = document.getElementById('captcha').value;
    let imagenCap = obtenerNombreDeImagen(document.getElementById('imagencaptcha').src)
    if (imagenCap === 'captcha1.png' && textoCaptcha === '263s2v') {
        return true;
    } else if (imagenCap === 'captcha2.png' && textoCaptcha === 'aaxue') {
        return true;
    } else if (imagenCap === 'captcha3.png' && textoCaptcha === 'mwxe2') {
        return true;
    } else {
        return false;
    }
}

function limpiarFormulario() {
    //Limpiar usuario
    var usuario = document.getElementById("id_username");
    if (usuario) {
        usuario.value = "";
    }

    // Limpiar contraseña
    var contra = document.getElementById("id_password");
    if (contra) {
        contra.value = "";
    }

    // Limpiar el campo de captcha
    var captcha = document.getElementById("captcha");
    if (captcha) {
        captcha.value = "";
    }
}

function validarEntrada() {
        // Verificar y logear si es exitoso
        if (!validarCaptcha()) {
            alert('Por favor, inténtelo de nuevo.');
            limpiarFormulario();
            cambiarCaptcha();
            return; // Detener el envío del formulario si el captcha no es válido
        }
        else{
            // Si el captcha es válido, enviar el formulario
            var form = document.getElementById("loginForm");
            form.submit();
        }
};
