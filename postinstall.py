import subprocess


def install_playwright():
    subprocess.run(["python", "-m", "playwright", "install"], check=True)


if __name__ == "__main__":
    install_playwright()
