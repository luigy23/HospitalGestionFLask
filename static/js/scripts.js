document.addEventListener('DOMContentLoaded', function () {
    // Cargar pacientes en el dropdown
    const pacienteDropdown = document.getElementById('paciente-dropdown');
    const pacienteEditarDropdown = document.getElementById('paciente_editar');
    if (!pacienteDropdown || !pacienteEditarDropdown) {
        console.error("Dropdown de pacientes no encontrado en el HTML.");
        return;
    }

    console.log("Dropdown de pacientes encontrado, cargando datos...");
    fetch('/citas/enviar/pacientes')
        .then(response => response.json())
        .then(data => {
            // Verifica si 'pacientes' es un array
            if (Array.isArray(data.pacientes)) {
                pacienteDropdown.innerHTML = '<option value="">Seleccione un paciente</option>';
                pacienteEditarDropdown.innerHTML = '<option value="">Seleccione un paciente</option>';
                data.pacientes.forEach(paciente => {
                    const option = document.createElement('option');
                    option.value = paciente.idPaciente;
                    option.textContent = paciente.nombre;
                    pacienteDropdown.appendChild(option);

                    // Opciones para el modal de edición
                    const optionEditar = document.createElement('option');
                    optionEditar.value = paciente.idPaciente;
                    optionEditar.textContent = paciente.nombre;
                    pacienteEditarDropdown.appendChild(optionEditar);
                });
                console.log("Pacientes añadidos a los dropdowns.");
            } else {
                console.error("La propiedad 'pacientes' no es un array");
            }
        })
        .catch(error => {
            console.error("Error al cargar los pacientes:", error);
        });

    // Cargar doctores en el dropdown
    const doctorDropdown = document.getElementById('doctor-dropdown');
    const doctorEditarDropdown = document.getElementById('doctor_editar');
    if (!doctorDropdown || !doctorEditarDropdown) {
        console.error("Dropdown de doctores no encontrado en el HTML.");
        return;
    }

    console.log("Dropdown de doctores encontrado, cargando datos...");
    fetch('/citas/enviar/doctores')
        .then(response => response.json())
        .then(data => {
            // Verifica si 'doctores' es un array
            if (Array.isArray(data.doctores)) {
                doctorDropdown.innerHTML = '<option value="">Seleccione un doctor</option>';
                doctorEditarDropdown.innerHTML = '<option value="">Seleccione un doctor</option>';
                data.doctores.forEach(doctor => {
                    const option = document.createElement('option');
                    option.value = doctor.idDoctor;
                    option.textContent = doctor.nombre;
                    doctorDropdown.appendChild(option);

                    // Opciones para el modal de edición
                    const optionEditar = document.createElement('option');
                    optionEditar.value = doctor.idDoctor;
                    optionEditar.textContent = doctor.nombre;
                    doctorEditarDropdown.appendChild(optionEditar);
                });
                console.log("Doctores añadidos a los dropdowns.");
            } else {
                console.error("La propiedad 'doctores' no es un array");
            }
        })
        .catch(error => {
            console.error("Error al cargar los doctores:", error);
        });

    // Función para crear la cita
    document.getElementById('form_create_cita').addEventListener('submit', function (e) {
        e.preventDefault();  // Evita la recarga de la página
        const formData = new FormData(this);
        const data = {};
        formData.forEach((value, key) => { data[key] = value });  // Convierte FormData a un objeto

        fetch('/citas/crear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),  // Convierte los datos a JSON
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);  // Mostrar el mensaje de error si existe
                } else {
                    alert('Cita creada con éxito');
                    loadCitas();  // Recargar la lista de citas
                    this.reset(); // Limpiar el formulario después de guardar
                }
            })
            .catch(error => {
                console.error('Error al crear la cita:', error);
                alert('Hubo un error al crear la cita.');
            });
    });

    // Función para eliminar la cita
    function borrarCita(event) {
        const idCita = event.target.getAttribute('data-id');
        if (confirm('¿Estás seguro de que deseas eliminar esta cita?')) {
            fetch(`/citas/eliminar/${idCita}`, {
                method: 'DELETE',
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message === 'Cita eliminada con éxito') {
                        alert('Cita eliminada con éxito');
                        loadCitas(); // Recargar la lista de citas después de eliminar
                    } else {
                        alert('Hubo un problema al eliminar la cita: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error al eliminar la cita:', error);
                    alert('Hubo un error al eliminar la cita.');
                });
        }
    }

    // Función para cargar las citas
    function loadCitas() {
        fetch('/citas/leer')
            .then(response => response.json())
            .then(data => {
                const tablaCitasBody = document.getElementById('tabla-citas-body');
                tablaCitasBody.innerHTML = '';

                data.citas.forEach(cita => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td hidden>${cita.idCita}</td>
                        <td>${cita.fecha}</td>
                        <td>${cita.hora}</td>
                        <td>${cita.proposito}</td>
                        <td>${cita.estado}</td>
                        <td>${cita.paciente}</td>
                        <td>${cita.doctor}</td>
                        <td>
                            <button class="btn-update" data-id="${cita.idCita}">Editar</button>
                            <button class="btn-delete" data-id="${cita.idCita}">Borrar</button>
                        </td>
                    `;
                    tablaCitasBody.appendChild(row);
                });

                // Event listeners para el botón de borrar
                document.querySelectorAll('.btn-delete').forEach(button => {
                    button.addEventListener('click', borrarCita);
                });

                // Event listeners para el botón de editar
                document.querySelectorAll('.btn-update').forEach(button => {
                    button.addEventListener('click', function () {
                        const idCita = this.getAttribute('data-id');
                        editarCita(idCita); // Abre el modal de edición
                    });
                });
            })
            .catch(error => {
                console.error('Error al cargar las citas:', error);
            });
    }

    // Abrir el modal y cargar los datos de la cita
    window.editarCita = function (idCita) {
        fetch(`/citas/leer/${idCita}`)
            .then(response => response.json())
            .then(data => {
                if (data) {
                    // Rellenar los campos del formulario con los datos de la cita
                    document.getElementById("id_cita_editar").value = data.idCita;
                    document.getElementById("fecha_editar").value = data.fecha;
                    document.getElementById("hora_editar").value = data.hora.substring(0, 5);
                    document.getElementById("proposito_editar").value = data.proposito;
                    document.getElementById("estado_editar").value = data.estado;
                    document.getElementById("paciente_editar").value = data.idPaciente;
                    document.getElementById("doctor_editar").value = data.idDoctor;

                    // Mostrar el modal
                    document.getElementById("modalEditarCita").style.display = "block";
                } else {
                    alert("Cita no encontrada");
                }
            })
            .catch(error => {
                console.error("Error al cargar los datos de la cita:", error);
                alert("Hubo un problema al cargar los datos de la cita");
            });
    };

    window.guardarEdicionCita = function () {
        const idCita = document.getElementById("id_cita_editar").value;
        const fecha = document.getElementById("fecha_editar").value;
        const hora = document.getElementById("hora_editar").value;
        const proposito = document.getElementById("proposito_editar").value;
        const estado = document.getElementById("estado_editar").value;
        const paciente = document.getElementById("paciente_editar").value;
        const doctor = document.getElementById("doctor_editar").value;

        // Asegúrate de que los valores no estén vacíos
        if (!fecha || !hora || !proposito || !estado || !paciente || !doctor) {
            alert("Todos los campos son obligatorios");
            return;
        }

        const data = {
            fecha,
            hora,
            proposito,
            estado,
            paciente: parseInt(paciente),
            doctor: parseInt(doctor)
        };

        fetch(`/citas/actualizar/${idCita}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    alert(data.message);
                    cerrarModal();
                    loadCitas();
                }
            })
            .catch(error => {
                console.error("Error al actualizar la cita:", error);
                alert("Hubo un problema al actualizar la cita");
            });
    };

    // Función para cerrar el modal
    window.cerrarModal = function () {
        document.getElementById("modalEditarCita").style.display = "none";
    };


    loadCitas(); // Inicialmente cargar las citas
});