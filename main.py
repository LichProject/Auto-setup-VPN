import threading

from config import vps_list
from core.ssh import SSH, SSHResult


def main():
    for vps in vps_list:
        threading.Thread(target=processing, args=(vps,)).start()

    input("Press ENTER to exit...\n\n")


def processing(vps):
    print(f"Now processing VPS: {vps['ip']} | Using RSA-key: {'yes' if vps['use_rsa_key'] is not None else 'no'}")
    client = SSH(vps['ip'], 'root', vps['password'], vps['use_rsa_key'])
    connection_result = client.connect()
    if connection_result is not SSHResult.NONE:
        print(f"[{vps['ip']}] Connection finished with error: {connection_result.name}")
        return
    create_result = client.create_vpn_script()
    if create_result is not SSHResult.NONE:
        print(f"[{vps['ip']}] Creating .sh script finished with error: {create_result.name}")
        return
    execute_result = client.execute()
    print(f"[{vps['ip']}] Executing script finished with {execute_result.name}")


if __name__ == '__main__':
    main()
