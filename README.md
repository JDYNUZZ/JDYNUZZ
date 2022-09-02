### Due to the large size of AOSP, we cannot provided the compiled AOSP here. Please follow the compliation instruction of official documents. For convience, we provide the key commands we used.

## Pre-processing
```
# -------------
# Download the AOSP, version android-12.0.0_r31
# Document https://source.android.com/docs/setup/build/downloading

# -------------
# Download and Extract Pixel 3 Driver Binary from https://developers.google.com/android/drivers#bluelinesp1a.210812.016.c1

# -------------
# Compilation 
# Document https://source.android.com/docs/setup/build/building

# Select the compilation target
lunch 4
# Enable hwaddress sanitizer
export SANITIZE_TARGET=hwaddress

# -------------
# Flash the system to device (Pixel 3)
adb reboot-bootloader
fastboot flashall -w
```

## JNI Anslyzer

## Fuzzing Client

## Fuzzing Server
