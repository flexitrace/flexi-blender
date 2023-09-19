import os
import bpy
import pandas as pd
from mathutils import Matrix

LOC_OR_GLOB = ["Local", "Global"]
OBJECT_NAME = "model"
ARMATURE_NAME = "Arm"
CSV_FILE = ".\\data\\sample.csv"
MATRIX_LOC_OR_GLOB = LOC_OR_GLOB[1]


def csv_to_animation2(obj, arm, csv_file, loc_or_glob):
    source_armature = bpy.data.objects[arm]
    object = bpy.data.objects[obj]
    blend_file = bpy.data.filepath
    blend_path = os.path.dirname(blend_file)
    df = pd.read_csv(os.path.join(blend_path, csv_file))
 
    frames = df['Frame_Order'].values
    frame_min, frame_max = frames.min(), frames.max()
    bone_names = df['Anchor_Name'].values
    
    cols = [f"{loc_or_glob}_Transform_col{col_idx}_{axis}"  
                for axis in "xyzw"
                for col_idx in range(4)]
    
    tuples = list(zip(*(df[col] for col in cols)))
    matrixes = [Matrix(tuple(t[i:i+4] for i in range(0, len(t), 4))) for t in tuples]
    matrix = list(zip(frames, bone_names, matrixes))

    bpy.context.scene.frame_start = int(frame_min)
    bpy.context.scene.frame_end = int(frame_max)

    for obj_modi in object.modifiers:
        if obj_modi.type == "ARMATURE":
            obj_modi.show_viewport = False

    for i in range(len(frames)):
        frame, bone_name, matrix_bone = matrix[i]
        bpy.context.scene.frame_set(frame)
        bone = source_armature.pose.bones[bone_name]

        if bone_name != "root":
            bone.matrix = matrix_bone
            bone.location = (0, 0, 0)
        else:
            bone.matrix = matrix_bone
            bone.keyframe_insert(data_path="location")
        
        bone.keyframe_insert(data_path="rotation_quaternion")

    for obj_modi in object.modifiers:
        if obj_modi.type == "ARMATURE":
            obj_modi.show_viewport = True

#### RUN FUNCTION ####
csv_to_animation2(
    OBJECT_NAME, 
    ARMATURE_NAME, 
    CSV_FILE, 
    MATRIX_LOC_OR_GLOB
    )