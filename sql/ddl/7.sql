-- Sequence: step_count_config.user_id_seq

-- DROP SEQUENCE step_count_config.user_id_seq;

CREATE SEQUENCE step_count_config.user_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE step_count_config.user_id_seq
  OWNER TO hiroga;

