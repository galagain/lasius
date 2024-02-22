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


def download_kitti_ground_truth_poses(work_path: str = os.getcwd()) -> None:
    """Downloads the KITTI odometry dataset ground truth poses into a specified directory.

    Args:
        work_path: The directory to download and extract the dataset into. Defaults to
                   the current working directory.

    Bibtex:
        @article{
            geiger2013vision,
            author = {Geiger, Andreas and Lenz, P and Stiller, Christoph and Urtasun, Raquel},
            year = {2013},
            month = {09},
            pages = {1231-1237},
            title = {Vision meets robotics: the KITTI dataset},
            volume = {32},
            journal = {The International Journal of Robotics Research},
            doi = {10.1177/0278364913491297}
        }
    """
    print("Downloading KITTI Ground Truth Poses...")
    commands = [
        "wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_odometry_poses.zip",
        "find . -type f -name '*.zip' -exec sh -c 'unzip -n -d \"${1%.*}\" \"$1\"' _ {} \\;",
        "mv data_odometry_poses/dataset/poses/* .",
        "rm -r data_odometry_poses/",
        "rm data_odometry_poses.zip",
    ]
    execute_commands(
        commands, os.path.join(os.path.join(work_path, "KITTI"), "data_odometry_poses")
    )


def download_kitti_calibration(work_path: str = os.getcwd()) -> None:
    """Downloads the KITTI odometry calibration data into a specified directory.

    Args:
        work_path: The directory to download and extract the dataset into. Defaults to
                   the current working directory.

    Bibtex:
        @article{
            geiger2013vision,
            author = {Geiger, Andreas and Lenz, P and Stiller, Christoph and Urtasun, Raquel},
            year = {2013},
            month = {09},
            pages = {1231-1237},
            title = {Vision meets robotics: the KITTI dataset},
            volume = {32},
            journal = {The International Journal of Robotics Research},
            doi = {10.1177/0278364913491297}
        }
    """
    print("Downloading KITTI Ground Odometry Calibration...")
    commands = [
        "wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_odometry_calib.zip",
        "find . -type f -name '*.zip' -exec sh -c 'unzip -n -d \"${1%.*}\" \"$1\"' _ {} \\;",
        "mv data_odometry_calib/dataset/sequences/* .",
        "rm -r data_odometry_calib/",
        "rm data_odometry_calib.zip",
    ]
    execute_commands(
        commands, os.path.join(os.path.join(work_path, "KITTI"), "data_odometry_calib")
    )


def download_kitti_odometry_gray(work_path: str = os.getcwd()) -> None:
    """Downloads the KITTI odometry dataset (grayscale images) into a specified directory.

    Args:
        work_path: The directory to download and extract the dataset into. Defaults to
                   the current working directory.

    Bibtex:
        @article{
            geiger2013vision,
            author = {Geiger, Andreas and Lenz, P and Stiller, Christoph and Urtasun, Raquel},
            year = {2013},
            month = {09},
            pages = {1231-1237},
            title = {Vision meets robotics: the KITTI dataset},
            volume = {32},
            journal = {The International Journal of Robotics Research},
            doi = {10.1177/0278364913491297}
        }
    """
    print("Downloading KITTI Data Odometry Gray...")
    commands = [
        "wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_odometry_gray.zip",
        "find . -type f -name '*.zip' -exec sh -c 'unzip -n -d \"${1%.*}\" \"$1\"' _ {} \\;",
        "find . -type f -name '*.zip' -exec rm {} \\;",
        "mv data_odometry_gray/dataset/sequences/* .",
        "rm -r data_odometry_gray/",
    ]
    execute_commands(
        commands, os.path.join(os.path.join(work_path, "KITTI"), "data_odometry_gray")
    )


def download_kitti_odometry_color(work_path: str = os.getcwd()) -> None:
    """Downloads the KITTI odometry dataset (color images) into a specified directory.

    Args:
        work_path: The directory to download and extract the dataset into. Defaults to
                   the current working directory.

    Bibtex:
        @article{
            geiger2013vision,
            author = {Geiger, Andreas and Lenz, P and Stiller, Christoph and Urtasun, Raquel},
            year = {2013},
            month = {09},
            pages = {1231-1237},
            title = {\href{https://www.researchgate.net/publication/258140919_Vision_meets_robotics_the_KITTI_dataset}{Vision meets robotics: the KITTI dataset}},
            volume = {32},
            journal = {The International Journal of Robotics Research},
            doi = {10.1177/0278364913491297}
        }
    """
    print("Downloading KITTI Data Odometry Color...")
    commands = [
        "wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_odometry_color.zip",
        "find . -type f -name '*.zip' -exec sh -c 'unzip -n -d \"${1%.*}\" \"$1\"' _ {} \\;",
        "find . -type f -name '*.zip' -exec rm {} \\;",
        "mv data_odometry_color/dataset/sequences/* .",
        "rm -r data_odometry_color/",
    ]
    execute_commands(
        commands, os.path.join(os.path.join(work_path, "KITTI"), "data_odometry_color")
    )


if __name__ == "__main__":

    work_path = input(
        "Enter the work path (press Enter for current directory): "
    ).strip()

    datasets = {
        "1": ("EuRoC MAV Dataset", download_euroc),
        "2": ("download_kitti_ground_truth_poses", download_kitti_ground_truth_poses),
        "3": ("download_kitti_calibration", download_kitti_calibration),
        "4": ("download_kitti_odometry_gray", download_kitti_odometry_gray),
        "5": ("download_kitti_odometry_color", download_kitti_odometry_color),
    }

    print("Select the datasets you want to download:")
    for key, (name, _) in datasets.items():
        print(f"  {key}. {name}")
    print("  all. Download all")

    choices = input("Enter your choices separated by commas (e.g., 1,3): ").split(",")

    if not work_path:
        work_path = os.getcwd()

    if not os.path.exists(work_path):
        os.makedirs(work_path)

    if "all" in choices:
        for _, func in datasets.values():
            func(work_path)
    else:
        for choice in choices:
            if choice in datasets:
                _, func = datasets[choice]
                func(work_path)
