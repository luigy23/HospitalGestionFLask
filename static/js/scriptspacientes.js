document.addEventListener('DOMContentLoaded', function() {
    const formCreatePaciente = document.getElementById('form_create_paciente');
    
    // Cambiar el eventListener para que se adapte a la estructura del formulario
    document.getElementById('addForm').addEventListener('submit', function(e) {
        e.preventDefault();  // Previene el comportamiento por defecto (recargar la página)

        const formData = new FormData(this);  // Obtiene todos los datos del formulario
        const data = {};
        formData.forEach((value, key) => {data[key] = value});  // Convierte FormData en un objeto

        fetch('/pacientes/crear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),  // Convierte los datos a formato JSON
        })
        .then(response => response.json())
        .then(data => {
            alert('Paciente agregado con éxito');
            loadPacientes();  // Recargar la lista de pacientes
        })
        .catch(error => {
            console.error('Error al agregar el paciente:', error);
            alert('Hubo un problema al agregar el paciente');
        });
    });

    // Función para cargar los pacientes en la tabla
    function loadPacientes() {
        fetch('/pacientes/leer')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#tabla_pacientes tbody');
            tableBody.innerHTML = '';  // Limpiar tabla antes de agregar nuevos datos

            if (data.pacientes && data.pacientes.length > 0) {
                data.pacientes.forEach(paciente => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${paciente.nombre}</td>
                        <td>${paciente.apellidos}</td>
                        <td>${paciente.fechaNacimiento}</td>
                        <td>${paciente.direccion}</td>
                        <td>${paciente.telefono}</td>
                        <td>
                            <button class="btn-delete" onclick="deletePaciente(${paciente.idPaciente})">Eliminar</button>
                            <button class="btn-update" onclick="detalle(${paciente.idPaciente})">Actualizar</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="7">No se encontraron pacientes</td>';
                tableBody.appendChild(row);
            }
        })
        .catch(error => {
            console.error('Error al cargar los pacientes:', error);
            alert('Hubo un problema al cargar los pacientes');
        });
    }

    window.filtrarPacientes = function() {
        const filtro = document.getElementById('filtroNombre').value.toLowerCase();
        const filas = document.querySelectorAll('#tabla_pacientes tbody tr');
    
        filas.forEach(fila => {
            const nombre = fila.cells[0].textContent.toLowerCase();
            fila.style.display = nombre.includes(filtro) ? '' : 'none';
        });
    };
    

    // Función para eliminar paciente con confirmación
    window.deletePaciente = function(idPaciente) {
        if (confirm('¿Estás seguro de que deseas eliminar este paciente? Esta acción no se puede deshacer.')) {
            fetch(`/pacientes/eliminar/${idPaciente}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('No se pudo eliminar el paciente');
                }
            })
            .then(data => {
                alert(data.message);
                loadPacientes();  // Recargar la lista de pacientes
            })
            .catch(error => {
                console.error('Error al eliminar el paciente:', error);
                alert('Hubo un problema al eliminar el paciente. Por favor, intenta nuevamente.');
            });
        } else {
            alert('Eliminación cancelada');
        }
    };
    loadPacientes();
    
// Función para abrir el modal con datos del paciente
window.detalle = function(idPaciente) {
    fetch(`/pacientes/leer/${idPaciente}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                // Rellenar los campos del formulario con los datos del paciente
                document.getElementById("idPaciente").value = data.idPaciente;
                document.getElementById("nombre_editar").value = data.nombre;
                document.getElementById("apellidos_editar").value = data.apellidos;
                document.getElementById("fechaNacimiento_editar").value = data.fechaNacimiento;
                document.getElementById("direccion_editar").value = data.direccion;
                document.getElementById("telefono_editar").value = data.telefono;

                // Mostrar el modal
                document.getElementById("modalActualizar").style.display = "flex";
            } else {
                alert("Paciente no encontrado");
            }
        })
        .catch(error => {
            console.error("Error al cargar los datos del paciente:", error);
            alert("Hubo un problema al cargar los datos del paciente");
        });
};

// Función para guardar los cambios
window.guardarEdicion = function() {
    const idPaciente = document.getElementById("idPaciente").value;
    const nombre = document.getElementById("nombre_editar").value;
    const apellidos = document.getElementById("apellidos_editar").value;
    const fechaNacimiento = document.getElementById("fechaNacimiento_editar").value;
    const direccion = document.getElementById("direccion_editar").value;
    const telefono = document.getElementById("telefono_editar").value;

    const data = {
        nombre,
        apellidos,
        fechaNacimiento,
        direccion,
        telefono
    };

    fetch(`/pacientes/actualizar/${idPaciente}`, {
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
            throw new Error("No se pudo actualizar el paciente");
        }
    })
    .then(data => {
        alert(data.message);
        cerrarModal();
        loadPacientes(); // Recargar la lista de pacientes
    })
    .catch(error => {
        console.error("Error al actualizar el paciente:", error);
        alert("Hubo un problema al actualizar el paciente");
    });
};

// Función para cerrar el modal
window.cerrarModal = function() {
    document.getElementById("modalActualizar").style.display = "none";
};
});