-- Table: step_count_config.watch_repositories

-- DROP TABLE step_count_config.watch_repositories;

CREATE TABLE step_count_config.watch_repositories
(
  create_timestamp timestamp with time zone NOT NULL,
  update_timestamp timestamp with time zone NOT NULL,
  delete_timestamp timestamp with time zone NOT NULL,
  userid character varying NOT NULL,
  repo_owner character varying NOT NULL,
  repo_name character varying NOT NULL,
  CONSTRAINT watch_repositories_pkey PRIMARY KEY (userid, repo_owner, repo_name),
  CONSTRAINT watch_repositories_userid_fkey FOREIGN KEY (userid)
      REFERENCES step_count_config."user" (userid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE step_count_config.watch_repositories
  OWNER TO hiroga;

