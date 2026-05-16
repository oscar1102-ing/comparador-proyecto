document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const usuarioId = params.get("id");
    const email = params.get("email");

    if (!usuarioId) {
        window.location.href = "/login.html";
        return;
    }

    document.getElementById("mensaje-info").textContent = 
        `Enviamos un código a ${email}`;

    const form = document.getElementById("mfaForm");
    const mensajeDiv = document.getElementById("mensajeMFA");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const codigo = document.getElementById("codigo").value.trim();

        try {
            const res = await fetch("http://127.0.0.1:8000/verificar-mfa", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ usuario_id: parseInt(usuarioId), codigo })
            });

            const data = await res.json();

            if (!res.ok) {
                mostrarMensaje("❌ " + (data.detail || "Código incorrecto"), "error");
                return;
            }

            localStorage.setItem("token", data.token);
            localStorage.setItem("usuario", JSON.stringify(data.usuario));
            mostrarMensaje("✅ Verificado. Entrando...", "success");
            setTimeout(() => window.location.href = "/index.html", 1500);

        } catch (err) {
            mostrarMensaje("❌ Error: " + err.message, "error");
        }
    });

    function mostrarMensaje(msg, tipo) {
        mensajeDiv.textContent = msg;
        mensajeDiv.style.padding = "10px";
        mensajeDiv.style.borderRadius = "5px";
        mensajeDiv.style.marginTop = "15px";
        mensajeDiv.style.backgroundColor = tipo === "error" ? "#f8d7da" : "#d4edda";
        mensajeDiv.style.color = tipo === "error" ? "#721c24" : "#155724";
    }
});
