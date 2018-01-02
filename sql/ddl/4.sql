-- Table: public."PGM_STEP_COUNT"

-- DROP TABLE public."PGM_STEP_COUNT";

CREATE TABLE public."pgm_step_count"
(
  "create_timestamp" timestamp with time zone,
  "update_timestamp" timestamp with time zone,
  "delete_timestamp" timestamp with time zone,
  "id" integer NOT NULL DEFAULT nextval('"pgm_step_count_id_seq"'::regclass),
  "user_id" integer,
  "date" date,
  "step_count" integer,
  CONSTRAINT "pgm_step_count_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "pgm_step_count_user_ID_fkey" FOREIGN KEY ("user_id")
      REFERENCES public."user" ("user_id") MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public."pgm_step_count"
  OWNER TO hiroga;
COMMENT ON TABLE public."pgm_step_count"
  IS 'ユーザーごとの1日に書いたプログラムのステップ数';

