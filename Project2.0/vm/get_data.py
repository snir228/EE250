## Team Members
##- Steve Cho (USC ID: 4314516349)
##- Sivan Nir (USC ID: 7594069996)

import subprocess, os

RPI_USER     = "pi"
RPI_HOST     = "snir.local"        # or IP address e.g. "192.168.1.42"
RPI_PATH     = "~/EE250/Project2.0/rpi"
LOCAL_OUTPUT = "./rpi_output"

def fetch():
    os.makedirs(LOCAL_OUTPUT, exist_ok=True)

    # step 1 - SSH into Pi and run the sensor script
    print("Running sensor script on RPi...")
    ssh = subprocess.run([
        "ssh", f"{RPI_USER}@{RPI_HOST}",
        f"cd {RPI_PATH} && python3 test_suite.py"
    ], capture_output=True, text=True)
    print(ssh.stdout)
    if ssh.returncode != 0:
        print("SSH error:", ssh.stderr)
        return False

    # step 2 - copy output folder from Pi to VM
    print("Pulling files from RPi...")
    scp = subprocess.run([
        "scp", "-r",
        f"{RPI_USER}@{RPI_HOST}:{RPI_PATH}/output/",
        LOCAL_OUTPUT
    ], capture_output=True, text=True)
    if scp.returncode != 0:
        print("SCP error:", scp.stderr)
        return False

    print("Done! Files saved to", LOCAL_OUTPUT)
    return True

if __name__ == "__main__":
    fetch()
