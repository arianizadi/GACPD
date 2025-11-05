import os, subprocess, shutil


def remove_all_files(directory_path):
    # Check if the directory exists
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        # Loop through all files and directories in the specified directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                # Remove file if it's a file, or recursively delete if it's a directory
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print("The specified directory does not exist or is not a directory.")


def create_git_folder(folder, repo_name):
    repo_name = repo_name.replace("\\", "/")
    repo_owner = repo_name.split("/")

    og_path = os.getcwd()
    if os.path.exists(folder + "/" + repo_owner[0] + "/" + repo_owner[1]):
        os.chdir(folder + "/" + repo_owner[0] + "/" + repo_owner[1])
    else:
        os.makedirs(folder + "/" + repo_owner[0] + "/" + repo_owner[1])
        os.chdir(folder + "/" + repo_owner[0] + "/" + repo_owner[1])

    command = [
        "git",
        "clone",
        f'https://github.com/{repo_owner[1]}/{repo_owner[2]}',
    ]

    subprocess.run(command)

    os.chdir(og_path)

def run_jscpd(extension, token):
    import os, platform, shutil, subprocess, sys

    def jscpd_bin():
        # Prefer npx if available (handles Windows/Unix, no path quirks)
        npx = shutil.which("npx")
        if npx:
            return [npx, "jscpd"]
        # Fallback to local .bin shims (Windows uses .cmd)
        bin_dir = os.path.join(os.getcwd(), "node_modules", ".bin")
        if platform.system() == "Windows":
            return [os.path.join(bin_dir, "jscpd.cmd")]
        return [os.path.join(bin_dir, "jscpd")]

    cmd = jscpd_bin() + [
        "--pattern", "**/*.{}".format(extension),
        "--min-tokens", str(token),
        # pass paths explicitly (see §3)
        "src", "cmp"
    ]
    result = subprocess.run(cmd, text=True, capture_output=True, cwd=os.getcwd())
    print(result.stdout, result.stderr, result.returncode)


def get_all_files(directory_path):
    files = []
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isfile(full_path):
            files.append(entry)
    print(files)
    return files


def main():
    folder = "Check"
    repo_name = "ardupilot"
    repo_owner = "Ardupilot"
    numCheck = '1'
    full_path = numCheck+"/"+repo_owner+"/"+repo_name

    # create_git_folder(folder, full_path)
    first_folder = "ArduSub"
    first_check_folder = folder+"/"+full_path+"/"+first_folder
    files1 = get_all_files(first_check_folder)

    second_folder = "Rover"
    second_check_folder = folder+"/"+full_path+"/"+second_folder
    shutil.copytree(second_check_folder, 'cmp', dirs_exist_ok=True)

    i = 0
    for entry in files1:
        i += 1
        print(f"{entry} - {i}")
        tokens = [50, 40, 30, 20, 10]
        shutil.copy(first_check_folder +"/"+entry, 'src')
        extension = entry.split(".")
        if len(extension) == 2:
            for token in tokens:

                run_jscpd(extension[1], token)
                exit(0)
                shutil.copytree('src',
                                f'Check/Repos_results/{numCheck}-{first_folder}-{second_folder}/{token}/{entry}/src',
                                dirs_exist_ok=True)
                shutil.copytree('cmp',
                                f'Check/Repos_results/{numCheck}-{first_folder}-{second_folder}/{token}/{entry}/cmp',
                                dirs_exist_ok=True)
                shutil.copytree('reports',
                                f'Check/Repos_results/{numCheck}-{first_folder}-{second_folder}/{token}/{entry}/reports',
                                dirs_exist_ok=True)
        remove_all_files('src')
        remove_all_files('reports')
    remove_all_files('cmp')
if __name__ == "__main__":
    main()