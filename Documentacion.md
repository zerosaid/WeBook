# WeBook

## Equipo:

***SCRUM Master:***
Daniel Santiago Gonzalez Hernandez

***Equipo de desarrollo:***
Juan Andres Molina
Isabela Carrillo Azain
Joseph Stif Martinez
Juan Andres Montero
Karol Castaño







**Institución: Campus Lands.**
**Ciudad: Bucaramanga**
**Fecha 27/03/2025**



## Descripción breve del proyecto:
### SCRUM MINI-SPRINT: Desarrollo de una Red Social en Python

**Objetivo: Desarrollar una red social en Python con interfaz de consola, aplicando Scrum en un mini Sprint ágil.**

1. Contexto del Proyecto
  Se creará una red social para un nicho específico (gamers, lectores, programadores, etc.). El desarrollo seguirá un marco ágil con Scrum. Se usará Firebase para almacenar datos y librerías como Rich, Textual o Curses para la interfaz.
2. Organización del Equipo
Scrum Master: Facilita el proceso y resuelve impedimentos. Product Owner (Docente): Define los requerimientos. Desarrolladores (3-4) o 3 devs + 1 tester: Implementan y prueban el producto.
3. Fases del Mini-Sprint
  Sesión 1 - Planificación: Definir backlog, épicas e historias de usuario.
  Sesión 2 - Desarrollo: Implementación, Daily Scrum y pruebas.
  Sesión 3 - Revisión: Presentación, retrospectiva y entrega en GitHub.
4. Funcionalidades Clave
  Registro e inicio de sesión de usuarios. Publicaciones y visualización de posts. Interacción con publicaciones (likes y comentarios). Listado de usuarios registrados.
5. Historias de Usuario
Gestión de usuarios: Registro, login, listado de usuarios. Publicación de contenido: Crear, ver, dar "Me gusta" y comentar posts. Experiencia de usuario: Navegación sencilla y cierre de sesión.


6. Criterios de Aceptación
Implementar al menos 3 funcionalidades clave. Código modular y funcional en Python. Demostración en la Sprint Review. Reflexión sobre mejoras en la Retrospective.
7. Evaluación y Entrega
Se evaluará la planificación, ejecución, colaboración y presentación final.
Entrega en GitHub con código, documentación del proceso y presentación. Objetivo final: Aplicar Scrum en un desarrollo real, optimizando tiempos y mejorando la calidad del producto.




1. ### Introducción

  Este documento detalla la planificación y gestión del desarrollo de Webook, una red social para lectores, basada en metodologías ágiles. Se establecen épicas e historias de usuario que guiarán el trabajo del equipo de desarrollo.

2. ### Metodología SCRUM
  El desarrollo se llevará a cabo utilizando SCRUM, dividiendo el trabajo en sprints iterativos de 4 días. Se asignan tareas a los miembros del equipo y se realizan reuniones diarias de seguimiento (Daily Scrum).

3. ### Épicas e Historias de Usuario
  A continuación, se detallan las épicas e historias de usuario establecidas para el desarrollo de la red social Webook.

**Épica 1: Gestión de Usuarios**
Historia 1.1: Registro de Usuario
Descripción: Como usuario nuevo, quiero registrarme en la plataforma proporcionando mi nombre de usuario y contraseña, para poder acceder y participar en la red social.
Criterios de Aceptación:

- Debe existir un formulario de registro.
- El usuario debe ingresar un nombre único y una contraseña segura.
- Se debe validar que el nombre de usuario no esté repetido.
- Los datos deben ser almacenados en la base de datos.
Historia 1.2: Inicio de Sesión
Descripción: Como usuario registrado, quiero iniciar sesión con mis credenciales, para acceder a mi cuenta y realizar publicaciones.
Criterios de Aceptación:
- Debe existir un formulario de inicio de sesión.
- El usuario debe ingresar un nombre de usuario y contraseña válidos.
- Se debe verificar la autenticidad de las credenciales.
- Si la autenticación es exitosa, el usuario es redirigido a la página principal.
Historia 1.3: Listado de Usuarios
Descripción: Como usuario de la plataforma, quiero ver una lista de los usuarios registrados, para poder conectarse y conocer nuevas personas dentro de la red social.
Criterios de Aceptación:
- Se debe mostrar una lista de usuarios registrados.
- La información debe incluir nombre de usuario y avatar (si aplica).
- La lista debe actualizarse dinámicamente.

**Épica 2: Publicación de Contenidos**
Historia 2.1: Crear una Publicación
Descripción: Como usuario registrado, quiero publicar mensajes en la red social, para compartir mis pensamientos con otros usuarios.
Criterios de Aceptación:

- Debe existir un formulario para escribir y enviar publicaciones.
- El mensaje debe almacenarse en la base de datos.
- La publicación debe ser visible para otros usuarios en su feed.
Historia 2.2: Ver Publicaciones de Otros Usuarios
Descripción: Como usuario de la red social, quiero ver las publicaciones de otros usuarios, para mantenerse informado y conocer sus opiniones.
Criterios de Aceptación:
- Se debe mostrar un feed con publicaciones ordenadas cronológicamente.
- Las publicaciones deben incluir el nombre de usuario, contenido y fecha.
- Se debe actualizar en tiempo real cuando haya nuevas publicaciones.
Historia 2.3: Interactuar con Publicaciones (Me gusta)
Descripción: Como usuario de la red social, quiero poder dar "Me gusta" a las publicaciones, para mostrar mi apoyo o interés en un contenido.
Criterios de Aceptación:
- Cada publicación debe incluir un botón de "Me gusta".
- Al presionar el botón, se debe incrementar el contador de "Me gusta".
- Se debe registrar qué usuarios dieron "Me gusta".
Historia 2.4: Comentar en una Publicación
Descripción: Como usuario de la red social, quiero poder comentar en las publicaciones de otros usuarios, para interactuar y expresar mi opinión sobre los temas compartidos.
Criterios de Aceptación:
- Debe haber un formulario para ingresar comentarios.
- Los comentarios deben almacenarse en la base de datos.
- Los comentarios deben mostrarse debajo de cada publicación.

**Épica 3: Interfaz de Usuario y Experiencia**
Historia 3.1: Navegación en la Consola
Descripción: Como usuario de la red social, quiero navegar fácilmente a través de las opciones disponibles, para acceder a las funciones sin complicaciones.
Criterios de Aceptación:

- Debe existir un menú de navegación intuitivo.
- Todas las funciones principales deben ser accesibles con pocos clics.
- La interfaz debe ser responsiva.
Historia 3.2: Cierre de Sesión
Descripción: Como usuario registrado, quiero cerrar sesión en la red social, para asegurar que mi cuenta no sea utilizada sin mi autorización.
Criterios de Aceptación:
- Debe haber una opción para cerrar sesión.
- Al cerrar sesión, el usuario debe ser redirigido a la página de inicio.
- La sesión debe invalidarse en el servidor.




4. ### Roadmap y Priorización

  - Sprint 1 (Día 1): El sprint del día uno se realizó la implementación y funciones de registro de sesión y múltiples usuarios además de garantizar y asegurar la integridad de los datos en un database en la aplicación de Google Firebase además de que se desglosaron las demás tareas del backlog como el desarrollo de las publicaciones y comentarios.

  ![img](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdXd9lwLfjnGOo5UUohw7VsgdRyAb1evDxvLTVlniereh2rnEGeSpGwDp6pVsr3viMrLtUFsxQR8itQBRPiMkJjcxBfFdKKmFC7uktc255rapWs9cfoUb6WroKbFcnnq-5VXao3?key=h1-kAncZPAX5eDXZq6A6YVlg)

  - **Sprint 2 (Día 2):** En base a las historias de usuarios proporcionadas por el product owner se desarrollaron las funciones con especificaciones y deseos de los usuarios para garantizar la conformidad de los mismos además del desarrollo y optimización de las funciones principales las cuales son: “interfaz de usuario, visualización de inicio y salvaguardado de los datos en la nube”

    ![img](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfNeR-e3rL_s4A2C56AzrGc1kd9-nV9228cOtyBnimXuD-Ox_fcWaurS_jfStc95fMSIOVS8EyGpUJfr28Mk5Ihovy0evqTfcQQ-BGzntIeTfUNhbWTs4418wefsPgpMDnFgsEZ?key=h1-kAncZPAX5eDXZq6A6YVlg)

  - **Sprint 3 (Día 3):** Desarrollo de las interacciones en el apartados de comentarios comos lo son las respuestas a comentarios por la misma u otras cuentas de usuarios así como la reacción de dar me gusta a una publicación, además de agregar la función de lista de publicaciones para que todos los usuarios pudiesen ver el historial de comentarios y respuestas.

    <img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXeQskmeDyAX1bxhOPTT8MhQHbasEloDcRf6j5ahr1SaYE9xNSOTJv9oCWK0Zhp4upwTE02UBUZbZ1ZmcBbtXi5T2s-ucSUuiHsyw-UHwka5G4w1Oz_L-pS0W9vhVDZIUcpJL3usTg?key=h1-kAncZPAX5eDXZq6A6YVlg" alt="img" />

  - **Sprint 4 (Día 4):** Optimización de la experiencia del usuario acompañado de la encriptación de los datos en el archivo salvaguardado en la nube y pruebas finales.


Pantallazos de los desarrolladores con el código en su rama del github

