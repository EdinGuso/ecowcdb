# Installation Guide

1. Download VirtualBox from this [webpage](https://www.virtualbox.org/wiki/Downloads). The link to the version we used: [VirtualBox 7.0.6](https://download.virtualbox.org/virtualbox/7.0.6/VirtualBox-7.0.6-155176-Win.exe) (Windows executable).

2. Download Ubuntu from this [webpage](https://ubuntu.com/download/desktop). The link to the version we used: [Ubuntu 22.04.2 LTS](https://ubuntu.com/download/desktop/thank-you?version=22.04.2&architecture=amd64).

3. Create a new VM using VirtualBox.
    - Select the ISO Image you just downloaded. Make sure you check "Skip Unattended Installation", press Next.
    - After selecting the base memory (suggested: 8GB) and number of processors (suggested: 4), press Next.
    - Select "Create a Virtual Hard Disk Now" and allocate at least 25GB, press Next.
    - Press Finish and start your VM. Follow the Ubuntu installation steps.

4. Once the VM is installed, run the following commands:
    - ```sudo apt update && sudo apt upgrade -y```
    - ```sudo snap refresh```
    - ```sudo apt install python3-pip```
    - ```pip install numpy```
    - ```pip install tabulate```
    - ```pip install tqdm```
    - ```pip install scipy```

5. Clone the [panco repository](https://github.com/Huawei-Paris-Research-Center/panco). Go to the file ```panco-main/panco/lpSolvePath.py``` and replace line 14: ```LPSOLVEPATH = ["wsl", "lp_solve", "-s5"]``` with:

    ```
    import os.path
    LPSOLVEPATH = [os.path.join(os.path.dirname(__file__), 'lp_solve')]
    ```

6. Download lp_solve from this [webpage](https://sourceforge.net/projects/lpsolve/). The link to the version we used: [lp_solve 5.5.2.11](https://sourceforge.net/projects/lpsolve/files/lpsolve/5.5.2.11/lp_solve_5.5.2.11_exe_ux64.tar.gz/download).

7. Extract the files using by running this command ```tar -xf lp_solve_5.5.2.11_exe_ux64.tar.gz```. One of the extracted files is ```lp_solve```. Move/copy this file into this directory ```panco-main/panco/```.

8. Create a new directory ```panco-main/test/``` and create a file ```test.py```. Add the following lines to the start of the script:

    ```
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
    ```

9. Now you can use all the panco libraries by importing them in ```panco-main/test/test.py``` in the following format: ```from panco.X.Y import Z```.