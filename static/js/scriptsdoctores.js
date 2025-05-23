document.addEventListener('DOMContentLoaded', function() {
    // Asignar el formulario de creación de doctores
    const formCreateDoctor = document.getElementById('form_create_doctor');

    // EventListener para la creación de doctores
    document.getElementById('addDoctorForm').addEventListener('submit', function(e) {
        e.preventDefault(); // Previene el comportamiento por defecto

        const formData = new FormData(this);
        const data = {};
        formData.forEach((value, key) => { data[key] = value }); // Convertir FormData a objeto

        fetch('/doctores/crear', { // Endpoint para creación de doctores
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data), // Convertir a JSON
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);  // Mostrar el mensaje de error si existe
            } else {
                alert('Doctor agregado con éxito');
                loadDoctores(); // Recargar la lista de doctores
                this.reset(); // Limpiar el formulario después de guardar
            }
        })
        .catch(error => {
            console.error('Error al agregar el doctor:', error);
            alert('Hubo un problema al agregar el doctor');
        });
    });

    // Función para cargar los doctores en la tabla
    function loadDoctores() {
        fetch('/doctores/leer')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#tabla_doctores tbody');
            tableBody.innerHTML = ''; // Limpiar la tabla

            if (data.doctores && data.doctores.length > 0) {
                data.doctores.forEach(doctor => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${doctor.nombre}</td>
                        <td>${doctor.apellidos}</td>
                        <td>${doctor.licencia}</td>
                        <td>${doctor.especialidad || 'N/A'}</td>
                        <td>${doctor.telefono || 'N/A'}</td>
                        <td>
                            <button class="btn-delete" onclick="deleteDoctor(${doctor.idDoctor})">Eliminar</button>
                            <button class="btn-update" onclick="detalle(${doctor.idDoctor})">Actualizar</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="7">No se encontraron doctores</td>';
                tableBody.appendChild(row);
            }
        })
        .catch(error => {
            console.error('Error al cargar los doctores:', error);
            alert('Hubo un problema al cargar los doctores');
        });
    }

    window.filtrarDoctores = function() {
        const filtro = document.getElementById('filtroNombre').value.toLowerCase();
        const filas = document.querySelectorAll('#tabla_doctores tbody tr');
    
        filas.forEach(fila => {
            const nombre = fila.cells[0].textContent.toLowerCase();
            fila.style.display = nombre.includes(filtro) ? '' : 'none';
        });
    };

    // Función para eliminar doctor con confirmación
    window.deleteDoctor = function(idDoctor) {
        if (confirm('¿Estás seguro de que deseas eliminar este doctor? Esta acción no se puede deshacer.')) {
            fetch(`/doctores/eliminar/${idDoctor}`, { method: 'DELETE' })
            .then(response => response.ok ? response.json() : Promise.reject('No se pudo eliminar el doctor'))
            .then(data => {
                alert(data.message);
                loadDoctores(); // Recargar la lista de doctores
            })
            .catch(error => {
                console.error('Error al eliminar el doctor:', error);
                alert('Hubo un problema al eliminar el doctor');
            });
        } else {
            alert('Eliminación cancelada');
        }
    };

    // Función para abrir el modal con datos del doctor
    window.detalle = function(idDoctor) {
        fetch(`/doctores/leer/${idDoctor}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                // Rellenar los campos del formulario con los datos del doctor
                document.getElementById("idDoctor").value = data.idDoctor;
                document.getElementById("nombre_editar").value = data.nombre;
                document.getElementById("apellidos_editar").value = data.apellidos;
                document.getElementById("licencia_editar").value = data.licencia;
                document.getElementById("especialidad_editar").value = data.especialidad || '';
                document.getElementById("telefono_editar").value = data.telefono || '';

                // Mostrar el modal
                document.getElementById("modalActualizar").style.display = "flex";
            } else {
                alert("Doctor no encontrado");
            }
        })
        .catch(error => {
            console.error("Error al cargar los datos del doctor:", error);
            alert("Hubo un problema al cargar los datos del doctor");
        });
    };

    // Función para guardar los cambios
    window.guardarEdicion = function() {
        const idDoctor = document.getElementById("idDoctor").value;
        const nombre = document.getElementById("nombre_editar").value;
        const apellidos = document.getElementById("apellidos_editar").value;
        const licencia = document.getElementById("licencia_editar").value;
        const especialidad = document.getElementById("especialidad_editar").value;
        const telefono = document.getElementById("telefono_editar").value;

        const data = {
            nombre,
            apellidos,
            licencia,
            especialidad,
            telefono
        };

        fetch(`/doctores/actualizar/${idDoctor}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.ok ? response.json() : Promise.reject("No se pudo actualizar el doctor"))
        .then(data => {
            alert(data.message);
            cerrarModal();
            loadDoctores(); // Recargar la lista de doctores
        })
        .catch(error => {
            console.error("Error al actualizar el doctor:", error);
            alert("Hubo un problema al actualizar el doctor");
        });
    };

    // Función para cerrar el modal
    window.cerrarModal = function() {
        document.getElementById("modalActualizar").style.display = "none";
    };

    loadDoctores(); // Cargar la lista de doctores al iniciar
});