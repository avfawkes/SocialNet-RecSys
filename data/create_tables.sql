DROP TABLE IF EXISTS user_data;

CREATE TABLE IF NOT EXISTS user_data
(
    user_id integer NOT NULL,
    gender smallint,
    age smallint,
    country character varying(25),
    city character varying(30),
    exp_group smallint,
    os character varying(15),
    source character varying(15),
    CONSTRAINT user_data_pkey PRIMARY KEY (user_id)
);

DROP TABLE IF EXISTS post_text_df;

CREATE TABLE IF NOT EXISTS post_text_df
(
    post_id smallint NOT NULL,
    text text,
    topic character varying(50),
    CONSTRAINT post_text_df_pkey PRIMARY KEY (post_id)
 );
 
 DROP TABLE IF EXISTS feed_data;
 
 CREATE TABLE IF NOT EXISTS feed_data
(
    "timestamp" timestamp without time zone,
    user_id integer,
    post_id smallint,
    action character varying(15),
    target smallint,
    CONSTRAINT post_id FOREIGN KEY (post_id)
        REFERENCES post_text_df (post_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES user_data (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)