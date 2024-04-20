from ursina import *
import twophase.solver as sv


#print(sv.solve(cubestring="DULDULDDLFUBDRFBBRRRDDFBURLFUURDLRBUFLBLLFBBLDFRRBFFUU"))

cc = sv.cubie.CubieCube()
cc.randomize()
fc = cc.to_facelet_cube()
begin_string = fc.to_string()
print(begin_string)

rotate_string = sv.solve(begin_string)
print(rotate_string)
# rotate_string = sv.solve("UBULURUFURURFRBRDRFUFLFRFDFDFDLDRDBDLULBLFLDLBUBRBLBDB")

rotate_dict = {
            'U': 'TOP',
            'D': 'BOTTOM',
            'F': 'FACE',
            'B': 'BACK',
            'L': 'LEFT',
            'R': 'RIGHT'
        }

def string_to_dict(rotate_string):
        # Разбиваем строку на список элементов по пробелам
        elements = rotate_string.split()
        elements.pop()
        # Создаем словарь
        list = []
        for element in elements:
            # Разбиваем каждый элемент на букву и число
            letter, number = element[0], int(element[1:])
            list.append([letter, number])
        return list
rotate_list = string_to_dict(rotate_string)
print(rotate_list)

def func_reverse_rotate_list(pairs):
    revesed_pairs = []
    for pair in pairs:
        revesed_pairs.append([pair[0], (4-int(pair[1]))])
    return revesed_pairs[::-1]

reverse_rotate_list = func_reverse_rotate_list(rotate_list)

print(reverse_rotate_list)

class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.fullscreen = False
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # plane
        Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)  # sky
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.model, self.texture = 'models/custom_cube', 'textures/rubik_texture'
        self.load_game()
        self.message = Text(text=rotate_string, origin=(0, 19), color=color.black, scale = 2, position= (0, 1.3))
        self.ctrl_pressed = False

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
        self.cubes_side_positons = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT, 'FACE': self.FACE,
                                    'BACK': self.BACK, 'TOP': self.TOP}
        self.animation_time = 0.3
        self.action_trigger = True
        self.action_mode = True
        self.message = Text(origin=(0, 19), color=color.black)
        self.toggle_game_mode()
        # self.create_sensors()
        #self.random_state(rotations=20) # initial state of the cube, rotations - number of side turns
        self.rotate_cube_without_animation(pairs=reverse_rotate_list)
        # self.rotate_cube_without_animation(pairs=rotate_list)
        #self.rotate_cube(pairs=rotate_list)
        # self.random_state_animation(rotations=10) # initial state of the cube, rotations - number of side turns

    def random_state(self, rotations=3):
        [self.rotate_side_without_animation(random.choice(list(self.rotation_axes))) for i in range(rotations)]

    def random_state_animation(self, rotations=3):
        for i in range(rotations):
            self.rotate_side(random.choice(list(self.rotation_axes)))
            invoke(self.toggle_animation_trigger, delay=self.animation_time)

    def rotate_side_without_animation(self, side_name):
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                if side_name in ['FACE', 'TOP', 'RIGHT']:
                    exec(f'self.PARENT.rotation_{rotation_axis} = 90')
                else:
                    exec(f'self.PARENT.rotation_{rotation_axis} = -90')

    # def create_sensors(self):
    #     '''detectors for each side, for detecting collisions with mouse clicks'''
    #     create_sensor = lambda name, pos, scale: Entity(name=name, position=pos, model='cube', color=color.dark_gray,
    #                                                     scale=scale, collider='box', visible=False)
    #     self.LEFT_sensor = create_sensor(name='LEFT', pos=(-0.99, 0, 0), scale=(1.01, 3.01, 3.01))
    #     self.FACE_sensor = create_sensor(name='FACE', pos=(0, 0, -0.99), scale=(3.01, 3.01, 1.01))
    #     self.BACK_sensor = create_sensor(name='BACK', pos=(0, 0, 0.99), scale=(3.01, 3.01, 1.01))
    #     self.RIGHT_sensor = create_sensor(name='RIGHT', pos=(0.99, 0, 0), scale=(1.01, 3.01, 3.01))
    #     self.TOP_sensor = create_sensor(name='TOP', pos=(0, 1, 0), scale=(3.01, 1.01, 3.01))
    #     self.BOTTOM_sensor = create_sensor(name='BOTTOM', pos=(0, -1, 0), scale=(3.01, 1.01, 3.01))

    def toggle_game_mode(self):
        '''switching view mode or interacting with Rubik's cube'''
        self.action_mode = not self.action_mode
        msg = dedent(f"{'ACTION mode ON' if self.action_mode else 'VIEW mode ON'}"
                     f" (to switch - press middle mouse button)").strip()
        #self.message.text = msg

    def toggle_animation_trigger(self):
        '''prohibiting side rotation during rotation animation'''
        self.action_trigger = not self.action_trigger

    def rotate_side(self, side_name):
        self.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                if side_name in ['FACE', 'TOP', 'RIGHT']:
                    eval(f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=self.animation_time)')
                else:
                    eval(f'self.PARENT.animate_rotation_{rotation_axis}(-90, duration=self.animation_time)')
                
        invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)


    def rotate_side_invert(self, side_name):
        self.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                if side_name in ['FACE', 'TOP', 'RIGHT']:
                    eval(f'self.PARENT.animate_rotation_{rotation_axis}(-90, duration=self.animation_time)')
                else:
                    eval(f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=self.animation_time)')
                
        invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP

    def input(self, key):
        test_rotate_list = rotate_list
        keys_list = ['u', 'd', 'f', 'b', 'l', 'r', 'control-u', 'control-d', 'control-f', 'control-b', 'control-l', 'control-r']
        if key in keys_list and self.action_mode and self.action_trigger:
            # Определите соответствие между клавишами и сторонами куба
            side_map = {
                'u': 'TOP',
                'd': 'BOTTOM',
                'f': 'FACE',
                'b': 'BACK',
                'l': 'LEFT',
                'r': 'RIGHT',
                'control-u': 'TOP',
                'control-d': 'BOTTOM',
                'control-f': 'FACE',
                'control-b': 'BACK',
                'control-l': 'LEFT',
                'control-r': 'RIGHT'
            }
            side_name = side_map.get(key)
            if "control" in key and side_name:
                self.rotate_side_invert(side_name)
            elif side_name:
                self.rotate_side(side_name)
                # self.rotate_side_without_animation(side_name)
            if key.upper() in test_rotate_list[0][0]:
                test_rotate_list[0][1] = test_rotate_list[0][1] - 1
                if test_rotate_list[0][1] == 0:
                    test_rotate_list.pop(0)
                if test_rotate_list:
                    self.message.text = str(test_rotate_list[0])
                else:
                    self.message.text = "OK"
            else:
                test_rotate_list.insert(0, [key.upper(), 3])
                self.message.text = str(test_rotate_list[0])
                


        if key == 'space': # Пример использования пробела для переключения режима
            self.toggle_game_mode()
        super().input(key)


    
    def rotate_cube_without_animation(self, pairs):
        for pair in pairs:
            [self.rotate_side_without_animation(rotate_dict[pair[0]]) for i in range(int(pair[1]))]

    def rotate_cube(self, pairs):
        for pair in pairs:
            [self.rotate_side(rotate_dict[pair[0]]) for i in range(int(pair[1]))]


    
    

if __name__ == '__main__':
    game = Game()
    
    game.run()
