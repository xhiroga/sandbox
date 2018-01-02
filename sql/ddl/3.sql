-- Table: public."USER"

-- DROP TABLE public."USER";

CREATE TABLE public."user"
(
  "create_timestamp" timestamp with time zone,
  "update_timestamp" timestamp with time zone,
  "delete_timestamp" timestamp with time zone,
  "user_id" integer NOT NULL DEFAULT nextval('"user_user_id_seq"'::regclass),
  CONSTRAINT "USER_pkey" PRIMARY KEY ("user_id")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public."user"
  OWNER TO hiroga;

