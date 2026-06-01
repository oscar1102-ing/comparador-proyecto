document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const mensajeDiv = document.getElementById("mensajeLogin");
 
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
 
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
 
        try {
            const res = await fetch("/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });
 
            const data = await res.json();
 
            if (!res.ok) {
                mostrarMensaje("❌ " + (data.detail || data.error || "Error al iniciar sesión"), "error");
                return;
            }
 
            // Login exitoso — guardar token y redirigir directo
            localStorage.setItem("token", data.token);
            localStorage.setItem("usuario", JSON.stringify(data.usuario));
 
            mostrarMensaje("✅ ¡Bienvenido! Entrando...", "success");
            setTimeout(() => window.location.href = "/index.html", 1200);
 
        } catch (err) {
            mostrarMensaje("❌ Error de conexión: " + err.message, "error");
        }
    });
 
    function mostrarMensaje(msg, tipo) {
        mensajeDiv.style.display = "block";
        mensajeDiv.textContent = msg;
        mensajeDiv.style.padding = "10px";
        mensajeDiv.style.borderRadius = "5px";
        mensajeDiv.style.marginTop = "15px";
        mensajeDiv.style.backgroundColor = tipo === "error" ? "#f8d7da" : "#d4edda";
        mensajeDiv.style.color = tipo === "error" ? "#721c24" : "#155724";
    }
});
