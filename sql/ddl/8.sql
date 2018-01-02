-- Table: step_count_config."user"

-- DROP TABLE step_count_config."user";

CREATE TABLE step_count_config."user"
(
  create_timestamp timestamp with time zone NOT NULL,
  update_timestamp timestamp with time zone NOT NULL,
  delete_timestamp timestamp with time zone NOT NULL,
  id serial NOT NULL,
  userid character varying NOT NULL,
  CONSTRAINT user_pkey PRIMARY KEY (id),
  CONSTRAINT user_userid_key UNIQUE (userid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE step_count_config."user"
  OWNER TO hiroga;

