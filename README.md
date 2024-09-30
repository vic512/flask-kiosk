# flask-kiosk

A simple Python/Flask/Pillow/Javascript web host image kiosk.

There aren't a lot of simple self-hosted options for digital frames, so I came up with this. Minimal functionality, singular in purpose. This allows you to upload images to a folder and then view them on a rotation similar to digital frames.

## Usage

The default port is `4444`.

Requires Flask and Pillow modules to be installed.

  pip install -r requirements.txt
  
  -- or --
  
  pip install Flask
  
  pip install Pillow
  

- To view the rotating images, navigate to `http://[your server's IP]:4444/` or `http://[your server's IP]:4444/gallery/`.

- To upload images, change the rotation timing, and manage the current images, navigate to `http://[your server's IP]:4444/upload/`.

My use case was leveraging an old Surface tablet, so I used these instructions to run Edge in kiosk mode to accomplish the digital frame feel: [Microsoft Edge Kiosk Mode](https://learn.microsoft.com/en-us/deployedge/microsoft-edge-configure-kiosk-mode)

## Settings

There are four settings on the upload URL page that can adjust the timings of the app:

- **Image Change Interval (seconds):** This sets the duration each image is displayed.
- **Gallery Refresh Interval (seconds):** This sets the interval at which the system refreshes the image list for displaying, so you do not have to refresh the browser to see the new images.
- **Image Width (pixels):** This sets the width of image resize at upload, aspect ratio is preserved.
- **Image Height (pixels):** This sets the height of image resize at upload, aspect ratio is preserved.
- **Rotate Images (degrees):** This sets the rotation of the image. Options are 0, 90, 180, 270.

[Docker Version - Preferred](https://hub.docker.com/r/cross512/flask-kiosk)
