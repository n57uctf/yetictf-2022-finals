#!/usr/bin/env bash
psql "postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST/$POSTGRES_DB?sslmode=disable" <<-EOSQL
--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE "user";
ALTER ROLE "user" WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'md50b48fb93e317aa444f910d5f4e6efbdb';

--
-- PostgreSQL database dump
--

-- Dumped from database version 12.10 (Debian 12.10-1.pgdg110+1)
-- Dumped by pg_dump version 12.10 (Debian 12.10-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: merc; Type: DATABASE; Schema: -; Owner: user
--

CREATE DATABASE merc WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE merc OWNER TO "user";

\connect merc

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: chat_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.chat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.chat_id_seq OWNER TO "user";

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chat; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.chat (
    id integer DEFAULT nextval('public.chat_id_seq'::regclass) NOT NULL,
    sender_id character varying(255) NOT NULL,
    receiver_id character varying(255) NOT NULL,
    message character varying(255) NOT NULL,
    timemark character varying(255) NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.chat OWNER TO "user";

--
-- Name: drivers_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.drivers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.drivers_id_seq OWNER TO "user";

--
-- Name: drivers; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.drivers (
    id integer DEFAULT nextval('public.drivers_id_seq'::regclass) NOT NULL,
    driver_id character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    vehicle character varying(255) NOT NULL,
    about character varying(255) NOT NULL,
    status integer NOT NULL
);


ALTER TABLE public.drivers OWNER TO "user";

--
-- Name: merchants_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.merchants_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.merchants_id_seq OWNER TO "user";

--
-- Name: merchants; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.merchants (
    id integer DEFAULT nextval('public.merchants_id_seq'::regclass) NOT NULL,
    name character varying(255) NOT NULL,
    passwd character varying(255) NOT NULL,
    merc_id character varying(255) NOT NULL
);


ALTER TABLE public.merchants OWNER TO "user";

--
-- Name: parsels_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.parsels_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.parsels_id_seq OWNER TO "user";

--
-- Name: parsels; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.parsels (
    id integer DEFAULT nextval('public.parsels_id_seq'::regclass) NOT NULL,
    dispatch character varying NOT NULL,
    destination character varying NOT NULL,
    note character varying NOT NULL,
    merc_id character varying NOT NULL,
    driver_id character varying NOT NULL
);


ALTER TABLE public.parsels OWNER TO "user";

--
-- Data for Name: chat; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.chat ("id", "sender_id", "receiver_id", "message", "timemark", "name") VALUES
(1,	'KlN1Z2FyTWFuODgq',	'627ebaa29fe01cabd6ef622abcdf56f2',	'as always',	'08:15',	'KlN1Z2FyTWFuODgq');



--
-- Data for Name: drivers; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.drivers ("id", "driver_id", "name", "vehicle", "about", "status") VALUES
(1,	'627ebaa29fe01cabd6ef622abcdf56f2',	'Crockett',	'Fiberglass Boat',	'Delivers controlled substances faster than Fed Ex',	1),
(2,	'33e867ce5904b38c71664136474f0b49',	'Jo Amon',	'Any',	'Seems like a reasonable dude',	1),
(3,	'1b4e0a8ddc5d8afb2c238e06d1d2b7d0',	'FamilyMan',	'Dodge Challenger',	'A man who values his family the most',	1),
(4,	'0f6e870c59d53be2d8ce191a8c43ac25',	'Fuji',	'Corolla 86',	'Dorifto master, uses it to deliver tofu in style',	1),
(5,	'e90a4a810492b4d6acf5b042244f4b9f',	'Ryan',	'Chevy Impala',	'He drives',	1),
(6,	'cd61c621710cef4c3f10abaf7f800211',	'Trevor',	'Generic NY Cab',	'Vietnam veteran, can provide protection for your cargo from all kinds of scum',	1),
(7,	'03b978c06502cb9c75aa1e4e6f378d10',	'Hamous',	'Ice Cream Truck',	'Has a merc cred for throwing down dictatorships in third world countries',	0);



--
-- Data for Name: merchants; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.merchants ("id", "name", "passwd", "merc_id") VALUES
(1,	'Garold',	'827ccb0eea8a706c4c34a16891f84e7b',	'R2Fyb2xk'),
(2,	'*SugarMan88*',	'2b43cb3825b6c627860e003c043eaf8e',	'KlN1Z2FyTWFuODgq');


--
-- Data for Name: parsels; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public.parsels ("id", "dispatch", "destination", "note", "merc_id", "driver_id") VALUES
(1,	'East London',	'Johannesburg',	'as always',	'KlN1Z2FyTWFuODgq',	'627ebaa29fe01cabd6ef622abcdf56f2');



--
-- Name: chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.chat_id_seq', 1, false);


--
-- Name: drivers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.drivers_id_seq', 1, false);


--
-- Name: merchants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.merchants_id_seq', 1, false);


--
-- Name: parsels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.parsels_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 12.10 (Debian 12.10-1.pgdg110+1)
-- Dumped by pg_dump version 12.10 (Debian 12.10-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--
EOSQL
