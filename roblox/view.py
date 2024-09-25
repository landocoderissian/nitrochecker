from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class RobloxView:
    def build(self):
        layout = BoxLayout(orientation='vertical')
        coming_soon_label = Label(
            text="Roblox view is Coming Soon!",
            font_size=24,
            halign="center",
            valign="middle"
        )
        coming_soon_label.bind(size=coming_soon_label.setter('text_size'))
        layout.add_widget(coming_soon_label)
        return layout
