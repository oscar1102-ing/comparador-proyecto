-- Esquema de la base de datos - Comparador de Precios

-- Tabla de tiendas
CREATE TABLE IF NOT EXISTS tiendas (
    id_tienda SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    url TEXT
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    categoria VARCHAR(100)
);

-- Tabla de precios (relaciona productos con tiendas)
CREATE TABLE IF NOT EXISTS precios (
    id_precio SERIAL PRIMARY KEY,
    producto_id INTEGER NOT NULL REFERENCES productos(id_producto),
    tienda_id INTEGER NOT NULL REFERENCES tiendas(id_tienda),
    precio NUMERIC(10,0) NOT NULL,
    fecha_actual TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mensaje de confirmación
SELECT 'Base de datos creada correctamente' as mensaje;