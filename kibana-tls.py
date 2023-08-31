import os
import subprocess
import shutil

def find_files(root_folder, filename):
    for root, dirs, files in os.walk(root_folder):
        if filename in files:
            yield os.path.join(root, filename)

def main():
    kibana_files = list(find_files('/', 'kibana.yml'))
    while kibana_files:
        for idx, f in enumerate(kibana_files[:9], 1):
            print(f"{idx}: {f}")
            subprocess.run(f"tail -n 4 {f}", shell=True)  # Ensure this line ends properly

        selection = input("Select a file by number or enter '0' for next set: ")
        if selection == '0':
            kibana_files = kibana_files[9:]
        elif selection.isdigit() and 1 <= int(selection) <= 9:
            chosen_file = kibana_files[int(selection) - 1]

            # Backup the original file before making changes
            backup_file = f"{chosen_file}.bak"
            shutil.copy(chosen_file, backup_file)
            print(f"Backup created at {backup_file}")

            cmd = f"sudo sed -i 's/server.ssl.supportedProtocols: \\[\"TLSv1\", \"TLSv1.1\", \"TLSv1.2\"\\]/server.ssl.supportedProtocols: \\[\"TLSv1.2\", \"TLSv1.3\"\\]/' {chosen_file} && sudo systemctl restart kibana"
            print(f"Updating {chosen_file}")
            subprocess.run(cmd, shell=True)
            break

if __name__ == "__main__":
    main()
