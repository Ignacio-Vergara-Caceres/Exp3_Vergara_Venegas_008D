function mostrarFeriados(){
    let url='https://api.boostr.cl/holidays.json';
    fetch(url)
    .then(response => response.json())
    .then(data => mostrarData(data))
    .catch(error => console.log(error))

    const mostrarData=(data)=>{
        console.log(data)
        let body=""
        for(var i=0;i<data.data.length;i++){
            body+=`<tr>
                <td>${data.data[i].date}</td>
                <td>${data.data[i].title}</td>
                <td>${data.data[i].type}</td>
                <td>${data.data[i].inalienable}</td>
                <td>${data.data[i].extra}</td>
                </tr>`
        }
        document.getElementById('dias').innerHTML=body
    }
}