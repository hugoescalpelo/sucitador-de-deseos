# Configuración

En este documento encontrarás las instrucciones de configuracicón para realizar Sucitador de Deseos.

- Instala Raspberry Pi OS. Realiza el procesio de instalación de Raspberry Pi OS con la ayuda de la herramienta oficial [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/). Asegurate de agregar una conexión a internet y activar la comunicación SSH.
- Coloca la tarjeta de memoria en la Raspberry Pi.
- Conecta una pantalla, mouse y teclado y energiza la Raspberry Pi, arranca el sistema operativo, asegurate de tener conexión a Internet.
- Actualiza la raspberry pi con los siguientes comandos:
    ```
    sudo apt update
    sudo apt upgrade
    sudo reboot
    ```
- Instala Git en la terminal con el comando.
    ```
    sudo apt install git
    ```
- Crea una carpeta en Documentos y clona el repositorio con los siguientes comandos.
    ```
    cd ~/Documentos
    mkdir GitHub
    cd GitHub
    git clone https://github.com/hugoescalpelo/sucitador-de-deseos.git
    ```
- Comprueba que Pyhton esté instalado.
    ```
    python3 --version
    pip3 --version
    ```
- En caso de que no tengas python instaldo, instalo con los siguientes comandos:
    ```
    sudo apt install python3
    sudo apt install python3-pip
    ```
- Instala las dependencias de python para el programa con el siguiente comando:
    ```
    sudo apt install python3-full
    sudo apt install ffmpeg
    sudo apt install python3-venv
    python3 -m venv myenv
    source myenv/bin/activate
    sudo apt install build-essential python3-dev libasound2-dev
    sudo apt install libportaudio2 libportaudio-dev
    sudo apt install portaudio19-dev
    pip3 install gpiozero sounddevice pydub numpy simpleaudio datetime
    sudo pip3 install sounddevice --break-system-packages
    sudo pip3 install simpleaudio --break-system-packages
    sudo pip3 install pydub --break-system-packages
    ```
- Conecta el microfono USB y el botón en los pines GND y 4, no tienen polaridad.
- Prueba el programa 