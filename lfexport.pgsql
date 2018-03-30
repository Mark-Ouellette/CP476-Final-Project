--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: ingredients_ingredientid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ingredients_ingredientid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ingredients_ingredientid_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: ingredients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingredients (
    ingredientid integer DEFAULT nextval('public.ingredients_ingredientid_seq'::regclass) NOT NULL,
    ingredientname character varying(40)
);


ALTER TABLE public.ingredients OWNER TO postgres;

--
-- Name: ingredientsPerRecipe; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ingredientsPerRecipe" (
    recipeid integer NOT NULL,
    ingredientid integer NOT NULL
);


ALTER TABLE public."ingredientsPerRecipe" OWNER TO postgres;

--
-- Name: recipes_recipeid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.recipes_recipeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_recipeid_seq OWNER TO postgres;

--
-- Name: recipes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recipes (
    recipeid integer DEFAULT nextval('public.recipes_recipeid_seq'::regclass) NOT NULL,
    authorid integer,
    recipedate date NOT NULL,
    recipedesc text,
    recipetitle character varying(100)
);


ALTER TABLE public.recipes OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    uid integer NOT NULL,
    firstname character varying(100),
    lastname character varying(100),
    email character varying(120),
    pwdhash character varying(100)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_uid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_uid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_uid_seq OWNER TO postgres;

--
-- Name: users_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_uid_seq OWNED BY public.users.uid;


--
-- Name: users uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN uid SET DEFAULT nextval('public.users_uid_seq'::regclass);


--
-- Data for Name: ingredients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ingredients (ingredientid, ingredientname) FROM stdin;
1	Whisky
2	Vodka
9	Bourbon
11	Scotch
14	Rum
\.


--
-- Data for Name: ingredientsPerRecipe; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ingredientsPerRecipe" (recipeid, ingredientid) FROM stdin;
\.


--
-- Data for Name: recipes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.recipes (recipeid, authorid, recipedate, recipedesc, recipetitle) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (uid, firstname, lastname, email, pwdhash) FROM stdin;
1	Hello	World	hello@world.com	pbkdf2:sha256:50000$Mvhntipb$8c3f12e3ef0c089219d92e44c6e7ef22dd4f0edd06ee2b020f0a7b30410242ee
3	Dalton	Dranitsaris	test@example.com	pbkdf2:sha256:50000$uNbBGJDl$2166fd07b6aec70789bd74f2f0276c7a3a7b7018d1b726e2e4c75dbba373dd10
4	Me	User	me@example.com	pbkdf2:sha256:50000$LAt0PbfO$2a932013d90901d63fc361f048b05c305e532479501ff44999c3a2bb4bb3ddbc
6	Me	User	me2@example.com	pbkdf2:sha256:50000$FZHsFjpO$8db46461bb5125af6c302044391facb21c5e20f0c13e0386fb7bf88d9f481b82
7	Kieth	Kinkaid	kieth.kinkaid@gmail.com	pbkdf2:sha256:50000$kFaz1fN3$db2aec25a0e8d1f07dba54175e46c0b1a193715d619ed701c016a20c4aac3428
8	Mikey	Roher	mikey.roher@example.com	pbkdf2:sha256:50000$9tJfFne5$cff407501e9e9afe926afb3d562c01bafc816f21a5c7966bcc59e5c3eac84997
\.


--
-- Name: ingredients_ingredientid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingredients_ingredientid_seq', 14, true);


--
-- Name: recipes_recipeid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.recipes_recipeid_seq', 1, false);


--
-- Name: users_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_uid_seq', 8, true);


--
-- Name: ingredientsPerRecipe ingredientsPerRecipe_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ingredientsPerRecipe"
    ADD CONSTRAINT "ingredientsPerRecipe_pkey" PRIMARY KEY (recipeid, ingredientid);


--
-- Name: ingredients ingredients_ingredientname_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_ingredientname_key UNIQUE (ingredientname);


--
-- Name: ingredients ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_pkey PRIMARY KEY (ingredientid);


--
-- Name: recipes recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (recipeid);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uid);


--
-- Name: uid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX uid ON public.recipes USING btree (authorid);


--
-- Name: ingredientsPerRecipe ingredientsPerRecipe_recipeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ingredientsPerRecipe"
    ADD CONSTRAINT "ingredientsPerRecipe_recipeid_fkey" FOREIGN KEY (recipeid) REFERENCES public.recipes(recipeid) ON DELETE CASCADE;


--
-- Name: ingredientsPerRecipe ingredientsPerRecipe_recipeid_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ingredientsPerRecipe"
    ADD CONSTRAINT "ingredientsPerRecipe_recipeid_fkey1" FOREIGN KEY (recipeid) REFERENCES public.ingredients(ingredientid) ON DELETE CASCADE;


--
-- Name: recipes recipes_authorid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_authorid_fkey FOREIGN KEY (authorid) REFERENCES public.users(uid);


--
-- PostgreSQL database dump complete
--

