# Captcha 1 Challenge Solver for defendtheweb.net
A python script to solve the playground challenge Captcha 1 for defendtheweb.net (if it fails try again, this works 80% of the time from my testing)

## Setup Guide
### 1. Prerequisites:
- Python: Make sure you have Python 3.6+ installed.
- Tesseract OCR

You must install the Tesseract OCR engine on your system.

Windows: Download the installer from Tesseract at [here](https://github.com/tesseract-ocr/tesseract/releases).

macOS: Install via Homebrew:
```
brew install tesseract
```

Linux: Use your package manager, for example on Ubuntu:
```
sudo apt-get install tesseract-ocr
```

### 2. Clone and Set Up the Project
Clone the Repository (if you haven't already):

```
git clone https://github.com/kagenay/defend-the-web-captcha1-solver.git
cd defend-the-web-captcha1-solver
```

```
pip install -r requirements.txt
```

### 3. Configuration
Edit the `cookies_dict` in your Python script to include the required cookie values.

### 4. Running the Script
Run the script using:

```
python dtw-captcha-1.py
```
