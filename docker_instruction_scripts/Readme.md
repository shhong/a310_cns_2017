## Installing NEURON via docker

1. Install Docker ([for macOS](https://docs.docker.com/docker-for-mac/), [Windows](https://docs.docker.com/docker-for-windows/), and [ArchLinux](https://docs.docker.com/engine/installation/linux/archlinux/)).

2. Start Docker.

3. In Windows, also [turn on drive sharing](https://rominirani.com/docker-on-windows-mounting-host-directories-d96f3f056a2c#.w4v0e42tn).

4. Download the docker image by entering the following in a terminal (PowerShell in Windows).

   ```shell
   docker pull shhongoist/headless-vnc-neuron
   ```

5. Download [start.sh](https://raw.githubusercontent.com/shhong/a310_cns_2017/master/docker_instruction_scripts/start.sh) (or [start.ps1](https://raw.githubusercontent.com/shhong/a310_cns_2017/master/docker_instruction_scripts/start.ps1) in Windows) and run it by

   ~~~shell
   ./start
   ~~~

6. Open [http://localhost:6901/vnc_auto.html?password=vncpassword](http://localhost:6901/vnc_auto.html?password=vncpassword).

7. Open a terminal (Top menu → Applications → Terminal Emulator)

8. Check if NEURON runs

   ~~~shell
   nrngui -python
   ~~~




By default, the directory that contains the start script is mounted at `/root/Documents`. If you want to change this, edit the start script and change ${PWD} to a local directory you want to use, etc.

Also The size of the desktop is 1360x768. If you want to change this, change `VNC_RESOLUTION=1360x768` in the start script to whichever size you want.

