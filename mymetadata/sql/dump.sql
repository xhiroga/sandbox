--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: hiroga
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: step_count_config; Type: SCHEMA; Schema: -; Owner: hiroga
--

CREATE SCHEMA step_count_config;


ALTER SCHEMA step_count_config OWNER TO hiroga;

--
-- Name: SCHEMA step_count_config; Type: COMMENT; Schema: -; Owner: hiroga
--

COMMENT ON SCHEMA step_count_config IS 'プログラムのステップ計測プログラムの設定スキーマ';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: pgm_step_count; Type: TABLE; Schema: public; Owner: hiroga
--

CREATE TABLE pgm_step_count (
    create_timestamp timestamp with time zone NOT NULL,
    update_timestamp timestamp with time zone NOT NULL,
    delete_timestamp timestamp with time zone NOT NULL,
    user_id character varying NOT NULL,
    date date NOT NULL,
    count integer NOT NULL
);


ALTER TABLE pgm_step_count OWNER TO hiroga;

--
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: hiroga
--

CREATE SEQUENCE user_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_user_id_seq OWNER TO hiroga;

--
-- Name: user; Type: TABLE; Schema: public; Owner: hiroga
--

CREATE TABLE "user" (
    create_timestamp timestamp with time zone,
    update_timestamp timestamp with time zone,
    delete_timestamp timestamp with time zone,
    id integer DEFAULT nextval('user_user_id_seq'::regclass) NOT NULL,
    user_id character varying NOT NULL
);


ALTER TABLE "user" OWNER TO hiroga;

SET search_path = step_count_config, pg_catalog;

--
-- Name: user; Type: TABLE; Schema: step_count_config; Owner: hiroga
--

CREATE TABLE "user" (
    create_timestamp timestamp with time zone NOT NULL,
    update_timestamp timestamp with time zone NOT NULL,
    delete_timestamp timestamp with time zone NOT NULL,
    id integer NOT NULL,
    userid character varying NOT NULL
);


ALTER TABLE "user" OWNER TO hiroga;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: step_count_config; Owner: hiroga
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_id_seq OWNER TO hiroga;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: step_count_config; Owner: hiroga
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: watch_repositories; Type: TABLE; Schema: step_count_config; Owner: hiroga
--

CREATE TABLE watch_repositories (
    create_timestamp timestamp with time zone NOT NULL,
    update_timestamp timestamp with time zone NOT NULL,
    delete_timestamp timestamp with time zone NOT NULL,
    userid character varying NOT NULL,
    repo_owner character varying NOT NULL,
    repo_name character varying NOT NULL
);


ALTER TABLE watch_repositories OWNER TO hiroga;

--
-- Name: user id; Type: DEFAULT; Schema: step_count_config; Owner: hiroga
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


SET search_path = public, pg_catalog;

--
-- Data for Name: pgm_step_count; Type: TABLE DATA; Schema: public; Owner: hiroga
--

COPY pgm_step_count (create_timestamp, update_timestamp, delete_timestamp, user_id, date, count) FROM stdin;
2018-01-02 10:48:09.900076+00	2018-01-02 10:48:09.900076+00	infinity	hiroga-cc	2017-12-31	0
2018-01-07 00:01:15.287122+00	2018-01-07 00:01:15.287122+00	infinity	hiroga-cc	2018-01-07	63
2018-01-03 07:47:11.280727+00	2018-01-03 07:47:11.280727+00	infinity	hiroga-cc	2017-12-25	0
2018-01-03 07:46:37.144165+00	2018-01-03 07:46:37.144165+00	infinity	hiroga-cc	2017-12-26	0
2018-01-03 07:39:56.79356+00	2018-01-03 07:39:56.79356+00	infinity	hiroga-cc	2018-01-01	0
2018-01-02 13:11:10.155002+00	2018-01-02 13:11:10.155002+00	infinity	hiroga-cc	2018-01-02	305
2018-01-03 07:00:26.294931+00	2018-01-03 07:00:26.294931+00	infinity	hiroga-cc	2018-01-03	133
2018-01-04 13:14:14.933693+00	2018-01-04 13:14:14.933693+00	infinity	hiroga-cc	2018-01-04	0
2018-01-05 13:14:14.842282+00	2018-01-05 13:14:14.842282+00	infinity	hiroga-cc	2018-01-05	0
2018-01-06 00:01:14.769908+00	2018-01-06 00:01:14.769908+00	infinity	hiroga-cc	2018-01-06	0
2018-01-03 07:42:34.601042+00	2018-01-03 07:42:34.601042+00	infinity	hiroga-cc	2018-01-13	0
2018-01-03 07:35:42.152791+00	2018-01-03 07:35:42.152791+00	infinity	hiroga-cc	2017-01-01	0
2018-01-07 01:11:19.174948+00	2018-01-07 01:11:19.174948+00	infinity	hiroga-cc	2017-01-02	0
2018-01-07 01:11:25.653852+00	2018-01-07 01:11:25.653852+00	infinity	hiroga-cc	2017-01-03	0
2018-01-07 01:11:32.462608+00	2018-01-07 01:11:32.462608+00	infinity	hiroga-cc	2017-01-04	0
2018-01-07 01:11:39.22831+00	2018-01-07 01:11:39.22831+00	infinity	hiroga-cc	2017-01-05	0
2018-01-07 01:11:45.942602+00	2018-01-07 01:11:45.942602+00	infinity	hiroga-cc	2017-01-06	0
2018-01-07 01:11:52.722534+00	2018-01-07 01:11:52.722534+00	infinity	hiroga-cc	2017-01-07	0
2018-01-07 01:13:04.156373+00	2018-01-07 01:13:04.156373+00	infinity	hiroga-cc	2017-01-08	0
2018-01-02 11:41:59.12274+00	2018-01-02 11:41:59.12274+00	infinity	hiroga-cc	2017-12-27	0
2018-01-03 07:45:31.953945+00	2018-01-03 07:45:31.953945+00	infinity	hiroga-cc	2017-12-28	0
2018-01-03 07:45:13.842724+00	2018-01-03 07:45:13.842724+00	infinity	hiroga-cc	2017-12-29	0
2018-01-02 11:00:57.370574+00	2018-01-02 11:00:57.370574+00	infinity	hiroga-cc	2017-12-30	0
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: hiroga
--

COPY "user" (create_timestamp, update_timestamp, delete_timestamp, id, user_id) FROM stdin;
2018-01-01 23:58:45.108893+00	2018-01-01 23:58:45.108893+00	infinity	1	hiroga-cc
\.


--
-- Name: user_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hiroga
--

SELECT pg_catalog.setval('user_user_id_seq', 1, true);


SET search_path = step_count_config, pg_catalog;

--
-- Data for Name: user; Type: TABLE DATA; Schema: step_count_config; Owner: hiroga
--

COPY "user" (create_timestamp, update_timestamp, delete_timestamp, id, userid) FROM stdin;
2018-01-02 00:42:29.397506+00	2018-01-02 00:42:29.397506+00	infinity	1	hiroga-cc
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: step_count_config; Owner: hiroga
--

SELECT pg_catalog.setval('user_id_seq', 1, false);


--
-- Data for Name: watch_repositories; Type: TABLE DATA; Schema: step_count_config; Owner: hiroga
--

COPY watch_repositories (create_timestamp, update_timestamp, delete_timestamp, userid, repo_owner, repo_name) FROM stdin;
2018-01-02 00:43:30.0998+00	2018-01-02 00:43:30.0998+00	infinity	hiroga-cc	hiroga-cc	yukicoder
2018-01-02 00:43:39.405359+00	2018-01-02 00:43:39.405359+00	infinity	hiroga-cc	hiroga-cc	atcoder
2018-01-03 07:41:28.446137+00	2018-01-03 07:41:28.446137+00	infinity	hiroga-cc	hiroga-cc	mymetadata
2018-01-07 01:54:21.343403+00	2018-01-07 01:54:21.343403+00	infinity	hiroga-cc	hiroga-cc	courseraMLpy
2018-01-07 01:54:35.123141+00	2018-01-07 01:54:35.123141+00	infinity	hiroga-cc	hiroga-cc	utilis_cc
\.


SET search_path = public, pg_catalog;

--
-- Name: user USER_pkey; Type: CONSTRAINT; Schema: public; Owner: hiroga
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT "USER_pkey" PRIMARY KEY (id);


--
-- Name: pgm_step_count pmg_step_count_pkey; Type: CONSTRAINT; Schema: public; Owner: hiroga
--

ALTER TABLE ONLY pgm_step_count
    ADD CONSTRAINT pmg_step_count_pkey PRIMARY KEY (user_id, date);


--
-- Name: user user_user_id_key; Type: CONSTRAINT; Schema: public; Owner: hiroga
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_user_id_key UNIQUE (user_id);


SET search_path = step_count_config, pg_catalog;

--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: step_count_config; Owner: hiroga
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_userid_key; Type: CONSTRAINT; Schema: step_count_config; Owner: hiroga
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_userid_key UNIQUE (userid);


--
-- Name: watch_repositories watch_repositories_pkey; Type: CONSTRAINT; Schema: step_count_config; Owner: hiroga
--

ALTER TABLE ONLY watch_repositories
    ADD CONSTRAINT watch_repositories_pkey PRIMARY KEY (userid, repo_owner, repo_name);


SET search_path = public, pg_catalog;

--
-- Name: pgm_step_count pmg_step_count_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hiroga
--

ALTER TABLE ONLY pgm_step_count
    ADD CONSTRAINT pmg_step_count_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(user_id);


SET search_path = step_count_config, pg_catalog;

--
-- Name: watch_repositories watch_repositories_userid_fkey; Type: FK CONSTRAINT; Schema: step_count_config; Owner: hiroga
--

ALTER TABLE ONLY watch_repositories
    ADD CONSTRAINT watch_repositories_userid_fkey FOREIGN KEY (userid) REFERENCES "user"(userid);


--
-- Name: public; Type: ACL; Schema: -; Owner: hiroga
--

REVOKE ALL ON SCHEMA public FROM rdsadmin;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO hiroga;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

