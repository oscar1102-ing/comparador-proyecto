document.addEventListener("DOMContentLoaded", () => {
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
            const nuevaURL = new URL(window.location);
            nuevaURL.searchParams.delete("categoria");
            window.history.replaceState({}, "", nuevaURL);
            cargarProductos(1);
        });
    }
});

// ── PAGINACIÓN ──
let paginaActual = 1;
let totalPaginas = 1;
let busquedaActual = "";

async function cargarProductos(pagina = 1) {
    const params = new URLSearchParams(window.location.search);
    busquedaActual = params.get("q") || "";

    const contenedor = document.getElementById("lista-productos");
    if (!contenedor) return;

    contenedor.innerHTML = "<p>Cargando productos...</p>";

    // Actualizar texto búsqueda
    const textoBusqueda = document.getElementById("texto-busqueda");
    if (textoBusqueda) {
        textoBusqueda.textContent = busquedaActual ? `"${busquedaActual}"` : "Todos los productos";
    }

    const usuario = JSON.parse(localStorage.getItem("usuario") || "null");
    if (usuario && busquedaActual.trim() && pagina === 1) {
        fetch("/api/historial/guardar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario_id: usuario.id, busqueda: busquedaActual })
        }).catch(() => {});
    }

    try {
        const response = await fetch(`/api/productos?q=${busquedaActual}&pagina=${pagina}&por_pagina=10`);
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
            const estaLogueado = localStorage.getItem("usuario");
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
                        <p class="precio">$${prod.precio}</p>
                        <p>${prod.tienda}</p>
                        <a href="producto.html?nombre=${prod.nombre}">Ver producto</a>
                        ${botonFavorito}
                    </div>
                </article>
            `;
        });

        renderizarPaginacion();

    } catch (error) {
        console.error(error);
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
                <p>$${p.precio}</p>
                <a href="producto.html?nombre=${p.nombre}">Ver</a>
            </div>
        `;
    });
}

// ── DETALLE PRODUCTO ──
async function cargarDetalle() {
    const params = new URLSearchParams(window.location.search);
    const nombre = params.get("nombre");
    if (!nombre) return;

    const res = await fetch(`/api/producto?nombre=${nombre}`);
    const data = await res.json();

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
        tiendasDiv.innerHTML += `<p>${t.tienda} - $${t.precio}</p>`;
    });

    const similaresDiv = document.getElementById("similares");
    similaresDiv.innerHTML = "";
    data.similares.forEach(s => {
        similaresDiv.innerHTML += `
            <div>
                <h4>${s.nombre}</h4>
                <p>$${s.precio}</p>
                <a href="producto.html?nombre=${s.nombre}">Ver</a>
            </div>
        `;
    });
}

// ── HEADER ──
function actualizarHeader() {
    const usuario = JSON.parse(localStorage.getItem("usuario") || "null");
    const authDiv = document.querySelector(".auth-buttons");
    if (!authDiv) return;
    if (usuario) {
        const esAdmin = usuario.rol === "admin";
        authDiv.innerHTML = `
            <span class="btn-auth">Hola, ${usuario.nombre}</span>
            ${esAdmin ? '<a href="admin.html" class="btn-auth" style="background:#1e293b;">⚙️ Admin</a>' : ''}
            <a href="dashboard.html" class="btn-auth">Mi cuenta</a>
            <button class="btn-auth" onclick="cerrarSesion()">Salir</button>
        `;
    }
}

function cerrarSesion() {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    window.location.href = "/index.html";
}

// ── FAVORITOS ──
async function agregarFavorito(productoId, nombreProducto, botonId) {
    const boton = document.getElementById(botonId);
    if (!boton || boton.disabled) return;
    boton.disabled = true;

    const usuario = JSON.parse(localStorage.getItem("usuario") || "null");
    if (!usuario) { window.location.href = "/login.html"; return; }

    try {
        const res = await fetch("/api/favoritos/toggle", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario_id: usuario.id, producto_id: productoId })
        });
        const data = await res.json();

        if (data.accion === "agregado") {
            boton.textContent = "⭐ Guardado";
            boton.style.background = "#22c55e";
        } else {
            boton.textContent = "⭐ Favorito";
            boton.style.background = "#ff6b00";
        }
        boton.style.transform = "scale(1.4)";
        boton.style.transition = "transform 0.2s ease";
        setTimeout(() => { boton.style.transform = "scale(1)"; }, 200);
        mostrarToast(data.accion === "agregado" ? "Agregado a favoritos" : "Eliminado de favoritos", data.accion === "agregado" ? "success" : "info");
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
