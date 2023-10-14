import os
from collections import deque
from PyQt5.QtWidgets import (QApplication, QComboBox, QMainWindow, QFileDialog,
    QLabel, QFrame, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import (QIntValidator, QDoubleValidator, QKeySequence,
    QDrag)
from file_input import AudioFilesInput
from characters import CharacterDropdown
from misc import NumField, BoolField, ComboField
from preview import AudioPreviewWidget
from vcinterface import VCInterface
from pathlib import Path

class AbstractVCFrame(QFrame):
    vc_interface = VCInterface()
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

    def input_dict(self):
        return {}

    def postinit(self):
        self.push_button = QPushButton()
        self.layout.addWidget(self.push_button)
        self.push_button.clicked.connect(self.push_to_vc)

        self.output_preview = AudioPreviewWidget()
        self.layout.addWidget(self.preview)
        # then do things related to pushing

    def load_file_ext(self, file):
        assert hasattr(self, "audio_input")
        self.audio_input.load_files(files = [file])

    def push_to_vc(self):
        if hasattr(self, "text_input"):
            user_text = self.text_input.toPlainText()
        else:
            user_text = ""

        assert hasattr(self, "audio_input")

        if len(self.audio_input.files) == 0:
            return
        file_outputs = []
        for file in self.audio_input.files:
            output_file = AbstractVCFrame.vc_interface.input(
                options = self.input_dict,
                user_text = user_text, user_file = file,
                output_filename_cb = self.out_filename)
            file_outputs.append(output_file)

        self.output_preview.set_text("Preview - "+str(file_outputs[0]))
        self.output_preview.from_file(file_outputs[0])

    def out_filename(self, filename):
        return Path(filename).stem+".wav"

class ControllableTalkNetFrame(AbstractVCFrame):
    @property
    def id(self):
        return "controllable_talknet"

    def __init__(self):
        super().__init__()

        self.audio_input = AudioFilesInput()
        self.layout.addWidget(self.audio_input)

        self.layout.addWidget(QLabel("Text input"))
        self.text_input = QPlainTextEdit()
        self.layout.addWidget(self.text_input)

        self.character_dropdown = CharacterDropdown(self.id)
        self.layout.addWidget(self.character_dropdown)

        self.disable_reference_audio = BoolField("Disable reference audio")
        self.pitch_factor = NumField("Transpose", "0", QIntValidator(0,11))
        self.auto_tune = BoolField("Auto-tune")
        self.reduce_metallic_sound = BoolField("Reduce metallic sound")
        self.layout.addWidget(self.pitch_factor)
        self.layout.addWidget(self.disable_reference_audio)
        self.layout.addWidget(self.auto_tune)
        self.layout.addWidget(self.reduce_metallic_sound)
        self.postinit()

    def input_dict(self):
        return {
            'Architecture': self.id,
            'Character': self.character_dropdown.currentText(),
            'Disable Reference Audio': self.disable_reference_audio.value
            'Pitch Factor': int(self.pitch_factor.value),
            'Auto Tune': self.auto_tune.value,
            'Reduce Metallic Sound': self.reduce_metallic_sound.value}

    def out_filename(self, filename):
        return (f"{Path(filename).stem}_{self.pitch_factor.value}_"
            f"{self.character_dropdown.currentText()}.wav")

class SoVitsSvc3Frame(AbstractVCFrame):
    @property
    def id(self):
        return "so_vits_svc_3"

    def __init__(self):
        super().__init__()

        self.audio_input = AudioFilesInput()
        self.layout.addWidget(self.audio_input)

        self.character_dropdown = CharacterDropdown(self.id)
        self.layout.addWidget(self.character_dropdown)

        self.pitch_factor = NumField("Transpose", "0", QIntValidator(-36,36))
        self.layout.addWidget(self.pitch_factor)
        self.postinit()

    def input_dict(self):
        return {
            'Architecture': self.id,
            'Character': self.character_dropdown.currentText(),
            'Pitch Shift': int(self.pitch_factor.value)}

    def out_filename(self, filename):
        return (f"{Path(filename).stem}_{self.pitch_factor.value}_"
            f"{self.character_dropdown.currentText()}.wav")

class SoVitsSvc4Frame(AbstractVCFrame):
    @property
    def id(self):
        return "so_vits_svc_4"

    def __init__(self):
        super().__init__()
        
        self.audio_input = AudioFilesInput()
        self.layout.addWidget(self.audio_input)

        self.character_dropdown = CharacterDropdown(self.id)
        self.layout.addWidget(self.character_dropdown)

        self.pitch_factor = NumField("Transpose", "0", QIntValidator(-36,36))
        self.character_likeness = NumField("Character Similarity", "0.0",
           QDoubleValidator(0,1.0))
        self.noise_scale = NumField("Noise Scale", "0.0",
            QDoubleValidator(0,1.0))
        self.predict_pitch = BoolField("Predict pitch")
        self.reduce_hoarseness = BoolField("Reduce hoarseness")
        self.apply_nsf_hifigan = BoolField("Apply NSF-HiFiGAN")
        self.layout.addWidget(self.pitch_factor)
        self.layout.addWidget(self.character_likeness)
        self.layout.addWidget(self.predict_pitch)
        self.layout.addWidget(self.reduce_hoarseness)
        self.layout.addWidget(self.apply_nsf_hifigan)
        self.layout.addWidget(self.noise_scale)
        self.postinit()

    def input_dict(self):
        return {
            'Architecture': self.id,
            'Character': self.character_dropdown.currentText(),
            'Pitch Shift': int(self.pitch_factor.value),
            'Slice Length': 0,
            'Cross-Fade Length': 0,
            'Character Likeness': float(self.character_likeness.value),
            'Reduce Hoarseness': self.reduce_hoarseness.value,
            'Apply nsf_hifigan': self.apply_nsf_hifigan.value,
            "Noise Scale", float(self.noise_scale.value)}

    def out_filename(self, filename):
        return (f"{Path(filename).stem}_{self.pitch_factor.value}_"
            f"{self.character_dropdown.currentText()}.wav")

class SoVitsSvc5Frame(AbstractVCFrame):
    @property
    def id(self):
        return "so_vits_svc_5"

    def __init__(self):
        super().__init__()
        
        self.audio_input = AudioFilesInput()
        self.layout.addWidget(self.audio_input)

        self.character_dropdown = CharacterDropdown(self.id)
        self.layout.addWidget(self.character_dropdown)

        self.pitch_factor = NumField("Transpose", "0", QIntValidator(-36,36))
        self.layout.addWidget(self.pitch_factor)
        self.postinit()

    def input_dict(self):
        return {
            'Architecture': self.id,
            'Character': self.character_dropdown.currentText(),
            'Pitch Shift': int(self.pitch_factor.value)}

    def out_filename(self, filename):
        return (f"{Path(filename).stem}_{self.pitch_factor.value}_"
            f"{self.character_dropdown.currentText()}.wav")

class RVCFrame(AbstractVCFrame):
    @property
    def id(self):
        return "rvc"

    def __init__(self):
        super().__init__()

        self.audio_input = AudioFilesInput()
        self.layout.addWidget(self.audio_input)

        self.character_dropdown = CharacterDropdown(self.id)
        self.layout.addWidget(self.character_dropdown)

        self.pitch_factor = NumField("Transpose", "0", QIntValidator(-36,36))
        self.f0_extraction_method = ComboField("Pitch method", ["crepe",
        "harvest", "parselmouth"])
        self.filter_radius = NumField("Filter radius", "0",
            QIntValidator(0,20))
        self.character_likeness = NumField("Character Similarity", "0.0",
           QDoubleValidator(0,1.0))
        self.voice_envelope_mix_ratio = NumField("Voice Envelope Mix Ratio",
           "0.0", QDoubleValidator(0,1.0))
        self.voiceless_consonants_protection_ratio = NumField(
            "Voiceless Consonants Protection Ratio", "0.0",
            QDoubleValidator(0,1.0))

        self.layout.addWidget(self.pitch_factor)
        self.layout.addWidget(self.f0_extraction_method)
        self.layout.addWidget(self.filter_radius)
        self.layout.addWidget(self.character_likeness)
        self.layout.addWidget(self.voice_envelope_mix_ratio)
        self.layout.addWidget(self.voiceless_consonants_protection_ratio)
        self.postinit()

    def input_dict(self):
        return {
            'Architecture': self.id,
            'Character': self.character_dropdown.currentText(),
            'Pitch Shift': int(self.pitch_factor.value),
            'f0 Extraction Method': self.f0_extraction_method.value,
            'Index Ratio': float(self.character_likeness.value),
            'Voice Envelope Mix Ratio':
            float(self.voice_envelope_mix_ratio.value),
            'Voiceless Consonants Protection Ratio':
            float(self.voiceless_consonants_protection_ratio.value)}

    def out_filename(self, filename):
        return (f"{Path(filename).stem}_{self.pitch_factor.value}_"
            f"{self.character_dropdown.currentText()}.wav")
