import bpy

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
    bpy.utils.register_class(LAPTOPMODE_PT_general_popover)
    bpy.types.TOPBAR_HT_upper_bar.prepend(view_header_gui)
def unregister():
    bpy.utils.unregister_class(LAPTOPMODE_PT_general_popover)
    bpy.types.TOPBAR_HT_upper_bar.remove(view_header_gui)
