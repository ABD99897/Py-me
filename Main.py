# اسم الملف: main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserListView
from yt_dlp import YoutubeDL
import os
import threading

class YouTubeDownloader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10

        # رابط الفيديو
        self.add_widget(Label(text="رابط الفيديو أو القائمة:"))
        self.url_input = TextInput()
        self.add_widget(self.url_input)

        # نوع التحميل
        self.add_widget(Label(text="نوع التحميل:"))
        self.type_spinner = Spinner(
            text='فيديو',
            values=('فيديو', 'صوت', 'قائمة تشغيل')
        )
        self.add_widget(self.type_spinner)

        # الجودة
        self.add_widget(Label(text="الجودة (افتراضي: best):"))
        self.quality_input = TextInput()
        self.add_widget(self.quality_input)

        # مجلد الحفظ
        self.add_widget(Label(text="مجلد الحفظ:"))
        self.folder_btn = Button(text="اختيار مجلد", on_press=self.browse_folder)
        self.add_widget(self.folder_btn)
        self.folder_path = ''

        # زر التحميل
        self.download_btn = Button(
            text="تحميل",
            background_color=(0, 1, 0, 1),
            on_press=self.start_download
        )
        self.add_widget(self.download_btn)

    def browse_folder(self, instance):
        self.file_chooser = FileChooserListView()
        self.file_chooser.bind(on_submit=self.select_folder)
        self.add_widget(self.file_chooser)

    def select_folder(self, instance, value, *args):
        self.folder_path = value[0]
        self.remove_widget(self.file_chooser)

    def download_thread(self):
        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([self.url_input.text])
            self.show_message("نجاح", "تم التحميل بنجاح!")
        except Exception as e:
            self.show_message("خطأ", f"حدث خطأ: {str(e)}")
        finally:
            self.download_btn.disabled = False

    def start_download(self, instance):
        url = self.url_input.text.strip()
        download_type = self.type_spinner.text
        quality = self.quality_input.text.strip()
        folder = self.folder_path

        if not url:
            self.show_message("تنبيه", "يرجى إدخال رابط الفيديو.")
            return

        # إعداد خيارات yt-dlp (مشابه للكود الأصلي)
        # ...

        self.download_btn.disabled = True
        threading.Thread(target=self.download_thread, daemon=True).start()

    def show_message(self, title, message):
        popup = BoxLayout(orientation='vertical')
        popup.add_widget(Label(text=message))
        close_btn = Button(text="إغلاق")
        popup.add_widget(close_btn)
        self.add_widget(popup)
        close_btn.bind(on_press=lambda x: self.remove_widget(popup))

class YouTubeApp(App):
    def build(self):
        return YouTubeDownloader()

if __name__ == '__main__':
    YouTubeApp().run()
