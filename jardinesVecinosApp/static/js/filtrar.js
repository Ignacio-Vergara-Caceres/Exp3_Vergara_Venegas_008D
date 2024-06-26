function mostrarProductos(){
    let url='https://ignacio-vergara-caceres.github.io/ProyWeb_Vergara_Venegas_008D/productos.json';
    //implementar Fetch que permita la información de los productos
    fetch(url)
    .then(response => response.json())
    .then(data => mostrarProductos(data.productos))
    .catch(error => console.log(error))

    const mostrarProductos=(data)=>{
        console.log(data)
        let body=""
        for(var i=0;i<data.length;i++){
            body+=`<tr>
                <td>${data[i].id}</td>
                <td>${data[i].nombre}</td>
                <td>${data[i].tipo}</td>
                <td>${data[i].precio}</td>
                </tr>`
        }
        document.getElementById('productos').innerHTML=body;
    }


}


function buscarTipo(){
    let url='https://ignacio-vergara-caceres.github.io/ProyWeb_Vergara_Venegas_008D/productos.json';
    let tipo=document.getElementById('tipo').value;
    //implementar Fetch que permita la información de los productos
    fetch(url)
    .then(response => response.json())
    .then(data => buscarProductos(data.productos))
    .catch(error => console.log(error))

    const buscarProductos=(data)=>{
        console.log(data)
        let body=""
        if (document.getElementById('tipo').selectedIndex==0){
            mostrarProductos();
        }
        else{

            for(var i=0;i<data.length;i++){
                if (tipo==data[i].tipo)
                {
                    body+=`<tr>
                    <td>${data[i].id}</td>
                    <td>${data[i].nombre}</td>
                    <td>${data[i].tipo}</td>
                    <td>${data[i].precio}</td>
                    </tr>`
    
                }
            }
            document.getElementById('productos').innerHTML=body;
        }
    }

}
