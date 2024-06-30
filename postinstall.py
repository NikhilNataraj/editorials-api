from playwright.sync_api import sync_playwright
import subprocess


def install_playwright():
    subprocess.run(["playwright", "install"], check=True)
    with sync_playwright() as p:
        p.chromium.launch()
        p.firefox.launch()
        p.webkit.launch()


if __name__ == "__main__":
    install_playwright()