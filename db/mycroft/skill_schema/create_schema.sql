-- create the schema that will be used to store user data
-- took out the "e" in "user" because "user" is a Postgres keyword
CREATE SCHEMA skill;
GRANT USAGE ON SCHEMA skill TO selene_crud;
GRANT USAGE ON SCHEMA skill to selene_view;
GRANT SELECT ON ALL TABLES IN SCHEMA skill TO selene_crud, selene_view;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA skill TO selene_crud;
