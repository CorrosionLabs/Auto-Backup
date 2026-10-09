import base64
import os
import threading
import time
import zipfile
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
from io import BytesIO


APP_TITLE = "Corrosion Labs // Auto Backup"
APP_VERSION = "v1.5"
LOGO_BASE64 = """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"""
DEFAULT_INTERVAL_MIN = 5
DEFAULT_MAX_BACKUPS = 10

# Corrosion Labs UI palette - based on the approved mockup.
COLOR_HEADER = "#171B1F"
COLOR_BODY = "#FFFFFF"
COLOR_SURFACE = "#FFFFFF"
COLOR_ENTRY_BG = "#E9ECEF"
COLOR_FG = "#16191D"
COLOR_MUTED = "#6F7780"
COLOR_BORDER = "#D6DADF"
COLOR_ACCENT = "#E22424"
COLOR_ACCENT_HOVER = "#C91D1D"
COLOR_BUTTON = "#ECEFF2"
COLOR_BUTTON_HOVER = "#E1E5E9"
COLOR_RING_TRACK = "#000000"
COLOR_STATUS_OK = "#22B95B"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AutoBackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("690x420")
        self.root.resizable(False, False)
        self.root.configure(fg_color=COLOR_BODY)

        self.running = False
        self.stop_event = threading.Event()
        self.worker_thread = None
        self.manual_thread = None

        # UI-only timing state. It mirrors the automatic loop; it does not control it.
        self.next_backup_deadline = None
        self.current_interval_seconds = DEFAULT_INTERVAL_MIN * 60
        self.backup_in_progress = False
        self.manual_backup_in_progress = False
        self.saving_blink_visible = True

        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()
        self.interval_var = tk.StringVar(value=str(DEFAULT_INTERVAL_MIN))
        self.max_backups_var = tk.StringVar(value=str(DEFAULT_MAX_BACKUPS))
        self.status_var = tk.StringVar(value="Stopped")

        self.build_ui()

        self.source_var.trace_add("write", self.update_start_button_state)
        self.dest_var.trace_add("write", self.update_start_button_state)
        self.update_start_button_state()

        self.update_countdown()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        # Overall composition: dark Corrosion Labs header, light working area.
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            self.root,
            fg_color=COLOR_HEADER,
            corner_radius=0,
            height=56
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        logo_image = Image.open(BytesIO(base64.b64decode(LOGO_BASE64))).convert("RGBA")
        self.header_logo = ctk.CTkImage(
            light_image=logo_image,
            dark_image=logo_image,
            size=(36, 36)
        )

        ctk.CTkLabel(
            header,
            image=self.header_logo,
            text=""
        ).grid(row=0, column=0, padx=(18, 10), pady=10)

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            title_row,
            text="AUTO BACKUP",
            text_color="#F5F5F5",
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        ).pack(side="left")

        ctk.CTkLabel(
            title_row,
            text=APP_VERSION,
            text_color="#8A929A",
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=9)
        ).pack(side="left", padx=(6, 0), pady=(2, 0))

        body = ctk.CTkFrame(
            self.root,
            fg_color=COLOR_BODY,
            corner_radius=0
        )
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # LEFT COLUMN -------------------------------------------------------
        left = ctk.CTkFrame(body, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(14, 8), pady=(12, 10))
        left.grid_columnconfigure(0, weight=1)

        self._field_label(left, "Source folder", 0)
        source_row = ctk.CTkFrame(left, fg_color="transparent")
        source_row.grid(row=1, column=0, sticky="ew", pady=(4, 8))
        source_row.grid_columnconfigure(0, weight=1)

        ctk.CTkEntry(
            source_row,
            textvariable=self.source_var,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family="Segoe UI", size=15)
        ).grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self._select_button(source_row, self.select_source).grid(
            row=0, column=1, sticky="ew"
        )

        self._field_label(left, "Destination folder", 2)
        dest_row = ctk.CTkFrame(left, fg_color="transparent")
        dest_row.grid(row=3, column=0, sticky="ew", pady=(4, 8))
        dest_row.grid_columnconfigure(0, weight=1)

        ctk.CTkEntry(
            dest_row,
            textvariable=self.dest_var,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family="Segoe UI", size=15)
        ).grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self._select_button(dest_row, self.select_dest).grid(
            row=0, column=1, sticky="ew"
        )

        options = ctk.CTkFrame(left, fg_color="transparent")
        options.grid(row=4, column=0, sticky="ew", pady=(2, 10))
        options.grid_columnconfigure((0, 1), weight=1)

        self._field_label(options, "Interval (minutes)", 0, column=0, padx=(0, 8))
        self._field_label(options, "Copies to keep", 0, column=1, padx=(8, 0))

        ctk.CTkEntry(
            options,
            textvariable=self.interval_var,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family="Segoe UI", size=15)
        ).grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(4, 0))

        ctk.CTkEntry(
            options,
            textvariable=self.max_backups_var,
            height=40,
            corner_radius=6,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family="Segoe UI", size=15)
        ).grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(4, 0))

        actions = ctk.CTkFrame(left, fg_color="transparent")
        actions.grid(row=5, column=0, sticky="ew")
        actions.grid_columnconfigure((0, 1), weight=1)

        self.start_button = ctk.CTkButton(
            actions,
            text="▶   Start",
            command=self.start_backup,
            height=46,
            corner_radius=6,
            fg_color="#000000",
            hover_color="#1F1F1F",
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            state="disabled"
        )
        self.start_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.stop_button = ctk.CTkButton(
            actions,
            text="■   Stop",
            command=self.stop_backup,
            height=46,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family="Segoe UI", size=17),
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # RIGHT COLUMN ------------------------------------------------------
        right = ctk.CTkFrame(body, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 14), pady=(6, 10))
        right.grid_columnconfigure(0, weight=1)

        self.timer_canvas = tk.Canvas(
            right,
            width=200,
            height=200,
            bg=COLOR_BODY,
            highlightthickness=0,
            bd=0
        )
        self.timer_canvas.grid(row=0, column=0, pady=(0, 6))

        # Anti-aliased circular progress ring.
        self.timer_ring_image_id = self.timer_canvas.create_image(
            0, 0, anchor="nw"
        )
        self.timer_ring_photo = None
        self.draw_timer_ring(0.0)

        self.timer_text = self.timer_canvas.create_text(
            100, 100,
            text="STOPPED",
            fill=COLOR_FG,
            font=("Segoe UI", 16, "bold"),
            anchor="center"
        )

        self.manual_button = ctk.CTkButton(
            right,
            text="▰   Create now",
            command=self.create_manual_backup,
            height=50,
            corner_radius=6,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        )
        self.manual_button.grid(
            row=1, column=0, pady=(0, 7)
        )
        self.manual_button.configure(width=200)

        # FOOTER ------------------------------------------------------------
        footer = ctk.CTkFrame(
            self.root,
            fg_color="#F6F6F6",
            corner_radius=0,
            height=38
        )
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)
        footer.grid_columnconfigure(0, weight=1)

        self.status_dot = ctk.CTkLabel(
            footer,
            text="●",
            text_color=COLOR_MUTED,
            width=20,
            font=ctk.CTkFont(size=15)
        )
        self.status_dot.grid(row=0, column=0, sticky="w", padx=(14, 4), pady=7)

        ctk.CTkLabel(
            footer,
            textvariable=self.status_var,
            text_color=COLOR_MUTED,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=14)
        ).grid(row=0, column=0, sticky="w", padx=(38, 0), pady=7)

        ctk.CTkLabel(
            footer,
            text="CORROSION LABS",
            text_color="#A0A0A0",
            font=ctk.CTkFont(family="Segoe UI", size=8)
        ).grid(row=0, column=1, sticky="e", padx=(0, 14), pady=7)

    def _field_label(self, parent, text, row, column=0, padx=0):
        ctk.CTkLabel(
            parent,
            text=text,
            text_color=COLOR_FG,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).grid(row=row, column=column, sticky="w", padx=padx)

    def _select_button(self, parent, command):
        return ctk.CTkButton(
            parent,
            text="Select",
            command=command,
            width=110,
            height=40,
            corner_radius=6,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_BUTTON_HOVER,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_FG,
            font=ctk.CTkFont(family="Segoe UI", size=14)
        )

    def draw_timer_ring(self, progress):
        progress = max(0.0, min(1.0, progress))

        size = 200
        scale = 4
        high_size = size * scale
        inset = 22 * scale
        width = 14 * scale

        image = Image.new("RGBA", (high_size, high_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        box = (inset, inset, high_size - inset, high_size - inset)

        draw.ellipse(
            box,
            outline=COLOR_RING_TRACK,
            width=width
        )

        if progress > 0:
            draw.arc(
                box,
                start=-90,
                end=-90 + (360 * progress),
                fill=COLOR_ACCENT,
                width=width
            )

        image = image.resize((size, size), Image.Resampling.LANCZOS)
        self.timer_ring_photo = ImageTk.PhotoImage(image)
        self.timer_canvas.itemconfigure(
            self.timer_ring_image_id,
            image=self.timer_ring_photo
        )

    def update_countdown(self):
        saving = self.backup_in_progress or self.manual_backup_in_progress

        if saving:
            text = "SAVING" if self.saving_blink_visible else ""
            ring_progress = 1.0
            timer_font = ("Segoe UI", 16, "bold")
            self.saving_blink_visible = not self.saving_blink_visible
        elif not self.running:
            text = "STOPPED"
            ring_progress = 0.0
            timer_font = ("Segoe UI", 16, "bold")
            self.saving_blink_visible = True
        elif self.next_backup_deadline is None:
            text = "SAVING"
            ring_progress = 1.0
            timer_font = ("Segoe UI", 16, "bold")
        else:
            remaining = max(0.0, self.next_backup_deadline - time.monotonic())
            total = max(1.0, self.current_interval_seconds)

            elapsed_progress = 1.0 - min(1.0, remaining / total)

            minutes = int(remaining) // 60
            seconds = int(remaining) % 60
            text = f"{minutes:02d}:{seconds:02d}"
            ring_progress = elapsed_progress
            timer_font = ("Segoe UI", 35, "normal")

        self.draw_timer_ring(ring_progress)
        self.timer_canvas.itemconfigure(
            self.timer_text,
            text=text,
            font=timer_font
        )
        self.root.after(500 if saving else 250, self.update_countdown)

    def update_start_button_state(self, *_):
        source_ok = bool(self.source_var.get().strip())
        dest_ok = bool(self.dest_var.get().strip())

        if self.running:
            self.start_button.configure(
                state="disabled",
                fg_color=COLOR_BUTTON,
                hover_color=COLOR_BUTTON_HOVER,
                text_color=COLOR_MUTED
            )
            self.stop_button.configure(
                state="normal",
                fg_color="#000000",
                hover_color="#1F1F1F",
                text_color="#FFFFFF",
                border_width=0
            )
        else:
            self.start_button.configure(
                state="normal" if source_ok and dest_ok else "disabled",
                fg_color="#000000" if source_ok and dest_ok else COLOR_BUTTON,
                hover_color="#1F1F1F" if source_ok and dest_ok else COLOR_BUTTON_HOVER,
                text_color="#FFFFFF" if source_ok and dest_ok else COLOR_MUTED
            )
            self.stop_button.configure(
                state="disabled",
                fg_color=COLOR_BUTTON,
                hover_color=COLOR_BUTTON_HOVER,
                text_color=COLOR_MUTED,
                border_width=1
            )

    def select_source(self):
        path = filedialog.askdirectory(title="Seleccionar carpeta de origen")
        if path:
            self.source_var.set(path)

    def select_dest(self):
        path = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        if path:
            self.dest_var.set(path)

    def validate_paths(self):
        source = Path(self.source_var.get().strip())
        dest = Path(self.dest_var.get().strip())

        if not source.is_dir():
            messagebox.showerror(APP_TITLE, "La carpeta de origen no es válida.")
            return None

        if not dest.is_dir():
            messagebox.showerror(APP_TITLE, "La carpeta de destino no es válida.")
            return None

        return source.resolve(), dest.resolve()

    def validate_settings(self):
        paths = self.validate_paths()
        if not paths:
            return None

        source, dest = paths

        try:
            interval = float(self.interval_var.get())
            if interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(APP_TITLE, "El intervalo debe ser mayor que 0.")
            return None

        try:
            max_backups = int(self.max_backups_var.get())
            if max_backups <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(APP_TITLE, "El máximo de ZIP debe ser un entero mayor que 0.")
            return None

        return source, dest, interval, max_backups

    def start_backup(self):
        settings = self.validate_settings()
        if not settings:
            return

        self.running = True
        self.stop_event.clear()
        self.update_start_button_state()
        self.status_var.set("Running")
        self.status_dot.configure(text_color=COLOR_STATUS_OK)
        self.backup_in_progress = True
        self.next_backup_deadline = None

        self.worker_thread = threading.Thread(
            target=self.backup_loop,
            args=settings,
            daemon=True
        )
        self.worker_thread.start()

    def stop_backup(self):
        self.running = False
        self.stop_event.set()
        self.update_start_button_state()
        self.status_var.set("Stopped")
        self.status_dot.configure(text_color=COLOR_MUTED)
        self.backup_in_progress = False
        self.next_backup_deadline = None

    def backup_loop(self, source, dest_root, interval, max_backups):
        auto_dir = dest_root / "Auto"
        auto_dir.mkdir(parents=True, exist_ok=True)

        while not self.stop_event.is_set():
            try:
                self.create_backup(
                    source=source,
                    target_dir=auto_dir,
                    excluded_root=dest_root
                )
                self.rotate_backups(auto_dir, max_backups)
            except Exception as exc:
                self.root.after(
                    0,
                    lambda e=exc: self.status_var.set(f"Error: {e}")
                )

            self.next_backup_deadline = time.monotonic() + (interval * 60)
            self.current_interval_seconds = interval * 60
            self.backup_in_progress = False

            if self.stop_event.wait(interval * 60):
                break

    def create_manual_backup(self):
        paths = self.validate_paths()
        if not paths:
            return

        description = simpledialog.askstring(
            "Snapshot manual",
            "Descripción opcional para el nombre del backup:",
            parent=self.root
        )

        if description is None:
            return

        source, dest_root = paths
        description = self.sanitize_description(description)

        self.manual_button.configure(state="disabled")
        self.manual_backup_in_progress = True
        self.saving_blink_visible = True
        self.status_var.set("Creating manual snapshot…")

        self.manual_thread = threading.Thread(
            target=self.manual_backup_worker,
            args=(source, dest_root, description),
            daemon=True
        )
        self.manual_thread.start()

    def manual_backup_worker(self, source, dest_root, description):
        try:
            manual_dir = dest_root / "Manual"
            manual_dir.mkdir(parents=True, exist_ok=True)

            zip_path = self.create_backup(
                source=source,
                target_dir=manual_dir,
                description=description,
                excluded_root=dest_root
            )

            self.root.after(
                0,
                lambda: self.status_var.set(
                    f"Manual snapshot created: {zip_path.name}"
                )
            )
        except Exception as exc:
            self.root.after(
                0,
                lambda e=exc: self.status_var.set(f"Error: {e}")
            )
        finally:
            def finish_manual_backup():
                self.manual_backup_in_progress = False
                self.saving_blink_visible = True
                self.manual_button.configure(state="normal")

            self.root.after(0, finish_manual_backup)

    def create_backup(self, source, target_dir, description="", excluded_root=None):
        target_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        suffix = f"_{description}" if description else ""
        zip_path = target_dir / f"Backup_{timestamp}{suffix}.zip"
        temp_path = target_dir / f".Backup_{timestamp}{suffix}.tmp"

        excluded_root = excluded_root.resolve() if excluded_root else None
        source = source.resolve()

        with zipfile.ZipFile(
            temp_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=6
        ) as zf:
            for root_dir, dirs, files in os.walk(source):
                root_path = Path(root_dir)

                if excluded_root:
                    dirs[:] = [
                        d for d in dirs
                        if not self.is_inside((root_path / d).resolve(), excluded_root)
                    ]

                for file_name in files:
                    file_path = root_path / file_name

                    if excluded_root and self.is_inside(file_path.resolve(), excluded_root):
                        continue

                    arcname = file_path.relative_to(source)
                    zf.write(file_path, arcname)

        temp_path.replace(zip_path)

        self.root.after(
            0,
            lambda: self.status_var.set(
                f"Last backup: {zip_path.name}"
            )
        )

        return zip_path

    @staticmethod
    def is_inside(path, parent):
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            return False

    @staticmethod
    def sanitize_description(text):
        text = text.strip()
        if not text:
            return ""

        invalid = '<>:"/\\|?*'
        cleaned = "".join(
            "-" if char.isspace() else char
            for char in text
            if char not in invalid and ord(char) >= 32
        )

        while "--" in cleaned:
            cleaned = cleaned.replace("--", "-")

        return cleaned.strip(" .-_")

    def rotate_backups(self, auto_dir, max_backups):
        backups = sorted(
            auto_dir.glob("Backup_*.zip"),
            key=lambda p: p.stat().st_mtime
        )

        while len(backups) > max_backups:
            oldest = backups.pop(0)
            try:
                oldest.unlink()
            except OSError:
                break

    def on_close(self):
        self.stop_event.set()
        self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = AutoBackupApp(root)
    root.mainloop()
