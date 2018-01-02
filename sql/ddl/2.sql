-- Sequence: public."PGM_STEP_COUNT_ID_seq"

-- DROP SEQUENCE public."PGM_STEP_COUNT_ID_seq";

CREATE SEQUENCE public."pgm_step_count_id_seq"
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE public."pgm_step_count_id_seq"
  OWNER TO hiroga;
