import pygame
from models import tello

def main():
    pygame.init()
    con = pygame.joystick.Joystick(0)
    con.init()

    drone = tello.Tello()

    dx, dy, dz, yaw = 0, 0, 0, 0
    while True:
        events = pygame.event.get()
        for event in events:
            """ Controller Input Mappings (xbox one)
                a - 0
                b - 1
                x - 2
                y - 3
                .....
                start - 8
            """
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.dict['button']
                
                # Initialize drone to accept commands
                if button == 8:
                    response = drone.send_command_with_response('command')
                    print(f'response: {response}') 
                #print(event.dict, event.joy, event.button, 'pressed')
            elif event.type == pygame.JOYAXISMOTION:
                axis = event.dict['axis']
                value = event.dict['value']*100
                
                """ direction values for LEFT joystick """
                if axis == 1 and value < 0:
                    dx = abs(value)
                if axis == 1 and value > 0:
                    dx = value * -1
                if axis == 0 and value < 0:
                    dy = abs(value)
                if axis == 0 and value > 0:
                    dy = value * -1

                """ direction values for RIGHT joystick """
                if axis == 3 and value < 0:
                    yaw = abs(value)
                if axis == 3 and value > 0:
                    yaw = value * -1
                if axis == 4 and value < 0:
                    dz = abs(value)
                if axis == 4 and value > 0:
                    dz = value * -1

                print(f'dx: {dx} -- dy: {dy} -- dz: {dz} -- yaw: {yaw}')
            else:
                dx, dy, dz, yaw = 0, 0, 0, 0

                

if __name__ == '__main__':
    main()
