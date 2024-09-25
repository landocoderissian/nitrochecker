import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.splitter import Splitter
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from tasks import generate_until_valid, keep_generating_until_stopped, check_existing_codes


class NitroGenApp(App):
    output_text = StringProperty('')
    valid_links = ListProperty([])
    webhook_url = StringProperty('')  # Store webhook URL
    stop_generating = False  # Flag to stop task

    def build(self):
        self.title = 'Nitro Generator and Checker'

        main_layout = BoxLayout(orientation='horizontal')

        # Left: Valid codes (with Splitter)
        valid_splitter = Splitter(sizable_from='right', size_hint=(0.3, 1))
        valid_box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        valid_scroll = ScrollView()
        self.valid_links_box = BoxLayout(orientation='vertical', size_hint_y=None)
        valid_scroll.add_widget(self.valid_links_box)
        valid_box.add_widget(Label(text="Valid Links Found"))
        valid_box.add_widget(valid_scroll)
        valid_splitter.add_widget(valid_box)
        main_layout.add_widget(valid_splitter)

        # Right: Output and buttons
        output_layout = BoxLayout(orientation='vertical', spacing=10)
        self.output_label = Label(size_hint_y=None, text_size=(800, None))
        scroll_output = ScrollView(size_hint=(1, 0.8))
        scroll_output.add_widget(self.output_label)

        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        start_button = Button(text='Start Task', on_release=self.show_task_popup)
        stop_button = Button(text='Stop Task', on_release=self.stop_task)
        settings_button = Button(text='Settings', on_release=self.show_settings_popup)
        button_layout.add_widget(start_button)
        button_layout.add_widget(stop_button)
        button_layout.add_widget(settings_button)

        output_layout.add_widget(scroll_output)
        output_layout.add_widget(button_layout)
        main_layout.add_widget(output_layout)

        return main_layout

    def show_task_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        task_spinner = Spinner(
            text='Select Task',
            values=('Generate and check N codes',
                    'Generate until N valid codes found',
                    'Keep generating until stopped',
                    'Check existing codes')
        )
        content.add_widget(Label(text='Select Task:'))
        content.add_widget(task_spinner)

        # Input for number of codes
        num_codes_input = TextInput(text='100', multiline=False, hint_text="Enter number of codes")
        content.add_widget(Label(text='Number of Codes:'))
        content.add_widget(num_codes_input)

        popup = Popup(title='Start Task', content=content, size_hint=(0.8, 0.4))
        start_button = Button(text='Start')
        cancel_button = Button(text='Cancel')
        content.add_widget(start_button)
        content.add_widget(cancel_button)

        start_button.bind(on_release=lambda x: self.start_task(task_spinner.text, int(num_codes_input.text), popup))
        cancel_button.bind(on_release=popup.dismiss)

        popup.open()

    def start_task(self, task_type, num_codes, popup):
        popup.dismiss()
        if task_type == 'Generate and check N codes':
            threading.Thread(target=self.run_nitro_check_task, args=(num_codes,)).start()
        elif task_type == 'Generate until N valid codes found':
            threading.Thread(target=generate_until_valid, args=(self, num_codes)).start()
        elif task_type == 'Keep generating until stopped':
            threading.Thread(target=keep_generating_until_stopped, args=(self,)).start()
        elif task_type == 'Check existing codes':
            self.show_check_existing_popup()

    def show_check_existing_popup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Option 1: File chooser
        file_chooser = FileChooserListView()
        content.add_widget(Label(text="Select File:"))
        content.add_widget(file_chooser)

        # Option 2: Paste codes manually
        codes_input = TextInput(hint_text="Paste your codes here", multiline=True)
        content.add_widget(Label(text="Or Paste Codes Manually:"))
        content.add_widget(codes_input)

        # Separator option
        separator_input = TextInput(text='\n', multiline=False, hint_text="Enter separator (default is newline)")
        content.add_widget(Label(text='Code Separator:'))
        content.add_widget(separator_input)

        popup = Popup(title='Check Existing Codes', content=content, size_hint=(0.8, 0.8))
        check_button = Button(text='Check')
        cancel_button = Button(text='Cancel')
        content.add_widget(check_button)
        content.add_widget(cancel_button)

        check_button.bind(on_release=lambda x: self.check_existing_codes(file_chooser.path, file_chooser.selection, codes_input.text, separator_input.text, popup))
        cancel_button.bind(on_release=popup.dismiss)

        popup.open()

    def check_existing_codes(self, path, file_selection, pasted_codes, separator, popup):
        popup.dismiss()

        # Use either file or pasted codes
        if file_selection:
            file_path = os.path.join(path, file_selection[0])
            threading.Thread(target=check_existing_codes, args=(self, file_path, separator)).start()
        elif pasted_codes:
            codes = pasted_codes.split(separator or '\n')
            threading.Thread(target=check_existing_codes, args=(self, codes)).start()

    def run_nitro_check_task(self, num_codes):
        from nitro_gen import NitroGen
        generator = NitroGen(update_output_callback=self.update_output, webhook_url=self.webhook_url)
        generator.run_async_check(num_codes)

    def stop_task(self, instance):
        self.stop_generating = True
        self.update_output("\nStopped generating codes.\n")

    def update_output(self, text):
        Clock.schedule_once(lambda dt: self._update_output(text))

    def _update_output(self, text):
        self.output_text += text
        self.output_label.text = self.output_text

    def update_valid_links(self, link):
        self.valid_links.append(link)
        Clock.schedule_once(lambda dt: self._update_valid_links())

    def _update_valid_links(self):
        self.valid_links_box.clear_widgets()
        for link in self.valid_links:
            link_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            link_label = Label(text=link, size_hint_x=0.8)
            self.valid_links_box.add_widget(link_label)

    def show_settings_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text='Enter Discord Webhook URL:')
        webhook_input = TextInput(text=self.webhook_url, multiline=False)
        content.add_widget(label)
        content.add_widget(webhook_input)

        save_button = Button(text='Save')
        cancel_button = Button(text='Cancel')
        content.add_widget(save_button)
        content.add_widget(cancel_button)

        popup = Popup(title='Settings', content=content, size_hint=(0.8, 0.4))
        cancel_button.bind(on_release=popup.dismiss)
        save_button.bind(on_release=lambda x: self.save_settings(webhook_input.text, popup))

        popup.open()

    def save_settings(self, webhook_url, popup):
        self.webhook_url = webhook_url
        popup.dismiss()


if __name__ == '__main__':
    NitroGenApp().run()
