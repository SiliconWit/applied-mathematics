import FreeCAD as App
import Part
import Draft
import math

# Create a new document
doc = App.newDocument("CowModel")

# Helper functions
def create_ellipsoid(center, radii, placement=None):
    """Create an ellipsoid at given center with given radii"""
    sphere = Part.makeSphere(1.0)
    # Scale the sphere in x, y, z directions
    mat = App.Matrix()
    mat.scale(radii[0], radii[1], radii[2])
    sphere = sphere.transformGeometry(mat)
    
    # Move to center
    if placement:
        sphere.translate(placement)
    else:
        sphere.translate(center)
    
    return sphere

def create_cylinder(radius, height, placement, direction=(0,0,1)):
    """Create a cylinder with given parameters"""
    cylinder = Part.makeCylinder(radius, height, placement, App.Vector(direction))
    return cylinder

def create_box(length, width, height, placement):
    """Create a box with given parameters"""
    box = Part.makeBox(length, width, height, placement)
    return box

def create_leg(placement, length=30, upper_radius=5, lower_radius=3):
    """Create a cow leg with joints"""
    # Upper leg (thigh)
    upper_leg = create_cylinder(upper_radius, length * 0.3, placement)
    
    # Knee joint
    knee_placement = App.Vector(placement.x, placement.y, placement.z - length * 0.3)
    knee_joint = create_ellipsoid(App.Vector(0,0,0), (upper_radius*1.1, upper_radius*1.1, upper_radius*0.9), knee_placement)
    
    # Lower leg placement (cannon bone)
    cannon_placement = App.Vector(placement.x, placement.y, placement.z - length * 0.32)
    
    # Cannon bone (shin)
    cannon = create_cylinder(lower_radius, length * 0.4, cannon_placement)
    
    # Fetlock joint
    fetlock_placement = App.Vector(placement.x, placement.y, placement.z - length * 0.73)
    fetlock_joint = create_ellipsoid(App.Vector(0,0,0), (lower_radius*1.2, lower_radius*1.2, lower_radius*0.8), fetlock_placement)
    
    # Pastern bone
    pastern_placement = App.Vector(placement.x, placement.y, placement.z - length * 0.75)
    pastern = create_cylinder(lower_radius*0.9, length * 0.15, pastern_placement)
    
    # Hoof placement
    hoof_placement = App.Vector(placement.x, placement.y, placement.z - length * 0.92)
    
    # Hoof - make it more detailed with a split
    hoof_base = create_ellipsoid(App.Vector(0,0,0), (lower_radius*1.5, lower_radius*2, lower_radius*0.8), hoof_placement)
    
    # Create a split in the hoof
    split_box = create_box(lower_radius*0.5, lower_radius*4, lower_radius*2, 
                         App.Vector(hoof_placement.x - lower_radius*0.25, hoof_placement.y - lower_radius*2, hoof_placement.z - lower_radius))
    hoof = hoof_base.cut(split_box)
    
    # Combine parts
    leg = upper_leg.fuse(knee_joint)
    leg = leg.fuse(cannon)
    leg = leg.fuse(fetlock_joint)
    leg = leg.fuse(pastern)
    leg = leg.fuse(hoof)
    
    return leg

# Start modeling the cow
# Body dimensions
body_length = 100
body_width = 40
body_height = 35

# Body - create a more anatomically correct body
body_center = App.Vector(0, 0, 40)
body = create_ellipsoid(body_center, (body_length/2, body_width/2, body_height/2))

# Create a more defined chest area
chest = create_ellipsoid(
    App.Vector(body_length/2 - 10, 0, body_center.z - 2),
    (body_length/8, body_width/2.1, body_height/1.9)
)
body = body.fuse(chest)

# Create more defined hindquarters
hindquarters = create_ellipsoid(
    App.Vector(-body_length/2 + 15, 0, body_center.z),
    (body_length/7, body_width/1.9, body_height/2.1)
)
body = body.fuse(hindquarters)

# Spine ridge
spine_ridge = create_ellipsoid(
    App.Vector(0, 0, body_center.z + body_height/2 - 2),
    (body_length/2 - 10, 5, 3)
)
body = body.fuse(spine_ridge)

# Neck - make it more curved and natural
neck_base = App.Vector(body_length/2 - 5, 0, body_center.z + 5)
neck_top = App.Vector(body_length/2 + 8, 0, body_center.z + body_height/2 + 15)
neck_control = App.Vector(body_length/2 + 5, 0, body_center.z + body_height/2 + 5)

# Create a more natural curved neck using multiple ellipsoids
neck_sections = []
neck_steps = 5
for i in range(neck_steps):
    t = i / (neck_steps - 1)
    # Quadratic Bezier curve for better neck curve
    x = (1-t)*(1-t)*neck_base.x + 2*(1-t)*t*neck_control.x + t*t*neck_top.x
    y = (1-t)*(1-t)*neck_base.y + 2*(1-t)*t*neck_control.y + t*t*neck_top.y
    z = (1-t)*(1-t)*neck_base.z + 2*(1-t)*t*neck_control.z + t*t*neck_top.z
    
    # Neck tapers toward the head
    radius = 12 - 4 * t
    
    section = create_ellipsoid(
        App.Vector(x, y, z),
        (radius, radius, 4 + 2 * t)
    )
    neck_sections.append(section)

# Fuse all neck sections
neck = neck_sections[0]
for section in neck_sections[1:]:
    neck = neck.fuse(section)

# Create neck muscles (dewlap)
dewlap = create_ellipsoid(
    App.Vector(body_length/2, 0, body_center.z - 5),
    (15, 10, 12)
)
neck = neck.fuse(dewlap)

# Head - more detailed cow head
head_center = App.Vector(body_length/2 + 20, 0, body_center.z + body_height/2 + 25)
head = create_ellipsoid(head_center, (18, 14, 14))

# Create forehead bump (common in cattle)
forehead_bump = create_ellipsoid(
    App.Vector(head_center.x - 2, head_center.y, head_center.z + 7),
    (10, 8, 5)
)
head = head.fuse(forehead_bump)

# Snout - more detailed with better proportions
snout_center = App.Vector(head_center.x + 15, 0, head_center.z - 5)
snout = create_ellipsoid(snout_center, (12, 9, 7))

# Add muzzle detail
muzzle = create_ellipsoid(
    App.Vector(snout_center.x + 8, 0, snout_center.z),
    (4, 7, 6)
)
snout = snout.fuse(muzzle)

# Ears - more realistic shape
left_ear_center = App.Vector(head_center.x - 8, head_center.y + 15, head_center.z + 8)
left_ear_base = create_ellipsoid(left_ear_center, (5, 3, 8))
# Add ear flap
left_ear_flap = create_ellipsoid(
    App.Vector(left_ear_center.x, left_ear_center.y + 5, left_ear_center.z + 5),
    (8, 2, 10)
)
left_ear = left_ear_base.fuse(left_ear_flap)

right_ear_center = App.Vector(head_center.x - 8, head_center.y - 15, head_center.z + 8)
right_ear_base = create_ellipsoid(right_ear_center, (5, 3, 8))
right_ear_flap = create_ellipsoid(
    App.Vector(right_ear_center.x, right_ear_center.y - 5, right_ear_center.z + 5),
    (8, 2, 10)
)
right_ear = right_ear_base.fuse(right_ear_flap)

# Eyes - more detailed with eyelids
left_eye_center = App.Vector(head_center.x + 12, head_center.y + 9, head_center.z + 3)
left_eye = create_ellipsoid(left_eye_center, (2.5, 1.5, 1.5))
# Eye socket
left_eye_socket = create_ellipsoid(left_eye_center, (3, 2.5, 2))
left_eye_socket = left_eye_socket.cut(left_eye)
left_eye_area = left_eye.fuse(left_eye_socket)

right_eye_center = App.Vector(head_center.x + 12, head_center.y - 9, head_center.z + 3)
right_eye = create_ellipsoid(right_eye_center, (2.5, 1.5, 1.5))
right_eye_socket = create_ellipsoid(right_eye_center, (3, 2.5, 2))
right_eye_socket = right_eye_socket.cut(right_eye)
right_eye_area = right_eye.fuse(right_eye_socket)

# Nostrils - more realistic oval shape
left_nostril_center = App.Vector(snout_center.x + 10, snout_center.y + 3.5, snout_center.z)
left_nostril = create_ellipsoid(left_nostril_center, (1, 2, 1.5))
# Create actual hole by cutting
nostril_cut_l = create_ellipsoid(left_nostril_center, (0.8, 1.8, 1.3))
left_nostril = left_nostril.cut(nostril_cut_l)

right_nostril_center = App.Vector(snout_center.x + 10, snout_center.y - 3.5, snout_center.z)
right_nostril = create_ellipsoid(right_nostril_center, (1, 2, 1.5))
nostril_cut_r = create_ellipsoid(right_nostril_center, (0.8, 1.8, 1.3))
right_nostril = right_nostril.cut(nostril_cut_r)

# Add mouth line
mouth_line = create_box(
    8, 
    12, 
    0.5,
    App.Vector(snout_center.x + 4, -6, snout_center.z - 3)
)
mouth_line = mouth_line.makeFillet(0.2, mouth_line.Edges)

# Legs - more realistic with joints
leg_length = 35  # Slightly longer for better proportions

# Front legs - position slightly wider apart
front_left_leg = create_leg(App.Vector(body_length/2 - 15, body_width/2 - 3, body_center.z - body_height/2), leg_length)
front_right_leg = create_leg(App.Vector(body_length/2 - 15, -body_width/2 + 3, body_center.z - body_height/2), leg_length)

# Back legs - slightly different shape than front legs
def create_back_leg(placement, length=35):
    """Create a back cow leg with different joint angles"""
    # Upper leg (thigh) - slightly thicker
    upper_radius = 6
    lower_radius = 3.5
    
    upper_leg = create_cylinder(upper_radius, length * 0.35, placement, (0.1, 0, -1))
    
    # Knee joint
    knee_placement = App.Vector(placement.x + length * 0.035, placement.y, placement.z - length * 0.35)
    knee_joint = create_ellipsoid(App.Vector(0,0,0), (upper_radius*1.2, upper_radius*1.2, upper_radius), knee_placement)
    
    # Lower leg placement - slight angle
    lower_placement = App.Vector(knee_placement.x - length * 0.02, knee_placement.y, knee_placement.z - length * 0.02)
    
    # Lower leg (shin)
    lower_leg = create_cylinder(lower_radius, length * 0.65, lower_placement, (-0.05, 0, -1))
    
    # Ankle joint
    ankle_placement = App.Vector(lower_placement.x - length * 0.03, lower_placement.y, lower_placement.z - length * 0.63)
    ankle_joint = create_ellipsoid(App.Vector(0,0,0), (lower_radius*1.3, lower_radius*1.3, lower_radius*0.9), ankle_placement)
    
    # Hoof placement
    hoof_placement = App.Vector(ankle_placement.x, ankle_placement.y, ankle_placement.z - lower_radius * 2)
    
    # Hoof - make it more detailed with a split
    hoof_base = create_ellipsoid(App.Vector(0,0,0), (lower_radius*1.5, lower_radius*2, lower_radius*0.8), hoof_placement)
    
    # Create a split in the hoof
    split_box = create_box(lower_radius*0.5, lower_radius*4, lower_radius*2, 
                         App.Vector(hoof_placement.x - lower_radius*0.25, hoof_placement.y - lower_radius*2, hoof_placement.z - lower_radius))
    hoof = hoof_base.cut(split_box)
    
    # Combine parts
    leg = upper_leg.fuse(knee_joint)
    leg = leg.fuse(lower_leg)
    leg = leg.fuse(ankle_joint)
    leg = leg.fuse(hoof)
    
    return leg

back_left_leg = create_back_leg(App.Vector(-body_length/2 + 18, body_width/2 - 3, body_center.z - body_height/2))
back_right_leg = create_back_leg(App.Vector(-body_length/2 + 18, -body_width/2 + 3, body_center.z - body_height/2))

# Tail - simpler version but still realistic
tail_base = App.Vector(-body_length/2 + 2, 0, body_center.z + 2)
tail_sections = []

# Create curved tail with multiple sections and improved connection
sections = 10
section_length = 4.5
total_length = section_length * sections

# Create a continuous curve for tail so pieces connect properly
for i in range(sections):
    t = i / (sections - 1)
    # Use a sine curve for a natural S-shape
    angle = t * math.pi * 0.8
    x_offset = -total_length * 0.6 * t
    z_offset = total_length * 0.3 * math.sin(angle)
    
    # Tail tapers until tuft
    if i < sections - 1:
        radius = 3 - (1.8 * i / (sections - 1))
    else:
        radius = 2.5  # Slightly thicker at tuft
    
    section = create_cylinder(
        radius, 
        section_length * 0.95,  # Slight overlap between sections
        App.Vector(tail_base.x + x_offset, tail_base.y, tail_base.z + z_offset),
        direction=(
            -math.cos(angle) if i < sections - 1 else 0, 
            0, 
            math.sin(angle) if i < sections - 1 else 1
        )
    )
    tail_sections.append(section)

# Create tail tuft at the end
tuft_placement = App.Vector(
    tail_base.x - total_length * 0.6,
    tail_base.y,
    tail_base.z + total_length * 0.05
)
tail_tuft = create_ellipsoid(tuft_placement, (4, 4, 5))
tail_sections.append(tail_tuft)

# Fuse all tail sections
tail = tail_sections[0]
for section in tail_sections[1:]:
    tail = tail.fuse(section)

# Udder - more anatomically correct
udder_center = App.Vector(-body_length/3, 0, body_center.z - body_height/2 + 5)
udder_main = create_ellipsoid(
    udder_center,
    (12, 11, 10)
)

# Add udder texture/divisions
udder_divide = create_box(
    1, 
    22, 
    12, 
    App.Vector(udder_center.x, -11, udder_center.z - 6)
)
udder = udder_main.cut(udder_divide)

# Teats with better shape and placement
teats = []
teat_positions = [
    (-body_length/3 - 6, 5, -3),
    (-body_length/3 - 6, -5, -3),
    (-body_length/3 + 2, 5, -3),
    (-body_length/3 + 2, -5, -3)
]

for pos in teat_positions:
    # Base of teat
    teat_base = create_cylinder(
        2, 
        3, 
        App.Vector(pos[0], pos[1], body_center.z - body_height/2 + pos[2])
    )
    
    # Tip of teat
    teat_tip = create_cylinder(
        1.5, 
        2, 
        App.Vector(pos[0], pos[1], body_center.z - body_height/2 + pos[2] - 3)
    )
    
    # End cap
    teat_end = create_ellipsoid(
        App.Vector(0,0,0),
        (1.5, 1.5, 1),
        App.Vector(pos[0], pos[1], body_center.z - body_height/2 + pos[2] - 5)
    )
    
    teat = teat_base.fuse(teat_tip).fuse(teat_end)
    teats.append(teat)

# Fuse all teats to udder
for teat in teats:
    udder = udder.fuse(teat)

# Add anatomical features to male/female cattle
# Navel - visible on the underside
navel = create_ellipsoid(
    App.Vector(body_length/6, 0, body_center.z - body_height/2 + 3),
    (5, 3, 1.5)
)

# Combine all parts to create the cow
cow = body.fuse(neck)
cow = cow.fuse(head)
cow = cow.fuse(snout)
cow = cow.fuse(left_ear)
cow = cow.fuse(right_ear)
cow = cow.fuse(left_eye_area)
cow = cow.fuse(right_eye_area)
cow = cow.fuse(left_nostril)
cow = cow.fuse(right_nostril)
cow = cow.fuse(mouth_line)
cow = cow.fuse(front_left_leg)
cow = cow.fuse(front_right_leg)
cow = cow.fuse(back_left_leg)
cow = cow.fuse(back_right_leg)
cow = cow.fuse(tail)
cow = cow.fuse(udder)
cow = cow.fuse(navel)

# Create a more realistic cow surface with subtle contours
# Add muscle definition to the body
shoulder_muscle = create_ellipsoid(
    App.Vector(body_length/3, 0, body_center.z + 5),
    (body_length/8, body_width/2.2, body_height/2.5)
)
cow = cow.fuse(shoulder_muscle)

# Add hip muscles
hip_muscle = create_ellipsoid(
    App.Vector(-body_length/3, 0, body_center.z + 5),
    (body_length/7, body_width/2.2, body_height/2.5)
)
cow = cow.fuse(hip_muscle)

# Add back ridge - use a different approach to avoid fillet errors
back_ridge = create_ellipsoid(
    App.Vector(0, 0, body_center.z + body_height/2 - 1),
    (body_length * 0.35, 2.5, 1.5)
)
cow = cow.fuse(back_ridge)

# Create Part objects with labels for each component
# We'll create separate objects for each body part for better labeling

# Main body
body_obj = doc.addObject("Part::Feature", "Body")
body_obj.Shape = body
body_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)  # Warm brown color

# Neck
neck_obj = doc.addObject("Part::Feature", "Neck")
neck_obj.Shape = neck
neck_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

# Head components
head_obj = doc.addObject("Part::Feature", "Head")
head_obj.Shape = head
head_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

snout_obj = doc.addObject("Part::Feature", "Snout")
snout_obj.Shape = snout
snout_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

left_ear_obj = doc.addObject("Part::Feature", "LeftEar")
left_ear_obj.Shape = left_ear
left_ear_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

right_ear_obj = doc.addObject("Part::Feature", "RightEar")
right_ear_obj.Shape = right_ear
right_ear_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

left_eye_obj = doc.addObject("Part::Feature", "LeftEye")
left_eye_obj.Shape = left_eye
left_eye_obj.ViewObject.ShapeColor = (0.1, 0.1, 0.1)  # Dark eye color

right_eye_obj = doc.addObject("Part::Feature", "RightEye")
right_eye_obj.Shape = right_eye
right_eye_obj.ViewObject.ShapeColor = (0.1, 0.1, 0.1)  # Dark eye color

left_nostril_obj = doc.addObject("Part::Feature", "LeftNostril")
left_nostril_obj.Shape = left_nostril
left_nostril_obj.ViewObject.ShapeColor = (0.7, 0.55, 0.4)  # Slightly darker

right_nostril_obj = doc.addObject("Part::Feature", "RightNostril")
right_nostril_obj.Shape = right_nostril
right_nostril_obj.ViewObject.ShapeColor = (0.7, 0.55, 0.4)

mouth_obj = doc.addObject("Part::Feature", "Mouth")
mouth_obj.Shape = mouth_line
mouth_obj.ViewObject.ShapeColor = (0.7, 0.55, 0.4)

# Legs
front_left_leg_obj = doc.addObject("Part::Feature", "FrontLeftLeg")
front_left_leg_obj.Shape = front_left_leg
front_left_leg_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

front_right_leg_obj = doc.addObject("Part::Feature", "FrontRightLeg")
front_right_leg_obj.Shape = front_right_leg
front_right_leg_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

back_left_leg_obj = doc.addObject("Part::Feature", "BackLeftLeg")
back_left_leg_obj.Shape = back_left_leg
back_left_leg_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

back_right_leg_obj = doc.addObject("Part::Feature", "BackRightLeg")
back_right_leg_obj.Shape = back_right_leg
back_right_leg_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

# Tail
tail_obj = doc.addObject("Part::Feature", "Tail")
tail_obj.Shape = tail
tail_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

# Udder and related parts
udder_obj = doc.addObject("Part::Feature", "Udder")
udder_obj.Shape = udder
udder_obj.ViewObject.ShapeColor = (0.95, 0.8, 0.7)  # Lighter color for udder

# Navel
navel_obj = doc.addObject("Part::Feature", "Navel")
navel_obj.Shape = navel
navel_obj.ViewObject.ShapeColor = (0.7, 0.55, 0.4)

# Muscles
shoulder_muscle_obj = doc.addObject("Part::Feature", "ShoulderMuscle")
shoulder_muscle_obj.Shape = shoulder_muscle
shoulder_muscle_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

hip_muscle_obj = doc.addObject("Part::Feature", "HipMuscle")
hip_muscle_obj.Shape = hip_muscle
hip_muscle_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

back_ridge_obj = doc.addObject("Part::Feature", "BackRidge")
back_ridge_obj.Shape = back_ridge
back_ridge_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

# Create a spherical cow approximation
# Calculate approximate volume of realistic cow
realistic_cow_volume = body.Volume + neck.Volume + head.Volume + snout.Volume + \
                       left_ear.Volume + right_ear.Volume + \
                       front_left_leg.Volume + front_right_leg.Volume + \
                       back_left_leg.Volume + back_right_leg.Volume + \
                       tail.Volume + udder.Volume

# Create a sphere with equivalent volume
sphere_radius = (3 * realistic_cow_volume / (4 * math.pi))**(1/3)
spherical_cow = Part.makeSphere(sphere_radius)
spherical_cow.translate(App.Vector(body_length + sphere_radius + 20, 0, sphere_radius))

spherical_cow_obj = doc.addObject("Part::Feature", "SphericalCow")
spherical_cow_obj.Shape = spherical_cow
spherical_cow_obj.ViewObject.ShapeColor = (0.8, 0.65, 0.5)

# Calculate and display properties for comparison
realistic_cow_surface_area = body.Area + neck.Area + head.Area + snout.Area + \
                            left_ear.Area + right_ear.Area + \
                            front_left_leg.Area + front_right_leg.Area + \
                            back_left_leg.Area + back_right_leg.Area + \
                            tail.Area + udder.Area
                            
spherical_cow_volume = spherical_cow.Volume
spherical_cow_surface_area = spherical_cow.Area

# Calculate surface area to volume ratios
realistic_cow_sa_to_vol = realistic_cow_surface_area / realistic_cow_volume
spherical_cow_sa_to_vol = spherical_cow_surface_area / spherical_cow_volume

# Calculate approximate projected areas for drag force calculations
# Front, side, and top projections for the realistic cow
realistic_cow_frontal_area = body_width * body_height * 0.7  # Frontal area (approximate)
realistic_cow_side_area = body_length * body_height * 0.7    # Side area (approximate)
realistic_cow_top_area = body_length * body_width * 0.8      # Top area (approximate)

# For spherical cow, projected area is the same in all directions
spherical_cow_projected_area = math.pi * sphere_radius**2

# Estimate drag forces (assuming constant drag coefficient and fluid density)
# For different flow velocities: v = 1, 5, 10, 15, 20 m/s
velocities = [1, 5, 10, 15, 20]
fluid_density = 1.225  # kg/m³ (air at sea level)
drag_coefficient = 0.8  # Approximate for cow-like shape

# Create lists to store the drag forces
realistic_frontal_drag = []
realistic_side_drag = []
realistic_top_drag = []
spherical_drag = []

for v in velocities:
    # Convert areas from mm² to m²
    area_conv_factor = 1e-6  # mm² to m²
    
    # Calculate drag forces (F = 0.5 * rho * v² * Cd * A)
    r_front = 0.5 * fluid_density * v**2 * drag_coefficient * (realistic_cow_frontal_area * area_conv_factor)
    r_side = 0.5 * fluid_density * v**2 * drag_coefficient * (realistic_cow_side_area * area_conv_factor)
    r_top = 0.5 * fluid_density * v**2 * drag_coefficient * (realistic_cow_top_area * area_conv_factor)
    s_drag = 0.5 * fluid_density * v**2 * drag_coefficient * (spherical_cow_projected_area * area_conv_factor)
    
    realistic_frontal_drag.append(r_front)
    realistic_side_drag.append(r_side)
    realistic_top_drag.append(r_top)
    spherical_drag.append(s_drag)

# Calculate moment of inertia (simplified approximation)
# For realistic cow, use approximation of ellipsoid
a = body_length/2
b = body_width/2
c = body_height/2
cow_mass = realistic_cow_volume * 1e-9 * 1000  # Assume density of 1000 kg/m³, converting mm³ to m³

# Moment of inertia for ellipsoid around x, y, z axes
I_x_realistic = (1/5) * cow_mass * (b**2 + c**2)
I_y_realistic = (1/5) * cow_mass * (a**2 + c**2)
I_z_realistic = (1/5) * cow_mass * (a**2 + b**2)

# For spherical cow, moment of inertia is the same around all axes
sphere_mass = spherical_cow_volume * 1e-9 * 1000  # Same density assumption
I_sphere = (2/5) * sphere_mass * sphere_radius**2

# Calculate heat dissipation rate (proportional to surface area)
# Assume temperature difference and heat transfer coefficient are the same
heat_dissipation_ratio = spherical_cow_surface_area / realistic_cow_surface_area

# Create objects to display in the model tree
# We'll use compound objects to group the cow parts
realistic_cow_group = doc.addObject("App::DocumentObjectGroup", "RealisticCow")
spherical_cow_group = doc.addObject("App::DocumentObjectGroup", "SphericalCowModel")

# Add all the parts to the realistic cow group
realistic_cow_group.addObject(body_obj)
realistic_cow_group.addObject(neck_obj)
realistic_cow_group.addObject(head_obj)
realistic_cow_group.addObject(snout_obj)
realistic_cow_group.addObject(left_ear_obj)
realistic_cow_group.addObject(right_ear_obj)
realistic_cow_group.addObject(left_eye_obj)
realistic_cow_group.addObject(right_eye_obj)
realistic_cow_group.addObject(left_nostril_obj)
realistic_cow_group.addObject(right_nostril_obj)
realistic_cow_group.addObject(mouth_obj)
realistic_cow_group.addObject(front_left_leg_obj)
realistic_cow_group.addObject(front_right_leg_obj)
realistic_cow_group.addObject(back_left_leg_obj)
realistic_cow_group.addObject(back_right_leg_obj)
realistic_cow_group.addObject(tail_obj)
realistic_cow_group.addObject(udder_obj)
realistic_cow_group.addObject(navel_obj)
realistic_cow_group.addObject(shoulder_muscle_obj)
realistic_cow_group.addObject(hip_muscle_obj)
realistic_cow_group.addObject(back_ridge_obj)

# Add the spherical cow to its group
spherical_cow_group.addObject(spherical_cow_obj)

# Create a spreadsheet with the comparison data
sheet = doc.addObject('Spreadsheet::Sheet', 'CowComparison')

# Set up headers
sheet.set('A1', 'Property')
sheet.set('B1', 'Realistic Cow')
sheet.set('C1', 'Spherical Cow')
sheet.set('D1', 'Ratio (Spherical/Realistic)')

# Add data rows
sheet.set('A2', 'Volume (mm³)')
sheet.set('B2', str(round(realistic_cow_volume, 2)))
sheet.set('C2', str(round(spherical_cow_volume, 2)))
sheet.set('D2', str(round(spherical_cow_volume/realistic_cow_volume, 4)))

sheet.set('A3', 'Surface Area (mm²)')
sheet.set('B3', str(round(realistic_cow_surface_area, 2)))
sheet.set('C3', str(round(spherical_cow_surface_area, 2)))
sheet.set('D3', str(round(spherical_cow_surface_area/realistic_cow_surface_area, 4)))

sheet.set('A4', 'Surface/Volume Ratio (mm⁻¹)')
sheet.set('B4', str(round(realistic_cow_sa_to_vol, 4)))
sheet.set('C4', str(round(spherical_cow_sa_to_vol, 4)))
sheet.set('D4', str(round(spherical_cow_sa_to_vol/realistic_cow_sa_to_vol, 4)))

sheet.set('A5', 'Frontal Area (mm²)')
sheet.set('B5', str(round(realistic_cow_frontal_area, 2)))
sheet.set('C5', str(round(spherical_cow_projected_area, 2)))
sheet.set('D5', str(round(spherical_cow_projected_area/realistic_cow_frontal_area, 4)))

sheet.set('A6', 'Side Area (mm²)')
sheet.set('B6', str(round(realistic_cow_side_area, 2)))
sheet.set('C6', str(round(spherical_cow_projected_area, 2)))
sheet.set('D6', str(round(spherical_cow_projected_area/realistic_cow_side_area, 4)))

sheet.set('A7', 'Top Area (mm²)')
sheet.set('B7', str(round(realistic_cow_top_area, 2)))
sheet.set('C7', str(round(spherical_cow_projected_area, 2)))
sheet.set('D7', str(round(spherical_cow_projected_area/realistic_cow_top_area, 4)))

sheet.set('A9', 'Mass (kg)')
sheet.set('B9', str(round(cow_mass, 2)))
sheet.set('C9', str(round(sphere_mass, 2)))
sheet.set('D9', str(round(sphere_mass/cow_mass, 4)))

sheet.set('A10', 'Moment of Inertia X (kg·m²)')
sheet.set('B10', str(round(I_x_realistic, 4)))
sheet.set('C10', str(round(I_sphere, 4)))
sheet.set('D10', str(round(I_sphere/I_x_realistic, 4)))

sheet.set('A11', 'Moment of Inertia Y (kg·m²)')
sheet.set('B11', str(round(I_y_realistic, 4)))
sheet.set('C11', str(round(I_sphere, 4)))
sheet.set('D11', str(round(I_sphere/I_y_realistic, 4)))

sheet.set('A12', 'Moment of Inertia Z (kg·m²)')
sheet.set('B12', str(round(I_z_realistic, 4)))
sheet.set('C12', str(round(I_sphere, 4)))
sheet.set('D12', str(round(I_sphere/I_z_realistic, 4)))

sheet.set('A14', 'Heat Dissipation Ratio')
sheet.set('C14', str(round(heat_dissipation_ratio, 4)))

# Format the spreadsheet - fix the style setting syntax
for i in range(1, 15):
    sheet.setStyle('A'+str(i), 'bold|italic', 'add')
sheet.setStyle('A1:D1', 'bold|underline', 'add')

# Set column widths
sheet.setColumnWidth('A', 200)
sheet.setColumnWidth('B', 150)
sheet.setColumnWidth('C', 150)
sheet.setColumnWidth('D', 200)

# Create named aliases for cells (using underscore naming convention)
# Volume data
sheet.setAlias('B2', 'realistic_cow_volume')
sheet.setAlias('C2', 'spherical_cow_volume')
sheet.setAlias('D2', 'volume_ratio')

# Surface area data
sheet.setAlias('B3', 'realistic_cow_surface_area')
sheet.setAlias('C3', 'spherical_cow_surface_area')
sheet.setAlias('D3', 'surface_area_ratio')

# Surface to volume ratio
sheet.setAlias('B4', 'realistic_cow_sa_vol_ratio')
sheet.setAlias('C4', 'spherical_cow_sa_vol_ratio')
sheet.setAlias('D4', 'sa_vol_ratio_comparison')

# Projected areas
sheet.setAlias('B5', 'realistic_cow_frontal_area')
sheet.setAlias('C5', 'spherical_cow_frontal_area')
sheet.setAlias('D5', 'frontal_area_ratio')

sheet.setAlias('B6', 'realistic_cow_side_area')
sheet.setAlias('C6', 'spherical_cow_side_area')
sheet.setAlias('D6', 'side_area_ratio')

sheet.setAlias('B7', 'realistic_cow_top_area')
sheet.setAlias('C7', 'spherical_cow_top_area')
sheet.setAlias('D7', 'top_area_ratio')

# Mass data
sheet.setAlias('B9', 'realistic_cow_mass')
sheet.setAlias('C9', 'spherical_cow_mass')
sheet.setAlias('D9', 'mass_ratio')

# Moment of inertia
sheet.setAlias('B10', 'realistic_cow_moi_x')
sheet.setAlias('C10', 'spherical_cow_moi_x')
sheet.setAlias('D10', 'moi_x_ratio')

sheet.setAlias('B11', 'realistic_cow_moi_y')
sheet.setAlias('C11', 'spherical_cow_moi_y')
sheet.setAlias('D11', 'moi_y_ratio')

sheet.setAlias('B12', 'realistic_cow_moi_z')
sheet.setAlias('C12', 'spherical_cow_moi_z')
sheet.setAlias('D12', 'moi_z_ratio')

# Heat dissipation
sheet.setAlias('C14', 'heat_dissipation_ratio')

# Create velocity vs drag plots using Python's matplotlib
# We'll save images to files and then display them in FreeCAD

import matplotlib.pyplot as plt
import os

# Plot drag force vs velocity
plt.figure(figsize=(10, 6))
plt.plot(velocities, realistic_frontal_drag, 'b-', label='Realistic Cow (Front)')
plt.plot(velocities, realistic_side_drag, 'g-', label='Realistic Cow (Side)')
plt.plot(velocities, realistic_top_drag, 'r-', label='Realistic Cow (Top)')
plt.plot(velocities, spherical_drag, 'k--', label='Spherical Cow (All directions)')
plt.xlabel('Velocity (m/s)')
plt.ylabel('Drag Force (N)')
plt.title('Drag Force vs Velocity')
plt.grid(True)
plt.legend()

# Save the plot to a file
plot_path = App.getUserAppDataDir() + '/drag_plot.png'
plt.savefig(plot_path)
plt.close()

# Create a bar chart for surface area to volume ratio
plt.figure(figsize=(8, 5))
plt.bar(['Realistic Cow', 'Spherical Cow'], [realistic_cow_sa_to_vol, spherical_cow_sa_to_vol])
plt.ylabel('Surface Area to Volume Ratio (mm⁻¹)')
plt.title('Surface Area to Volume Ratio Comparison')
plt.grid(True, axis='y')

# Save the plot to a file
ratio_plot_path = App.getUserAppDataDir() + '/ratio_plot.png'
plt.savefig(ratio_plot_path)
plt.close()

# Create a bar chart for moment of inertia comparison
plt.figure(figsize=(10, 6))
labels = ['X-axis', 'Y-axis', 'Z-axis']
realistic_moi = [I_x_realistic, I_y_realistic, I_z_realistic]
spherical_moi = [I_sphere, I_sphere, I_sphere]

x = range(len(labels))
width = 0.35

plt.bar([i - width/2 for i in x], realistic_moi, width, label='Realistic Cow')
plt.bar([i + width/2 for i in x], spherical_moi, width, label='Spherical Cow')
plt.xlabel('Rotation Axis')
plt.ylabel('Moment of Inertia (kg·m²)')
plt.title('Moment of Inertia Comparison')
plt.xticks(x, labels)
plt.legend()
plt.grid(True, axis='y')

# Save the plot to a file
moi_plot_path = App.getUserAppDataDir() + '/moi_plot.png'
plt.savefig(moi_plot_path)
plt.close()

# Print the paths to find the plots
print("\nPlots saved to:")
print(f"1. Drag Force vs Velocity: {plot_path}")
print(f"2. Surface Area to Volume Ratio: {ratio_plot_path}")
print(f"3. Moment of Inertia Comparison: {moi_plot_path}")

# Print comparison data to the console with scientific insights
print("\nComparison of Realistic Cow vs. Spherical Cow Model")
print("======================================================")
print(f"Realistic Cow Volume: {realistic_cow_volume:.2f} mm³")
print(f"Spherical Cow Volume: {spherical_cow_volume:.2f} mm³")
print(f"Realistic Cow Surface Area: {realistic_cow_surface_area:.2f} mm²")
print(f"Spherical Cow Surface Area: {spherical_cow_surface_area:.2f} mm²")
print(f"Surface Area Ratio (Spherical/Realistic): {spherical_cow_surface_area/realistic_cow_surface_area:.2f}")
print(f"Heat Dissipation Ratio: {heat_dissipation_ratio:.2f}")

print("\nEngineering Insights:")
print("1. A sphere has the minimum surface area for a given volume, explaining why")
print("   the spherical cow has approximately {:.0f}% of the surface area of the realistic cow.".format(heat_dissipation_ratio*100))
print("2. The realistic cow has a higher surface area to volume ratio, which would allow for better thermoregulation")
print("   but also higher heat loss in cold environments.")
print("3. Drag forces on the spherical cow are identical in all directions, whereas the realistic cow experiences")
print("   different drag forces depending on orientation, with {:0.1f}% more drag from the side than the front.".format(
      (realistic_side_drag[2]/realistic_frontal_drag[2]-1)*100))
print("4. The moment of inertia differences mean that the realistic cow would rotate more easily around some axes")
print("   than others, while the spherical cow has identical rotational inertia in all directions.")
print("5. The realistic cow's higher surface area would allow it to dissipate heat {:.1f}x faster than the".format(1/heat_dissipation_ratio))
print("   spherical cow, which has implications for metabolic efficiency and thermal regulation.")

# Compute and recompute
doc.recompute()

# Final view adjustments
App.activeDocument().recompute()
Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")

print("\nRealistic and spherical cow models created successfully!")
