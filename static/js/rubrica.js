//prepare document for add/remove rows
$('#mas-filas').click(()=>{añadirFila()});
$('#menos-filas').click(()=>{quitarFila()});




//funcion para traer los aspectos de la rubrica a la pagina
var idRubrica;
var detalleRubrica;
var sumaRubrica;

function traerRubrica(){

    idRubrica= $(this).attr("id");
    let nombre;
    let descripcion;
    //buscar info rubrica
    for(let i=0; i<rubricasJs.length; i++){
        if(rubricasJs[i][0]==idRubrica){
            nombre=rubricasJs[i][1];
            descripcion=rubricasJs[i][2] ;
        }
    }
    $('#new-nombre').html(nombre);
    $('#new-descripcion').html(descripcion);

    $.ajax({
        data : {'id' : idRubrica},
        url : 'busqueda_rubrica_ajax',
        type : 'get',
        success: (data)=>{jsonToTable(data);
                            window.location.href = '#rubrica-detalle';}
        ,
    });

}
//añadir un fila a la rubrica
function añadirFila(){
    let ultimaFila=detalleRubrica.length;
    let nuevoElemento={'fila': ultimaFila, 'columna': 0,
                       'puntaje':  "0.0", 'nombreFila': 'Aspecto '+ (ultimaFila+1),
                        'descripcion' : 'Nivel 1'};
    let nuevaFila=[nuevoElemento];
    detalleRubrica.push(nuevaFila);
    jsonToTable(detalleRubrica);
}


//quitar una fila de la rubrica
function quitarFila(){
    detalleRubrica.pop();
    jsonToTable(detalleRubrica);
}

//añadir una columna a la fila correspondiente
function añadirColumna(fila){
    columnaAnterior=detalleRubrica[fila].length-1
    elementoAnterior=detalleRubrica[fila][columnaAnterior];
    puntajeAnterior=(parseFloat(elementoAnterior['puntaje'])+1);
    puntajeNuevo=puntajeAnterior.toFixed(1);
    nuevoElemento={'fila': fila, 'columna': (columnaAnterior+1),
                       'puntaje':  puntajeNuevo, 'nombreFila': elementoAnterior['nombreFila'],
                        'descripcion' : 'Nivel '+(columnaAnterior+2)};
    detalleRubrica[fila].push(nuevoElemento);
    jsonToTable(detalleRubrica);
}

//quitar columna a la fila correspondiente
function quitarColumna(fila){
    if(detalleRubrica[fila].length <= 1){
        detalleRubrica.splice(fila,1);
    } else {
    detalleRubrica[fila].pop();
    }
    jsonToTable(detalleRubrica);
}


//traducir el json a tabla
function jsonToTable(data){
    observerPuntaje.disconnect();
    observerDescripcion.disconnect();
    observerNombreFila.disconnect();
    detalleRubrica=data;
    let html = "<tbody>";
    let mayorColumna = 0;
    actualizarPuntaje();
    for(let i=0; i<data.length ; i++){
        for(let j=0; j<data[i].length;j++){
            if(j==0){
                //comparar la maxima columna
                mayorColumna=Math.max(mayorColumna,data[i].length);
                html += '<tr class="w3-display-container"> <th id="info-'+i+'" class="w3-red tabla-elemento-rubrica w3-small ';
                if(is_admin){
                    html+=' w3-hover-opacity  ';    
                }
                html+='" style="height: 60px"';
                if(is_admin){
                    html+='  contenteditable="true" ';
                }
                html+=' >' + data[i][j]['nombreFila']+ '</th>';
            }
            html +='<td id="'+i+'__'+j+'" class="w3-display-container ';
            if(is_admin){
                html += ' w3-hover-gray '
            } 
            html +=  'w3-tiny tabla-elemento-rubrica"  >'+' <div id="'+i+'__'+j+'-descripcion" ';
            if(is_admin){
                html += ' contenteditable="true" '
            }
            html += '>' +data[i][j]['descripcion'] +'</div><div id="'+i+'__'+j+'-puntaje" style="width: 60px" class="w3-display-topleft w3-container w3-green w3-medium"';
            if(is_admin){
                html+= ' contenteditable="true" ';
             }
            html+='>'+data[i][j]['puntaje']+'</div>';
                            

            if(j!=(data[i].length-1)){
                 html+='</td>';

            }else{
                if(is_admin){
                html+='<div id="prueba" style="height:50px; width: 20%;" class="w3-container w3-display-right w3-display-container">'+
                                    '<i id="mas-'+i+'" class="fas fa-plus-circle w3-text-blue-gray zoom w3-medium" style="margin-top:5px"></i>'+
                                    '<i id="menos-'+i+'" class="fas fa-minus-circle w3-text-red zoom w3-medium" style="margin-top:5px"></i>'+
                            '</div>';
                }
                html +='</td></tr>';

            }

        }

    }

    let width=Math.floor(100/(mayorColumna+1));
    html +='</tbody>';
    head = '<thead> <tr> <th class="w3-red tabla-elemento-rubrica" style="width: '+width+'% ; height: 60px"> Niveles </th>' ;
    for(let i=1;i<=mayorColumna;i++){
        head += '<th style="width: '+width+'%" class="w3-red tabla-elemento-rubrica"> Nivel ' + i +'</th>';
    }
    head += '</tr></thead>'
    html = head + html;
    $('#mas-menos-filas').css('width',(width*2)+'%');
    $('#tabla-rubrica').html(html);
    $('#rubrica-detalle').show();
    for(let i=0; i<data.length;i++){
        $('#mas-'+i).click(()=>{añadirColumna(i)});
        $('#menos-'+i).click(()=>{quitarColumna(i)});
        observerNombreFila.observe(document.getElementById('info-'+i),config);
        for(let j=0; j<data[i].length;j++){
            observerDescripcion.observe(document.getElementById(i+'__'+j+'-descripcion'),config);
            observerPuntaje.observe(document.getElementById(i+"__"+j+"-puntaje"),config);
        }
    }

}



//observador para los elementos de la tabla


// Options for the observer (which mutations to observe)
var config = {subtree: true , characterData: true};

// Observadores
//actualizar fila info
var observarNombreFila = function(mutationsList,observer){
    for(let mutation of mutationsList){
        if(mutation.target.parentNode!=null){
            let rawData = mutation.target.data;
            let fila = mutation.target.parentNode.id.split('-')[1];
            for(let i=0;i<detalleRubrica[fila].length;i++){
                detalleRubrica[fila][i]['nombreFila']=stripHtml(rawData);
            }
        }
    }

}

//actualizar descripcion
var observarDescripcion = function(mutationsList,observer){
    for(let mutation of mutationsList){
        if(mutation.target.parentNode!=null){
            let rawData = mutation.target.data;
            let position = mutation.target.parentNode.id.split('__');
            let x = position[0];
            let y = position[1].split('-')[0];
            detalleRubrica[x][y]['descripcion'] = stripHtml(rawData);

        }
}}



var observarPuntaje = function(mutationsList, observer) {
    for(let mutation of mutationsList) {

            if(mutation.target.parentNode!=null){
                let rawData = mutation.target.data;
                let position = mutation.target.parentNode.id.split("__");
                let x = position[0];
                let y = position[1].split("-")[0];
                detalleRubrica[x][y]['puntaje'] = stripHtml(rawData);
                actualizarPuntaje();
            }

    }
};

// Create an observer instance linked to the callback function
var observerPuntaje = new MutationObserver(observarPuntaje);
var observerNombreFila = new MutationObserver(observarNombreFila);
var observerDescripcion = new MutationObserver(observarDescripcion);


// actualizar puntaje
function actualizarPuntaje(){
    sumaRubrica=0;
    let ultimo=0;
    for(let i=0;i<detalleRubrica.length;i++){
        ultimo = (detalleRubrica[i].length - 1);
        sumaRubrica+=parseFloat(detalleRubrica[i][ultimo]['puntaje']);
        }
    $('#puntaje-total').val(sumaRubrica.toFixed(1));
    if(sumaRubrica<6){
        $('#puntaje-total').css('color','#e8a814');
    }
    else{
        if(Math.abs(sumaRubrica-6)< Number.EPSILON){
        $('#puntaje-total').css('color','#2fba2a');
        }   else{
        $('#puntaje-total').css('color','#d62f26');
    }
}
}

//actualizar Rubricas
// Sending in JSON format using POST method
//
function sendAspectosRubrica(){
    if(Math.abs(sumaRubrica-6)>Number.EPSILON){
        alert("La suma de los puntajes asociados a la rúbrica debe ser 6 puntos");
        return;
    }
    var xhr = new XMLHttpRequest();
    var url = 'update_aspectos_rubrica';
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    //se actualizan los valores de la tabla al objeto Rubrica (los puntajes ya estan actualizados)

    let newNombre=$('#new-nombre').text();
    let newDescripcion=$('#new-descripcion').text();
    let data={'idRubrica':idRubrica, 'nombre':newNombre, 'descripcion': newDescripcion};

    data['aspectosRubrica']=detalleRubrica
    xhr.send(JSON.stringify(data));
}