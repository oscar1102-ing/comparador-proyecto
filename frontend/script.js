document.addEventListener("DOMContentLoaded", () => {


cargarProductos();
cargarTop();
cargarDetalle();
/* =========================
   CARRUSEL
========================= */

document.querySelectorAll(".comparacion").forEach(carrusel => {

    const items = carrusel.querySelectorAll(".tienda");
    if(items.length === 0) return;

    let index = 0;
    let intervalo;
    const visible = 3;

    function moverCarrusel(){
        const itemWidth = items[0].getBoundingClientRect().width;

        index++;
        if(index > items.length - visible){
            index = 0;
        }

        carrusel.scrollTo({
            left: index * itemWidth,
            behavior: "smooth"
        });
    }

    function iniciarCarrusel(){
        intervalo = setInterval(moverCarrusel, 3000);
    }

    function detenerCarrusel(){
        clearInterval(intervalo);
    }

    iniciarCarrusel();

    carrusel.addEventListener("mouseenter", detenerCarrusel);
    carrusel.addEventListener("mouseleave", iniciarCarrusel);

});


/* =========================
   BUSQUEDA + FILTROS
========================= */

const textoBusqueda = document.getElementById("texto-busqueda");

if(textoBusqueda){

    const params = new URLSearchParams(window.location.search);
    const busqueda = params.get("q");
    const categoriaURL = params.get("categoria");

    const cantidadResultados = document.getElementById("cantidad-resultados");
    const productos = document.querySelectorAll(".producto-busqueda");
    const todosLosProductos = Array.from(productos);
    const paginacion = document.getElementById("paginacion");
    const mensajeSinResultados = document.getElementById("sin-resultados");

    const productosPorPagina = 10;

    let resultados = [];
    let paginaActual = 1;

    const texto = busqueda ? busqueda.toLowerCase().trim() : "";

    /* =========================
       INICIALIZAR FILTROS
    ========================= */

    if(categoriaURL){
        document.querySelectorAll(".filtro-categoria").forEach(cb => {
            if(cb.value === categoriaURL){
                cb.checked = true;
            }
        });
    }

    /* =========================
       TEXTO BUSQUEDA
    ========================= */

    function actualizarTexto(categorias){
        if(busqueda){
            textoBusqueda.textContent = `"${busqueda}"`;
        }
        else if(categorias.length > 0){
            textoBusqueda.textContent = `Categoría: ${categorias.join(", ")}`;
        }
        else{
            textoBusqueda.textContent = "Todos los productos";
        }
    }

    /* =========================
       FILTRAR (ÚNICA LÓGICA)
    ========================= */

    function filtrarProductos(){

        const precioMin = parseInt(document.getElementById("precioMin").value) || 0;
        const precioMax = parseInt(document.getElementById("precioMax").value) || Infinity;

        const categorias = Array.from(document.querySelectorAll(".filtro-categoria:checked"))
            .map(el => el.value);

        const tiendas = Array.from(document.querySelectorAll(".filtro-tienda:checked"))
            .map(el => el.value);

        resultados = todosLosProductos.filter(producto => {

            const nombre = producto.dataset.nombre.toLowerCase();
            const categoria = producto.dataset.categoria.toLowerCase();
            const tienda = producto.dataset.tienda.toLowerCase();
            const precio = parseInt(producto.dataset.precio);

            let cumpleBusqueda = !texto || nombre.includes(texto);
            let cumpleCategoria = true;

            if(categorias.length > 0){
                cumpleCategoria = categorias.includes(categoria);
            } 
            else if(categoriaURL){
                cumpleCategoria = categoria === categoriaURL;
            }
            let cumpleTienda = tiendas.length === 0 || tiendas.includes(tienda);
            let cumplePrecio = precio >= precioMin && precio <= precioMax;

            return cumpleBusqueda && cumpleCategoria && cumpleTienda && cumplePrecio;
        });

        actualizarTexto(categorias);

        cantidadResultados.textContent = resultados.length + " productos encontrados";
        mensajeSinResultados.style.display = resultados.length === 0 ? "block" : "none";

        mostrarPagina(1);
    }

    /* =========================
       PAGINACION
    ========================= */

    function mostrarPagina(pagina){

        paginaActual = pagina;

        const inicio = (pagina-1) * productosPorPagina;
        const fin = inicio + productosPorPagina;

        productos.forEach(p => p.style.display = "none");

        resultados.slice(inicio, fin).forEach(p => {
            p.style.display = "flex";
        });

        crearPaginacion();
    }

    function crearPaginacion(){

        paginacion.innerHTML = "";

        const totalPaginas = Math.ceil(resultados.length / productosPorPagina);
        if(totalPaginas <= 1) return;

        const anterior = document.createElement("button");
        anterior.textContent = "Anterior";
        anterior.disabled = paginaActual === 1;
        anterior.onclick = () => mostrarPagina(paginaActual - 1);
        paginacion.appendChild(anterior);

        for(let i = 1; i <= totalPaginas; i++){
            const btn = document.createElement("button");
            btn.textContent = i;

            if(i === paginaActual){
                btn.classList.add("pagina-activa");
            }

            btn.onclick = () => mostrarPagina(i);
            paginacion.appendChild(btn);
        }

        const siguiente = document.createElement("button");
        siguiente.textContent = "Siguiente";
        siguiente.disabled = paginaActual === totalPaginas;
        siguiente.onclick = () => mostrarPagina(paginaActual + 1);
        paginacion.appendChild(siguiente);
    }

    /* =========================
       EVENTOS
    ========================= */

    const aplicarFiltros = document.querySelector(".aplicar-filtros");

    if(aplicarFiltros){
        aplicarFiltros.addEventListener("click", () => {

            // limpiar categoria de la URL (solo visual)
            const nuevaURL = new URL(window.location);
            nuevaURL.searchParams.delete("categoria");
            window.history.replaceState({}, "", nuevaURL);

            filtrarProductos();
        });
    }

    /* =========================
       CARGA INICIAL
    ========================= */

    filtrarProductos();
}


/* =========================
   PANEL FILTROS
========================= */

const btnFiltros = document.querySelector(".btn-filtros");
const panelFiltros = document.getElementById("panelFiltros");
const cerrarFiltros = document.getElementById("cerrarFiltros");
const overlay = document.getElementById("overlay");

if(btnFiltros){

    btnFiltros.addEventListener("click", () => {
        panelFiltros.classList.add("activo");
        overlay.classList.add("activo");
    });

    cerrarFiltros.addEventListener("click", cerrarPanel);
    overlay.addEventListener("click", cerrarPanel);

    function cerrarPanel(){
        panelFiltros.classList.remove("activo");
        overlay.classList.remove("activo");
    }
}


/* =========================
   TOGGLE FILTROS
========================= */

document.querySelectorAll(".toggle-filtro").forEach(toggle => {

    toggle.addEventListener("click", () => {

        const contenido = toggle.nextElementSibling;

        if(contenido.style.display === "block"){
            contenido.style.display = "none";
            toggle.innerHTML = toggle.innerHTML.replace("-", "+");
        } else {
            contenido.style.display = "block";
            toggle.innerHTML = toggle.innerHTML.replace("+", "-");
        }

    });

});

});

async function cargarProductos() {

    const params = new URLSearchParams(window.location.search);
    const busqueda = params.get("q") || "";

    const contenedor = document.getElementById("lista-productos");

    if (!contenedor) return;

    contenedor.innerHTML = "<p>Cargando productos...</p>";
    
    const usuario = JSON.parse(localStorage.getItem("usuario") || "null");
    if (usuario && busqueda.trim()) {
        fetch("http://127.0.0.1:8000/historial/guardar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario_id: usuario.id, busqueda: busqueda })
        }).catch(() => {}); // silencioso, no bloquea
    }

    try {
        const response = await fetch(`/api/productos?q=${busqueda}`);
        const data = await response.json();

        contenedor.innerHTML = "";

        if (data.length === 0) {
            contenedor.innerHTML = "<p>No se encontraron productos</p>";
            return;
        }

        data.forEach(prod => {
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
                    <img src="${prod.imagen}" alt="producto">
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

    } catch (error) {
        console.error(error);
        contenedor.innerHTML = "<p>Error al cargar productos</p>";
    }
}

async function cargarTop() {

    const contenedor = document.getElementById("productos-top");
    if (!contenedor) return;

    const res = await fetch("/api/productos/top");
    const data = await res.json();

    contenedor.innerHTML = "";

    data.forEach(p => {
        contenedor.innerHTML += `
            <div>
                <img src="${p.imagen}">
                <h3>${p.nombre}</h3>
                <p>$${p.precio}</p>
                <a href="producto.html?nombre=${p.nombre}">Ver</a>
            </div>
        `;
    });
}

async function cargarDetalle() {

    const params = new URLSearchParams(window.location.search);
    const nombre = params.get("nombre");

    if (!nombre) return;

    const res = await fetch(`/api/producto?nombre=${nombre}`);
    const data = await res.json();


    document.getElementById("nombre").innerText = data.producto.nombre;
    document.getElementById("imagen").src = data.producto.imagen;
    
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
            <p>${t.tienda} - $${t.precio}</p>
        `;
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



actualizarHeader();

// Auth header dinámico
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

async function agregarFavorito(productoId, nombreProducto, botonId) {
    const boton = document.getElementById(botonId);
    if (!boton || boton.disabled) return;
    boton.disabled = true;

    const usuario = JSON.parse(localStorage.getItem("usuario") || "null");
    if (!usuario) {
        window.location.href = "/login.html";
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:8000/favoritos/toggle", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario_id: usuario.id, producto_id: productoId })
        });
        const data = await res.json();

        if (data.accion === "agregado") {
            boton.textContent = "⭐ Guardado";
            boton.style.background = "#22c55e";
            boton.style.transform = "scale(1.4)";
            boton.style.transition = "transform 0.2s ease";
            setTimeout(() => { boton.style.transform = "scale(1)"; }, 200);
            mostrarToast("Agregado a favoritos");
        } else {
            boton.textContent = "⭐ Favorito";
            boton.style.background = "#ff6b00";
            boton.style.transform = "scale(1.4)";
            boton.style.transition = "transform 0.2s ease";
            setTimeout(() => { boton.style.transform = "scale(1)"; }, 200);
            mostrarToast("Eliminado de favoritos", "info");
        }

        boton.disabled = false;

    } catch (err) {
        boton.disabled = false;
        mostrarToast("Error de conexión", "error");
    }
}

function mostrarToast(mensaje, tipo = "success") {
    // Eliminar toast anterior si existe
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
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: ${bg};
        color: white;
        padding: 14px 22px;
        border-radius: 10px;
        font-size: 15px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 9999;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s ease;
    `;
    document.body.appendChild(toast);

    // Animar entrada
    requestAnimationFrame(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";
    });

    // Animar salida
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(20px)";
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

actualizarHeader();
