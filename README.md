# Job Application Automator
A simple Python tool to automate job applications: saves job postings as PDFs, organizes them into folders, and logs details in a CSV. Optionally moves your latest resume and cover letter from Downloads for each application.

## Features
Automatically logs job applications by:
- Reading job URL from clipboard
- Saving the job posting as PDF
- Optionally moving your latest resume & cover letter
- Logging all entries into a CSV

## Setup
1. **Clone this repo** (or download the script files).

2. **Install Python dependencies**

   ```bash
    pip install -r requirements.txt
   ```

3. **Install system dependencies for WeasyPrint**

   WeasyPrint requires GTK libraries on your system.

   ### Windows

   Download and install GTK3 runtime environment before running the script: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

   ### Linux (Ubuntu/Debian)

   ```bash
   sudo apt install libgtk-3-0 libpango1.0-0 libcairo2
   ```

   ### macOS

   ```bash
   brew install gtk+3
   ```

## Usage
1. Open main.py and update the following configuration:

    * USER_NAME with your name (used to name resume/cover letter files)

    * BASE_DIR with base folder for saving job applications

    * Keywords for your resume & cover letter

2. Copy the job URL to your clipboard.

3. Run the script:

   ```bash
   python main.py
   ```

4. Follow prompts to optionally move your latest resume/cover letter PDFs if found.

5. Follow the prompt to enter the application status. Press Enter to use the default: "applied".

6. Your job posting will be saved as a PDF in a newly created folder named after the job title.

## Notes

* The script checks if the job URL is already logged to avoid duplicate entries.
* Make sure to install GTK dependencies, or WeasyPrint will raise errors like:

  ```
  OSError: cannot load library 'libgobject-2.0-0'
  ```

## License

MIT License
