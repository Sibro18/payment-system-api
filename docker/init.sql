CREATE USER compendium_user WITH PASSWORD '1234567890';
CREATE DATABASE test_task_db OWNER compendium_user;

GRANT ALL PRIVILEGES ON DATABASE test_task_db TO compendium_user;
