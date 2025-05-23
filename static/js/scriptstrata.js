const selectTratamiento = document.getElementById('tratamiento');
const btnAgregarTratamiento = document.getElementById('agregarTratamiento');

document.addEventListener('DOMContentLoaded', function () {
    // Obtener el dropdown de pacientes
    const pacienteDropdown = document.getElementById('paciente');

    // Hacer la solicitud al servidor para obtener los pacientes
    fetch('/tratamientos/enviar/pacientes')
        .then(response => response.json())
        .then(data => {
            const pacientes = data.pacientes;

            // Vaciar el dropdown antes de llenarlo
            pacienteDropdown.innerHTML = '';

            // Añadir una opción predeterminada para el dropdown
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.text = 'Seleccionar paciente';
            pacienteDropdown.appendChild(defaultOption);

            // Llenar el dropdown con los pacientes obtenidos
            pacientes.forEach(paciente => {
                const option = document.createElement('option');
                option.value = paciente.idPaciente;
                option.text = paciente.nombre;
                pacienteDropdown.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error al obtener los pacientes:', error);
        });
    // Función para obtener los tratamientos del paciente seleccionado
    function loadTratamientos() {
        fetch('/tratamientos/leer')
            .then(response => response.json())
            .then(data => {
                const tablaTratamientosBody = document.getElementById('tabla-tratamientos-body');
                tablaTratamientosBody.innerHTML = '';

                data.tratamientos.forEach(tratamiento => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                    <td hidden>${tratamiento.codigoTratamiento}</td>
                    <td>${tratamiento.nombre}</td>
                    <td>${tratamiento.descripcion}</td>
                    <td>${tratamiento.duracion}</td>
                    <td>${tratamiento.paciente}</td>
                    <td>
                        <button class="btn-update" data-id="${tratamiento.codigoTratamiento}">Editar</button>
                        <button class="btn-delete" data-id="${tratamiento.codigoTratamiento}">Borrar</button>
                    </td>
                `;
                    tablaTratamientosBody.appendChild(row);
                });

                // Event listeners para el botón de borrar
                document.querySelectorAll('.btn-delete').forEach(button => {
                    button.addEventListener('click', borrarTratamiento);
                });

                // Event listeners para el botón de editar
                document.querySelectorAll('.btn-update').forEach(button => {
                    button.addEventListener('click', function () {
                        const codigoTratamiento = this.getAttribute('data-id');
                        editarTratamiento(codigoTratamiento); // Abre el modal de edición
                    });
                });
            })
            .catch(error => {
                console.error('Error al cargar las tratamientos:', error);
            });
    }

    window.filtrarPacientes = function() {
        const filtro = document.getElementById('filtroNombre').value.toLowerCase();
        const filas = document.querySelectorAll('#tabla-tratamientos tbody tr');
    
        filas.forEach(fila => {
            const nombre = fila.cells[4].textContent.toLowerCase();
            fila.style.display = nombre.includes(filtro) ? '' : 'none';
        });
    };

    //funcion para crear el tratamiento
    document.getElementById('form_create_tratamiento').addEventListener('submit', function(e) {
        e.preventDefault();  // Evita la recarga de la página
        const formData = new FormData(this);
        const data = {};
        formData.forEach((value, key) => { data[key] = value });  // Convierte FormData a un objeto
        fetch('/tratamientos/crear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),  // Convierte los datos a JSON
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 201) {
                alert('Tratamiento creado con éxito');
                loadTratamientos();  // Recargar la lista de tratamientos
                this.reset(); // Limpiar el formulario después de guardar
            } else {
                alert('Hubo un problema al crear la tratamiento: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error al crear la tratamiento:', error);
            alert('Hubo un error al crear la tratamiento.');
        });
    });

    // Función para eliminar el tratamiento
    function borrarTratamiento(event) {
        const idTratamiento = event.target.getAttribute('data-id');
        if (confirm('¿Estás seguro de que deseas eliminar este tratamiento?')) {
            fetch(`/tratamientos/eliminar/${idTratamiento}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 200) {
                    alert('Tratamiento eliminado con éxito');
                    loadTratamientos(); // Recargar la lista de tratamientos después de eliminar
                } else {
                    alert('Hubo un problema al eliminar el tratamiento: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error al eliminar el tratamiento:', error);
                alert('Hubo un error al eliminar el tratamiento.');
            });
        }
    }

    // Abrir el modal y cargar los datos del tratamiento
    window.editarTratamiento = function (idTratamiento) {
        fetch(`/tratamientos/leer/${idTratamiento}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data) {
                    // Rellenar los campos del formulario con los datos del tratamiento
                    document.getElementById("id_tratamiento_editar").value = data.codigoTratamiento;
                    document.getElementById("nombre_editar").value = data.nombre;
                    document.getElementById("descripcion_editar").value = data.descripcion;
                    document.getElementById("duracion_editar").value = data.duracion;

                    // Mostrar el modal
                    document.getElementById("modalEditarTratamiento").style.display = "block";
                } else {
                    alert("tratamiento no encontrado");
                }
            })
            .catch(error => {
                console.error("Error al cargar los datos de la tratamiento:", error);
                alert("Hubo un problema al cargar los datos de la tratamiento");
            });
    };

    window.guardarEdicionTratamiento = function () {
        const idTratamiento = document.getElementById("id_tratamiento_editar").value;
        const nombre = document.getElementById("nombre_editar").value;
        const descripcion = document.getElementById("descripcion_editar").value;
        const duracion = document.getElementById("duracion_editar").value;

        // Asegúrate de que los valores no estén vacíos
        if (!nombre || !descripcion || !duracion) {
            alert("Todos los campos son obligatorios");
            return;
        }

        const data = {
            nombre,
            descripcion,
            duracion
        };

        fetch(`/tratamientos/actualizar/${idTratamiento}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("No se pudo actualizar la tratamiento");
                }
            })
            .then(data => {
                alert(data.message);
                cerrarModal();
                loadTratamientos(); // Recargar la lista de tratamientos
            })
            .catch(error => {
                console.error("Error al actualizar la tratamiento:", error);
                alert("Hubo un problema al actualizar la tratamiento");
            });
    };

    // Función para cerrar el modal
    window.cerrarModal = function () {
        document.getElementById("modalEditarTratamiento").style.display = "none";
    };


    loadTratamientos();
});


