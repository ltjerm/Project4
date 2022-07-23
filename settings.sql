-- settings.sql
CREATE DATABASE munch;
CREATE USER munchuser WITH PASSWORD 'munch';
GRANT ALL PRIVILEGES ON DATABASE munch TO munchuser;