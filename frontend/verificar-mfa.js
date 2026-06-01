document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const usuarioId = params.get("id");
    const email = params.get("email");
    if (!usuarioId) {
        window.location.href = "/login.html";
        return;
    }
    document.getElementById("mensaje-info").textContent = `Enviamos un código a ${email}`;
    const form = document.getElementById("mfaForm");
    const mensajeDiv = document.getElementById("mensajeMFA");
    const btnReenviar = document.getElementById("btnReenviar");
    const contadorSpan = document.getElementById("contador");
    let segundosRestantes = 60;

    function iniciarContador() {
        segundosRestantes = 60;
        contadorSpan.textContent = segundosRestantes;
        btnReenviar.disabled = true;
        btnReenviar.style.color = "#888";
        btnReenviar.style.cursor = "not-allowed";
        btnReenviar.textContent = `Reenviar código (${segundosRestantes}s)`;

        const intervalo = setInterval(() => {
            segundosRestantes--;
            btnReenviar.textContent = `Reenviar código (${segundosRestantes}s)`;
            if (segundosRestantes <= 0) {
                clearInterval(intervalo);
                btnReenviar.disabled = false;
                btnReenviar.style.color = "#ff7a00";
                btnReenviar.style.cursor = "pointer";
                btnReenviar.textContent = "Reenviar código";
            }
        }, 1000);
    }

    iniciarContador();

    btnReenviar.addEventListener("click", async () => {
        try {
            await fetch("/api/reenviar-codigo", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ usuario_id: parseInt(usuarioId) })
            });
            mostrarMensaje("✅ Código reenviado, revisa tu correo", "success");
        } catch (err) {
            mostrarMensaje("❌ Error al reenviar", "error");
        }
        iniciarContador();
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const codigo = document.getElementById("codigo").value.trim();
        try {
            const res = await fetch("/api/verificar-mfa", {
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
