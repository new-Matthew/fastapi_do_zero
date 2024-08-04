psql:
SELECT * FROM contas_pagar_receber; para visualizar os dados do bd

p rodar o teste:
python -m pytest 




criar bd com docker:
docker run --name db_fastapidozero -p 5432:5432 -e POSTGRES_DB=db_fastapidozero -e POSTGRES_PASSWORD=162636 -d postgres

local:
docker run -d --name db_fastapidozero -p 5432:5432 -e POSTGRES_PASSWORD=162636 -v pgdata:/var/lib/postgresql/data postgres
