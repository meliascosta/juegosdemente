# Instrucciones de Instalación #
Las instrucciones siguientes son para usuarios de Ubuntu (o Debian). Si tenés otra distribución de Linux, deberían ser similares. Si no tenés linux, empezá por arreglar ese error, ;)

### 0) Requisitos ###
  * svn: `sudo apt-get install subversion`
  * Python: `sudo apt-get install python python-imaging`
  * MySQL: `sudo apt-get install mysql-server python-mysqldb`

### 1) Instalar Django http://www.djangoproject.com/download/ ###
```
wget http://www.djangoproject.com/download/1.2.3/tarball/ -O Django-1.2.3.tar.gz
tar xzvf Django-1.2.3.tar.gz
cd Django-1.2.3
sudo python setup.py install
```

### 2) Descargar el código del server Django http://code.google.com/p/juegosdemente/source/checkout ###
```
svn checkout http://juegosdemente.googlecode.com/svn/trunk/ juegosdemente
```

### 3) Ir a la carpeta de juegosdemente ###
```
cd juegosdemente
```

### 4) Editar el archivo common\_settings.py con la configuracion de MySQL (en la carpeta juegosdemente) ###
Cambiar las líneas de database para que queden así (o el equivalente a tu configuración)
```
DATABASE_ENGINE = 'mysql' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'labgamesdb'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
```

### 5) Crear la base de datos para guardar los datos de los juegos (labgamesdb) ###
```
mysql -uroot
CREATE DATABASE labgamesdb;
exit
```

### 6) Crear la estructura de la base de datos ###
```
python manage.py syncdb --settings settings_main_site
python manage.py syncdb --settings settings_games_site
```

### 7) Iniciar el servidor ###
```
./scripts/start_games.sh
```

### 8) Abrir en un navegador la aplicación: http://localhost:8080/ ###
Y disfrutar, ;)