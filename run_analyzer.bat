@echo off
echo ==========================================
echo    Video ROI Analyzer for Kerr Contrast
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    REM Python installed, check Python script
    if exist "video_roi_analyzer.py" (
        echo Python detected. Setting up environment...
        
        REM Check if virtual environment exists, create if it doesn't
        if not exist "venv\" (
            echo Creating virtual environment...
            python -m venv venv
            if %ERRORLEVEL% NEQ 0 (
                echo Failed to create virtual environment!
                echo Trying to proceed with system Python...
            ) else (
                echo Virtual environment created successfully.
            )
        ) else (
            echo Virtual environment already exists.
        )
        
        REM Activate the virtual environment if it exists
        if exist "venv\" (
            echo Activating virtual environment...
            call venv\Scripts\activate.bat
            
            echo Upgrading pip in virtual environment...
            python -m pip install --upgrade pip
            
            REM Install dependencies from requirements.txt if it exists
            if exist "requirements.txt" (
                echo Installing dependencies from requirements.txt...
                python -m pip install -r requirements.txt
            ) else (
                echo No requirements.txt found. Installing required packages...
                
                REM Install dependencies
                echo Installing OpenCV...
                python -m pip install opencv-python
                
                echo Installing NumPy and Pandas...
                python -m pip install numpy pandas
                
                echo Installing Matplotlib...
                python -m pip install matplotlib
                
                echo Installing Pillow...
                python -m pip install pillow
                
                REM Create requirements.txt for future use
                echo Creating requirements.txt file...
                pip freeze > requirements.txt
                echo Requirements file created.
            )
        ) else (
            REM If venv creation failed, fall back to system Python
            echo Installing dependencies to system Python...
            
            REM Install dependencies
            echo Installing OpenCV...
            python -m pip install opencv-python
            
            echo Installing NumPy and Pandas...
            python -m pip install numpy pandas
            
            echo Installing Matplotlib...
            python -m pip install matplotlib
            
            echo Installing Pillow...
            python -m pip install pillow
        )
        
        echo.
        echo ==========================================
        echo    Running Video ROI Analyzer...
        echo ==========================================
        echo.
        echo INSTRUCTIONS:
        echo 1. Click "Open Video" to select your video file
        echo 2. Click "Select ROI" then drag to select a region
        echo 3. Click "Process Video" to analyze intensity values
        echo 4. Click "Save Results" to export data and plot
        echo.
        
        REM If using venv and it exists
        if exist "venv\Scripts\python.exe" (
            echo Starting application with virtual environment...
            venv\Scripts\python.exe video_roi_analyzer.py
        ) else (
            echo Starting application with system Python...
            python video_roi_analyzer.py
        )
        
        REM Deactivate virtual environment if using it
        if exist "venv\Scripts\activate.bat" (
            call venv\Scripts\deactivate.bat
        )
        
        exit /b 0
    ) else (
        echo [ERROR] Python script video_roi_analyzer.py not found!
        echo Please make sure the script file is in the same directory as this batch file.
        pause
        exit /b 1
    )
) else (
    REM Python not found
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python:
    echo   - Download from https://www.python.org/downloads/
    echo   - Make sure to check "Add Python to PATH" during installation
    echo.
    echo After installing Python, run this batch file again.
    pause
    exit /b 1
)
