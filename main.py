import os
import glob

import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.core.window import Window

try:
  long
except NameError:
  long = int

# Tamil vowels (Uyir Ezhuthu)
TAMIL_VOWELS = [
    "அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ", "ஃ"
]

# Tamil consonants (Mei Ezhuthu)
TAMIL_CONSONANTS = [
    "க", "ங", "ச", "ஞ", "ட", "ண", "த", "ந", "ப", "ம", "ய", "ர", "ல", "வ", "ழ", "ள", "ற", "ன"
]

class FlashCard:
    def __init__(self, l, r):
        self.lrange = l
        self.hrange = r
        self.current = self.lrange
        self.is_seq_or_rnd = 0  # 0=sequential, 1=random

    def next_seq(self):
        current = self.current
        if self.current >= self.hrange:
            self.current = self.lrange
        else:
            self.current += 1
        return current

    def next_rnd(self):
        self.current = random.randint(self.lrange, self.hrange)
        return self.current

    def next(self):
        if self.is_seq_or_rnd == 0:
            return self.next_seq()
        else:
            return self.next_rnd()

class TamtutApp(App):
    def build(self):
        self.is_v_or_c = 1      # 0 for vowels, 1 for consonants
        self.is_seq_or_rand = 0 # 0 for sequence, 1 for random

        self.vLetters = TAMIL_VOWELS
        self.cLetters = TAMIL_CONSONANTS
        self.flashCard = FlashCard(1, len(self.cLetters))

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Large Tamil character display
        self.letter_label = Label(
            text="", font_size=self.get_dynamic_font_size(), size_hint=(1, 0.6),
            font_name="fonts/Noto_Sans_Tamil/NotoSansTamil-VariableFont_wdth,wght.ttf"
        )
        main_layout.add_widget(self.letter_label)

        self.status = Label(text="Welcome!", size_hint=(1, 0.1))
        main_layout.add_widget(self.status)

        # Controls
        controls = BoxLayout(size_hint=(1, 0.1))
        self.next_btn = Button(text="Next Alphabet")
        self.next_btn.bind(on_press=self.show_next)
        controls.add_widget(self.next_btn)
        main_layout.add_widget(controls)

        # Toggles
        toggles = BoxLayout(size_hint=(1, 0.1))
        self.vowel_btn = ToggleButton(text="Vowels", group="vc", on_press=self.set_vowel, allow_no_selection=False)
        toggles.add_widget(self.vowel_btn)
        self.cons_btn = ToggleButton(text="Consonants", group="vc", on_press=self.set_consonant, state='down', allow_no_selection=False)
        toggles.add_widget(self.cons_btn)
        self.seq_btn = ToggleButton(text="Sequence", group="seqrand", on_press=self.set_seq, state='down', allow_no_selection=False)
        toggles.add_widget(self.seq_btn)
        self.rand_btn = ToggleButton(text="Random", group="seqrand", on_press=self.set_rand, allow_no_selection=False)
        toggles.add_widget(self.rand_btn)
        main_layout.add_widget(toggles)

        # Bind window resize for dynamic font
        Window.bind(on_resize=self.on_window_resize)

        self.show_next()
        return main_layout

    def get_dynamic_font_size(self):
        # Use a fraction of screen height for font size
        return Window.height * 0.5

    def on_window_resize(self, instance, width, height):
        self.letter_label.font_size = self.get_dynamic_font_size()

    def set_vowel(self, instance):
        self.is_v_or_c = 0
        self.flashCard.hrange = len(self.vLetters)
        self.status.text = "Now showing: Vowels"
        self.show_next()

    def set_consonant(self, instance):
        self.is_v_or_c = 1
        self.flashCard.hrange = len(self.cLetters)
        self.status.text = "Now showing: Consonants"
        self.show_next()

    def set_seq(self, instance):
        self.is_seq_or_rand = 0
        self.flashCard.is_seq_or_rnd = 0
        self.status.text = "Now in sequence mode"

    def set_rand(self, instance):
        self.is_seq_or_rand = 1
        self.flashCard.is_seq_or_rnd = 1
        self.status.text = "Now in random mode"

    def show_next(self, instance=None):
        letters = self.cLetters if self.is_v_or_c else self.vLetters
        pos = self.flashCard.next()
        # Clamp to available range
        idx = min(max(pos - 1, 0), len(letters) - 1)
        letter = letters[idx]
        self.letter_label.text = letter
        typetxt = "Consonant" if self.is_v_or_c else "Vowel"
        self.status.text = f"Type: {typetxt}, Pos: {idx+1} Letter: {letter}"

if __name__ == "__main__":
    TamtutApp().run()
