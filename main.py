import os
import subprocess
import shutil


def execute_commands(commands: list[str], work_path: str = os.getcwd()) -> None:
    """Executes a list of shell commands in a specified working directory.

    Args:
        commands (list[str]): A list of shell commands to be executed.
        work_path (str): The directory in which the commands should be executed.
                         Defaults to the current working directory of the script.
    """
    for command in commands:
        # Create the working directory if it does not exist
        if not os.path.exists(work_path):
            os.makedirs(work_path)

        # Execute each command in the specified working directory
        subprocess.run(command, shell=True, cwd=work_path)


def download_euroc(work_path: str = os.getcwd()) -> None:
    """Downloads the EuRoC MAV Dataset into a specified directory.

    Args:
        work_path (str): The directory path where the EuRoC dataset will be downloaded and
                         extracted. Defaults to the current working directory of the script.

    Bibtex:
        @article {
            burri2016euroc,
            author = {Burri, Michael and Nikolic, Janosch and Gohl, Pascal and Schneider, Thomas and Rehder, Joern and Omari, Sammy and Achtelik, Markus W and Siegwart, Roland},
            title = {\href{https://www.researchgate.net/publication/291954561_The_EuRoC_micro_aerial_vehicle_datasets}{The EuRoC micro aerial vehicle datasets},
            year = {2016},
            doi = {10.1177/0278364915620033},
            URL = {http://ijr.sagepub.com/content/early/2016/01/21/0278364915620033.abstract},
            eprint = {http://ijr.sagepub.com/content/early/2016/01/21/0278364915620033.full.pdf+html},
            journal = {The International Journal of Robotics Research}
        }
    """
    print("Downloading EuRoC MAV Dataset...")
    commands = [
        "wget -r -np -R 'index.html*' http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/",
        "mv robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/* .",
        "rm -r robotics.ethz.ch/",
        "find . -type f -name '*.zip' -exec sh -c 'unzip -n -d \"${1%.*}\" \"$1\"' _ {} \\;",
        "find . -type f -name '*.zip' -exec rm {} \\;",
        "find . -type f -name '.DS_Store' -delete",
        "find . -type d -name '__MACOSX' -exec rm -r {} +",
        "find . -type d -name 'mav0' -exec sh -c \"cd '{}' && mv -t .. *\" \\;",
        "find . -type d -name 'mav0' -exec rm -r {} +",
    ]
    execute_commands(commands, os.path.join(work_path, "EuRoC"))

    os.chdir(os.path.join(work_path, "EuRoC"))

    dirs = [dirs for dirs in os.listdir() if os.path.isdir(dirs)]

    for dir in dirs:
        os.chdir(dir)
        seqs = [seqs for seqs in os.listdir() if os.path.isdir(seqs)]
        for seq in seqs:
            os.chdir(seq)
            bag = [bag for bag in os.listdir() if bag.endswith(".bag")]
            if bag:
                os.rename(bag[0], os.path.join(bag[0][:-4], bag[0]))

            os.rename(seq, os.path.join("../../", seq))
            os.chdir("..")

        os.chdir("..")
        shutil.rmtree(dir)
