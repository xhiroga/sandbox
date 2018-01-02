-- Table: public.pgm_step_count

-- DROP TABLE public.pgm_step_count;

CREATE TABLE public.pgm_step_count
(
  create_timestamp timestamp with time zone NOT NULL,
  update_timestamp timestamp with time zone NOT NULL,
  delete_timestamp timestamp with time zone NOT NULL,
  user_id character varying NOT NULL,
  date date NOT NULL,
  count integer NOT NULL,
  CONSTRAINT pmg_step_count_pkey PRIMARY KEY (user_id, date),
  CONSTRAINT pmg_step_count_user_id_fkey FOREIGN KEY (user_id)
      REFERENCES public."user" (user_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.pgm_step_count
  OWNER TO hiroga;
