from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from nitro.view import NitroView  # Importing Nitro view
from roblox.view import RobloxView  # Placeholder for Roblox view


class MainApp(App):
    def build(self):
        self.title = 'Nitro and Roblox Checker'

        self.main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Spinner for view switching
        self.view_spinner = Spinner(
            text='Nitro',
            values=('Nitro', 'Roblox'),
            size_hint=(None, None),
            size=(150, 44),
            pos_hint={'right': 1}
        )
        self.view_spinner.bind(text=self.switch_view)

        top_bar_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        top_bar_layout.add_widget(Label(text="View:", size_hint=(0.9, 1)))
        top_bar_layout.add_widget(self.view_spinner)

        self.main_layout.add_widget(top_bar_layout)

        # Load the default Nitro view
        self.content_layout = BoxLayout(orientation='vertical', spacing=10)
        self.main_layout.add_widget(self.content_layout)
        self.switch_view(self.view_spinner, 'Nitro')

        return self.main_layout

    def switch_view(self, spinner, text):
        self.content_layout.clear_widgets()

        if text == 'Nitro':
            self.content_layout.add_widget(NitroView().build())  # Load Nitro view
        elif text == 'Roblox':
            self.content_layout.add_widget(RobloxView().build())  # Load placeholder view for Roblox


if __name__ == '__main__':
    MainApp().run()
