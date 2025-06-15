import os
import glob
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label

# to handle latest cython during bundling for android
try:
    long
except NameError:
    long = int

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class TamLetter:
    def __init__(self, t, p):
        self.type = t
        self.pos = p
        self.filename = os.path.join(BASE_DIR, "images", f"{self.type}{self.pos}.JPG")

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

def get_letters(letter_type):
    prefix = os.path.join(BASE_DIR, "images", f"{letter_type}*.JPG")
    files = sorted(glob.glob(prefix))
    letter_objs = []
    for f in files:
        p = os.path.basename(f).replace(".JPG", "").replace(letter_type, "")
        letter_objs.append(TamLetter(letter_type, p))
    return letter_objs

class TamtutApp(App):
    def build(self):
        self.is_v_or_c = 1      # 0 for vowels, 1 for consonants
        self.is_seq_or_rand = 0 # 0 for sequence, 1 for random

        self.vLetters = get_letters('v')
        self.cLetters = get_letters('c')
        self.flashCard = FlashCard(1, len(self.cLetters))

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.header = Image(source=os.path.join(BASE_DIR, "images", "header.JPG"), size_hint=(1, 0.3))
        main_layout.add_widget(self.header)

        self.img = Image(size_hint=(1, 0.5))
        main_layout.add_widget(self.img)

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

        self.show_next()

        return main_layout

    def set_vowel(self, instance):
        self.is_v_or_c = 0
        self.flashCard.hrange = len(self.vLetters)
        self.status.text = "Now showing: Vowels"

    def set_consonant(self, instance):
        self.is_v_or_c = 1
        self.flashCard.hrange = len(self.cLetters)
        self.status.text = "Now showing: Consonants"

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
        letter = next((x for x in letters if int(x.pos) == int(pos)), letters[0])
        self.img.source = letter.filename
        self.status.text = f"Type: {letter.type.upper()}, Pos: {letter.pos}"

if __name__ == "__main__":
    TamtutApp().run()
