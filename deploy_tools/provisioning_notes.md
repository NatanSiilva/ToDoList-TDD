# Provisionamento de um novo site

## Pacotes necessários:

-   Nginx
-   Python 3.6
-   Git
-   virtualenv + pip

Exemplo no Ubuntu 16.04 LTS:

    sudo apt-get update
    sudo apt-get install nginx git python3.6 python3.6-venv

## Configuração do Nginx

-   Verifique se o arquivo de configuração do Nginx está na pasta /etc/nginx/sites-available
-   Se não estiver, crie um arquivo chamado 'superlists' na pasta /etc/nginx/sites-available
-   Se estiver, abra o arquivo e verifique se o conteúdo é igual ao abaixo:

```
server {
    listen 80;
    server_name superlists-staging.natandev.com.br www.superlists-staging.natandev.com.br;

    location /static {
        alias /home/deploy/sites/superlists-staging.natandev.com.br.conf/ToDoList-TDD/static;
    }

    location / {
        proxy_pass http://unix:/tmp/superlists-staging.natandev.com.br.conf.socket;
        proxy_set_header Host $host;
    }
}
```

-   Se o conteúdo for igual, pule para o próximo passo
-   Se o conteúdo for diferente, substitua o conteúdo pelo acima

-   Crie um link simbólico para o arquivo de configuração do Nginx na pasta /etc/nginx/sites-enabled
    sudo ln -s /etc/nginx/sites-available/superlists-staging.natandev.com.br.conf \
     /etc/nginx/sites-enabled/superlists-staging.natandev.com.br.conf

-   Reinicie o Nginx
    sudo systemctl reload nginx

## Configuração do Gunicorn

-   Crie um arquivo chamado 'gunicorn-superlists-staging.ottimizza.com.br' na pasta /etc/systemd/system
-   Abra o arquivo e verifique se o conteúdo é igual ao abaixo:

```
[Unit]
Description=Gunicorn server for superlists-staging.natandev.com.br

[Service]
Restart=on-failure
User=deploy
WorkingDirectory=/home/deploy/sites/superlists-staging.natandev.com.br.conf/ToDoList-TDD
ExecStart=/home/deploy/sites/superlists-staging.natandev.com.br.conf/ToDoList-TDD/venv/bin/gunicorn \
    --bind unix:/tmp/superlists-staging.natandev.com.br.conf.socket \
    superlists.wsgi:application

[Install]
WantedBy=multi-user.target
```

-   Se o conteúdo for igual, pule para o próximo passo
-   Se o conteúdo for diferente, substitua o conteúdo pelo acima

-   Inicie o serviço do Gunicorn
    sudo systemctl daemon-reload
    sudo systemctl enable gunicorn-superlists-staging.ottimizza.com.br
    sudo systemctl start gunicorn-superlists-staging.ottimizza.com.br
