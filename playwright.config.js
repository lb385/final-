# Playwright configuration for E2E tests

[playwright]
browsers = chromium firefox webkit

[browser.chromium]
launch_args = ["--disable-blink-features=AutomationControlled"]

[browser.firefox]

[browser.webkit]

# Test settings
timeout = 30000
slow_mo = 1000
