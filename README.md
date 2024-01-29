# mm-test
This repository demonstrates how to run simple autotest using appium, pytest and OpenCV on your local Android device.

### Requirements
1. Python 3.7+
2. Appium
3. Pytest
4. cv2 package
5. Android SDK

## **How to Run :**
1. Connect your Android device and check `adb devices`
2. Start Appium server `appium` (with uiautomator2)
3. _**Run:`pytest tests/test_mm.py --no-header -v` in this repo directory**_
4. Check Report in `/report_screens` directory (it will clear itself each test run)