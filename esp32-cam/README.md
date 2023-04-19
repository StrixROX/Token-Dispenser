# ESP32-CAM (with PSRAM) and ESP32-CAM-MB
## Softwares and Libraries used
- Arduino IDE 2.0.4 ([Link](https://www.arduino.cc/en/software/))
- ESP32CAM Arduino Board Manager ([URL](https://espressif.github.io/arduino-esp32/package_esp32_index.json))
- ESP32QRCodeReader ([GitHub Repo](https://github.com/alvarowolfx/ESP32QRCodeReader/tree/master))

## Installation
1. Install Arduino IDE: [Link](https://www.arduino.cc/en/software/).
2. Install the board manager for ESP32CAM.
    - Open Arduino IDE.
    - Go to `File > Preferences...`.
    - In the `Additional boards manager URLs` input box, add this URL:
    ```
    https://espressif.github.io/arduino-esp32/package_esp32_index.json
    ```
    - Click `OK`.
    - Go to `Tools > Board > Boards Manager...`.
    - Search for `esp32`.
    - Install `esp32` by `Espressif Systems`.
4. Close your Arduino IDE.
5. Connect your `esp32-cam` to your PC.
6. Open `qr_scanner.ino` with Arduino IDE.
7. Setup Arduino IDE to use the new board manager.
    - Select `Tools > Board > esp32 > AI Thinker ESP32-CAM`.
    - Select `Tools > Port > [Your Port]`.
    - Select `Tools > CPU Frequency > 240MHz`.
    - Select `Tools > Flash Frequency > 40MHz`.
    - Select `Tools > Flash Mode > DIO`.
8. Click `Verify` to verify the sketch.
9. Resolve any errors and click `Upload` to upload your sketch to the `esp32-cam`.
10. When the Output window prompts the following:
    ```
    Connecting........
    ```
    press the `RST` button on your `esp32-cam` and it should start uploading the sketch.
    > NOTE: Timing matters.
11. After uploading is complete, press the `RST` button again to boot the camera.

## Usage
1. After [Installation](#installation) is complete, connect the `esp32-cam` to your PC and open the Serial Monitor (`Tools > Serial Monitor`) in your Arduino IDE.
2. Set the baud rate to `115200` and the serial monitor should start logging the output from the camera.
3. Voila!
> NOTE: Make sure the QR code being scanned is at an appropriate distance from the camera.