import pygame
import pyautogui
import time

# SETTINGS - CUSTOMIZABLE
mouse_speed = 50        # CURSOR SPEED (LEFT STICK)
left_deadzone = 0.4     # LEFT JOYSTICK DEADZONE
right_deadzone = 0.3    # RIGHT JOYSTICK DEADZONE  
scroll_speed = 280      # SCROLL SPEED (RIGHT STICK)
dpad_speed = 10          # DPAD STEP SIZE
sleep_delay = 0.001    # SMOOTHNESS VS. CPU USAGE

# try mouse_speed = 20 and dpad_speed = 100 to let stick do fine adj.
# try mouse_speed = 50 and dpad_speed = 10 to let dpad do fine adj.

# Initialize pygame
pygame.init()
pygame.joystick.init()

# Ensure controller is connected
if pygame.joystick.get_count() == 0:
    print("No controller detected.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Using controller: {joystick.get_name()}")

# For debouncing button clicks
left_click_down = False
right_click_down = False

try:
    while True:
        for event in pygame.event.get():
            pass  # clear queue

        # Read left stick
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        # Apply deadzone for left stick
        axis_x = 0 if abs(axis_x) < left_deadzone else axis_x
        axis_y = 0 if abs(axis_y) < left_deadzone else axis_y

        # Move cursor with left stick
        dx = int(axis_x * mouse_speed)
        dy = int(axis_y * mouse_speed)
        if dx != 0 or dy != 0:
            pyautogui.moveRel(dx, dy)

        # D-Pad control (buttons 11, 12, 13, 14)
        dpad_up = joystick.get_button(11)    # D-Pad up
        dpad_down = joystick.get_button(12)  # D-Pad down
        dpad_left = joystick.get_button(13)  # D-Pad left
        dpad_right = joystick.get_button(14) # D-Pad right

        # Move cursor with D-Pad (simulating relative movement)
        if dpad_up:
            pyautogui.moveRel(0, -dpad_speed)
        if dpad_down:
            pyautogui.moveRel(0, dpad_speed)
        if dpad_left:
            pyautogui.moveRel(-dpad_speed, 0)
        if dpad_right:
            pyautogui.moveRel(dpad_speed, 0)

        # Left click with "A" button (button 0)
        if joystick.get_button(0):  # A button
            if not left_click_down:
                pyautogui.click(button='left')
            left_click_down = True
        else:
            left_click_down = False

        # Right click with "B" button (button 1)
        if joystick.get_button(1):  # B button
            if not right_click_down:
                pyautogui.click(button='right')
                right_click_down = True
        else:
            right_click_down = False
            
        # Scroll with right stick (button 3 and 4 are typically the right stick's axes)
        right_axis_y = joystick.get_axis(3)  # Right stick Y-axis
        if abs(right_axis_y) > right_deadzone:  # Apply deadzone
            # Scroll up or down
            pyautogui.scroll(int(right_axis_y * scroll_speed * -1))

        time.sleep(sleep_delay)

except KeyboardInterrupt:
    print("\nExiting.")
    pygame.quit()
