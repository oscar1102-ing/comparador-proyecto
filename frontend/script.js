document.addEventListener("DOMContentLoaded", () => {
    verificarSesionActiva();
    cargarProductos();
    cargarTop();
    cargarDetalle();
    actualizarHeader();

    
    

    // Carrusel
    document.querySelectorAll(".comparacion").forEach(carrusel => {
        const items = carrusel.querySelectorAll(".tienda");
        if (items.length === 0) return;
        let index = 0;
        let intervalo;
        const visible = 3;
        function moverCarrusel() {
            const itemWidth = items[0].getBoundingClientRect().width;
            index++;
            if (index > items.length - visible) index = 0;
            carrusel.scrollTo({ left: index * itemWidth, behavior: "smooth" });
        }
        function iniciarCarrusel() { intervalo = setInterval(moverCarrusel, 3000); }
        function detenerCarrusel() { clearInterval(intervalo); }
        iniciarCarrusel();
        carrusel.addEventListener("mouseenter", detenerCarrusel);
        carrusel.addEventListener("mouseleave", iniciarCarrusel);
    });

    // Panel filtros
    const btnFiltros = document.querySelector(".btn-filtros");
    const panelFiltros = document.getElementById("panelFiltros");
    const cerrarFiltrosBtn = document.getElementById("cerrarFiltros");
    const overlay = document.getElementById("overlay");
    if (btnFiltros) {
        btnFiltros.addEventListener("click", () => {
            panelFiltros.classList.add("activo");
            overlay.classList.add("activo");
        });
        cerrarFiltrosBtn.addEventListener("click", cerrarPanel);
        overlay.addEventListener("click", cerrarPanel);
        function cerrarPanel() {
            panelFiltros.classList.remove("activo");
            overlay.classList.remove("activo");
        }
    }

    // Toggle filtros
    document.querySelectorAll(".toggle-filtro").forEach(toggle => {
        toggle.addEventListener("click", () => {
            const contenido = toggle.nextElementSibling;
            if (contenido.style.display === "block") {
                contenido.style.display = "none";
                toggle.innerHTML = toggle.innerHTML.replace("-", "+");
            } else {
                contenido.style.display = "block";
                toggle.innerHTML = toggle.innerHTML.replace("+", "-");
            }
        });
    });

    // Aplicar filtros
    const aplicarFiltros = document.querySelector(".aplicar-filtros");
    if (aplicarFiltros) {
        aplicarFiltros.addEventListener("click", () => {
            const categorias = [...document.querySelectorAll(".filtro-categoria:checked")]
                .map(c => c.value);
            const tiendas = [...document.querySelectorAll(".filtro-tienda:checked")]
                .map(t => t.value);
            const precioMin = document.getElementById("precioMin")?.value || "";
            const precioMax = document.getElementById("precioMax")?.value || "";

            const nuevaURL = new URL(window.location);
            // Mantener búsqueda actual
            nuevaURL.searchParams.delete("categoria");
            nuevaURL.searchParams.delete("tienda");
            nuevaURL.searchParams.delete("precio_min");
            nuevaURL.searchParams.delete("precio_max");

            if (categorias.length === 1) nuevaURL.searchParams.set("categoria", categorias[0]);
            if (tiendas.length > 0) nuevaURL.searchParams.set("tienda", tiendas.join(","));
            if (precioMin) nuevaURL.searchParams.set("precio_min", precioMin);
            if (precioMax) nuevaURL.searchParams.set("precio_max", precioMax);

            window.history.replaceState({}, "", nuevaURL);

            // Cerrar panel
            document.getElementById("panelFiltros").classList.remove("activo");
            document.getElementById("overlay").classList.remove("activo");

            cargarProductos(1);
        });
    }
    
    // Limpiar filtros
    const limpiarFiltros = document.querySelector(".limpiar-filtros");
    if (limpiarFiltros) {
        limpiarFiltros.addEventListener("click", () => {
            document.querySelectorAll(".filtro-categoria, .filtro-tienda")
                .forEach(c => c.checked = false);
            document.getElementById("precioMin").value = "";
            document.getElementById("precioMax").value = "";

            const nuevaURL = new URL(window.location);
            nuevaURL.searchParams.delete("categoria");
            nuevaURL.searchParams.delete("tienda");
            nuevaURL.searchParams.delete("precio_min");
            nuevaURL.searchParams.delete("precio_max");
            window.history.replaceState({}, "", nuevaURL);
            cargarProductos(1);
        });
    }
});

// ── UTILIDADES ──
function formatearPrecio(precio) {
    return precio.toLocaleString('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    });
}

function obtenerUsuarioActual() {
    const token = localStorage.getItem("token");
    if (!token) return null;
    try {
        const usuario = JSON.parse(localStorage.getItem("usuario") || "null");
        if (!usuario) return null;
        return usuario;  // ← lee del objeto, siempre actualizado
    } catch (e) {
        return null;
    }
}



function manejarGratis() {
    const u = obtenerUsuarioActual();
    if (!u) {
        window.location.href = "/registrar.html";
    } else if (u.rol === "usuario") {
        mostrarToast("Ya tienes el plan gratuito", "info");
    } else {
        solicitarPlan("usuario", document.getElementById("btn-gratis"));
    }
}


// ── PAGINACIÓN ──
let paginaActual = 1;
let totalPaginas = 1;
let busquedaActual = "";

async function cargarProductos(pagina = 1) {

    const params = new URLSearchParams(window.location.search);
    busquedaActual = params.get("q") || "";
    const categoriaActual = params.get("categoria") || "";
    const tiendaActual = params.get("tienda") || "";
    const precioMin = params.get("precio_min") || "";
    const precioMax = params.get("precio_max") || "";

    const contenedor = document.getElementById("lista-productos");
    if (!contenedor) return;

    contenedor.innerHTML = "<p>Cargando productos...</p>";

    // Actualizar texto búsqueda
    const textoBusqueda = document.getElementById("texto-busqueda");
    if (textoBusqueda) {
        textoBusqueda.textContent = categoriaActual 
            ? categoriaActual.charAt(0).toUpperCase() + categoriaActual.slice(1)
            : busquedaActual ? `"${busquedaActual}"` : "Todos los productos";
    }

    const usuario = obtenerUsuarioActual();
    if (usuario && busquedaActual.trim() && pagina === 1) {
        fetch("/api/historial/guardar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario_id: usuario.id, busqueda: busquedaActual })
        }).catch(() => {});
    }

    try {
        const response = await fetch(
        `/api/productos?q=${busquedaActual}&categoria=${categoriaActual}&tienda=${tiendaActual}&precio_min=${precioMin}&precio_max=${precioMax}&pagina=${pagina}&por_pagina=10`
    );
        const data = await response.json();

        paginaActual = data.pagina;
        totalPaginas = data.total_paginas;

        // Actualizar cantidad
        const cantidadResultados = document.getElementById("cantidad-resultados");
        if (cantidadResultados) {
            cantidadResultados.textContent = `${data.total} productos encontrados`;
        }

        contenedor.innerHTML = "";

        if (data.productos.length === 0) {
            contenedor.innerHTML = "<p>No se encontraron productos</p>";
            const pag = document.getElementById("paginacion");
            if (pag) pag.innerHTML = "";
            return;
        }

        data.productos.forEach(prod => {
            const estaLogueado = obtenerUsuarioActual();
            const botonFavorito = estaLogueado ? `
                <button id="fav-${prod.id}"
                    onclick="agregarFavorito(${prod.id}, '${prod.nombre}', 'fav-${prod.id}')"
                    style="background:#ff6b00; color:white; border:none; padding:6px 12px;
                           border-radius:4px; cursor:pointer; margin-top:8px; font-size:14px;">
                    ⭐ Favorito
                </button>` : '';

            contenedor.innerHTML += `
                <article class="producto-busqueda">
                    <img src="${(prod.imagen && prod.imagen !== 'null') ? prod.imagen : 'imagenes/logo1.png'}"
                         alt="producto" style="width:100px; height:100px; object-fit:contain;">
                    <div class="info-producto-busqueda">
                        <h3>${prod.nombre}</h3>
                        <p class="precio">${formatearPrecio(prod.precio)}</p>
                        <p>${prod.tienda}</p>
                        <a href="producto.html?nombre=${prod.nombre}">Ver producto</a>
                        ${botonFavorito}
                    </div>
                </article>
            `;
        });

        renderizarPaginacion();

    } catch (error) {
        console.error("Error completo:", error);
        console.error("Mensaje:", error.message);
        contenedor.innerHTML = "<p>Error al cargar productos</p>";
    }
}

function renderizarPaginacion() {
    const contenedor = document.getElementById("paginacion");
    if (!contenedor) return;
    contenedor.innerHTML = "";
    if (totalPaginas <= 1) return;

    const btnAnterior = document.createElement("button");
    btnAnterior.textContent = "← Anterior";
    btnAnterior.disabled = paginaActual === 1;
    btnAnterior.onclick = () => {
        cargarProductos(paginaActual - 1);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };
    contenedor.appendChild(btnAnterior);

    const indicador = document.createElement("span");
    indicador.textContent = `Página ${paginaActual} de ${totalPaginas}`;
    indicador.style.cssText = "padding: 0 16px; font-size: 14px; color: #64748b;";
    contenedor.appendChild(indicador);

    const btnSiguiente = document.createElement("button");
    btnSiguiente.textContent = "Siguiente →";
    btnSiguiente.disabled = paginaActual === totalPaginas;
    btnSiguiente.onclick = () => {
        cargarProductos(paginaActual + 1);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };
    contenedor.appendChild(btnSiguiente);
}

// ── TOP PRODUCTOS ──
async function cargarTop() {
    const contenedor = document.getElementById("productos-top");
    if (!contenedor) return;
    const res = await fetch("/api/productos/top");
    const data = await res.json();
    contenedor.innerHTML = "";
    data.forEach(p => {
        contenedor.innerHTML += `
            <div>
                <img src="${(p.imagen && p.imagen !== 'null') ? p.imagen : 'imagenes/logo1.png'}"
                     style="width:100px; height:100px; object-fit:contain;">
                <h3>${p.nombre}</h3>
                <p>${formatearPrecio(p.precio)}</p>
                <a href="producto.html?nombre=${p.nombre}">Ver</a>
            </div>
        `;
    });
}

// ── DETALLE PRODUCTO ──
async function cargarDetalle() {
    const params = new URLSearchParams(window.location.search);
    let nombre = params.get("nombre");

    // 🔥 Si el nombre es un objeto (ej: [object HTMLHeadingElement])
    if (nombre && typeof nombre === 'object') {
        nombre = nombre.textContent || nombre.innerText || '';
    }
    // Si es un string que parece un objeto serializado
    if (typeof nombre === 'string' && (nombre.startsWith('[object') || nombre === 'null')) {
        console.error('Nombre inválido:', nombre);
        document.getElementById("nombre").innerText = "Producto no válido";
        document.getElementById("precio-principal").innerText = "$0";
        document.getElementById("tiendas").innerHTML = "<p>Error en el enlace.</p>";
        document.getElementById("similares").innerHTML = "<p>No se pudo cargar.</p>";
        return;
    }
    if (!nombre) return;

    try {
        const res = await fetch(`/api/producto?nombre=${encodeURIComponent(nombre)}`);
        const data = await res.json();

        if (!data || !data.producto) {
            console.error('Producto no encontrado:', nombre);
            document.getElementById("nombre").innerText = "Producto no encontrado";
            document.getElementById("precio-principal").innerText = "$0";
            document.getElementById("tiendas").innerHTML = "<p>No hay información disponible.</p>";
            document.getElementById("similares").innerHTML = "<p>No se encontraron similares.</p>";
            return;
        }

        // ✅ Resto del código original (mostrar producto, tiendas, similares, etc.)
        document.getElementById("nombre").innerText = data.producto.nombre;
        document.getElementById("imagen").src = data.producto.imagen || 'imagenes/logo1.png';

        const usuario = JSON.parse(localStorage.getItem("usuario") || "null");
        const contenedorInfo = document.querySelector(".info-producto");
        if (usuario && contenedorInfo && data.producto.id) {
            contenedorInfo.innerHTML += `
                <button id="fav-detalle"
                    onclick="agregarFavorito(${data.producto.id}, '${data.producto.nombre}', 'fav-detalle')"
                    style="background:#ff6b00; color:white; border:none; padding:10px 20px;
                           border-radius:6px; cursor:pointer; margin-top:12px; font-size:15px;">
                    ⭐ Favorito
                </button>
            `;
        }

        const tiendasDiv = document.getElementById("tiendas");
        tiendasDiv.innerHTML = "";
        data.tiendas.forEach(t => {
            tiendasDiv.innerHTML += `
                <div style="display:flex; justify-content:space-between; align-items:center; 
                            padding:10px; border-bottom:1px solid #eee;">
                    <span>${t.tienda}</span>
                    <span class="precio">${formatearPrecio(t.precio)}</span>
                    ${t.url ? `<a href="${t.url}" target="_blank" 
                        style="background:#ff7a00; color:white; padding:8px 14px; 
                        border-radius:5px; text-decoration:none; font-size:14px;">
                        Comprar →</a>` : ''}
                </div>
            `;
        });

        const similaresDiv = document.getElementById("similares");
        similaresDiv.innerHTML = "";
        data.similares.forEach(s => {
            // Protección adicional: si s.nombre es objeto, extraer texto
            let nombreSimilar = s.nombre;
            if (nombreSimilar && typeof nombreSimilar === 'object') {
                nombreSimilar = nombreSimilar.textContent || nombreSimilar.innerText || '';
            }
            similaresDiv.innerHTML += `
                <div>
                    <h4>${nombreSimilar}</h4>
                    <p>${formatearPrecio(s.precio)}</p>
                    <a href="producto.html?nombre=${encodeURIComponent(nombreSimilar)}">Ver</a>
                </div>
            `;
        });

    } catch (err) {
        console.error("Error cargando detalle:", err);
        document.getElementById("nombre").innerText = "Error al cargar";
    }
}

// ── HEADER ──
function actualizarHeader() {
    const usuario = JSON.parse(localStorage.getItem("usuario") || "null");
    const authDiv = document.querySelector(".auth-buttons");
    if (!authDiv) return;
    if (usuario) {
        const esAdmin = usuario.rol === "admin" || usuario.rol === "root";
        authDiv.innerHTML = `
            <a href="planes.html" class="btn-auth" style="background:#f1f5f9; color:#ff6b00;">💎 Planes</a>
            <span class="btn-auth">Hola, ${usuario.nombre}</span>
            ${esAdmin ? '<a href="admin.html" class="btn-auth" style="background:#1e293b;">⚙️ Admin</a>' : ''}
            <a href="dashboard.html" class="btn-auth">Mi cuenta</a>
            <button class="btn-auth" onclick="cerrarSesion()">Salir</button>
        `;
    } else {
        authDiv.innerHTML = `
            <a href="planes.html" class="btn-auth" style="background:#f1f5f9; color:#ff6b00;">💎 Planes</a>
            <a href="login.html" class="btn-auth">Ingresar</a>
            <a href="registrar.html" class="btn-auth">Registro</a>
        `;
    }
}

function cerrarSesion() {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    window.location.href = "/index.html";
}

async function verificarSesionActiva() {
    const usuario = JSON.parse(localStorage.getItem("usuario") || "null");
    if (!usuario) return;
    
    try {
        const res = await fetch(`/api/usuarios/${usuario.id}`);
        const data = await res.json();
        
        // Si el rol cambió, actualizar localStorage
        if (data.rol !== usuario.rol) {
            usuario.rol = data.rol;
            localStorage.setItem("usuario", JSON.stringify(usuario));
            // Recargar para aplicar cambios
            window.location.reload();
        }
    } catch (e) {
        console.error("Error verificando sesión:", e);
    }
}

// ── FAVORITOS (actualizado con límite) ──
async function agregarFavorito(productoId, nombreProducto, botonId) {
    const boton = document.getElementById(botonId);
    if (!boton || boton.disabled) return;
    boton.disabled = true;
 
    const usuario = obtenerUsuarioActual();
    if (!usuario) { window.location.href = "/login.html"; return; }
 
    try {
        const res = await fetch("/api/favoritos/toggle", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario_id: usuario.id, producto_id: productoId })
        });
        const data = await res.json();
 
        if (data.limite_alcanzado) {
            mostrarModalLimite("favoritos", data.limite);
            boton.disabled = false;
            return;
        }
 
        if (data.accion === "agregado") {
            boton.textContent = "⭐ Guardado";
            boton.style.background = "#22c55e";
        } else {
            boton.textContent = "⭐ Favorito";
            boton.style.background = "#ff6b00";
        }
        boton.style.color = "white";
        boton.style.transform = "scale(1.4)";
        boton.style.transition = "transform 0.2s ease";
        setTimeout(() => { boton.style.transform = "scale(1)"; }, 200);
        mostrarToast(data.accion === "agregado" ? "Agregado a favoritos" : "Eliminado de favoritos",
                     data.accion === "agregado" ? "success" : "info");
        boton.disabled = false;
 
    } catch (err) {
        boton.disabled = false;
        mostrarToast("Error de conexión", "error");
    }
}


// ── TOAST ──
function mostrarToast(mensaje, tipo = "success") {
    const anterior = document.getElementById("toast-favorito");
    if (anterior) anterior.remove();

    const colores = {
        success: { bg: "#22c55e", icon: "✅" },
        info:    { bg: "#f59e0b", icon: "ℹ️" },
        error:   { bg: "#ef4444", icon: "❌" }
    };
    const { bg, icon } = colores[tipo] || colores.success;

    const toast = document.createElement("div");
    toast.id = "toast-favorito";
    toast.textContent = `${icon} ${mensaje}`;
    toast.style.cssText = `
        position: fixed; bottom: 30px; right: 30px;
        background: ${bg}; color: white; padding: 14px 22px;
        border-radius: 10px; font-size: 15px; font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); z-index: 9999;
        opacity: 0; transform: translateY(20px); transition: all 0.3s ease;
    `;
    document.body.appendChild(toast);
    requestAnimationFrame(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";
    });
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(20px)";
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}


// ── COMPARACION (nuevo) ──
let dataTiendasGlobal = [];
 
async function inicializarComparacion(tiendas) {
    dataTiendasGlobal = tiendas;
    const usuario = obtenerUsuarioActual();
 
    // Sin cuenta — mostrar bloqueo
    if (!usuario) {
        document.getElementById("comparacion-sin-cuenta").style.display = "block";
        document.getElementById("comparacion-btn-container").style.display = "none";
        document.getElementById("tiendas").style.display = "none";
        return;
    }
 
    // Con cuenta — mostrar botón y contador
    document.getElementById("comparacion-sin-cuenta").style.display = "none";
    document.getElementById("comparacion-btn-container").style.display = "block";
    document.getElementById("tiendas").style.display = "none";
 
    // Mostrar cuántas comparaciones le quedan
    try {
        const res = await fetch(`/api/plan/${usuario.id}`);
        const plan = await res.json();
        const restantes = document.getElementById("comparacion-restantes");
        if (plan.comparaciones_limite === null) {
            restantes.textContent = "Comparaciones ilimitadas ✨";
        } else {
            const quedan = plan.comparaciones_limite - plan.comparaciones_usadas;
            restantes.textContent = `Te quedan ${quedan} de ${plan.comparaciones_limite} comparaciones este mes`;
            if (quedan <= 0) {
                const btn = document.getElementById("btn-ver-comparacion");
                btn.disabled = false;
                btn.style.background = "#7c3aed";
                btn.textContent = "🚀 Mejorar plan para ver más";
                btn.onclick = () => mostrarModalLimite("comparaciones", plan.comparaciones_limite);
            }
        }
    } catch (_) {}
}

async function verComparacion() {
    const usuario = obtenerUsuarioActual();
    if (!usuario) { window.location.href = "/login.html"; return; }
 
    const btn = document.getElementById("btn-ver-comparacion");
    btn.disabled = true;
    btn.textContent = "Verificando...";
 
    try {
        const res = await fetch("/api/comparaciones/verificar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario_id: parseInt(usuario.id) })
        });
        const data = await res.json();
 
        if (!data.permitido) {
            mostrarModalLimite("comparaciones", data.limite);
            btn.disabled = false;
            btn.textContent = "📊 Ver comparación de precios";
            return;
        }
 
        // Mostrar comparación
        document.getElementById("comparacion-btn-container").style.display = "none";
        const tiendasDiv = document.getElementById("tiendas");
        tiendasDiv.style.display = "block";
        tiendasDiv.innerHTML = "";
 
        const tiendas = dataTiendasGlobal;
        const precioMin = tiendas[0].precio;
        const precioMax = tiendas[tiendas.length - 1].precio;
 
        tiendas.forEach((t, i) => {
            const esMasBarato = i === 0;
            const porcentajeBarra = ((t.precio - precioMin) / (precioMax - precioMin || 1)) * 45 + 55;
            const colorBarra = i === 0 ? '#16a34a' : i === tiendas.length - 1 ? '#ef4444' : '#f59e0b';
 
            tiendasDiv.innerHTML += `
                <div class="tienda-fila">
                    <div class="tienda-logo-box ${getLogoClass(t.tienda)}">${getLogoLetras(t.tienda)}</div>
                    <div class="tienda-datos">
                        <div class="tienda-nombre-fila">
                            ${t.tienda}
                            ${esMasBarato ? '<span class="tag-barato">✓ Más barato</span>' : ''}
                        </div>
                        <div class="tienda-entrega">Disponible online</div>
                        <div class="barra-comparacion" style="width:${porcentajeBarra}%;background:${colorBarra}"></div>
                    </div>
                    <div class="tienda-precio-fila ${esMasBarato ? 'precio-verde' : ''}">${formatearPrecio(t.precio)}</div>
                    ${t.url ? `<a href="${t.url}" target="_blank" class="btn-ir-tienda">Ver →</a>` : ''}
                </div>
            `;
        });
 
        // Actualizar contador
        if (data.limite !== null) {
            mostrarToast(`Comparación usada. Te quedan ${data.restantes} este mes.`, "info");
        }
 
    } catch (err) {
        btn.disabled = false;
        btn.textContent = "📊 Ver comparación de precios";
        mostrarToast("Error de conexión", "error");
    }
}
 
// ── MAPA (restricción visitantes) ──

function inicializarMapa(tiendas) {
    const usuario = obtenerUsuarioActual();
    if (!usuario) {
        document.getElementById("mapa-sin-cuenta").style.display = "block";
        document.getElementById("mapa-con-cuenta").style.display = "none";
        return;
    }
    document.getElementById("mapa-sin-cuenta").style.display = "none";
    document.getElementById("mapa-con-cuenta").style.display = "block";
    if (tiendas.length > 0) cargarMapaTiendas(tiendas);
}

 
// ── MODAL DE LÍMITE ──
function mostrarModalLimite(tipo, limite) {
    const anterior = document.getElementById("modal-limite");
    if (anterior) anterior.remove();
 
    const textos = {
        favoritos: {
            titulo: `Límite de ${limite} favoritos alcanzado`,
            desc: "Mejora tu plan para guardar más productos favoritos.",
        },
        comparaciones: {
            titulo: `Límite de ${limite} comparaciones mensuales alcanzado`,
            desc: "Mejora tu plan para ver más comparaciones este mes.",
        }
    };
 
    const { titulo, desc } = textos[tipo] || textos.favoritos;
 
    const modal = document.createElement("div");
    modal.id = "modal-limite";
    modal.style.cssText = `
        position: fixed; inset: 0; background: rgba(0,0,0,0.5);
        display: flex; align-items: center; justify-content: center;
        z-index: 9999; padding: 20px;
    `;
    modal.innerHTML = `
        <div style="background:white; border-radius:16px; padding:32px; max-width:400px;
                    width:100%; text-align:center; box-shadow:0 20px 60px rgba(0,0,0,0.2);">
            <div style="font-size:48px; margin-bottom:12px;">🚀</div>
            <h3 style="margin:0 0 8px; font-size:18px; color:#1a1a1a;">${titulo}</h3>
            <p style="color:#888; font-size:14px; margin:0 0 24px;">${desc}</p>
            <div style="display:flex; flex-direction:column; gap:10px;">
                <a href="planes.html"
                   style="background:#ff6b00; color:white; padding:12px; border-radius:10px;
                          text-decoration:none; font-size:15px; font-weight:600;">
                    ⭐ Ver planes
                </a>
                <button onclick="document.getElementById('modal-limite').remove()"
                    style="background:#f1f5f9; color:#64748b; border:none; padding:12px;
                           border-radius:10px; cursor:pointer; font-size:14px;">
                    Ahora no
                </button>
            </div>
        </div>
    `;
    modal.addEventListener("click", e => {
        if (e.target === modal) modal.remove();
    });
    document.body.appendChild(modal);
}
