# dynamic crud interface

:warning: Work in progress - Only backend service included


# setup dev env

## VS Code 

Install vscode and remote container extension. 

After that: F1 -> rebuild and reopen in container

## Install missing ressourcesr in Container
Install in container
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-test.txt
```

Activate pre commit chekcs:  ```pre-commit install```

## Testing

For testing I am currently using a wordpress instance. 
Here is the Docker Compose file

```
version: "3.9"

services:
  db:
    image: mysql:5.7
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: somewordpress
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress

  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    volumes:
      - wordpress_data:/var/www/html
    ports:
      - "8000:80"
    restart: always
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
volumes:
  db_data: {}
  wordpress_data: {}%
```