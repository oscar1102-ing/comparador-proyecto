document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const usuarioId = params.get("id");
    
    // ============================================
    // TEMPORIZADOR DE 2 MINUTOS (120 segundos)
    // ============================================
    const TOTAL_SEGUNDOS = 120;
    let segundosRestantes = TOTAL_SEGUNDOS;

    if (!usuarioId) {
        mostrarMensaje("❌ Enlace inválido. Regístrate nuevamente.", "error");
        setTimeout(() => window.location.href = "/registrar.html", 3000);
        return;
    }

    const btn = document.getElementById("btnVerificar");
    const inputCodigo = document.getElementById("codigoTotp");
    const mensajeDiv = document.getElementById("mensaje");

    // Crear elementos visuales del temporizador (barra y texto)
    const timerContainer = document.createElement("div");
    timerContainer.innerHTML = `
        <div class="timer-bar-wrapper" style="width:100%; background:#eee; border-radius:8px; margin:15px 0 5px 0; height:10px;">
            <div class="timer-bar" id="timerBar" style="height:10px; background:#ff7a00; border-radius:8px; width:100%; transition:width 1s linear;"></div>
        </div>
        <div class="timer-texto" style="text-align:center; font-size:14px; margin-bottom:15px;">
            Tienes <span id="timerTexto">2:00</span> para completar la activación
        </div>
    `;
    // Insertar antes del campo de código
    document.querySelector(".auth-card").insertBefore(timerContainer, inputCodigo);

    const timerBar = document.getElementById("timerBar");
    const timerTexto = document.getElementById("timerTexto");

    const intervaloTimer = setInterval(() => {
        segundosRestantes--;
        const porcentaje = (segundosRestantes / TOTAL_SEGUNDOS) * 100;
        timerBar.style.width = porcentaje + "%";
        
        if (segundosRestantes <= 60) {
            timerBar.style.background = "#dc3545";
            timerTexto.style.color = "#dc3545";
        }
        
        const minutos = Math.floor(segundosRestantes / 60);
        const segundos = segundosRestantes % 60;
        timerTexto.textContent = `${minutos}:${segundos.toString().padStart(2, "0")}`;
        
        if (segundosRestantes <= 0) {
            clearInterval(intervaloTimer);
            btn.disabled = true;
            inputCodigo.disabled = true;
            mostrarMensaje("⏰ El tiempo expiró. Tu cuenta fue eliminada. Regístrate de nuevo.", "error");
            setTimeout(() => window.location.href = "/registrar.html", 2000);
        }
    }, 1000);

    // ============================================
    // VERIFICAR CÓDIGO TOTP
    // ============================================
    btn.addEventListener("click", async () => {
        const codigo = inputCodigo.value.trim();
        if (!/^\d{6}$/.test(codigo)) {
            mostrarMensaje("❌ Ingresa exactamente 6 dígitos numéricos.", "error");
            return;
        }

        try {
            const response = await fetch("/api/verificar-mfa", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    usuario_id: parseInt(usuarioId),
                    codigo: codigo
                })
            });

            const data = await response.json();

            if (!response.ok) {
                mostrarMensaje("❌ " + (data.detail || data.error || "Código incorrecto o expirado"), "error");
                return;
            }

            // Éxito: la cuenta ha sido activada
            clearInterval(intervaloTimer);  // Detener el temporizador
            mostrarMensaje("✅ ¡Cuenta activada correctamente! Ahora inicia sesión.", "success");
            
            // Redirigir al login después de 2 segundos (sin guardar token ni auto-login)
            setTimeout(() => {
                window.location.href = "/login.html";
            }, 2000);

        } catch (err) {
            mostrarMensaje("❌ Error de conexión: " + err.message, "error");
        }
    });

    // Permitir presionar Enter en el input
    inputCodigo.addEventListener("keypress", (e) => {
        if (e.key === "Enter") btn.click();
    });

    // ============================================
    // FUNCIÓN AUXILIAR PARA MOSTRAR MENSAJES
    // ============================================
    function mostrarMensaje(msg, tipo) {
        mensajeDiv.style.display = "block";
        mensajeDiv.textContent = msg;
        mensajeDiv.style.padding = "10px";
        mensajeDiv.style.borderRadius = "5px";
        mensajeDiv.style.backgroundColor = tipo === "error" ? "#f8d7da" : "#d4edda";
        mensajeDiv.style.color = tipo === "error" ? "#721c24" : "#155724";
    }
});
