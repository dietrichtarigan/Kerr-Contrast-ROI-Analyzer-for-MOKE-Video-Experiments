"""
Video ROI Analyzer with Integrated GUI

This module provides an integrated GUI for video ROI analysis with Kerr contrast,
featuring a single window design for better user experience.
"""

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import threading
import time


class VideoROIAnalyzerGUI:
    """
    An integrated GUI application for analyzing ROIs in video files.
    
    Features:
    - Single window interface with video display and controls
    - Live ROI selection directly on displayed video
    - Real-time progress updates
    - Embedded plot visualization
    - Export results to CSV and PNG
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root (tk.Tk): Root window of the application
        """
        self.root = root
        self.root.title("Video ROI Analyzer")
        self.root.minsize(1000, 700)
        
        # Initialize variables
        self.video_path = None
        self.cap = None
        self.frame = None
        self.display_frame = None
        self.gray_frame = None
        self.roi_start = None
        self.roi_end = None
        self.roi_coords = None
        self.intensities = []
        self.frame_numbers = []
        self.processing = False
        self.zoom_factor = 1.0
        
        # Set up the UI components
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the main UI components."""
        # Main layout frames
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # File selection
        file_frame = ttk.LabelFrame(control_frame, text="Video Selection", padding=5)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(file_frame, text="Open Video", command=self.open_video).pack(side=tk.LEFT, padx=5)
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Action buttons
        action_frame = ttk.LabelFrame(control_frame, text="Actions", padding=5)
        action_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(action_frame, text="1.").pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(action_frame, text="Select ROI", command=self.toggle_roi_mode).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(action_frame, text="2.").pack(side=tk.LEFT, padx=(15, 0))
        self.process_btn = ttk.Button(action_frame, text="Process Video", command=self.process_video, state=tk.DISABLED)
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(action_frame, text="3.").pack(side=tk.LEFT, padx=(15, 0))
        self.save_btn = ttk.Button(action_frame, text="Save Results", command=self.save_results, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Content area with video display and plot
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Video display area
        video_frame = ttk.LabelFrame(content_frame, text="Video Preview & ROI Selection", padding=5)
        video_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self.canvas = tk.Canvas(video_frame, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Canvas events for ROI selection
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Results/Plot area
        plot_frame = ttk.LabelFrame(content_frame, text="Results", padding=5)
        plot_frame.grid(row=0, column=1, sticky="nsew")
        
        self.plot_area = ttk.Frame(plot_frame)
        self.plot_area.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Status bar
        status_frame = ttk.Frame(main_frame, relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(status_frame, variable=self.progress_var, length=200)
        self.progress.pack(side=tk.RIGHT, padx=5)
        
        # Initialize flags
        self.roi_selection_mode = False
    
    def open_video(self):
        """Open a video file and display the first frame."""
        # Clean up any existing video capture
        if self.cap is not None:
            self.cap.release()
        
        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
            
        # Update state
        self.video_path = file_path
        self.file_label.config(text=os.path.basename(file_path))
        self.status_var.set(f"Loaded video: {os.path.basename(file_path)}")
        
        # Reset ROI and results
        self.roi_coords = None
        self.intensities = []
        self.frame_numbers = []
        self.save_btn.config(state=tk.DISABLED)
        
        # Load first frame
        self.cap = cv2.VideoCapture(file_path)
        ret, frame = self.cap.read()
        
        if not ret:
            messagebox.showerror("Error", "Could not read the video file.")
            self.cap.release()
            self.cap = None
            return
            
        # Store and display frame
        self.frame = frame
        self.gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.display_frame = self.frame.copy()
        self.show_frame()
        
        # Enable ROI selection
        self.process_btn.config(state=tk.DISABLED)
        
    def show_frame(self):
        """Display the current frame on the canvas."""
        if self.display_frame is None:
            return
            
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # If canvas not yet fully initialized
        if canvas_width <= 1:
            self.root.after(100, self.show_frame)
            return
            
        # Convert from BGR to RGB for PIL
        image = cv2.cvtColor(self.display_frame, cv2.COLOR_BGR2RGB)
        
        # Calculate scaling to fit canvas while maintaining aspect ratio
        img_height, img_width = image.shape[:2]
        scale_width = canvas_width / img_width
        scale_height = canvas_height / img_height
        scale = min(scale_width, scale_height)
        
        # Apply scaling
        new_width = int(img_width * scale * self.zoom_factor)
        new_height = int(img_height * scale * self.zoom_factor)
        
        if scale * self.zoom_factor != 1.0:
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Convert to PhotoImage
        self.tk_image = ImageTk.PhotoImage(Image.fromarray(image))
        
        # Display on canvas
        self.canvas.delete("all")
        
        # Center image on canvas
        x_pos = max(0, (canvas_width - new_width) // 2)
        y_pos = max(0, (canvas_height - new_height) // 2)
        
        self.canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=self.tk_image)
        
        # Draw ROI if it exists
        if self.roi_coords:
            x, y, w, h = self.roi_coords
            # Scale ROI to match displayed image
            roi_x = int(x * scale * self.zoom_factor) + x_pos
            roi_y = int(y * scale * self.zoom_factor) + y_pos
            roi_w = int(w * scale * self.zoom_factor)
            roi_h = int(h * scale * self.zoom_factor)
            
            # Draw rectangle
            self.canvas.create_rectangle(
                roi_x, roi_y, roi_x + roi_w, roi_y + roi_h, 
                outline="lime", width=2
            )
    
    def toggle_roi_mode(self):
        """Toggle ROI selection mode on/off."""
        # Make sure we have a video loaded
        if self.frame is None:
            messagebox.showinfo("Information", "Please open a video first.")
            return
            
        # Toggle mode
        self.roi_selection_mode = not self.roi_selection_mode
        
        if self.roi_selection_mode:
            self.status_var.set("ROI Selection Mode: Click and drag to select region")
        else:
            self.status_var.set("Ready")
            
    def on_mouse_down(self, event):
        """Handle mouse button press for ROI selection."""
        if not self.roi_selection_mode or self.frame is None:
            return
            
        # Get canvas dimensions and image position
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_height, img_width = self.frame.shape[:2]
        
        scale_width = canvas_width / img_width
        scale_height = canvas_height / img_height
        scale = min(scale_width, scale_height)
        
        new_width = int(img_width * scale * self.zoom_factor)
        new_height = int(img_height * scale * self.zoom_factor)
        
        x_pos = max(0, (canvas_width - new_width) // 2)
        y_pos = max(0, (canvas_height - new_height) // 2)
        
        # Check if click is within image bounds
        if (x_pos <= event.x <= x_pos + new_width and
            y_pos <= event.y <= y_pos + new_height):
            
            # Save start point
            self.roi_start = (event.x, event.y)
            
            # Reset end point
            self.roi_end = None
            
            # Create a copy of the frame for drawing
            self.display_frame = self.frame.copy()
            self.show_frame()
    
    def on_mouse_move(self, event):
        """Handle mouse movement for ROI selection."""
        if not self.roi_selection_mode or self.roi_start is None:
            return
            
        # Update end point
        self.roi_end = (event.x, event.y)
        
        # Create a copy of the original frame
        self.display_frame = self.frame.copy()
        
        # Get canvas dimensions and image position
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_height, img_width = self.frame.shape[:2]
        
        scale_width = canvas_width / img_width
        scale_height = canvas_height / img_height
        scale = min(scale_width, scale_height)
        
        new_width = int(img_width * scale * self.zoom_factor)
        new_height = int(img_height * scale * self.zoom_factor)
        
        x_pos = max(0, (canvas_width - new_width) // 2)
        y_pos = max(0, (canvas_height - new_height) // 2)
        
        # Draw temporary rectangle on canvas
        self.canvas.delete("temp_rect")
        self.canvas.create_rectangle(
            self.roi_start[0], self.roi_start[1],
            self.roi_end[0], self.roi_end[1],
            outline="yellow", width=2, tags="temp_rect"
        )
    
    def on_mouse_up(self, event):
        """Handle mouse button release for ROI selection."""
        if not self.roi_selection_mode or self.roi_start is None:
            return
            
        # Update end point
        self.roi_end = (event.x, event.y)
        
        # Get canvas dimensions and image position
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_height, img_width = self.frame.shape[:2]
        
        scale_width = canvas_width / img_width
        scale_height = canvas_height / img_height
        scale = min(scale_width, scale_height)
        
        new_width = int(img_width * scale * self.zoom_factor)
        new_height = int(img_height * scale * self.zoom_factor)
        
        x_pos = max(0, (canvas_width - new_width) // 2)
        y_pos = max(0, (canvas_height - new_height) // 2)
        
        # Calculate ROI in original image coordinates
        x1 = min(self.roi_start[0], self.roi_end[0])
        y1 = min(self.roi_start[1], self.roi_end[1])
        x2 = max(self.roi_start[0], self.roi_end[0])
        y2 = max(self.roi_start[1], self.roi_end[1])
        
        # Convert to original image coordinates
        x1 = max(0, int((x1 - x_pos) / (scale * self.zoom_factor)))
        y1 = max(0, int((y1 - y_pos) / (scale * self.zoom_factor)))
        x2 = min(img_width, int((x2 - x_pos) / (scale * self.zoom_factor)))
        y2 = min(img_height, int((y2 - y_pos) / (scale * self.zoom_factor)))
        
        # Store ROI as (x, y, width, height)
        self.roi_coords = (x1, y1, x2 - x1, y2 - y1)
        
        # Exit ROI selection mode
        self.roi_selection_mode = False
        
        # Update status
        self.status_var.set(f"ROI selected: x={x1}, y={y1}, width={x2-x1}, height={y2-y1}")
        
        # Enable processing button
        self.process_btn.config(state=tk.NORMAL)
        
        # Redraw frame with final ROI
        self.display_frame = self.frame.copy()
        self.show_frame()
    
    def process_video(self):
        """Process the video and calculate ROI intensities."""
        if self.processing:
            return
            
        if not self.video_path or not self.roi_coords:
            messagebox.showinfo("Information", "Please open a video and select an ROI first.")
            return
            
        # Reset previous results
        self.intensities = []
        self.frame_numbers = []
        
        # Start processing in a background thread
        self.processing = True
        self.progress_var.set(0)
        
        # Update status
        self.status_var.set("Processing video...")
        
        # Disable buttons during processing
        self.process_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self.run_processing)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def run_processing(self):
        """Run video processing in a background thread."""
        try:
            # Open video
            cap = cv2.VideoCapture(self.video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Get ROI coordinates
            x, y, w, h = self.roi_coords
            
            # Process each frame
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Convert to grayscale
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Extract ROI
                roi = gray_frame[y:y+h, x:x+w]
                
                # Calculate mean intensity
                mean_intensity = np.mean(roi)
                
                # Store results
                self.intensities.append(mean_intensity)
                self.frame_numbers.append(frame_count)
                
                # Update progress (in main thread)
                frame_count += 1
                if frame_count % 10 == 0:
                    progress = int((frame_count / total_frames) * 100)
                    self.root.after(0, lambda p=progress, f=frame_count, t=total_frames: 
                                    self.update_progress(p, f, t))
            
            # Clean up
            cap.release()
            
            # Show results
            self.root.after(0, self.show_results)
            
        except Exception as e:
            # Show error
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {str(e)}"))
            self.root.after(0, self.reset_processing)
    
    def update_progress(self, progress, current_frame, total_frames):
        """Update progress bar and status text."""
        self.progress_var.set(progress)
        self.status_var.set(f"Processing: {current_frame}/{total_frames} frames ({progress}%)")
    
    def reset_processing(self):
        """Reset processing state."""
        self.processing = False
        self.process_btn.config(state=tk.NORMAL)
    
    def show_results(self):
        """Display the results of the analysis."""
        # Reset processing flag
        self.processing = False
        
        # Update status
        self.status_var.set(f"Processing complete. Analyzed {len(self.intensities)} frames.")
        
        # Create plot
        self.create_plot()
        
        # Enable buttons
        self.process_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
    
    def create_plot(self):
        """Create and display the results plot."""
        # Clear previous plot
        for widget in self.plot_area.winfo_children():
            widget.destroy()
        
        # Create figure
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot data
        ax.plot(self.frame_numbers, self.intensities, 'b-', linewidth=1.5)
        
        # Add labels and title
        ax.set_xlabel('Magnetic Field Step (Frame Number)')
        ax.set_ylabel('Mean ROI Intensity')
        ax.set_title('Kerr Contrast: ROI Intensity vs Magnetic Field')
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        if self.intensities:
            min_intensity = min(self.intensities)
            max_intensity = max(self.intensities)
            contrast_ratio = (max_intensity - min_intensity) / min_intensity * 100
            
            stats_text = (f'Contrast Ratio: {contrast_ratio:.1f}%\n'
                          f'Min: {min_intensity:.1f}\n'
                          f'Max: {max_intensity:.1f}')
                          
            ax.text(0.02, 0.98, stats_text, 
                   transform=ax.transAxes, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Adjust layout
        fig.tight_layout()
        
        # Display in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def save_results(self):
        """Save the analysis results."""
        if not self.intensities:
            messagebox.showinfo("Information", "No results to save.")
            return
            
        # Create DataFrame
        df = pd.DataFrame({
            'Frame_Number': self.frame_numbers,
            'Magnetic_Field_Step': self.frame_numbers,  # Using frame number as placeholder
            'Mean_ROI_Intensity': self.intensities
        })
        
        # Ask where to save CSV
        csv_file = filedialog.asksaveasfilename(
            title="Save Intensity Data",
            defaultextension=".csv",
            initialfile="roi_intensity_data.csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if csv_file:
            # Save CSV
            df.to_csv(csv_file, index=False)
            
            # Create and save plot
            fig = plt.Figure(figsize=(10, 6), dpi=300)
            ax = fig.add_subplot(111)
            
            # Plot data
            ax.plot(self.frame_numbers, self.intensities, 'b-', linewidth=1.5)
            
            # Add labels and title
            ax.set_xlabel('Magnetic Field Step (Frame Number)')
            ax.set_ylabel('Mean ROI Intensity')
            ax.set_title('Kerr Contrast: ROI Intensity vs Magnetic Field')
            ax.grid(True, alpha=0.3)
            
            # Add statistics
            min_intensity = min(self.intensities)
            max_intensity = max(self.intensities)
            contrast_ratio = (max_intensity - min_intensity) / min_intensity * 100
            
            ax.text(0.02, 0.98, f'Contrast Ratio: {contrast_ratio:.1f}%\nMin: {min_intensity:.1f}\nMax: {max_intensity:.1f}', 
                   transform=ax.transAxes, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Adjust layout
            fig.tight_layout()
            
            # Save plot
            plot_file = os.path.splitext(csv_file)[0] + ".png"
            fig.savefig(plot_file, dpi=300, bbox_inches='tight')
            
            # Update status
            self.status_var.set(f"Results saved to {os.path.basename(csv_file)} and {os.path.basename(plot_file)}")
            
            # Show confirmation
            messagebox.showinfo("Success", f"Results saved successfully to:\n{csv_file}\n{plot_file}")


def main():
    """Start the Video ROI Analyzer application."""
    root = tk.Tk()
    app = VideoROIAnalyzerGUI(root)
    
    # Set initial window size and position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Start application
    root.mainloop()


if __name__ == "__main__":
    main()
