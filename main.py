import base64
import json
import mimetypes
import os
import random
import sys
import traceback
import urllib.error
import urllib.request
from pathlib import Path

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QColor, QFont, QImage, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


BASE_DIR = Path(__file__).resolve().parent


def add_shadow(widget, blur=28, color=QColor(0, 0, 0, 95), y_offset=10):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setColor(color)
    shadow.setOffset(0, y_offset)
    widget.setGraphicsEffect(shadow)


def clamp(value, low=0, high=255):
    return max(low, min(high, int(value)))


def clean_reference_pixmap(pixmap):
    if pixmap.isNull():
        return pixmap
    width = pixmap.width()
    height = pixmap.height()
    top_crop = 0.12 if height >= width else 0.08
    bottom_crop = 0.2 if height >= width else 0.16
    side_crop = 0.04
    x = int(width * side_crop)
    y = int(height * top_crop)
    cropped_width = max(1, width - int(width * side_crop * 2))
    cropped_height = max(1, height - y - int(height * bottom_crop))
    cropped = pixmap.copy(x, y, cropped_width, cropped_height)
    return cropped if not cropped.isNull() else pixmap


class ChoiceButton(QPushButton):
    def __init__(self, text, accent="#42d6c7", active=False, min_height=38):
        super().__init__(text)
        self.accent = accent
        self.setCheckable(True)
        self.setChecked(active)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(min_height)
        self.refresh_style()

    def refresh_style(self):
        active = self.isChecked()
        border = self.accent if active else "#2f3440"
        background = "rgba(66, 214, 199, 0.18)" if active else "#171a21"
        foreground = "#effffc" if active else "#d4d9e2"
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {background};
                color: {foreground};
                border: 1px solid {border};
                border-radius: 12px;
                padding: 10px 14px;
                text-align: center;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                border-color: {self.accent};
            }}
            """
        )


class ToggleSwitch(QPushButton):
    def __init__(self, checked=False):
        super().__init__()
        self.setCheckable(True)
        self.setChecked(checked)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(48, 26)
        self.clicked.connect(self.refresh_style)
        self.refresh_style()

    def refresh_style(self, checked=False):
        background = "#42d6c7" if self.isChecked() else "#2a2f38"
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {background};
                border: none;
                border-radius: 13px;
            }}
            """
        )

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#eef6f8"))
        x_pos = 26 if self.isChecked() else 4
        painter.drawEllipse(x_pos, 4, 18, 18)


class PresetCard(QFrame):
    def __init__(self, key, title, subtitle, accent, source, image_path=""):
        super().__init__()
        self.setObjectName("presetCard")
        self.key = key
        self.title = title
        self.subtitle = subtitle
        self.accent = accent
        self.source = source
        self.image_path = image_path
        self.on_click = None
        self.active = False
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(154, 182)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        cover = QLabel()
        self.cover = cover
        cover.setFixedHeight(96)
        cover.setAlignment(Qt.AlignCenter)
        cover.setScaledContents(False)

        title_label = QLabel(title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("color:#f6f8fb; font-size:14px; font-weight:700;")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setWordWrap(True)
        subtitle_label.setStyleSheet("color:#98a0ae; font-size:11px;")
        source_label = QLabel(source)
        source_label.setWordWrap(True)
        source_label.setStyleSheet("color:#72dfd4; font-size:10px;")

        layout.addWidget(cover)
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(source_label)
        self.load_cover_image()
        self.refresh_style()

    def load_cover_image(self):
        pixmap = QPixmap(self.image_path) if self.image_path else QPixmap()
        if pixmap.isNull():
            self.cover.setPixmap(QPixmap())
            self.cover.setStyleSheet(
                f"background:qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 {self.accent}, stop:1 #2b2e37); border-radius: 12px;"
            )
            return
        cleaned = clean_reference_pixmap(pixmap)
        scaled = cleaned.scaled(
            240,
            120,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )
        self.cover.setPixmap(scaled)
        self.cover.setStyleSheet(
            """
            border-radius: 12px;
            background-color: #1a1f27;
            padding: 0px;
            margin: 0px;
            """
        )

    def set_active(self, active):
        self.active = active
        self.refresh_style()

    def refresh_style(self):
        border = self.accent if self.active else "#2c313c"
        background = "#16191f" if self.active else "#13161c"
        self.setStyleSheet(
            f"""
            QFrame#presetCard {{
                background-color: {background};
                border: 1px solid {border};
                border-radius: 18px;
            }}
            """
        )

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if callable(self.on_click):
            self.on_click(self)


class ToolRow(QFrame):
    def __init__(self, title, subtitle="", checked=False):
        super().__init__()
        self.title = title
        self.toggle = ToggleSwitch(checked)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(10)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(1)
        title_label = QLabel(title)
        title_label.setStyleSheet("color:#f2f5f8; font-size:12px; font-weight:700;")
        text_layout.addWidget(title_label)
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("color:#79808e; font-size:10px;")
            text_layout.addWidget(subtitle_label)

        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(self.toggle)


class ImageCanvas(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("imageCanvas")
        self.pixmap = QPixmap()
        self.file_dropped_callback = None
        self.setAcceptDrops(True)

        self.empty_title = QLabel("Upload an image to start")
        self.empty_title.setAlignment(Qt.AlignCenter)
        self.empty_title.setStyleSheet("color:#f5f7fa; font-size:22px; font-weight:700;")

        self.empty_subtitle = QLabel("Drop a house image here or choose one from the left panel.")
        self.empty_subtitle.setAlignment(Qt.AlignCenter)
        self.empty_subtitle.setStyleSheet("color:#8b93a2; font-size:13px;")

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.hide()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.addStretch()
        layout.addWidget(self.empty_title)
        layout.addWidget(self.empty_subtitle)
        layout.addWidget(self.image_label)
        layout.addStretch()

        self.setStyleSheet(
            """
            QFrame#imageCanvas {
                background-color: #111419;
                border: 1px solid #232833;
                border-radius: 30px;
            }
            """
        )
        add_shadow(self, blur=34, color=QColor(0, 0, 0, 115), y_offset=12)

    def clear_canvas(self):
        self.pixmap = QPixmap()
        self.image_label.clear()
        self.image_label.hide()
        self.empty_title.show()
        self.empty_subtitle.show()
        self.empty_subtitle.setText("Drop a house image here or choose one from the left panel.")

    def set_pixmap(self, pixmap):
        if pixmap.isNull():
            return
        self.pixmap = pixmap
        self.refresh_preview()

    def refresh_preview(self):
        if self.pixmap.isNull():
            self.clear_canvas()
            return
        scaled = self.pixmap.scaled(
            self.width() - 60,
            self.height() - 60,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled)
        self.image_label.show()
        self.empty_title.hide()
        self.empty_subtitle.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.pixmap.isNull():
            self.refresh_preview()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls and callable(self.file_dropped_callback):
            self.file_dropped_callback(urls[0].toLocalFile())


class HistoryThumb(QPushButton):
    def __init__(self, title, pixmap):
        super().__init__(title)
        self.preview_pixmap = pixmap
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(120, 112)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(96, 64))
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #151a22;
                border: 1px solid #2c3340;
                border-radius: 16px;
                color: #eef2f7;
                font-size: 11px;
                font-weight: 700;
                text-align: left;
                padding: 70px 10px 10px 10px;
            }
            QPushButton:hover {
                border-color: #42d6c7;
            }
            """
        )


class VisualizeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.source_pixmap = QPixmap()
        self.generated_pixmap = QPixmap()
        self.object_reference_pixmap = QPixmap()
        self.current_file_path = ""
        self.object_file_path = ""
        self.site_context_text = ""
        self.active_preset_key = "brick-roof-loft"
        self.latest_style_summary = ""
        self.latest_refined_prompt = ""
        self.latest_negative_prompt = "text, watermark, logo, signage, blurry facade, distorted proportions"
        self.preset_cards = []
        self.option_groups = {}
        self.tool_rows = []
        self.seed_value = None
        self.api_model_name = "gemini-2.5-flash-image"
        self.text_test_model_name = "gemini-2.5-flash"
        self.result_history = []

        self.preset_catalog = {
            "brick-roof-loft": {
                "title": "Slim Vertical House",
                "subtitle": "Tall narrow townhouse with greenery and street motion",
                "accent": "#b9c5db",
                "source": "Sample reference 01",
                "image": str(BASE_DIR / "Refer" / "New folder" / "photo_2026-03-14_15-08-36.jpg"),
                "prompt": "slim vertical townhouse, tall narrow facade, minimalist white walls, dark flat roof canopy, hanging greenery on balconies, warm interior lighting, realistic street-front architecture, light traffic motion blur with motorbikes, soft overcast dusk sky, lush roadside vegetation, no text, no watermark, no logo",
                "analysis_hint": "Focus on the tall narrow proportions, minimalist white facade, deep roof canopy, hanging balcony plants, warm interior windows, street-level realism with passing motorbikes, and a calm overcast residential atmosphere.",
                "warmth": 11,
                "contrast": 1.1,
                "brightness": 6,
                "green_reduce": 0.82,
                "blue_boost": 8,
            },
            "garden-c4-bungalow": {
                "title": "Garden C4 Courtyard",
                "subtitle": "Compact two-story home with planted balcony and calm courtyard",
                "accent": "#d58c72",
                "source": "Sample reference 02",
                "image": str(BASE_DIR / "Refer" / "New folder" / "photo_2026-03-14_15-08-34 (3).jpg"),
                "prompt": "compact two story courtyard home, red clay tile roof, planted balcony, warm interior lighting, cozy front garden, open metal gate, realistic residential street-front architecture, soft dusk sky, clean sidewalk, calm neighborhood context, no text, no watermark, no logo",
                "analysis_hint": "Focus on the compact two-story proportions, red tile roof, planted balcony edge, warm evening window light, quiet front courtyard, open gate, and realistic family-house street-front composition with a calm dusk atmosphere.",
                "warmth": 15,
                "contrast": 1.06,
                "brightness": 10,
                "green_reduce": 0.78,
                "blue_boost": 4,
            },
            "garden-c4-streetfront": {
                "title": "Streetfront Garden C4",
                "subtitle": "Open-gate bungalow with roadside trees and front landscape",
                "accent": "#7fb6c8",
                "source": "Sample reference 03",
                "image": str(BASE_DIR / "Refer" / "New folder" / "photo_2026-03-14_15-08-34 (5).jpg"),
                "prompt": "modern bungalow street-front view, open metal gate, broad front courtyard, roadside trees, visible road and sidewalk, realistic neighborhood environment, daylight architectural photography, subtle motion blur from passing traffic, no text, no watermark, no logo",
                "analysis_hint": "Focus on the open gate, broad front courtyard, mature roadside trees, visible road and sidewalk, passing street activity, and calm suburban landscaping context in bright natural daylight.",
                "warmth": 8,
                "contrast": 1.04,
                "brightness": 12,
                "green_reduce": 0.8,
                "blue_boost": 10,
            },
            "night-garden-cottage": {
                "title": "Night Garden Cottage",
                "subtitle": "Small warm home with lush tropical landscaping at night",
                "accent": "#d08b62",
                "source": "Sample reference 04",
                "image": str(BASE_DIR / "Refer" / "New folder" / "photo_2026-03-14_15-08-34 (6).jpg"),
                "prompt": "small tropical cottage at night, warm garden lighting, tiled roof, lush tropical landscaping, flowering foreground plants, cozy realistic house facade, soft blue evening sky, cinematic residential environment, no text, no watermark, no logo",
                "analysis_hint": "Focus on the intimate small-house proportions, warm night lighting, tiled roof, dense tropical foreground plants, flowering garden edges, soft blue sky, and cozy landscaped evening mood.",
                "warmth": 20,
                "contrast": 1.07,
                "brightness": 3,
                "green_reduce": 0.8,
                "blue_boost": 5,
            },
            "classic-palm-villa": {
                "title": "Classic Palm Villa",
                "subtitle": "Elegant villa with palms, layered shrubs, and bright driveway mood",
                "accent": "#d9c38e",
                "source": "Sample reference 05",
                "image": str(BASE_DIR / "Refer" / "New folder" / "photo_2026-03-14_15-08-34 (7).jpg"),
                "prompt": "classic luxury villa facade at twilight, symmetrical composition, palm trees, layered shrubs, chandelier foyer, premium curved driveway, warm luxury lighting, elegant residential landscape, realistic night exterior, no text, no watermark, no logo",
                "analysis_hint": "Focus on the classical villa language, symmetrical massing, bright warm lighting, palm-lined driveway, layered tropical shrubs, chandelier entry, and premium luxury residential night atmosphere.",
                "warmth": 20,
                "contrast": 1.09,
                "brightness": 5,
                "green_reduce": 0.75,
                "blue_boost": 7,
            },
            "slim-urban-house": {
                "title": "Grand Glass Residence",
                "subtitle": "Modern three-story villa with glass facade and elegant front garden",
                "accent": "#d2d7e4",
                "source": "Sample reference 06",
                "image": str(BASE_DIR / "Refer" / "photo_2026-03-14_11-53-13 (6).jpg"),
                "prompt": "modern three-story luxury residence, expansive glass facade, dark metal and stone accents, symmetrical front elevation, warm interior lighting, elegant front garden, clean premium driveway, refined suburban neighborhood, realistic dusk architectural photography, lush but controlled landscaping, no text, no watermark, no logo",
                "analysis_hint": "Focus on the premium three-story massing, large glass windows, dark modern trim, vertical center screen detail, balanced landscaping, clean driveway composition, and realistic luxury residential dusk atmosphere.",
                "warmth": 14,
                "contrast": 1.12,
                "brightness": 6,
                "green_reduce": 0.8,
                "blue_boost": 8,
            },
        }

        self.setWindowTitle("AI House Visualizer")
        self.resize(1450, 900)
        self.setMinimumSize(1240, 780)
        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background-color: #0b0d12;
                color: #eef2f7;
                font-family: 'Segoe UI';
            }
            QLabel {
                background: transparent;
                border: none;
            }
            QFrame[class="panel"] {
                background-color: #12161d;
                border: 1px solid #222833;
                border-radius: 24px;
            }
            QLineEdit, QTextEdit {
                background-color: #171b22;
                border: 1px solid #242b36;
                border-radius: 14px;
                color: #eef2f7;
                padding: 12px 14px;
                font-size: 13px;
            }
            QTextEdit {
                padding-top: 12px;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            """
        )

        self.build_ui()
        self.reset_workspace()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(18, 16, 18, 18)
        root.setSpacing(14)

        root.addWidget(self.build_header())

        content = QHBoxLayout()
        content.setSpacing(18)
        root.addLayout(content)

        content.addWidget(self.build_left_panel(), 27)
        content.addWidget(self.build_center_panel(), 46)
        content.addWidget(self.build_right_panel(), 27)

    def build_header(self):
        frame = QFrame()
        frame.setObjectName("headerFrame")
        frame.setFixedHeight(84)
        frame.setStyleSheet(
            """
            QFrame#headerFrame {
                background-color: #0f1319;
                border: 1px solid #1d232d;
                border-radius: 24px;
            }
            """
        )
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(22, 16, 22, 16)

        badge = QLabel("សាល")
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedSize(78, 46)
        badge.setStyleSheet(
            """
            background:qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #d96a72, stop:0.58 #6f2a31, stop:1 #111111);
            border-radius: 14px;
            color: white;
            font-size: 19px;
            font-weight: 700;
            padding-bottom: 1px;
            """
        )

        title_box = QVBoxLayout()
        title_box.setSpacing(1)
        title = QLabel("AI House Visualizer")
        title.setStyleSheet("font-size:18px; font-weight:700; color:#f6f8fb;")
        subtitle = QLabel("New session ready for house facade visualization")
        subtitle.setStyleSheet("font-size:12px; color:#8b93a2;")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        self.session_state_label = QLabel("READY")
        self.session_state_label.setAlignment(Qt.AlignCenter)
        self.session_state_label.setFixedHeight(36)
        self.session_state_label.setStyleSheet(
            """
            background-color: rgba(66, 214, 199, 0.12);
            border: none;
            border-radius: 12px;
            color: #9ff3ea;
            padding: 0 16px;
            font-size: 12px;
            font-weight: 700;
            """
        )

        self.new_session_button = QPushButton("New Session")
        self.new_session_button.setCursor(Qt.PointingHandCursor)
        self.new_session_button.setFixedHeight(38)
        self.new_session_button.setStyleSheet(
            """
            QPushButton {
                background-color: #1b212b;
                border: 1px solid #313948;
                border-radius: 12px;
                color: #edf2f8;
                font-size: 13px;
                font-weight: 700;
                padding: 0 18px;
            }
            QPushButton:hover {
                border-color: #42d6c7;
            }
            """
        )
        self.new_session_button.clicked.connect(self.reset_workspace)

        layout.addWidget(badge)
        layout.addLayout(title_box)
        layout.addStretch()
        layout.addWidget(self.session_state_label)
        layout.addSpacing(10)
        layout.addWidget(self.new_session_button)
        return frame

    def build_left_panel(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        panel = QFrame()
        panel.setProperty("class", "panel")
        add_shadow(panel)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        layout.addWidget(self.section_title("Project Controls", "Choose image and style"))

        self.select_image_button = self.primary_button("Select Image", accent_a="#42d6c7", accent_b="#4d95ff")
        self.select_image_button.clicked.connect(self.open_image)
        layout.addWidget(self.select_image_button)

        self.clear_image_button = self.secondary_button("Clear Current Image")
        self.clear_image_button.clicked.connect(self.clear_loaded_image)
        layout.addWidget(self.clear_image_button)

        self.selected_file_label = QLabel("No image selected")
        self.selected_file_label.setWordWrap(True)
        self.selected_file_label.setStyleSheet("color:#8e97a6; font-size:12px;")
        layout.addWidget(self.selected_file_label)

        layout.addWidget(self.label_title("Visual Preset"))
        preset_grid = QGridLayout()
        preset_grid.setSpacing(12)
        for index, (key, config) in enumerate(self.preset_catalog.items()):
            card = PresetCard(key, config["title"], config["subtitle"], config["accent"], config["source"], config.get("image", ""))
            card.on_click = self.select_preset
            self.preset_cards.append(card)
            preset_grid.addWidget(card, index // 2, index % 2)
        layout.addLayout(preset_grid)

        self.preset_description = QLabel()
        self.preset_description.setWordWrap(True)
        self.preset_description.setStyleSheet("color:#78e2d7; font-size:12px;")
        layout.addWidget(self.preset_description)

        layout.addWidget(self.label_title("Instructions"))
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Describe the house mood, material, landscape or details you want to improve...")
        self.prompt_input.setFixedHeight(92)
        layout.addWidget(self.prompt_input)

        self.analyze_button = self.secondary_button("Analyze Style")
        self.analyze_button.clicked.connect(self.analyze_scene)
        layout.addWidget(self.analyze_button)

        layout.addWidget(self.label_title("Edit Tools"))
        for name, color in [
            ("Crop Framing", "#f0b04a"),
            ("Perspective", "#43c7c7"),
            ("Photo Polish", "#57d8b5"),
            ("Animation Mood", "#7d69ff"),
            ("Post Production", "#ff8344"),
        ]:
            button = self.secondary_button(name)
            button.clicked.connect(lambda checked=False, text=name: self.show_tool_message(text))
            button.setStyleSheet(
                button.styleSheet() + f"QPushButton:hover {{ border-color: {color}; color: #ffffff; }}"
            )
            layout.addWidget(button)

        layout.addWidget(self.label_title("Render Settings"))
        self.render_style_buttons = self.create_choice_row(["Photo", "3D Render"], "#42d6c7")
        layout.addLayout(self.render_style_buttons["layout"])

        self.image_count_buttons = self.create_choice_row(["1", "2", "3", "4"], "#42d6c7", compact=True)
        count_wrap = QVBoxLayout()
        count_wrap.setSpacing(8)
        count_wrap.addWidget(self.small_label("Number of Images"))
        count_wrap.addLayout(self.image_count_buttons["layout"])
        layout.addLayout(count_wrap)

        self.render_button = self.primary_button("Render Visual", accent_a="#42d6c7", accent_b="#3aa0ff")
        self.render_button.clicked.connect(self.handle_generate_click)
        layout.addWidget(self.render_button)

        layout.addStretch()
        scroll.setWidget(panel)
        return scroll

    def build_center_panel(self):
        wrap = QFrame()
        wrap.setStyleSheet("QFrame { background: transparent; border: none; }")

        layout = QVBoxLayout(wrap)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        title = QLabel("Preview Workspace")
        title.setStyleSheet("font-size:24px; font-weight:700; color:#f6f8fb;")
        subtitle = QLabel("Load a house photo, choose a preset, then render a cleaner and more polished facade mood.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("font-size:13px; color:#8c95a4;")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.preview_canvas = ImageCanvas()
        self.preview_canvas.file_dropped_callback = self.load_image_from_path
        layout.addWidget(self.preview_canvas, 1)

        bottom = QFrame()
        bottom.setObjectName("previewBottomFrame")
        bottom.setStyleSheet(
            """
            QFrame#previewBottomFrame {
                background-color: #10141b;
                border: 1px solid #1f2631;
                border-radius: 22px;
            }
            """
        )
        bottom_layout = QVBoxLayout(bottom)
        bottom_layout.setContentsMargins(18, 18, 18, 18)
        bottom_layout.setSpacing(10)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color:#d4dbe5; font-size:14px;")
        bottom_layout.addWidget(self.status_label)

        self.summary_label = QTextEdit()
        self.summary_label.setReadOnly(True)
        self.summary_label.setMinimumHeight(72)
        self.summary_label.setMaximumHeight(170)
        self.summary_label.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.summary_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.summary_label.setStyleSheet(
            """
            QTextEdit {
                background-color: transparent;
                border: none;
                color: #8791a1;
                font-size: 12px;
                padding: 0px;
            }
            """
        )
        summary_row = QHBoxLayout()
        summary_row.setSpacing(8)
        summary_row.addWidget(self.summary_label, 1)

        self.copy_prompt_button = QPushButton("📋")
        self.copy_prompt_button.setCursor(Qt.PointingHandCursor)
        self.copy_prompt_button.setFixedSize(34, 34)
        self.copy_prompt_button.setStyleSheet(
            """
            QPushButton {
                background-color: #1a1f27;
                border: none;
                border-radius: 10px;
                color: #edf2f8;
                font-size: 16px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #202733;
            }
            """
        )
        self.copy_prompt_button.clicked.connect(self.copy_prompt_to_clipboard)
        summary_row.addWidget(self.copy_prompt_button, 0, Qt.AlignTop)
        bottom_layout.addLayout(summary_row)

        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        self.show_original_button = self.secondary_button("Show Original")
        self.show_original_button.clicked.connect(self.show_original_preview)
        action_row.addWidget(self.show_original_button)

        self.show_generated_button = self.secondary_button("Show Generated")
        self.show_generated_button.clicked.connect(self.show_generated_preview)
        action_row.addWidget(self.show_generated_button)

        self.save_result_button = self.secondary_button("Save Result")
        self.save_result_button.clicked.connect(self.save_generated_image)
        action_row.addWidget(self.save_result_button)

        self.export_source_button = self.secondary_button("Save Original")
        self.export_source_button.clicked.connect(self.save_original_image)
        action_row.addWidget(self.export_source_button)

        bottom_layout.addLayout(action_row)

        gallery_title = QLabel("Result History")
        gallery_title.setStyleSheet("color:#f3f6fa; font-size:13px; font-weight:700;")
        bottom_layout.addWidget(gallery_title)

        self.history_scroll = QScrollArea()
        self.history_scroll.setWidgetResizable(True)
        self.history_scroll.setFixedHeight(142)
        self.history_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.history_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.history_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        self.history_container = QWidget()
        self.history_layout = QHBoxLayout(self.history_container)
        self.history_layout.setContentsMargins(0, 0, 0, 0)
        self.history_layout.setSpacing(10)
        self.history_layout.addStretch()
        self.history_scroll.setWidget(self.history_container)
        bottom_layout.addWidget(self.history_scroll)

        layout.addWidget(bottom)
        return wrap

    def build_right_panel(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        panel = QFrame()
        panel.setProperty("class", "panel")
        add_shadow(panel)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        layout.addWidget(self.section_title("Scene Settings", "These settings affect generated mood"))

        self.camera_buttons = self.build_option_group(layout, "Camera", ["Default", "Wide Camera"], "#42d6c7")
        self.time_buttons = self.build_option_group(layout, "Time Of Day", ["Default", "Morning", "Late Afternoon", "Evening"], "#f0b04a")
        self.weather_buttons = self.build_option_group(layout, "Weather", ["Clear Skies", "Partly Cloudy", "Overcast", "Light Rain"], "#4ca8f3")
        self.wind_buttons = self.build_option_group(layout, "Wind Strength", ["None", "Light Breeze", "Strong Wind"], "#39d3b4")
        self.resolution_buttons = self.build_option_group(layout, "Resolution", ["1K", "2K", "4K"], "#42d6c7")
        self.aspect_buttons = self.build_option_group(layout, "Aspect Ratio", ["Original", "1:1", "4:3", "16:9"], "#42d6c7")

        layout.addWidget(self.label_title("Gemini API"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setPlaceholderText("Enter GEMINI_API_KEY")
        layout.addWidget(self.api_key_input)

        self.api_model_input = QLineEdit()
        self.api_model_input.setPlaceholderText("Model name")
        self.api_model_input.setText(self.api_model_name)
        layout.addWidget(self.api_model_input)

        self.billing_hint_label = QLabel(
            "Text/chat/analyze uses gemini-2.5-flash and can work on free tier. "
            "Image generation uses gemini-2.5-flash-image and usually needs image-model access or billing."
        )
        self.billing_hint_label.setWordWrap(True)
        self.billing_hint_label.setStyleSheet("color:#f1c27d; font-size:12px;")
        layout.addWidget(self.billing_hint_label)

        self.test_api_button = self.secondary_button("Test API Key")
        self.test_api_button.clicked.connect(self.test_api_key)
        layout.addWidget(self.test_api_button)

        layout.addWidget(self.label_title("Seed"))
        seed_row = QHBoxLayout()
        seed_row.setSpacing(10)
        self.seed_input = QLineEdit()
        self.seed_input.setPlaceholderText("Random")
        seed_row.addWidget(self.seed_input, 1)
        self.random_seed_button = self.secondary_button("Random")
        self.random_seed_button.clicked.connect(self.randomize_seed)
        seed_row.addWidget(self.random_seed_button)
        layout.addLayout(seed_row)

        layout.addWidget(self.label_title("Tool Toggles"))
        self.search_grounding = ToolRow("Search Grounding", "Use reference context while generating", True)
        self.smart_enhance = ToolRow("Smart Enhance", "Refine facade contrast and color", True)
        self.editor_mode = ToolRow("Editor Mode", "Keep the result cleaner and less extreme", False)
        self.video_mode = ToolRow("Video Mood", "Adds a more cinematic toning pass", False)
        for row in [self.search_grounding, self.smart_enhance, self.editor_mode, self.video_mode]:
            self.tool_rows.append(row)
            layout.addWidget(row)

        self.add_object_card = self.info_card("Add Objects", "Upload a reference image to place into the next render.")
        self.add_object_button = self.secondary_button("Choose Object Image")
        self.add_object_button.clicked.connect(self.open_object_image)
        self.add_object_card.layout().addWidget(self.add_object_button)
        self.add_object_value = QLabel("No object image selected")
        self.add_object_value.setWordWrap(True)
        self.add_object_value.setStyleSheet("color:#7fdcd0; font-size:11px;")
        self.add_object_card.layout().addWidget(self.add_object_value)

        self.site_context_card = self.info_card("Site Context", "Add neighborhood, roads, plants, and environment details.")
        self.site_context_button = self.secondary_button("Configure Site Context")
        self.site_context_button.clicked.connect(self.configure_site_context)
        self.site_context_card.layout().addWidget(self.site_context_button)
        self.site_context_value = QLabel("No site context configured")
        self.site_context_value.setWordWrap(True)
        self.site_context_value.setStyleSheet("color:#7fdcd0; font-size:11px;")
        self.site_context_card.layout().addWidget(self.site_context_value)

        layout.addWidget(self.add_object_card)
        layout.addWidget(self.site_context_card)

        layout.addStretch()
        scroll.setWidget(panel)
        return scroll

    def section_title(self, title, subtitle):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        title_label = QLabel(title)
        title_label.setStyleSheet("color:#f6f8fb; font-size:20px; font-weight:700;")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color:#818a98; font-size:12px;")
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        return frame

    def label_title(self, text):
        label = QLabel(text)
        label.setStyleSheet("color:#f4f7fb; font-size:14px; font-weight:700;")
        return label

    def small_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("color:#8892a0; font-size:11px; font-weight:700;")
        return label

    def primary_button(self, text, accent_a="#42d6c7", accent_b="#4d95ff"):
        button = QPushButton(text)
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(44)
        button.setStyleSheet(
            f"""
            QPushButton {{
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 {accent_a}, stop:1 {accent_b});
                border:none;
                border-radius: 14px;
                color:#081315;
                font-size:14px;
                font-weight:800;
                padding: 0 18px;
            }}
            QPushButton:hover {{
                color:#040d0f;
            }}
            """
        )
        return button

    def secondary_button(self, text):
        button = QPushButton(text)
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(40)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #1a1f27;
                border: none;
                border-radius: 14px;
                color: #edf2f8;
                font-size: 13px;
                font-weight: 700;
                padding: 0 16px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #202733;
            }
            """
        )
        return button

    def create_choice_row(self, options, accent, compact=False):
        row = QHBoxLayout()
        row.setSpacing(8)
        buttons = []
        for index, text in enumerate(options):
            button = ChoiceButton(text, accent=accent, active=index == 0, min_height=34 if compact else 38)
            row.addWidget(button)
            buttons.append(button)
        self.make_exclusive(buttons)
        return {"layout": row, "buttons": buttons}

    def build_option_group(self, parent_layout, title, options, accent):
        box = QFrame()
        box.setObjectName("optionGroupFrame")
        box.setStyleSheet(
            """
            QFrame#optionGroupFrame {
                background-color: #161b23;
                border: 1px solid #262d38;
                border-radius: 18px;
            }
            """
        )
        layout = QVBoxLayout(box)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        layout.addWidget(self.label_title(title))
        grid = QGridLayout()
        grid.setSpacing(8)
        buttons = []
        for index, text in enumerate(options):
            button = ChoiceButton(text, accent=accent, active=index == 0)
            buttons.append(button)
            grid.addWidget(button, index // 2, index % 2)
        self.make_exclusive(buttons)
        layout.addLayout(grid)
        parent_layout.addWidget(box)
        return buttons

    def info_card(self, title, description):
        box = QFrame()
        box.setObjectName("infoCardFrame")
        box.setStyleSheet(
            """
            QFrame#infoCardFrame {
                background-color: #151a22;
                border: 1px solid #2a323e;
                border-radius: 18px;
            }
            """
        )
        layout = QVBoxLayout(box)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)
        title_label = QLabel(title)
        title_label.setStyleSheet("color:#f5f7fa; font-size:14px; font-weight:800;")
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color:#8390a0; font-size:11px;")
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        return box

    def copy_prompt_to_clipboard(self):
        prompt = (self.latest_refined_prompt or self.prompt_input.toPlainText()).strip()
        if not prompt:
            self.set_status("There is no prompt to copy yet.")
            return
        QApplication.clipboard().setText(prompt)
        self.set_status("Prompt copied to clipboard.")

    def open_object_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select object reference image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)",
        )
        if not file_path:
            return
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.set_status("The selected object image could not be opened.")
            return
        self.object_reference_pixmap = pixmap
        self.object_file_path = file_path
        self.add_object_value.setText(os.path.basename(file_path))
        self.set_status("Object reference image added. The next render will blend it into the scene if possible.")
        self.update_summary()

    def configure_site_context(self):
        text, ok = QInputDialog.getMultiLineText(
            self,
            "Site Context",
            "Describe the neighborhood, road condition, landscaping, climate, and surrounding environment:",
            self.site_context_text,
        )
        if not ok:
            return
        self.site_context_text = text.strip()
        self.site_context_value.setText(self.site_context_text or "No site context configured")
        self.set_status("Site context updated." if self.site_context_text else "Site context cleared.")
        self.update_summary()

    def make_exclusive(self, buttons):
        for button in buttons:
            button.clicked.connect(
                lambda checked=False, current=button, group=buttons: self.activate_choice(current, group)
            )

    def activate_choice(self, current, buttons):
        for button in buttons:
            button.setChecked(button is current)
            button.refresh_style()

    def selected_text(self, buttons):
        for button in buttons:
            if button.isChecked():
                return button.text()
        return buttons[0].text() if buttons else ""

    def clear_history(self):
        self.result_history = []
        while self.history_layout.count():
            item = self.history_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.history_layout.addStretch()

    def add_result_to_history(self, pixmap, label):
        if pixmap.isNull():
            return
        thumb_pixmap = pixmap.scaled(240, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.result_history.append({"label": label, "pixmap": pixmap})

        if self.history_layout.count() > 0 and self.history_layout.itemAt(self.history_layout.count() - 1).spacerItem():
            spacer = self.history_layout.takeAt(self.history_layout.count() - 1)
            del spacer

        button = HistoryThumb(label, thumb_pixmap)
        index = len(self.result_history) - 1
        button.clicked.connect(lambda checked=False, history_index=index: self.open_history_item(history_index))
        self.history_layout.addWidget(button)
        self.history_layout.addStretch()

    def open_history_item(self, index):
        if 0 <= index < len(self.result_history):
            entry = self.result_history[index]
            self.preview_canvas.set_pixmap(entry["pixmap"])
            self.set_status(f"Opened history item: {entry['label']}")

    def reset_workspace(self):
        self.source_pixmap = QPixmap()
        self.generated_pixmap = QPixmap()
        self.object_reference_pixmap = QPixmap()
        self.current_file_path = ""
        self.object_file_path = ""
        self.site_context_text = ""
        self.latest_style_summary = ""
        self.latest_refined_prompt = ""
        self.latest_negative_prompt = "text, watermark, logo, signage, blurry facade, distorted proportions"
        self.seed_value = None
        self.preview_canvas.clear_canvas()
        self.clear_history()
        self.selected_file_label.setText("No image selected")
        self.add_object_value.setText("No object image selected")
        self.site_context_value.setText("No site context configured")
        self.seed_input.clear()
        self.prompt_input.clear()
        self.api_key_input.setText(os.getenv("GEMINI_API_KEY", ""))
        self.api_model_input.setText(self.api_model_name)
        self.summary_label.setText(
            "Analyze Style uses gemini-2.5-flash (text/free-tier friendly). "
            "Render Visual uses gemini-2.5-flash-image (image access/billing may be required)."
        )
        self.set_status("New session started. Text analyze can use free tier; image generate depends on image-model access.")
        self.session_state_label.setText("READY")

        self.activate_choice(self.render_style_buttons["buttons"][0], self.render_style_buttons["buttons"])
        self.activate_choice(self.image_count_buttons["buttons"][0], self.image_count_buttons["buttons"])
        self.activate_choice(self.camera_buttons[0], self.camera_buttons)
        self.activate_choice(self.time_buttons[0], self.time_buttons)
        self.activate_choice(self.weather_buttons[0], self.weather_buttons)
        self.activate_choice(self.wind_buttons[0], self.wind_buttons)
        self.activate_choice(self.resolution_buttons[0], self.resolution_buttons)
        self.activate_choice(self.aspect_buttons[0], self.aspect_buttons)

        self.search_grounding.toggle.setChecked(True)
        self.search_grounding.toggle.refresh_style()
        self.smart_enhance.toggle.setChecked(True)
        self.smart_enhance.toggle.refresh_style()
        self.editor_mode.toggle.setChecked(False)
        self.editor_mode.toggle.refresh_style()
        self.video_mode.toggle.setChecked(False)
        self.video_mode.toggle.refresh_style()

        first_preset = None
        for card in self.preset_cards:
            if card.key == self.active_preset_key:
                first_preset = card
            card.set_active(False)
        if first_preset:
            self.select_preset(first_preset, update_status=False)

    def select_preset(self, preset_card, update_status=True):
        self.active_preset_key = preset_card.key
        self.latest_style_summary = ""
        self.latest_refined_prompt = ""
        self.latest_negative_prompt = "text, watermark, logo, signage, blurry facade, distorted proportions"
        for card in self.preset_cards:
            card.set_active(card is preset_card)
        self.preset_description.setText(self.preset_catalog[preset_card.key]["prompt"])
        self.prompt_input.setPlainText(self.preset_catalog[preset_card.key]["prompt"])
        if update_status:
            self.set_status(f"Preset selected: {preset_card.title}. This style will guide the generated facade mood.")

    def set_status(self, text):
        self.status_label.setText(text)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select house image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)",
        )
        if file_path:
            self.load_image_from_path(file_path)

    def load_image_from_path(self, file_path):
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.set_status("The selected image could not be opened. Please choose another file.")
            return
        self.source_pixmap = pixmap
        self.generated_pixmap = QPixmap()
        self.current_file_path = file_path
        self.preview_canvas.set_pixmap(pixmap)
        self.selected_file_label.setText(os.path.basename(file_path))
        self.session_state_label.setText("IMAGE LOADED")
        self.set_status("Image loaded successfully. Choose your settings and click Render Visual.")
        self.update_summary()

    def clear_loaded_image(self):
        self.source_pixmap = QPixmap()
        self.generated_pixmap = QPixmap()
        self.current_file_path = ""
        self.preview_canvas.clear_canvas()
        self.selected_file_label.setText("No image selected")
        self.session_state_label.setText("READY")
        self.set_status("Image removed. The workspace is ready for a new house photo.")
        self.update_summary()

    def show_original_preview(self):
        if self.source_pixmap.isNull():
            self.set_status("No original image is loaded.")
            return
        self.preview_canvas.set_pixmap(self.source_pixmap)
        self.set_status("Showing the original source image.")

    def show_generated_preview(self):
        if self.generated_pixmap.isNull():
            self.set_status("No generated result is available yet.")
            return
        self.preview_canvas.set_pixmap(self.generated_pixmap)
        self.set_status("Showing the latest generated result.")

    def save_pixmap_to_file(self, pixmap, default_name):
        if pixmap.isNull():
            self.set_status("There is no image available to save.")
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save image",
            default_name,
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg)",
        )
        if not file_path:
            return
        if pixmap.save(file_path):
            self.set_status(f"Image saved successfully to {os.path.basename(file_path)}.")
        else:
            self.set_status("Failed to save the image.")

    def save_generated_image(self):
        self.save_pixmap_to_file(self.generated_pixmap, "generated_visual.png")

    def save_original_image(self):
        self.save_pixmap_to_file(self.source_pixmap, "source_image.png")

    def randomize_seed(self):
        self.seed_value = random.randint(100000, 999999)
        self.seed_input.setText(str(self.seed_value))
        self.set_status(f"Seed updated to {self.seed_value}. The next render will use this value.")

    def analyze_scene(self):
        prompt = self.prompt_input.toPlainText().strip() or self.preset_catalog[self.active_preset_key]["prompt"]
        api_key = self.api_key_input.text().strip() or os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            analysis = [
                f"Preset: {self.preset_catalog[self.active_preset_key]['title']}",
                f"Render style: {self.selected_text(self.render_style_buttons['buttons'])}",
                f"Time: {self.selected_text(self.time_buttons)}",
                f"Weather: {self.selected_text(self.weather_buttons)}",
                f"Prompt focus: {prompt[:90]}",
            ]
            self.set_status("No API key found. Showing local analysis only.")
            self.summary_label.setText(" | ".join(analysis))
            return

        self.set_status("Analyzing with gemini-2.5-flash text model...")
        try:
            refined_prompt, analysis, negative_prompt = self.call_text_analysis(api_key, prompt)
        except RuntimeError as error:
            self.set_status(str(error))
            return

        if refined_prompt:
            self.prompt_input.setPlainText(refined_prompt)
            self.latest_refined_prompt = refined_prompt
        self.latest_style_summary = analysis
        self.latest_negative_prompt = negative_prompt or self.latest_negative_prompt
        self.session_state_label.setText("TEXT OK")
        self.set_status("Text analysis complete using gemini-2.5-flash.")
        self.summary_label.setText(f"{analysis}\nNegative prompt: {negative_prompt}")

    def show_tool_message(self, tool_name):
        self.set_status(f"{tool_name} is available as a workflow control. The button now acts as a quick action placeholder.")

    def update_summary(self):
        file_name = os.path.basename(self.current_file_path) if self.current_file_path else "No source image"
        object_name = os.path.basename(self.object_file_path) if self.object_file_path else "No object"
        context_preview = self.site_context_text[:40] + ("..." if len(self.site_context_text) > 40 else "")
        if not context_preview:
            context_preview = "No site context"
        summary = (
            f"Source: {file_name} | Preset: {self.preset_catalog[self.active_preset_key]['title']} | "
            f"Time: {self.selected_text(self.time_buttons)} | Weather: {self.selected_text(self.weather_buttons)} | "
            f"Resolution: {self.selected_text(self.resolution_buttons)} | Object: {object_name} | Context: {context_preview}"
        )
        self.summary_label.setText(summary)

    def handle_generate_click(self):
        try:
            self.generate_visual()
        except Exception as error:
            log_path = os.path.join(os.path.dirname(__file__), "gemini_error.log")
            details = traceback.format_exc()
            try:
                with open(log_path, "w", encoding="utf-8") as log_file:
                    log_file.write(details)
            except OSError:
                pass
            self.session_state_label.setText("ERROR")
            self.set_status(f"Generate failed: {error}")
            self.summary_label.setText(
                f"Full error details were written to {log_path}. Please send me that error if generate still fails."
            )

    def build_generation_prompt(self):
        base_prompt = self.preset_catalog[self.active_preset_key]["prompt"]
        user_prompt = self.prompt_input.toPlainText().strip()
        effective_prompt = user_prompt or base_prompt
        time_of_day = self.selected_text(self.time_buttons)
        weather = self.selected_text(self.weather_buttons)
        camera = self.selected_text(self.camera_buttons)
        render_style = self.selected_text(self.render_style_buttons["buttons"])
        prompt_parts = [
            effective_prompt,
            f"Camera: {camera}.",
            f"Time of day: {time_of_day}.",
            f"Weather: {weather}.",
            f"Style target: {render_style}, realistic architectural visualization, high-end residential facade, photoreal result.",
            "Match the preset reference image mood with believable landscaping, front yard composition, trees, plants, sidewalk, driveway, and neighborhood atmosphere around the house.",
        ]
        if self.latest_style_summary:
            prompt_parts.append(f"Preset analysis summary: {self.latest_style_summary}")
        if self.site_context_text:
            prompt_parts.append(f"Site context: {self.site_context_text}.")
        if not self.object_reference_pixmap.isNull():
            prompt_parts.append("Blend the uploaded object reference naturally into the scene with correct scale, lighting, and realistic placement.")
        if self.latest_negative_prompt:
            prompt_parts.append(f"Avoid: {self.latest_negative_prompt}.")
        if self.smart_enhance.toggle.isChecked():
            prompt_parts.append("Keep details crisp, clean lines, realistic materials, balanced light and shadow.")
        if self.editor_mode.toggle.isChecked():
            prompt_parts.append("Keep the result faithful to the original house structure and proportions.")
        if self.video_mode.toggle.isChecked():
            prompt_parts.append("Use a slightly cinematic but still realistic exterior presentation.")
        return " ".join(part for part in prompt_parts if part).strip()

    def test_api_key(self):
        api_key = self.api_key_input.text().strip() or os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            self.set_status("សូមបញ្ចូល Gemini API key មុនពេល test។")
            return

        self.api_model_name = self.api_model_input.text().strip() or self.api_model_name
        self.session_state_label.setText("TESTING")
        self.set_status("កំពុងពិនិត្យ Gemini API key និង model access...")

        try:
            response_text = self.call_gemini_text_test(api_key, self.api_model_name)
        except RuntimeError as error:
            primary_error = str(error)
            try:
                fallback_text = self.call_gemini_text_test(api_key, self.text_test_model_name)
            except RuntimeError as fallback_error:
                self.session_state_label.setText("ERROR")
                self.set_status(self.translate_api_error(str(fallback_error)))
                self.summary_label.setText(
                    "Image model និង text model សុទ្ធតែ test មិនបាន។ សូមពិនិត្យ quota, project, billing ឬ API restrictions។"
                )
                return

            self.session_state_label.setText("TEXT OK")
            self.set_status(
                "API key ប្រើបានសម្រាប់ text model ប៉ុន្តែ image model មិនទាន់ប្រើបាន។"
            )
            self.summary_label.setText(
                f"Text fallback success with {self.text_test_model_name}: {fallback_text}\n"
                f"Image model issue: {self.translate_api_error(primary_error)}"
            )
            return

        self.session_state_label.setText("API OK")
        self.set_status("Gemini API key ប្រើបាន ហើយ model ដែលបានជ្រើសអាចចូលប្រើបាន។")
        self.summary_label.setText(response_text or "API key test passed successfully.")

    def generate_visual(self):
        api_key = self.api_key_input.text().strip() or os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            self.set_status("Gemini API key is required. Text analyze and image generate both need a valid key.")
            return

        prompt = self.build_generation_prompt()
        self.prompt_input.setPlainText(prompt)
        self.api_model_name = self.api_model_input.text().strip() or self.api_model_name

        try:
            generated_pixmap, response_text = self.call_gemini_image_api(api_key, prompt)
        except RuntimeError as error:
            self.set_status(str(error))
            self.summary_label.setText(
                "Image generation failed. Text features may still work on free tier with gemini-2.5-flash."
            )
            return

        self.generated_pixmap = generated_pixmap
        self.preview_canvas.set_pixmap(self.generated_pixmap)
        self.session_state_label.setText("GENERATED")
        self.set_status("Gemini image generation complete. The preview now shows the API-generated image result.")
        self.summary_label.setText(response_text or "Gemini returned an image result without extra text.")
        self.add_result_to_history(
            self.generated_pixmap,
            f"{self.preset_catalog[self.active_preset_key]['title']} #{len(self.result_history) + 1}",
        )

    def call_gemini_text_test(self, api_key, model_name):
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model_name}:generateContent"
        )
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": "Reply with the exact text: API test successful."}],
                }
            ],
            "generationConfig": {"responseModalities": ["TEXT"]},
        }
        response_json = self.post_gemini_request(endpoint, api_key, payload)
        response_text = self.extract_text_from_response(response_json)
        if not response_text:
            raise RuntimeError("Gemini API responded, but no text was returned during the key test.")
        return response_text

    def call_text_analysis(self, api_key, prompt):
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.text_test_model_name}:generateContent"
        )
        preset = self.preset_catalog[self.active_preset_key]
        analysis_prompt = (
            "You are an expert architectural visualization prompt engineer. "
            "Analyze the uploaded house image together with the selected preset reference image and any object reference. "
            "Use the preset reference image as the main style anchor. Preserve the uploaded building's core proportions and layout, but transfer the preset's facade language, roof character, lighting, landscaping, street atmosphere, and mood with photoreal accuracy. "
            "Extract the exact facade language, lighting, roof form, materials, landscaping, street context, front yard composition, camera composition, and realism cues. "
            "Return JSON with keys: refined_prompt, style_summary, negative_prompt. "
            "The refined_prompt must be a single highly specific prompt for photoreal image generation, under 140 words, "
            "and must explicitly say no text, no watermark, no logo, no signage. "
            "The style_summary must be 3 short sentences. "
            "The negative_prompt must be a comma-separated line of things to avoid. "
            "If site context is provided, incorporate it naturally. "
            "If an object reference is provided, mention realistic placement, scale, and matching light direction.\n\n"
            f"Selected preset title: {preset['title']}\n"
            f"Selected preset base prompt: {preset['prompt']}\n"
            f"Selected preset style hint: {preset.get('analysis_hint', '')}\n"
            f"User instructions: {prompt}\n"
            f"Site context: {self.site_context_text or 'None'}\n"
            f"Object reference included: {'Yes' if self.object_file_path else 'No'}\n"
            f"Scene settings: camera={self.selected_text(self.camera_buttons)}, "
            f"time_of_day={self.selected_text(self.time_buttons)}, "
            f"weather={self.selected_text(self.weather_buttons)}, "
            f"render_style={self.selected_text(self.render_style_buttons['buttons'])}."
        )
        parts = [{"text": analysis_prompt}]
        preset_inline_data = self.preset_inline_data(self.active_preset_key)
        if preset_inline_data:
            parts.append({"inlineData": preset_inline_data})
        if self.current_file_path and os.path.exists(self.current_file_path):
            mime_type = mimetypes.guess_type(self.current_file_path)[0] or "image/jpeg"
            with open(self.current_file_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            parts.append({"inlineData": {"mimeType": mime_type, "data": encoded_image}})
        if self.object_file_path and os.path.exists(self.object_file_path):
            mime_type = mimetypes.guess_type(self.object_file_path)[0] or "image/jpeg"
            with open(self.object_file_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            parts.append({"inlineData": {"mimeType": mime_type, "data": encoded_image}})
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": parts,
                }
            ],
            "generationConfig": {"responseModalities": ["TEXT"]},
        }
        response_json = self.post_gemini_request(endpoint, api_key, payload)
        response_text = self.extract_text_from_response(response_json)
        if not response_text:
            raise RuntimeError("Text analysis succeeded but no text response was returned.")
        refined_prompt = prompt
        style_summary = response_text
        negative_prompt = "text, watermark, logo, signage, blurry facade, distorted proportions"
        try:
            parsed = json.loads(response_text)
            refined_prompt = parsed.get("refined_prompt", refined_prompt).strip() or refined_prompt
            style_summary = parsed.get("style_summary", style_summary).strip() or style_summary
            negative_prompt = parsed.get("negative_prompt", negative_prompt).strip() or negative_prompt
        except json.JSONDecodeError:
            pass
        return refined_prompt, style_summary, negative_prompt

    def preset_inline_data(self, preset_key):
        preset = self.preset_catalog.get(preset_key)
        if not preset:
            return None
        image_path = preset.get("image", "")
        if not image_path or not os.path.exists(image_path):
            return None
        cleaned = clean_reference_pixmap(QPixmap(image_path))
        return self.pixmap_to_inline_data(cleaned)

    def current_render_base_inline_data(self):
        if self.current_file_path and os.path.exists(self.current_file_path):
            mime_type = mimetypes.guess_type(self.current_file_path)[0] or "image/jpeg"
            with open(self.current_file_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return {"mimeType": mime_type, "data": encoded_image}
        if not self.generated_pixmap.isNull():
            return self.pixmap_to_inline_data(self.generated_pixmap)
        return None

    def pixmap_to_inline_data(self, pixmap):
        if pixmap.isNull():
            return None
        temp_path = BASE_DIR / "_temp_generated_reference.png"
        pixmap.save(str(temp_path), "PNG")
        try:
            encoded_image = base64.b64encode(temp_path.read_bytes()).decode("utf-8")
        finally:
            try:
                temp_path.unlink()
            except OSError:
                pass
        return {"mimeType": "image/png", "data": encoded_image}

    def call_gemini_image_api(self, api_key, prompt):
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.api_model_name}:generateContent"
        )
        parts = [{"text": prompt}]
        preset_inline_data = self.preset_inline_data(self.active_preset_key)
        if preset_inline_data:
            parts.append({"inlineData": preset_inline_data})
        base_inline_data = self.current_render_base_inline_data()
        if base_inline_data:
            parts.append({"inlineData": base_inline_data})
        if self.object_file_path and os.path.exists(self.object_file_path):
            mime_type = mimetypes.guess_type(self.object_file_path)[0] or "image/jpeg"
            with open(self.object_file_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            parts.append({"inlineData": {"mimeType": mime_type, "data": encoded_image}})

        payload = {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
        }

        seed_text = self.seed_input.text().strip()
        if seed_text.isdigit():
            payload["generationConfig"]["seed"] = int(seed_text)

        response_json = self.post_gemini_request(endpoint, api_key, payload)
        pixmap = self.extract_pixmap_from_response(response_json)
        if pixmap.isNull():
            raise RuntimeError("Gemini API did not return an image. Check the model name and your account permissions.")

        response_text = self.extract_text_from_response(response_json)
        return pixmap, response_text

    def post_gemini_request(self, endpoint, api_key, payload):
        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key,
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="ignore")
            raise RuntimeError(self.translate_api_error(f"Gemini API error {error.code}: {body}")) from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"បញ្ហា network ពេលហៅ Gemini API: {error}") from error
        except json.JSONDecodeError as error:
            raise RuntimeError(f"Gemini API returned invalid JSON: {error}") from error

    def translate_api_error(self, message):
        lowered = message.lower()
        if "limit: 0" in lowered or "resource_exhausted" in lowered:
            return (
                "Quota របស់ project នេះសម្រាប់ model នេះមិនអនុញ្ញាត free tier ទេ ឬបានអស់ហើយ "
                "(limit: 0 / RESOURCE_EXHAUSTED)។ សូមប្ដូរ model, ប្ដូរ project, ឬបើក billing។"
            )
        if "exceeded your current quota" in lowered or "quota exceeded" in lowered:
            return "អ្នកបានអស់ quota សម្រាប់ project នេះហើយ។ សូមរង់ចាំ quota reset ឬបើក billing។"
        if "api key not valid" in lowered or "permission_denied" in lowered:
            return "API key មិនត្រឹមត្រូវ ឬ project/model នេះមិនមានសិទ្ធិចូលប្រើ។"
        if "model not found" in lowered or "not found" in lowered:
            return "Model name មិនត្រឹមត្រូវ ឬ model នេះមិនមានសម្រាប់ account/project របស់អ្នក។"
        return message

    def extract_pixmap_from_response(self, response_json):
        for candidate in response_json.get("candidates", []):
            content = candidate.get("content", {})
            for part in content.get("parts", []):
                inline_data = part.get("inlineData") or part.get("inline_data")
                if inline_data and inline_data.get("data"):
                    try:
                        image_bytes = base64.b64decode(inline_data["data"])
                    except (ValueError, TypeError):
                        continue
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_bytes)
                    if not pixmap.isNull():
                        return pixmap
        return QPixmap()

    def extract_text_from_response(self, response_json):
        texts = []
        for candidate in response_json.get("candidates", []):
            content = candidate.get("content", {})
            for part in content.get("parts", []):
                text = part.get("text")
                if text:
                    texts.append(text.strip())
        return "\n".join(text for text in texts if text)

    def apply_visual_style(self, pixmap):
        preset = self.preset_catalog[self.active_preset_key]
        image = pixmap.toImage().convertToFormat(QImage.Format_RGB32)
        if image.width() > 1500:
            image = image.scaledToWidth(1500, Qt.SmoothTransformation)

        time_of_day = self.selected_text(self.time_buttons).lower()
        weather = self.selected_text(self.weather_buttons).lower()
        render_style = self.selected_text(self.render_style_buttons["buttons"]).lower()
        editor_mode = self.editor_mode.toggle.isChecked()
        video_mode = self.video_mode.toggle.isChecked()
        smart_enhance = self.smart_enhance.toggle.isChecked()

        warmth = preset["warmth"]
        contrast = preset["contrast"]
        brightness = preset["brightness"]
        green_reduce = preset["green_reduce"]
        blue_boost = preset["blue_boost"]

        if "morning" in time_of_day:
            brightness += 8
            blue_boost += 6
        elif "late afternoon" in time_of_day:
            warmth += 8
            brightness += 5
        elif "evening" in time_of_day:
            warmth += 12
            brightness -= 4
            contrast += 0.03

        if "overcast" in weather:
            contrast -= 0.04
            blue_boost += 6
        elif "partly" in weather:
            contrast += 0.02
        elif "rain" in weather:
            blue_boost += 10
            brightness -= 6

        if "3d render" in render_style:
            contrast += 0.05
            warmth += 3

        if editor_mode:
            contrast -= 0.03
            warmth -= 2

        if video_mode:
            contrast += 0.04
            blue_boost += 4

        width = image.width()
        height = image.height()
        for y in range(height):
            vertical_ratio = y / max(1, height - 1)
            sky_factor = max(0.0, 1.0 - vertical_ratio * 1.28)
            for x in range(width):
                color = QColor(image.pixel(x, y))
                red = color.red()
                green = color.green()
                blue = color.blue()

                red = clamp((red - 128) * contrast + 128 + brightness)
                green = clamp((green - 128) * contrast + 128 + brightness)
                blue = clamp((blue - 128) * contrast + 128 + brightness)

                if green > red * 0.93 and green > blue * 0.93:
                    green = clamp(green * green_reduce)
                    red = clamp(red + 10)

                red = clamp(red + warmth + sky_factor * 2)
                green = clamp(green + warmth * 0.35)
                blue = clamp(blue + blue_boost * sky_factor)

                if smart_enhance and (red + green + blue) / 3 > 155:
                    red = clamp(red + 6)
                    green = clamp(green + 4)
                    blue = clamp(blue + 2)

                vignette_x = abs((x / max(1, width - 1)) - 0.5) * 2.0
                vignette_y = abs((y / max(1, height - 1)) - 0.5) * 2.0
                vignette = max(vignette_x, vignette_y)
                dim = 1.0 - vignette * 0.06
                red = clamp(red * dim)
                green = clamp(green * dim)
                blue = clamp(blue * dim)

                image.setPixelColor(x, y, QColor(red, green, blue))
        return image


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 11))
    window = VisualizeWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
