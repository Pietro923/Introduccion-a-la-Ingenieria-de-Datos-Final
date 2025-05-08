# Docker Compose - Ejemplo 1

En este ejemplo se puede observar un `yaml` más completo. El mismo está compuesto de cuatro servicios para montar una página web usando nginx, mysql, postgres y pg_admin (gestor de bases de datos). También se declaran diferentes volúmenes utilizados para la persistencia de datos y de un network.

A su vez, cuando se inicializa postgress, el mismo levanta los scripts de dos bases de datos declarados en la carpeta `.init/`. 

Por último, este ejemplo utiliza un archivo `.env`para las diferentes variables que los servicios utilizan. 

## Cómo ejecutarlo
Iniciar los servicios
```bash
docker compose up -d
```
<!-- 
## Acceso a los servicios:
* Zabbix: http://localhost/zabbix
Usuario: Admin
Contraseña: zabbix
* Portainer: 
    * http://localhost/portainer
    * Crear credenciales en el primer inicio
* CheckMK: 
    * http://localhost/checkmk
    * Usuario: cmkadmin
    * Contraseña: cmk123

## Notas importantes:
1. Ajusta las contraseñas antes de implementar en producción
2. Considera agregar SSL para producción
3. Ajusta las zonas horarias según tu ubicación
4. Los volúmenes persistirán los datos
5. Asegúrate de tener suficientes recursos en tu máquina

## Para gestionar: -->

Otras instrucciones para gestionar a docker compose

Ver logs para identificar problemas
```bash
docker compose logs -f [servicio]
```
Reiniciar un servicio
```bash
docker compose restart [servicio]
```
Detener todo
```bash
docker compose down
```

Detener y eliminar volúmenes
```bash
docker compose down -v
```

Detener y eliminar todo
```bash
docker compose down --rmi all --volumes
```




