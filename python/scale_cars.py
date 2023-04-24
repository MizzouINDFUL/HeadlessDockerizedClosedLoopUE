import unreal

for mesh in unreal.EditorLevelLibrary.get_all_level_actors():
    if mesh.get_actor_label() == "SM_Sedan_01a" or mesh.get_actor_label() == "SM_SUV_01a":
        #make a random scale between 0.5 and 1.5
        scale_unit = unreal.MathLibrary.random_float_in_range(0.5, 1.5)
        scale = unreal.Vector(scale_unit, scale_unit, scale_unit)
        #set the scale
        mesh.set_actor_scale3d(scale)
        
