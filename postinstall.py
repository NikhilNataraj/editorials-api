from playwright.sync_api import sync_playwright


def install_playwright():
    with sync_playwright() as p:
        p.chromium.launch()
        p.firefox.launch()
        p.webkit.launch()


if __name__ == "__main__":
    install_playwright()