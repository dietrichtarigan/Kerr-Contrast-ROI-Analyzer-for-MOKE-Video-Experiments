# Kerr Contrast ROI Analyzer for MOKE Video Experiments

A comprehensive GUI application for analyzing Region of Interest (ROI) in video files to study Kerr contrast during magnetic field sweeps. This application provides real-time video preview, interactive ROI selection, automatic frame processing, and data visualization for magneto-optical research applications.

> [!NOTE] Features
> - **Interactive GUI interface** with real-time video preview and ROI selection
> - **Single-window design** combining video display, controls, and results visualization
> - **Automatic frame processing** with progress tracking and status updates
> - **Real-time data visualization** with embedded matplotlib plots
> - **CSV data export** for further analysis and research
> - **Multiple video format support** (MP4, AVI, MOV, MKV, WMV, FLV)
> - **Automated setup and launch** through batch script
> - **Modular architecture** separating GUI, processing logic, and utilities

# Quick Start

### Installation

1. **Automatic Installation (Recommended)**
   Simply run the batch file:
   ```
   run_analyzer.bat
   ```
   This will:
   - Check if Python is installed
   - Create a virtual environment in the `venv` folder
   - Install all required dependencies
   - Launch the application

2. **Manual Installation**

   If you prefer to install manually:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python video_roi_analyzer.py
   ```

### Basic Usage

1. **Open Video:** Click "Open Video" to select your video file
2. **Select ROI:** Click "Select ROI" and draw a rectangle around the area of interest
3. **Process Video:** Click "Process Video" to analyze all frames
4. **View Results:** Real-time plot shows intensity variations across frames
5. **Save Results:** Export data to CSV and plot to PNG for further analysis

# File Structure

| File                     | Description                                    |
| ------------------------ | ---------------------------------------------- |
| `video_roi_analyzer.py`  | Main GUI application with integrated interface |
| `run_analyzer.bat`       | Automated setup and launch script             |
| `requirements.txt`       | Required Python packages                      |
| `README.md`              | Project documentation and usage guide         |

# Component Overview

### `video_roi_analyzer.py`

The main application module built with Tkinter, OpenCV, and Matplotlib integration.

**Key Class:**
- `VideoROIAnalyzerGUI`: Main GUI class that:
  - Creates the integrated user interface
  - Handles video file loading and display
  - Manages interactive ROI selection
  - Processes video frames in background threads
  - Displays real-time results and data visualization
  - Exports results to CSV and PNG formats

**Key Methods:**
- `setup_ui()`: Creates all UI components and layout
- `open_video()`: Loads video file and displays first frame
- `toggle_roi_mode()`: Enables/disables ROI selection mode
- `on_mouse_down/move/up()`: Handles interactive ROI drawing
- `process_video()`: Processes all frames and calculates intensities
- `show_results()`: Creates and displays matplotlib plots
- `save_results()`: Exports data to CSV and plots to PNG

**Processing Features:**
- Frame-by-frame video analysis
- ROI intensity calculation using mean pixel values
- Progress tracking with visual feedback
- Error handling and user notifications
- Background processing to maintain UI responsiveness

### `run_analyzer.bat`

Automated setup and launch script for Windows systems.

**Key Functions:**
- Python installation detection
- Virtual environment creation and management
- Dependency installation from requirements.txt
- Application launching with error handling
- Fallback to system Python if virtual environment fails

**Setup Process:**
1. Checks for Python availability
2. Creates virtual environment if not exists
3. Activates virtual environment
4. Installs required packages
5. Launches the main application
6. Provides error messages and troubleshooting guidance

# User Interface Design

The application features a modern, single-window interface design:

### Main Components

1. **Control Panel**
   - Video file selection with file path display
   - Sequential action buttons (Open → Select ROI → Process → Save)
   - Clear workflow guidance with numbered steps

2. **Video Display Area**
   - Real-time video preview with scaling and centering
   - Interactive ROI selection with mouse drawing
   - Visual feedback during ROI selection process
   - Support for various video resolutions and aspect ratios

3. **Results Visualization**
   - Embedded matplotlib plots showing intensity vs. frame number
   - Real-time updates during processing
   - Statistical information and contrast analysis
   - High-quality plot rendering for publication

4. **Status and Progress**
   - Real-time status updates and user guidance
   - Progress bar showing processing completion
   - Error messages and troubleshooting information

# ROI Selection Process

The interactive ROI selection provides precise control over analysis regions:

### Selection Method
1. **Activation**: Click "Select ROI" to enter selection mode
2. **Drawing**: Click and drag on the video preview to draw rectangle
3. **Visual Feedback**: Yellow outline shows selected region in real-time
4. **Confirmation**: Release mouse to confirm selection
5. **Coordinates**: Display shows exact pixel coordinates and dimensions

### Technical Details
- Mouse events are mapped to original video coordinates
- Automatic scaling handles different video resolutions
- Bounds checking prevents selection outside video area
- ROI coordinates stored as (x, y, width, height) format

# Data Processing Workflow

### Frame Analysis Process
1. **Video Loading**: OpenCV loads video file and extracts metadata
2. **Frame Extraction**: Sequential frame processing with progress tracking
3. **ROI Analysis**: Calculate mean pixel intensity within selected region
4. **Data Collection**: Store frame numbers and corresponding intensities
5. **Statistical Analysis**: Calculate contrast ratios and variations
6. **Visualization**: Real-time plot updates showing intensity curves

### Output Generation
- **CSV Export**: Frame numbers and intensity values in structured format
- **Plot Export**: High-resolution PNG images (300 DPI) for publication
- **Statistical Summary**: Contrast ratios and intensity statistics

# Technical Specifications

### Video Support
- **Formats**: MP4, AVI, MOV, MKV, WMV, FLV
- **Codecs**: H.264, H.265, MPEG-4, and others supported by OpenCV
- **Resolution**: Automatic scaling for display, full resolution for analysis
- **Frame Rate**: Processes all frames regardless of original frame rate

### Performance Features
- **Background Processing**: Non-blocking frame analysis
- **Memory Management**: Efficient frame handling for large videos
- **Progress Tracking**: Real-time feedback on processing status
- **Error Recovery**: Graceful handling of corrupted frames or files

# Requirements

- **Python**: 3.7 or higher
- **OpenCV**: >=4.5.0 for video processing and image manipulation
- **NumPy**: >=1.20.0 for numerical computations
- **Pandas**: >=1.3.0 for data handling and CSV export
- **Matplotlib**: >=3.3.0 for plotting and visualization
- **Pillow**: >=8.2.0 for image processing and display
- **Tkinter**: Built-in GUI framework (included with Python)

See `requirements.txt` for the complete list of dependencies with version specifications.

# Application Workflow

### Step-by-Step Process

1. **Video Selection**
   - Click "Open Video" to browse and select video file
   - First frame automatically displayed for preview
   - Video metadata loaded (resolution, frame count, etc.)

2. **ROI Definition**
   - Click "Select ROI" to enter selection mode
   - Draw rectangle around area of interest (e.g., magnetic domain)
   - ROI coordinates displayed for verification

3. **Video Processing**
   - Click "Process Video" to start frame analysis
   - Progress bar shows completion percentage
   - Real-time plot updates show intensity variations

4. **Results Analysis**
   - View embedded plot showing intensity vs. frame number
   - Analyze contrast variations and magnetic domain behavior
   - Statistical information displayed alongside plot

5. **Data Export**
   - Click "Save Results" to export data
   - CSV file contains frame numbers and intensity values
   - PNG plot saved at publication quality (300 DPI)

# Research Applications

### Magneto-Optical Kerr Effect (MOKE) Studies
- Analysis of magnetic domain wall motion
- Hysteresis loop measurements from video data
- Temporal analysis of magnetic switching events
- Quantitative contrast measurements

### Data Analysis Capabilities
- Frame-by-frame intensity tracking
- Statistical analysis of contrast variations
- Export capabilities for further processing
- Integration with magnetic field sweep data

# Troubleshooting

### Common Issues

**Video Loading Problems**
- Ensure video file is not corrupted or in use by another application
- Check if video codec is supported by OpenCV
- Try converting video to MP4 format if issues persist

**ROI Selection Issues**
- Make sure video is properly loaded before selecting ROI
- Click and drag within the video preview area
- ROI must be fully contained within video boundaries

**Processing Errors**
- Check available memory for large video files
- Ensure ROI selection is valid and within frame boundaries
- Close other applications if system resources are limited

**Installation Issues**
- Run `run_analyzer.bat` as administrator if permission errors occur
- Check Python installation and PATH configuration
- Manually install dependencies if automatic installation fails

### Performance Optimization
- Use smaller ROI areas for faster processing
- Close unnecessary applications to free system resources
- Process shorter video segments for initial testing

## License

This application is provided under the MIT License. Feel free to use, modify, and distribute according to the license terms.
