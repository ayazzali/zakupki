--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: notifications_pk; Type: SEQUENCE; Schema: public; Owner: roveo
--

CREATE SEQUENCE notifications_pk
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notifications_pk OWNER TO roveo;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: notifications; Type: TABLE; Schema: public; Owner: roveo; Tablespace: 
--

CREATE TABLE notifications (
    id bigint DEFAULT nextval('notifications_pk'::regclass) NOT NULL,
    rec_id bigint NOT NULL,
    notification_number character(19) NOT NULL,
    notification_type character(6),
    version_number integer,
    create_date timestamp without time zone,
    publish_date timestamp without time zone,
    placer_regnum character(11),
    placer_name text,
    order_name text,
    last_name text,
    first_name text,
    middle_name text,
    post_address text,
    email text,
    phone text,
    href text,
    print_form text,
    folder_name character(64)
);


ALTER TABLE public.notifications OWNER TO roveo;

--
-- Name: pk_notification_id; Type: CONSTRAINT; Schema: public; Owner: roveo; Tablespace: 
--

ALTER TABLE ONLY notifications
    ADD CONSTRAINT pk_notification_id PRIMARY KEY (id);


--
-- Name: ind_notification_publish_date; Type: INDEX; Schema: public; Owner: roveo; Tablespace: 
--

CREATE INDEX ind_notification_publish_date ON notifications USING btree (publish_date);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

