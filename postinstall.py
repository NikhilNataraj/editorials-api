import subprocess


def install_playwright():
    subprocess.run(["playwright", "install", "chromium"], check=True)
    subprocess.run(["playwright", "install", "firefox"], check=True)
    subprocess.run(["playwright", "install", "webkit"], check=True)


if __name__ == "__main__":
    install_playwright()
