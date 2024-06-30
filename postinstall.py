import subprocess


def install_playwright():
    subprocess.run(["playwright", "install"], check=True)


if __name__ == "__main__":
    install_playwright()
