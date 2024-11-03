import os
import platform
import psutil
from datetime import datetime
import subprocess

def get_network_information():
    network_info = {}

    # Network interfaces and configurations
    network_info['Network Interfaces'] = get_network_interfaces()

    # Open ports and listening services
    network_info['Open Ports'] = get_open_ports()

    # Connected devices in the local network
    network_info['Connected Devices'] = scan_local_network()

    return network_info

def get_network_interfaces():
    interfaces = psutil.net_if_addrs()
    interface_info = {}
    for interface, addrs in interfaces.items():
        addr_info = []
        for addr in addrs:
            addr_info.append({
                'family': addr.family,
                'address': addr.address,
                'netmask': addr.netmask,
                'broadcast': addr.broadcast
            })
        interface_info[interface] = addr_info
    return interface_info

def get_open_ports():
    open_ports = []
    try:
        with subprocess.Popen(['netstat', '-an'], stdout=subprocess.PIPE, text=True) as proc:
            netstat_output = proc.stdout.readlines()
            for line in netstat_output:
                parts = line.split()
                if len(parts) == 4 and parts[1] == 'TCP' and parts[3] == 'LISTENING':
                    open_ports.append(int(parts[2].split(':')[-1]))
    except Exception as e:
        print(f"Error retrieving open ports: {e}")
    return open_ports

def scan_local_network():
    connected_devices = []
    try:
        with subprocess.Popen(['arp', '-a'], stdout=subprocess.PIPE, text=True) as proc:
            arp_output = proc.stdout.readlines()
            for line in arp_output[3:]:
                parts = line.split()
                if len(parts) == 3:
                    connected_devices.append({
                        'IP Address': parts[0],
                        'MAC Address': parts[1],
                        'Type': parts[2]
                    })
    except Exception as e:
        print(f"Error scanning local network: {e}")
    return connected_devices

def check_file_permissions(file_path):
    try:
        os.stat(file_path)
        return os.access(file_path, os.R_OK)
    except Exception as e:
        print(f"Error checking file permissions for {file_path}: {e}")
        return False

def check_folder_permissions(folder_path):
    try:
        os.listdir(folder_path)
        return os.access(folder_path, os.R_OK)
    except Exception as e:
        print(f"Error checking folder permissions for {folder_path}: {e}")
        return False

def get_system_information():
    system_info = {}

    # Basic system information
    system_info['System'] = platform.system()
    system_info['Node Name'] = platform.node()
    system_info['Release'] = platform.release()
    system_info['Version'] = platform.version()
    system_info['Machine'] = platform.machine()
    system_info['Processor'] = platform.processor()

    # CPU information
    cpu_info = {}
    cpu_info['Physical Cores'] = psutil.cpu_count(logical=False)
    cpu_info['Total Cores'] = psutil.cpu_count(logical=True)
    cpu_info['CPU Usage (%)'] = psutil.cpu_percent(interval=1)
    system_info['CPU Info'] = cpu_info

    # Memory information
    mem_info = {}
    mem = psutil.virtual_memory()
    mem_info['Total Memory (GB)'] = round(mem.total / (1024 ** 3), 2)
    mem_info['Used Memory (GB)'] = round(mem.used / (1024 ** 3), 2)
    mem_info['Free Memory (GB)'] = round(mem.free / (1024 ** 3), 2)
    system_info['Memory Info'] = mem_info

    # Network information
    system_info['Network Info'] = get_network_information()

    # Disk information
    disk_info = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_info = psutil.disk_usage(partition.mountpoint)
        disk_info[partition.device] = {
            'Total Size (GB)': round(partition_info.total / (1024 ** 3), 2),
            'Used Space (GB)': round(partition_info.used / (1024 ** 3), 2),
            'Free Space (GB)': round(partition_info.free / (1024 ** 3), 2)
        }
    system_info['Disk Info'] = disk_info

    # Software information
    software_info = {}
    software_info['Installed Software'] = get_installed_software()
    system_info['Software Info'] = software_info

    # Security and Compliance checks
    system_info['Security Checks'] = run_security_checks()

    # System time
    system_info['Current Time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return system_info

def get_installed_software():
    installed_software = []
    try:
        with subprocess.Popen(['wmic', 'product', 'get', 'name'], stdout=subprocess.PIPE, text=True) as proc:
            installed_software = proc.stdout.readlines()[1:]
    except Exception as e:
        print(f"Error retrieving installed software: {e}")

    return [software.strip() for software in installed_software]

def run_security_checks():
    security_checks = {}

    # Example security checks
    security_checks['User Accounts'] = check_user_accounts()
    security_checks['Password Policies'] = check_password_policies()

    # Additional security checks can be added here

    return security_checks

def check_user_accounts():
    # Check for specific user accounts
    suspicious_users = ['admin', 'testuser']
    users = psutil.users()
    return any(user.name.lower() in suspicious_users for user in users)

def check_password_policies():
    # Check Windows password policy
    try:
        result = subprocess.check_output(['net', 'accounts'], universal_newlines=True)
        return 'Minimum password length:' in result and 'Minimum password age:' in result
    except subprocess.CalledProcessError as e:
        print(f"Error checking password policies: {e}")
        return 'Not Available'

def print_system_information(system_info):
    print("\nSystem Information:")
    for key, value in system_info.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for sub_k, sub_v in v.items():
                        print(f"    {sub_k}: {sub_v}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")

if _name_ == "_main_":
    # Example usage
    file_to_check = r'D:\HP 840 g3\Certificates\Python Certificate.pdf'  # Replace with the actual file path
    folder_to_check = r'D:\HP 840 g3\Certificates'  # Replace with the actual folder path

    if os.path.isfile(file_to_check):
        if check_file_permissions(file_to_check):
            print(f"The file '{file_to_check}' can be accessed based on permissions.")
        else:
            print(f"The file '{file_to_check}' cannot be accessed due to insufficient permissions.")
    else:
        print(f"The specified path '{file_to_check}' is not a valid file.")

    if os.path.isdir(folder_to_check):
        if check_folder_permissions(folder_to_check):
            print(f"The folder '{folder_to_check}' can be accessed based on permissions.")
        else:
            print(f"The folder '{folder_to_check}' cannot be accessed due to insufficient permissions.")
    else:
        print(f"The specified path '{folder_to_check}' is not a valid folder.")

    # System information
    system_info = get_system_information()
    print_system_information(system_info)