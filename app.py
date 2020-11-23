import pygame
from models import tello, gui
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from threading import Thread

def main():
    drone = tello.Tello()
    
    # gui blocks pygame input if not created in main
    g = gui.GUI()
    g.set_self_drone(drone)
    g.show()
    
    # start pygame (used for controller and keyboard inputs)
    pygame.init()
    con = None
    try:
        con = pygame.joystick.Joystick(0)
        con.init()
    except Exception as e:
        print('No controller connected!')

    dx, dy, dz, yaw = 0, 0, 0, 0
    last = [0, 0, 0, 0] 
    # deadzone for controller sticks
    deadzone = 20 

    while True:
        events = pygame.event.get()
        for event in events:
            """
            Controller mapping
            (https://www.pygame.org/docs/ref/joystick.html)
            0   -   a
            1   -   b
            8   -   start
            10  -   xbox guide button
            """
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.dict['button']
                if button == 0:
                    response = drone.send_command_with_response('takeoff')
                    print(f'response: {response}')
                elif button == 1:
                    response = drone.send_command_with_response('land')
                    print(f'response: {response}')
                # Initialize drone to accept commands
                elif button == 8:
                    response = drone.send_command_with_response('command')
                    print(f'response: {response}')
                # sends command to start video streaming and turns on video
                elif button == 10:
                    response = drone.send_command_with_response('streamon')
                    print(f'response: {response}')
                    # run video feed in separate thread
                    thread = Thread(target=g.show_video_feed, args=())
                    thread.start()

            # temporary keyboard input because my os update broke controller support
            if event.type == pygame.KEYDOWN:
                key = event.dict['key']
                print(event.dict)
                if key == 32:
                    response = drone.send_command_with_response('command')
                    print(f'response: {response}')
                elif key == 8:
                    response = drone.send_command_with_response('streamon')
                    print(f'response: {response}')
                    thread = Thread(target=g.show_video_feed, args=())
                    thread.start()
                
                #print(event.dict, event.joy, event.button, 'pressed')
            elif event.type == pygame.JOYAXISMOTION:
                axis = event.dict['axis']
                value = event.dict['value']*100
                value = round(value, 2)
                
                """
                direction values for left joystick
                axis 0 is left / right
                axis 1 is up / down
                """
                if axis == 0 and value < 0:
                    dx = value
                if axis == 0 and value > 0:
                    dx = abs(value)
                if axis == 1 and value < 0:
                    dy = abs(value)
                if axis == 1 and value > 0:
                    dy = value * -1
                
                """
                direction values for right joystick
                axis 3 is left / right
                axis 4 is up / down
                """
                if axis == 3 and value < 0:
                    yaw = value
                if axis == 3 and value > 0:
                    yaw = abs(value)
                if axis == 4 and value < 0:
                    dz = abs(value)
                if axis == 4 and value > 0:
                    dz = value * -1
                
                # when letting go of the joystick, need to stop drone from moving
                if dx <= deadzone and dx >= -deadzone:
                    if dy <= deadzone and dy >= -deadzone:
                        dx, dy = 0, 0
                if dz <= deadzone and dz >= -deadzone:
                    if yaw <= deadzone and yaw >= -deadzone:
                        dz, yaw = 0, 0

                if dx != last[0] or dy != last[1] or dz != last[2] or yaw != last[3]:
                    drone.test_rc(dx, dy, dz, yaw)
                    drone.send_command_continuous(f'rc {dx} {dy} {dz} {yaw}')
                
                last = [dx, dy, dz, yaw]

if __name__ == '__main__':
    main()
