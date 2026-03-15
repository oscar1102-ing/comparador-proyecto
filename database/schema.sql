--
-- PostgreSQL database dump
--

\restrict RxWMczrokx5fPgxahNtJ4HHe0cFaUoXd7VIhxbOrpp6LqphxDTrr7VICJcq2Xtf

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-03-15 10:18:19

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 4935 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 224 (class 1259 OID 16410)
-- Name: precios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.precios (
    id_precio integer NOT NULL,
    producto_id integer NOT NULL,
    tienda_id integer NOT NULL,
    precio numeric(10,0) NOT NULL,
    fecha_actual timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.precios OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16409)
-- Name: precios_id_precio_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.precios_id_precio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.precios_id_precio_seq OWNER TO postgres;

--
-- TOC entry 4936 (class 0 OID 0)
-- Dependencies: 223
-- Name: precios_id_precio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.precios_id_precio_seq OWNED BY public.precios.id_precio;


--
-- TOC entry 222 (class 1259 OID 16401)
-- Name: productos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.productos (
    id_producto integer NOT NULL,
    nombre character varying(200) NOT NULL,
    categoria character varying(100)
);


ALTER TABLE public.productos OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16400)
-- Name: productos_id_producto_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.productos_id_producto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.productos_id_producto_seq OWNER TO postgres;

--
-- TOC entry 4937 (class 0 OID 0)
-- Dependencies: 221
-- Name: productos_id_producto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.productos_id_producto_seq OWNED BY public.productos.id_producto;


--
-- TOC entry 220 (class 1259 OID 16390)
-- Name: tiendas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tiendas (
    id_tienda integer NOT NULL,
    nombre character varying(200) NOT NULL,
    url text
);


ALTER TABLE public.tiendas OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16389)
-- Name: tiendas_id_tienda_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tiendas_id_tienda_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tiendas_id_tienda_seq OWNER TO postgres;

--
-- TOC entry 4938 (class 0 OID 0)
-- Dependencies: 219
-- Name: tiendas_id_tienda_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tiendas_id_tienda_seq OWNED BY public.tiendas.id_tienda;


--
-- TOC entry 4767 (class 2604 OID 16413)
-- Name: precios id_precio; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.precios ALTER COLUMN id_precio SET DEFAULT nextval('public.precios_id_precio_seq'::regclass);


--
-- TOC entry 4766 (class 2604 OID 16404)
-- Name: productos id_producto; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos ALTER COLUMN id_producto SET DEFAULT nextval('public.productos_id_producto_seq'::regclass);


--
-- TOC entry 4765 (class 2604 OID 16393)
-- Name: tiendas id_tienda; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tiendas ALTER COLUMN id_tienda SET DEFAULT nextval('public.tiendas_id_tienda_seq'::regclass);


--
-- TOC entry 4929 (class 0 OID 16410)
-- Dependencies: 224
-- Data for Name: precios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.precios (id_precio, producto_id, tienda_id, precio, fecha_actual) FROM stdin;
\.


--
-- TOC entry 4927 (class 0 OID 16401)
-- Dependencies: 222
-- Data for Name: productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.productos (id_producto, nombre, categoria) FROM stdin;
\.


--
-- TOC entry 4925 (class 0 OID 16390)
-- Dependencies: 220
-- Data for Name: tiendas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tiendas (id_tienda, nombre, url) FROM stdin;
\.


--
-- TOC entry 4939 (class 0 OID 0)
-- Dependencies: 223
-- Name: precios_id_precio_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.precios_id_precio_seq', 1, false);


--
-- TOC entry 4940 (class 0 OID 0)
-- Dependencies: 221
-- Name: productos_id_producto_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.productos_id_producto_seq', 1, false);


--
-- TOC entry 4941 (class 0 OID 0)
-- Dependencies: 219
-- Name: tiendas_id_tienda_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tiendas_id_tienda_seq', 1, false);


--
-- TOC entry 4774 (class 2606 OID 16419)
-- Name: precios pk_id_precio; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.precios
    ADD CONSTRAINT pk_id_precio PRIMARY KEY (id_precio);


--
-- TOC entry 4772 (class 2606 OID 16408)
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (id_producto);


--
-- TOC entry 4770 (class 2606 OID 16399)
-- Name: tiendas tiendas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tiendas
    ADD CONSTRAINT tiendas_pkey PRIMARY KEY (id_tienda);


--
-- TOC entry 4775 (class 2606 OID 16420)
-- Name: precios fk_id_producto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.precios
    ADD CONSTRAINT fk_id_producto FOREIGN KEY (producto_id) REFERENCES public.productos(id_producto);


--
-- TOC entry 4776 (class 2606 OID 16425)
-- Name: precios fk_id_tienda; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.precios
    ADD CONSTRAINT fk_id_tienda FOREIGN KEY (tienda_id) REFERENCES public.tiendas(id_tienda);


-- Completed on 2026-03-15 10:18:19

--
-- PostgreSQL database dump complete
--

\unrestrict RxWMczrokx5fPgxahNtJ4HHe0cFaUoXd7VIhxbOrpp6LqphxDTrr7VICJcq2Xtf

