import bpy

class LAPTOPMODE_PT_tablet_ui(bpy.types.Panel):
    bl_label = "Tablet UI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tablet"

    def draw(self, context):
        scene = context.scene
        screen = context.screen

        layout = self.layout

        layout.scale_y = 3.0
        layout.scale_x = 1.5

        row = layout.row()
        row.operator("wm.open_mainfile", text="Open", icon="FILE_FOLDER")
        row.operator("wm.save_mainfile", text="Save", icon="DISK_DRIVE")

        row = layout.row()
        row.operator("ed.undo", text="Undo", icon="LOOP_BACK")
        row.operator("ed.redo", text="Redo", icon="LOOP_FORWARDS")

        row = layout.row(align=True)
        row.prop(scene.tool_settings, "use_keyframe_insert_auto", text="", icon="RADIOBUT_ON")
        row.prop(scene, "use_preview_range", text="", icon="PREVIEW_RANGE")
        row.prop(scene, "use_audio", text="", icon="PLAY_SOUND", invert_checkbox=True)
        row.separator()
        row.operator("anim.end_frame_set", text="Set Start")
        row.operator("anim.start_frame_set", text="Set End")

        row = layout.row(align=True)
        #row.scale_x = 1.5
        row.operator("screen.frame_jump", text="", icon='REW').end = False
        row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False
        row.operator("screen.frame_offset", text="", icon='FRAME_PREV').delta = -1
        if not screen.is_animation_playing:
            # if using JACK and A/V sync:
            #   hide the play-reversed button
            #   since JACK transport doesn't support reversed playback
            if scene.sync_mode == 'AUDIO_SYNC' and context.preferences.system.audio_device == 'JACK':
                row.scale_x = 2
                row.operator("screen.animation_play", text="", icon='PLAY')
                row.scale_x = 1
            else:
                row.operator("screen.animation_play", text="", icon='PLAY_REVERSE').reverse = True
                row.operator("screen.animation_play", text="", icon='PLAY')
        else:
            row.scale_x = 2
            row.operator("screen.animation_play", text="", icon='PAUSE')
            row.scale_x = 1
        row.operator("screen.frame_offset", text="", icon='FRAME_NEXT').delta = 1
        row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
        row.operator("screen.frame_jump", text="", icon='FF').end = True

class LAPTOPMODE_PT_general_popover(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Laptop"
    bl_ui_units_x = 12

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout=self.layout
        prefs = context.preferences

        col = layout.column(align=True)
        col.prop(prefs.view, "ui_scale")
        col.separator()
        col.prop(prefs.inputs, "use_emulate_numpad")
        col.prop(prefs.inputs, "use_numeric_input_advanced")
        col.separator()
        col.prop(prefs.inputs, "use_mouse_emulate_3_button")
        col.prop(prefs.inputs, "mouse_emulate_3_button_modifier", text="")


def view_header_gui(self, context):
    if context.region.alignment == 'RIGHT':
        row=self.layout.row(align=True)
        #row.label(text="", icon="AUTO")
        row.popover(panel="LAPTOPMODE_PT_general_popover", text="", icon="AUTO")

### REGISTER ---
def register():
    bpy.utils.register_class(LAPTOPMODE_PT_tablet_ui)
    bpy.utils.register_class(LAPTOPMODE_PT_general_popover)
    bpy.types.TOPBAR_HT_upper_bar.prepend(view_header_gui)
def unregister():
    bpy.utils.unregister_class(LAPTOPMODE_PT_tablet_ui)
    bpy.utils.unregister_class(LAPTOPMODE_PT_general_popover)
    bpy.types.TOPBAR_HT_upper_bar.remove(view_header_gui)
