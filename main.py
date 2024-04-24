from ursina import *
import twophase.solver as sv


#print(sv.solve(cubestring="DULDULDDLFUBDRFBBRRRDDFBURLFUURDLRBUFLBLLFBBLDFRRBFFUU"))

class RubiksCube:
    def __init__(self):
        self.rotate_dict = {
            'U': 'TOP',
            'D': 'BOTTOM',
            'F': 'FACE',
            'B': 'BACK',
            'L': 'LEFT',
            'R': 'RIGHT'
        }
        self.begin_rotation_string = self.generate_cube()
        # self.begin_rotation_string = 'UUUUURUFBLBLURDDFDLRDDFLUFRBLFDDURBFRBBFLRDLRFRFBBDLLB'
        self.solve_rotation_string = self.solve_cube(self.begin_rotation_string)
        self.solve_rotation_dict = self.string_to_dict(self.solve_rotation_string)
        self.reverse_rotation_dict = self.reverse_rotate_dict(self.solve_rotation_dict)
        self.count_rotation = len(self.solve_rotation_dict)
        self.current_solve_rotation_dict = self.solve_rotation_dict
        self.yet_rotation_dict = []
        self.current_count_rotation = 0

    def print(self):
        print(self.begin_rotation_string)
        print(self.solve_rotation_string)
        print(self.solve_rotation_dict)
        print(self.reverse_rotation_dict)
        print(self.count_rotation)


    def string_to_dict(self, rotate_string):
        elements = rotate_string.split()
        elements.pop()
        print(elements)
        list = []
        for element in elements:
            letter, number = element[0], int(element[1:])
            list.append([letter, number])
        return list

    def reverse_rotate_dict(self, pairs):
        revesed_pairs = []
        for pair in pairs:
            revesed_pairs.append([pair[0], (4-int(pair[1]))])
        return revesed_pairs[::-1]

    def generate_cube(self):
        cc = sv.cubie.CubieCube()
        cc.randomize()
        fc = cc.to_facelet_cube()
        begin_string = fc.to_string()
        return begin_string

    def solve_cube(self, begin_string):
        solve_rotation_string = sv.solve(begin_string)
        return solve_rotation_string
    
cube = RubiksCube()
cube.print()


class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.fullscreen = False
        window.borderless = False
        window.size = (1280, 720)
        cube_model = Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # plane
        Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)  # sky
        EditorCamera()
        camera.world_position = (0, 0, -15)
        # camera.look_at(cube_model)
        # camera.look_at(Entity.position)
        self.model, self.texture = 'models/custom_cube', 'textures/rubik_texture'
        self.load_game()
        self.message = Text(text=(str(cube.solve_rotation_dict[0][0])+str(cube.solve_rotation_dict[0][1])), origin=(0, 19), color=color.black, scale = 2, position= (0, 1.3))
        self.solve_text = Text(text=("для сборки " + cube.solve_rotation_string), origin=(0, 19), color=color.black, scale = 1, position= (0, 0.001))
        self.current_solve_text = Text(text=("текущее " + cube.solve_rotation_string), origin=(0, 19), color=color.black, scale = 0.8, position= (0, 0.005))
        self.yet_rot_text = Text(text=("нажато: " + str(cube.yet_rotation_dict)), origin=(0, 19), color=color.black, scale = 0.8, position= (0, 0.1), width=500)
        self.current_count_rotation_text = Text(text=("сделано поворотов: " + str(cube.current_count_rotation)), origin=(0, 19), color=color.black, scale = 1, position= (0, 0.75))

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
        self.rotate_cube_without_animation(pairs=cube.reverse_rotation_dict)
        # self.rotate_cube(pairs=cube.reverse_rotation_dict)
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

    def input(self, key, is_raw=False):
        # self.message.text1
        # cube.current_solve_rotation_dict = cube.current_solve_rotation_dict
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
            if cube.current_solve_rotation_dict and key.upper()[len(key)-1] in cube.current_solve_rotation_dict[0][0]:
                if "control" in key:
                    cube.current_solve_rotation_dict[0][1] = (cube.current_solve_rotation_dict[0][1] - 3) % 4
                    cube.yet_rotation_dict.append([key.upper()[len(key)-1], 3])
                else:
                    cube.current_solve_rotation_dict[0][1] = cube.current_solve_rotation_dict[0][1] - 1
                    cube.yet_rotation_dict.append([key.upper(), 1])

                if cube.current_solve_rotation_dict[0][1] == 0:
                    cube.current_solve_rotation_dict.pop(0)
                if cube.current_solve_rotation_dict:
                    self.message.text = str(str(cube.current_solve_rotation_dict[0][0])+str(cube.current_solve_rotation_dict[0][1]))
                else:
                    self.message.text = "OK"
                self.yet_rot_text.text = "нажато: " + str(cube.yet_rotation_dict)
            else:
                if "control" in key:
                    cube.current_solve_rotation_dict.insert(0, [key.upper()[len(key)-1], 1])
                    cube.yet_rotation_dict.append([key.upper()[len(key)-1], 3])
                else:
                    cube.current_solve_rotation_dict.insert(0, [key.upper(), 3])
                    cube.yet_rotation_dict.append([key.upper(), 1])
                self.message.text = str(str(cube.current_solve_rotation_dict[0][0])+str(cube.current_solve_rotation_dict[0][1]))
            if cube.current_solve_rotation_dict and cube.current_solve_rotation_dict[0][0] != cube.yet_rotation_dict[-1][0]:
                cube.current_count_rotation += 1
            if not cube.current_solve_rotation_dict:
                cube.current_count_rotation += 1
            print(cube.current_count_rotation)
            self.current_count_rotation_text.text = ("сделано поворотов: " + str(cube.current_count_rotation))
            self.current_solve_text.text = "текущее: " + str(cube.current_solve_rotation_dict)
                


        if key == 'space': # Пример использования пробела для переключения режима
            self.toggle_game_mode()
        # if key == 's':
        #     self.rotate_cube_without_animation(current_rotation_list)
        #     current_rotation_list = []
        # if key == 'v':
        #     # print(camera.get_position())
        #     self.random_state_animation()

        super().input(key)

        if key == 'n':
            pairs = cube.reverse_rotate_dict(cube.yet_rotation_dict)
            self.rotate_cube_without_animation(pairs)
            ####################################################################
            cube.solve_rotation_dict = cube.string_to_dict(cube.solve_rotation_string)
            #ПОЧЕМУ БЕЗ СТРОКИ СВЕРХУ НЕ РАБОТАЕТ
            ###########################################################################
            cube.current_solve_rotation_dict = cube.solve_rotation_dict
            cube.yet_rotation_dict = []
            # print(cube.solve_rotation_string)
            # print(cube.solve_rotation_dict)
            # print(cube.current_solve_rotation_dict)
            # print(cube.yet_rotation_dict)
            self.message.text = str(str(cube.solve_rotation_dict[0][0])+str(cube.solve_rotation_dict[0][1]))
            self.yet_rot_text.text = "нажато: " + str(cube.yet_rotation_dict)
            self.current_solve_text.text = "текущее " + cube.solve_rotation_string
            cube.current_count_rotation = 0
            self.current_count_rotation_text.text = ("сделано поворотов: " + str(cube.current_count_rotation))


    
    def rotate_cube_without_animation(self, pairs):
        for pair in pairs:
            [self.rotate_side_without_animation(cube.rotate_dict[pair[0]]) for i in range(int(pair[1]))]

    def rotate_cube(self, pairs):
        for pair in pairs:
            [self.rotate_side(cube.rotate_dict[pair[0]]) for i in range(int(pair[1]))]


    
    

if __name__ == '__main__':
    game = Game()
    
    game.run()
