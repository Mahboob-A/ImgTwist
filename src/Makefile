
# ### Docker management commands 
 
docker-up: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml up --build -d --remove-orphans

docker-down: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml down

docker-down-v: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml down -v

docker-logs: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml logs 

docker-logs-imgtwist: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml logs dev-imgtwist-api

docker-restart-imgtwist: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml restart dev-imgtwist-api

docker-restart-nginx:
	docker compose -p dev_imgtwist_backend_api -f dev.yml restart nginx

docker-exec-imgtwist: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml exec dev-imgtwist-api /bin/bash 

docker-check-deploy-imgtwist:
	docker compose -p dev_imgtwist_backend_api -f dev.yml run --rm dev-imgtwist-api python manage.py check --deploy 

# ## 

# ### Docker Volume and Postgres Database 

docker-exec-pg: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml exec postgres /bin/bash 

docker-pgdb: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml exec postgres psql --username="$(POSTGRES_USER)" --dbname="$(POSTGRES_DB)" 

# ## 

# ### Services logs commands 

docker-logs-pg: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml logs postgres

# ## 


# ### Django Commands

makemigrations: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml run --rm dev-imgtwist-api python manage.py makemigrations

migrate: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml run --rm dev-imgtwist-api python manage.py migrate

collectstatic: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml run --rm dev-imgtwist-api python manage.py collectstatic --no-input --clear 

superuser: 
	docker compose -p dev_imgtwist_backend_api -f dev.yml run --rm dev-imgtwist-api python manage.py createsuperuser 

# ## 
