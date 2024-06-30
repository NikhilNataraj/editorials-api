import subprocess


def install_playwright():
    subprocess.run(["playwright", "install", "chromium"], check=True)
    subprocess.run(["playwright", "install-deps"], check=True)
