# back-switcher

## Sinopsis

El proyecto se titula **El Switcher**.

La aplicación web **Switcher** es una plataforma en línea que digitaliza el popular juego de mesa [El Switcher](https://maldon.com.ar/blog/projects/el-switcher/), proporcionando una experiencia de juego interactiva de hasta 4 jugadores online. Permite a los usuarios disfrutar del conocido juego de mesa en un formato virtual, simple y fiel al original.

## Requerimientos para montar la aplicación (back-end):

***Instalar la ultima version de Python y Pip***

```
sudo apt install python3 python3-pip
```

***Crear entorno virtual:***

```
python3 -m venv .venv
```

***Instalar dependencias:***

```
source .venv/bin/activate
```

```
python3 -m pip install -r requirements.txt
```

***Como correr el servidor:***

```
python3 -m uvicorn main:app --reload
```

***Para salir del entorno virutal:***

```
deactivate
```

***Correr test y coverage:***

```
coverage run -m pytest
```

```
coverage report
```

***Coverage como html:***

```
coverage html
```

```
firefox htmlcov/index.html
```
Utilizar junto a [front-switcher](https://github.com/AguilaMolinera/Switcher-Front)
