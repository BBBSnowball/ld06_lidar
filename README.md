# LD06 Lidar demo in Python

This is based on a fork of the ROS driver but it doesn't use ROS.

Quick start:

  1. Install gcc, make, pyserial and tkinter, e.g. run `nix-shell`.
  2. Build the native library: `make`
  3. Start the Python script: `python3 ld06.py`

If your LD06 is not at `dev/ttyUSB0`, you have to edit this in the Python script.

## Why?

I want to test my LD06 on my desktop because I don't have the Raspberry Pi, yet.
The *build* instructions for ROS start by installing multiple things from custom APT
repositories (and I couldn't find any documentation for building those) so I don't
think I could have installed it on NixOS in reasonable time. Writing the Python script
was easier.
