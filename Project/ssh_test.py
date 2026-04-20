import paramiko, os

RPI_IP   = "172.20.10.3"
RPI_USER = "pi"
RPI_PASS = "000"
RPI_PATH = "/home/pi/EE250/Project"

def fetch():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(RPI_IP, username=RPI_USER, password=RPI_PASS)

    # run test_suite.py on the Pi
    print("Running sensor script on RPi...")
    stdin, stdout, stderr = ssh.exec_command(f"cd {RPI_PATH} && python3 test_suite.py")
    print(stdout.read().decode())
    err = stderr.read().decode()

    # pull data.csv from Pi to VM
    os.makedirs("./rpi_output", exist_ok=True)
    sftp = ssh.open_sftp()
    sftp.get(f"{RPI_PATH}/output/data.csv", "./rpi_output/data.csv")
    sftp.close()
    ssh.close()
    print("Done!")
    return True
