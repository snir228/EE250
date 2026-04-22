import paramiko, os

RPI_IP   = "172.20.10.3"
RPI_USER = "pi"
RPI_PASS = "000"
RPI_PATH = "/home/pi/EE250/ee250_final_project"

# ssh connection using paramiko
def fetch():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # automatically accept any host key
    ssh.connect(RPI_IP, username=RPI_USER, password=RPI_PASS)

    # run rpi.py on the Pi
    print("Running sensor script on RPi...")
    _, stdout, _ = ssh.exec_command(f"cd {RPI_PATH} && python3 rpi.py")
    print(stdout.read().decode())

    # pull data.csv from Pi to Laptop
    os.makedirs("./rpi_output", exist_ok=True)
    sftp = ssh.open_sftp()
    sftp.get(f"{RPI_PATH}/output/data.csv", "./rpi_output/data.csv")
    sftp.close()
    ssh.close()
    print("Done!")
    return True
