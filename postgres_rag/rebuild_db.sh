psql postgres://postgres:root@127.0.0.1:5432/template1 -c 'DROP DATABASE IF EXISTS django_rag;'
psql postgres://postgres:root@127.0.0.1:5432/template1 -c 'CREATE DATABASE django_rag;'
psql postgres://postgres:root@127.0.0.1:5432/django_rag -c 'CREATE EXTENSION IF NOT EXISTS vector;'
