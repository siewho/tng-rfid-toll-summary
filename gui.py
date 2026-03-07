import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD as _TkDnD
    _DND_MODULE = _TkDnD
except Exception:
    _DND_MODULE = None
    DND_FILES = None

from extract_amount_mupdf import extract_amounts

# ── Design tokens (Swiss/Minimalism) ──────────────────────────────────────────
BG      = "#FFFFFF"
TEXT    = "#000000"
MUTED   = "#808080"
BORDER  = "#D1D1D1"
BEIGE   = "#F5F1E8"
MONO    = "Courier"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def get_asset(name):
    base = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets", name)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color=BG)

        # Try to inject tkdnd support into this Tk instance
        self._dnd_available = False
        if _DND_MODULE is not None:
            try:
                _DND_MODULE._require(self)
                self._dnd_available = True
            except Exception:
                pass

        self.title("TNG Toll Summary")
        self.geometry("480x520")
        self.minsize(400, 420)
        self.resizable(True, True)

        try:
            ico_path = get_asset("app-icon.ico")
            if os.path.exists(ico_path):
                self.wm_iconbitmap(ico_path)
            else:
                img = tk.PhotoImage(file=get_asset("app-icon.png"))
                self.iconphoto(True, img)
        except Exception:
            pass

        self.container = ctk.CTkFrame(self, fg_color=BG)
        self.container.pack(fill="both", expand=True)

        self._dot_job = None
        self._show_drop()

    # ── Drop view ──────────────────────────────────────────────────────────────

    def _show_drop(self):
        self._clear_container()
        frame = ctk.CTkFrame(self.container, fg_color=BG)
        frame.pack(fill="both", expand=True)

        box = ctk.CTkFrame(
            frame,
            width=340, height=180,
            corner_radius=0,
            border_width=1,
            border_color=TEXT,
            fg_color=BG,
            cursor="hand2",
        )
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)

        lbl_main = ctk.CTkLabel(
            box,
            text="Drag PDF here",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT,
        )
        lbl_main.pack(expand=True, pady=(40, 4))

        lbl_sub = ctk.CTkLabel(
            box,
            text="or click to select file",
            font=ctk.CTkFont(size=16),
            text_color=MUTED,
        )
        lbl_sub.pack(pady=(0, 40))

        for w in (box, lbl_main, lbl_sub):
            w.bind("<Button-1>", lambda _e: self._browse())

        if self._dnd_available:
            box.drop_target_register(DND_FILES)
            box.dnd_bind("<<Drop>>", self._on_drop)

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Select TNG eWallet PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if path:
            self._start_processing(path)

    def _on_drop(self, event):
        path = event.data.strip()
        if path.startswith("{") and path.endswith("}"):
            path = path[1:-1]
        if path.lower().endswith(".pdf"):
            self._start_processing(path)
        else:
            messagebox.showerror("Invalid file", "Please drop a PDF file.")

    # ── Processing view ────────────────────────────────────────────────────────

    def _start_processing(self, pdf_path):
        self._show_processing()
        threading.Thread(target=self._run_extraction, args=(pdf_path,), daemon=True).start()

    def _show_processing(self):
        self._clear_container()
        if self._dot_job:
            self.after_cancel(self._dot_job)
            self._dot_job = None

        frame = ctk.CTkFrame(self.container, fg_color=BG)
        frame.pack(fill="both", expand=True)

        self._loading_label = ctk.CTkLabel(
            frame,
            text="Reading PDF",
            font=ctk.CTkFont(size=15),
            text_color=MUTED,
        )
        self._loading_label.place(relx=0.5, rely=0.5, anchor="center")

        self._dot_count = 0
        self._animate_dots()

    def _animate_dots(self):
        self._dot_count = (self._dot_count + 1) % 4
        self._loading_label.configure(text=f"Reading PDF{'.' * self._dot_count}")
        self._dot_job = self.after(400, self._animate_dots)

    def _run_extraction(self, pdf_path):
        try:
            amounts = extract_amounts(pdf_path)
            filename = os.path.basename(pdf_path)
            self.after(0, lambda: self._show_results(filename, amounts))
        except Exception as exc:
            self.after(0, lambda: self._on_error(str(exc)))

    def _on_error(self, msg):
        if self._dot_job:
            self.after_cancel(self._dot_job)
            self._dot_job = None
        messagebox.showerror("Error", f"Failed to process PDF:\n{msg}")
        self._show_drop()

    # ── Results view ───────────────────────────────────────────────────────────

    def _show_results(self, filename, amounts):
        if self._dot_job:
            self.after_cancel(self._dot_job)
            self._dot_job = None
        self._clear_container()

        frame = ctk.CTkFrame(self.container, fg_color=BG)
        frame.pack(fill="both", expand=True, padx=28, pady=20)

        # ── Header ──
        header = ctk.CTkFrame(frame, fg_color=BG)
        header.pack(fill="x", pady=(0, 20))

        ctk.CTkButton(
            header,
            text="← Back",
            width=60, height=24,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color=MUTED,
            hover_color=BEIGE,
            corner_radius=0,
            border_width=0,
            command=self._show_drop,
        ).pack(side="left")

        name = filename if len(filename) <= 38 else f"...{filename[-35:]}"
        ctk.CTkLabel(
            header,
            text=name,
            font=ctk.CTkFont(size=11),
            text_color=MUTED,
            anchor="e",
        ).pack(side="right")

        # ── Section label ──
        ctk.CTkLabel(
            frame,
            text="TRANSACTIONS",
            font=ctk.CTkFont(size=10),
            text_color=MUTED,
            anchor="w",
        ).pack(fill="x", pady=(0, 6))

        # ── 1px top border ──
        tk.Frame(frame, bg=TEXT, height=1).pack(fill="x")

        # ── Scrollable list ──
        scroll = ctk.CTkScrollableFrame(frame, fg_color=BG, corner_radius=0)
        scroll.pack(fill="both", expand=True)

        for i, amt in enumerate(amounts, 1):
            row = ctk.CTkFrame(scroll, fg_color=BG)
            row.pack(fill="x", pady=0)

            ctk.CTkLabel(
                row,
                text=f"{i:02d}",
                font=ctk.CTkFont(family=MONO, size=13),
                text_color=MUTED,
                width=32,
                anchor="w",
            ).pack(side="left", padx=(4, 0), pady=3)

            ctk.CTkLabel(
                row,
                text=f"{amt:.2f}",
                font=ctk.CTkFont(family=MONO, size=13),
                text_color=TEXT,
                anchor="e",
            ).pack(side="right", padx=(0, 4), pady=3)

            # thin row separator
            tk.Frame(scroll, bg=BORDER, height=1).pack(fill="x")

        # ── 1px bottom border + total ──
        tk.Frame(frame, bg=TEXT, height=1).pack(fill="x", pady=(0, 12))

        total = sum(amounts)
        total_col = ctk.CTkFrame(frame, fg_color=BG)
        total_col.pack(anchor="e")

        ctk.CTkLabel(
            total_col,
            text=f"RM  {total:.2f}",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT,
            anchor="e",
        ).pack(anchor="e")

        self._copy_btn = ctk.CTkButton(
            total_col,
            text="Copy",
            width=72, height=28,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color=TEXT,
            hover_color=BEIGE,
            corner_radius=0,
            border_width=1,
            border_color=TEXT,
            command=lambda: self._copy_total(total),
        )
        self._copy_btn.pack(anchor="e", pady=(6, 0))

    def _copy_total(self, total):
        self.clipboard_clear()
        self.clipboard_append(f"{total:.2f}")
        self._copy_btn.configure(text="Copied!")
        self.after(1500, lambda: self._copy_btn.configure(text="Copy"))

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _clear_container(self):
        for child in self.container.winfo_children():
            child.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
