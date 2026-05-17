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
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(datosRegistro)
                });

                console.log("📡 Status:", response.status);
                const data = await response.json();
                console.log("📥 Respuesta:", data);

                if (!response.ok) {
                    mostrarMensaje("❌ " + (data.detail || "Error en el servidor"), "error");
                    return;
                }

                mostrarMensaje("✅ ¡Registro exitoso! Redirigiendo...", "success");
                form.reset();
                
                let segundos = 3;

mostrarMensaje(`✅ Registro exitoso. Redirigiendo en ${segundos}...`, "success");

const intervalo = setInterval(() => {
    segundos--;

    if (segundos > 0) {
        mostrarMensaje(`✅ Registro exitoso. Redirigiendo en ${segundos}...`, "success");
    } else {
        clearInterval(intervalo);
        window.location.href = "/login.html";
    }
}, 1000);

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
