Multisite Test
==============

Example of multiple sites with one Django source.

This is just an example project to illustrate Django's multisite feature.


## Run local server

We use `docker-compose` to launch development server. The command is wrapped
inside `Makefile`, so you can just type:

```
$ make up
```

Then, open `http://127.0.0.1:8000` or `http://site1.local:8000` in the browser
to access the server. This makes you can see the contents of default site 1.
If you want to visit site 2, just try `http://site2.local:8000`. You can see
different contents depending on the address you typed.

If you want to re-build the docker images later, you can use another make
command.

```
$ make build
```
