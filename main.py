from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint

app = Ursina()

grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')

all_blocks = {1: grass_texture, 2: stone_texture, 3: brick_texture, 4: dirt_texture}
selected_block = grass_texture

def update():
    global selected_block
    for key in [1, 2, 3, 4]:
        if held_keys[str(key)]:
            selected_block = all_blocks[key]
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = grass_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = .5,
            texture = texture,
            color = color.color(0, 0, random.uniform(0.9, 1)),
            scale = .5,
        )
    
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                voxel = Voxel(position=self.position + mouse.normal, texture=selected_block)
            
            if key == 'right mouse down':
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 150,
            double_sided = True,
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model ='assets/arm',
            texture = arm_texture,
            scale = .2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.4, -0.6),
        )

    def active(self):
        self.position = Vec2(0.4, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

def make_y_position():
    if randint(0, 3) == 0:
        return 1
    else:
        return 0

for z in range(8):
    for x in range(8):
        voxel = Voxel(position=(x, make_y_position(), z))

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run() 
