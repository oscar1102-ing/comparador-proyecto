document.addEventListener("DOMContentLoaded", () => {
    console.log("🚀 Registro.js cargado");
    
    const form = document.getElementById("registerForm");
    const mensajeDiv = document.getElementById("mensajeRegistro");

    if (form) {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            
            const nombre = document.getElementById("nombre").value.trim();
            const email = document.getElementById("email").value.trim();
            const edad = document.getElementById("edad").value;
            const password = document.getElementById("password").value;
            const confirmPassword = document.getElementById("confirmPassword").value;
            
            // Validar nombre: solo letras y espacios
            const regexNombre = /^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]+$/;
            if (!regexNombre.test(nombre)) {
                mostrarMensaje("❌ El nombre solo puede contener letras", "error");
                return;
            }

            // Validar edad: no negativa y mayor de 0
            if (Number(edad) <= 0 || Number(edad) > 120) {
                mostrarMensaje("❌ Ingresa una edad válida", "error");
                return;
            }

            if (!nombre || !email || !edad || !password) {
                mostrarMensaje("❌ Completa todos los campos", "error");
                return;
            }

            if (password !== confirmPassword) {
                mostrarMensaje("❌ Las contraseñas no coinciden", "error");
                return;
            }

            // 🔥 IMPORTANTE: Llamar DIRECTAMENTE a FastAPI (evitando el proxy)
            const API_URL = "/api/registro";
            
            const datosRegistro = {
                nombre: nombre,
                email: email,
                password: password,
                edad: Number(edad)
            };

            console.log("📤 Enviando a:", API_URL);
            console.log("📦 Datos:", datosRegistro);

            try {
                const response = await fetch(API_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosRegistro)
                });

                const data = await response.json();

                if (!response.ok) {
                    mostrarMensaje("❌ " + (data.detail || data.error || "Error en el servidor"), "error");
                    return;
                }

                // Obtener el ID del usuario desde la respuesta
                const usuarioId = data.usuario_id;
                if (!usuarioId) {
                    mostrarMensaje("❌ Error: no se recibió el ID de usuario", "error");
                    return;
                }

                mostrarMensaje("✅ " + (data.mensaje || "Registro exitoso. Revisa tu correo para el QR."), "success");
                form.reset();

                // Redirigir a la página de verificación de código
                setTimeout(() => {
                    window.location.href = `/verificar-cuenta.html?id=${usuarioId}`;
                }, 2000);

            } catch (error) {
                console.error("❌ Error:", error);
                mostrarMensaje("❌ Error de conexión: " + error.message, "error");
            }
        });
    }

    function mostrarMensaje(mensaje, tipo) {
        mensajeDiv.style.display = "block";
        mensajeDiv.textContent = mensaje;
        mensajeDiv.style.padding = "10px";
        mensajeDiv.style.borderRadius = "5px";
        mensajeDiv.style.marginTop = "15px";
        
        if (tipo === "error") {
            mensajeDiv.style.backgroundColor = "#f8d7da";
            mensajeDiv.style.color = "#721c24";
        } else {
            mensajeDiv.style.backgroundColor = "#d4edda";
            mensajeDiv.style.color = "#155724";
        }
        
        setTimeout(() => {
            if (tipo !== "success") {
                mensajeDiv.style.display = "none";
            }
        }, 5000);
    }
});
