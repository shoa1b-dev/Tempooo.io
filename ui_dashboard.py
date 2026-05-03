# import customtkinter as ctk
# import sensor_reader
# import time
# from plyer import notification
# import time

# TEMP_THRESHOLD = 80
# _last_notified = 0          # cooldown tracker

# ctk.set_appearance_mode("dark")

# # ── COLOUR PALETTE ──────────────────────────────────────────────────────────
# BG          = "#080810"
# CARD        = "#0D0D1A"
# CARD_BORDER = "#1A1A35"
# ACCENT      = "#00D4FF"       # cyan
# ACCENT2     = "#7C3AED"       # violet
# GREEN       = "#00FF9F"
# YELLOW      = "#FFD700"
# ORANGE      = "#FF8C00"
# RED         = "#FF3355"
# MUTED       = "#555577"
# TEXT        = "#E0E0FF"
# TEXT_DIM    = "#6B6B99"

# # ── TEMPERATURE COLOUR THRESHOLDS ────────────────────────────────────────────
# def temp_color(val_str):
#     try:
#         v = float(str(val_str).replace("°C","").strip())
#         if v < 55:   return GREEN
#         if v < 70:   return YELLOW
#         if v < 85:   return ORANGE
#         return RED
#     except:
#         return TEXT_DIM

# def usage_color(val_str):
#     try:
#         v = float(str(val_str).replace("%","").strip())
#         if v < 50:  return GREEN
#         if v < 75:  return YELLOW
#         if v < 90:  return ORANGE
#         return RED
#     except:
#         return TEXT_DIM


# class GlowCard(ctk.CTkFrame):
#     """A card with a subtle top-accent border stripe."""
#     def __init__(self, master, accent_color=ACCENT, **kwargs):
#         super().__init__(master, fg_color=CARD, corner_radius=12,
#                          border_width=1, border_color=CARD_BORDER, **kwargs)
#         # thin coloured stripe on the left edge
#         self._stripe = ctk.CTkFrame(self, fg_color=accent_color,
#                                     corner_radius=6, width=3)
#         self._stripe.place(x=0, y=12, relheight=0.75)


# class SectionLabel(ctk.CTkLabel):
#     def __init__(self, master, text, **kwargs):
#         super().__init__(master, text=text,
#                          font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
#                          text_color=ACCENT, **kwargs)


# class MetricRow(ctk.CTkFrame):
#     """Label + value + optional progress bar in one row."""
#     def __init__(self, master, label, show_bar=False, **kwargs):
#         super().__init__(master, fg_color="transparent", **kwargs)
#         self.columnconfigure(1, weight=1)

#         ctk.CTkLabel(self, text=label,
#                      font=ctk.CTkFont(family="Consolas", size=11),
#                      text_color=TEXT_DIM, width=110, anchor="w").grid(
#                          row=0, column=0, sticky="w", padx=(10, 4))

#         self.val_lbl = ctk.CTkLabel(self, text="──",
#                                     font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
#                                     text_color=TEXT, width=120, anchor="w")
#         self.val_lbl.grid(row=0, column=1, sticky="w")

#         self.bar = None
#         if show_bar:
#             self.bar = ctk.CTkProgressBar(self, height=4, width=130,
#                                           fg_color="#1A1A35",
#                                           progress_color=ACCENT,
#                                           corner_radius=2)
#             self.bar.set(0)
#             self.bar.grid(row=1, column=1, sticky="w", pady=(1, 4))

#     def update(self, text, pct=None, color=TEXT):
#         self.val_lbl.configure(text=text, text_color=color)
#         if self.bar is not None and pct is not None:
#             self.bar.set(max(0.0, min(1.0, pct / 100.0)))
#             self.bar.configure(progress_color=color)


# # ── MAIN APP ─────────────────────────────────────────────────────────────────
# class TempoooApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Tempooo.io 3.1")
#         self.geometry("480x580")
#         self.resizable(True, True)
#         self.configure(fg_color=BG)

#         cpu_name, gpu_name = sensor_reader.get_hardware_names()
#         self._pulse_state = True
#         self._build_ui(cpu_name, gpu_name)
#         self.storage_loaded = False
#         self.update_dashboard()

#     # ── BUILD ─────────────────────────────────────────────────────────────────
#     def _build_ui(self, cpu_name, gpu_name):
#         # ── HEADER ──────────────────────────────────────────────────────────
#         hdr = ctk.CTkFrame(self, fg_color="transparent")
#         hdr.pack(fill="x", padx=16, pady=(14, 6))

#         title_lbl = ctk.CTkLabel(hdr,
#             text="TEMPOOO.IO",
#             font=ctk.CTkFont(family="Consolas", size=22, weight="bold"),
#             text_color=ACCENT)
#         title_lbl.pack(side="left")

#         ver_lbl = ctk.CTkLabel(hdr, text="v3.1",
#                                font=ctk.CTkFont(family="Consolas", size=10),
#                                text_color=ACCENT2)
#         ver_lbl.pack(side="left", padx=(4, 0), pady=(8, 0))

#         # live pulse dot
#         self.pulse_dot = ctk.CTkLabel(hdr, text="●",
#                                       font=ctk.CTkFont(size=14),
#                                       text_color=GREEN)
#         self.pulse_dot.pack(side="right", padx=4)

#         self.clock_lbl = ctk.CTkLabel(hdr, text="",
#                                       font=ctk.CTkFont(family="Consolas", size=11),
#                                       text_color=TEXT_DIM)
#         self.clock_lbl.pack(side="right", padx=8)

#         # divider
#         ctk.CTkFrame(self, fg_color=ACCENT2, height=1, corner_radius=0).pack(
#             fill="x", padx=16, pady=(0, 8))

#         # ── SCROLLABLE BODY ──────────────────────────────────────────────────
#         scroll = ctk.CTkScrollableFrame(self, fg_color=BG, corner_radius=0,
#                                         scrollbar_button_color=CARD_BORDER,
#                                         scrollbar_button_hover_color=ACCENT2)
#         scroll.pack(fill="both", expand=True)

#         # ── HARDWARE ID ──────────────────────────────────────────────────────
#         hw_card = GlowCard(scroll, accent_color=ACCENT2)
#         hw_card.pack(fill="x", padx=12, pady=(0, 8))

#         SectionLabel(hw_card, text="◈  SYSTEM HARDWARE").pack(
#             anchor="w", padx=16, pady=(10, 6))

#         def hw_row(parent, label, value):
#             f = ctk.CTkFrame(parent, fg_color="transparent")
#             f.pack(fill="x", padx=16, pady=(0, 4))
#             ctk.CTkLabel(f, text=label,
#                          font=ctk.CTkFont(family="Consolas", size=10),
#                          text_color=TEXT_DIM, width=40, anchor="w").pack(side="left")
#             ctk.CTkLabel(f, text=value,
#                          font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
#                          text_color=TEXT, anchor="w").pack(side="left", padx=(6,0))

#         hw_row(hw_card, "CPU", cpu_name)
#         hw_row(hw_card, "GPU", gpu_name)
#         ctk.CTkFrame(hw_card, fg_color="transparent", height=4).pack()

#         # ── LOAD & MEMORY ────────────────────────────────────────────────────
#         load_card = GlowCard(scroll, accent_color=ACCENT)
#         load_card.pack(fill="x", padx=12, pady=(0, 8))

#         SectionLabel(load_card, text="◈  PROCESSING & MEMORY").pack(
#             anchor="w", padx=16, pady=(10, 6))

#         self.cpu_row = MetricRow(load_card, "CPU Usage", show_bar=True)
#         self.cpu_row.pack(fill="x")
#         self.gpu_row = MetricRow(load_card, "GPU Usage", show_bar=False)
#         self.gpu_row.pack(fill="x")
#         self.gpu_temp_row = MetricRow(load_card, "GPU Temp")
#         self.gpu_temp_row.pack(fill="x")
#         self.ram_row = MetricRow(load_card, "RAM Load", show_bar=True)
#         self.ram_row.pack(fill="x")

#         self.ram_hw_lbl = ctk.CTkLabel(load_card, text="",
#                                         font=ctk.CTkFont(family="Consolas", size=10, slant="italic"),
#                                         text_color=ACCENT2)
#         self.ram_hw_lbl.pack(anchor="w", padx=120, pady=(0, 6))

#         # ── STORAGE ──────────────────────────────────────────────────────────
#         self.storage_card = GlowCard(scroll, accent_color=YELLOW)
#         self.storage_card.pack(fill="x", padx=12, pady=(0, 8))

#         SectionLabel(self.storage_card, text="◈  PHYSICAL DRIVES & PARTITIONS").pack(
#             anchor="w", padx=16, pady=(10, 6))

#         # ── THERMAL READINGS ─────────────────────────────────────────────────
#         temp_card = GlowCard(scroll, accent_color=ORANGE)
#         temp_card.pack(fill="x", padx=12, pady=(0, 8))

#         SectionLabel(temp_card, text="◈  THERMAL READINGS").pack(
#             anchor="w", padx=16, pady=(10, 6))

#         # column headers
#         hdr_f = ctk.CTkFrame(temp_card, fg_color="transparent")
#         hdr_f.pack(fill="x", padx=14)
#         for col, w, txt in [("Sensor",120,"SENSOR"),("Live",60,"LIVE"),
#                              ("Min",55,"MIN"),("Max",55,"MAX"),("Load",55,"LOAD")]:
#             ctk.CTkLabel(hdr_f, text=txt,
#                          font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
#                          text_color=MUTED, width=int(w), anchor="w").pack(side="left")

#         ctk.CTkFrame(temp_card, fg_color=CARD_BORDER, height=1).pack(
#             fill="x", padx=14, pady=(2, 4))

#         self.core_rows = []
#         for i in range(6):
#             row_f = ctk.CTkFrame(temp_card, fg_color="transparent")
#             row_f.pack(fill="x", padx=14, pady=1)

#             ctk.CTkLabel(row_f, text=f"Core #{i}",
#                          font=ctk.CTkFont(family="Consolas", size=11),
#                          text_color=TEXT_DIM, width=120, anchor="w").pack(side="left")

#             lbls = {}
#             for key, w in [("temp",60),("min",55),("max",55),("load",55)]:
#                 lbl = ctk.CTkLabel(row_f, text="──",
#                                    font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
#                                    text_color=TEXT, width=w, anchor="w")
#                 lbl.pack(side="left")
#                 lbls[key] = lbl
#             self.core_rows.append(lbls)

#         ctk.CTkFrame(temp_card, fg_color="transparent", height=6).pack()

#         # ── SYSTEM HEALTH ────────────────────────────────────────────────────
#         self.health_card = GlowCard(scroll, accent_color=GREEN)
#         self.health_card.pack(fill="x", padx=12, pady=(0, 16))

#         inner_h = ctk.CTkFrame(self.health_card, fg_color="transparent")
#         inner_h.pack(pady=14)

#         self.health_icon = ctk.CTkLabel(inner_h, text="◉",
#                                          font=ctk.CTkFont(size=20),
#                                          text_color=GREEN)
#         self.health_icon.pack(side="left", padx=(0, 8))

#         self.health_lbl = ctk.CTkLabel(inner_h, text="SYSTEM HEALTH  ──  ASSESSING",
#                                         font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
#                                         text_color=GREEN)
#         self.health_lbl.pack(side="left")
#     def _check_and_notify(self, core_data):
#         global _last_notified
#         now = time.time()
#         if now - _last_notified < 60:   # max 1 alert per 60 seconds
#             return

#         hot_cores = []
#         for i, d in enumerate(core_data):
#             try:
#                 val = float(str(d["temp"]).replace("°C","").strip())
#                 if val >= TEMP_THRESHOLD:
#                     hot_cores.append(f"Core #{i}: {d['temp']}")
#             except:
#                 pass

#         if hot_cores:
#             notification.notify(
#                 title="⚠️ Tempooo.io — High Temperature!",
#                 message="\n".join(hot_cores),
#                 app_name="Tempooo.io",
#                 timeout=6
#             )
#             _last_notified = now
#     # ── UPDATE ────────────────────────────────────────────────────────────────
#     def update_dashboard(self):
#         # clock + pulse
#         self.clock_lbl.configure(text=time.strftime("%H:%M:%S"))
#         self._pulse_state = not self._pulse_state
#         self.pulse_dot.configure(text_color=GREEN if self._pulse_state else BG)

#         # CPU
#         cpu_val = sensor_reader.get_cpu_usage()
#         try:
#             cpu_pct = float(str(cpu_val).replace("%",""))
#         except:
#             cpu_pct = 0
#         c_col = usage_color(cpu_val)
#         self.cpu_row.update(f"{cpu_val}%", pct=cpu_pct, color=c_col)

#         # GPU usage
#         gpu_u = sensor_reader.get_gpu_usage()
#         self.gpu_row.update(gpu_u, color=TEXT_DIM if "N/A" in str(gpu_u) else usage_color(gpu_u))

#         # RAM
#         ram_usage, ram_hw = sensor_reader.get_ram_info()
#         try:
#             ram_pct = float(str(ram_usage).split("(")[1].replace("%)","").strip())
#         except:
#             ram_pct = 0
#         r_col = usage_color(str(ram_pct))
#         self.ram_row.update(ram_usage, pct=ram_pct, color=r_col)
#         self.ram_hw_lbl.configure(text=f"[ {ram_hw} ]")

#         # GPU temp
#         overall_temp = sensor_reader.get_overall_temp()
#         sensor_reader.check_temp_alert(overall_temp)
#         gpu_t = sensor_reader.get_gpu_temp(overall_temp)
#         self.gpu_temp_row.update(f"{gpu_t} °C", color=temp_color(gpu_t))

#         # Storage (once)
#         if not self.storage_loaded:
#             physical_drives, partitions = sensor_reader.get_storage_info()
#             for drive in physical_drives:
#                 ctk.CTkLabel(self.storage_card, text=f"▸  {drive}",
#                              font=ctk.CTkFont(family="Consolas", size=11, slant="italic"),
#                              text_color=ACCENT).pack(anchor="w", padx=20, pady=(0, 2))

#             for p in partitions:
#                 pct = p['percent']
#                 bar_color = GREEN if pct < 75 else (YELLOW if pct < 90 else RED)

#                 pf = ctk.CTkFrame(self.storage_card, fg_color="transparent")
#                 pf.pack(fill="x", padx=20, pady=(0, 4))

#                 ctk.CTkLabel(pf, text=f"  {p['letter']}:",
#                              font=ctk.CTkFont(family="Consolas", size=11),
#                              text_color=TEXT_DIM, width=30, anchor="w").pack(side="left")
#                 ctk.CTkLabel(pf,
#                              text=f"{p['used']}G / {p['total']}G  ({pct}%)",
#                              font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
#                              text_color=bar_color).pack(side="left", padx=(4, 8))

#                 bar = ctk.CTkProgressBar(pf, height=4, width=100,
#                                          fg_color="#1A1A35",
#                                          progress_color=bar_color,
#                                          corner_radius=2)
#                 bar.set(pct / 100.0)
#                 bar.pack(side="left")

#             ctk.CTkFrame(self.storage_card, fg_color="transparent", height=4).pack()
#             self.storage_loaded = True

#         # Per-core
#         core_data = sensor_reader.get_per_core_data()
#         self._check_and_notify(core_data)
#         for i in range(6):
#             d = core_data[i]
#             lbls = self.core_rows[i]
#             t_col = temp_color(d["temp"])
#             lbls["temp"].configure(text=d["temp"],  text_color=t_col)
#             lbls["min"].configure(text=d["min"],    text_color=TEXT_DIM)
#             lbls["max"].configure(text=d["max"],    text_color=RED)
#             lbls["load"].configure(text=d["load"],  text_color=ACCENT)

#         # Health
#         health = sensor_reader.get_health_status(overall_temp)
#         colors = {"Critical": RED, "Normal": YELLOW, "Optimal": GREEN}
#         icons  = {"Critical": "◉", "Normal": "◎", "Optimal": "◉"}
#         h_col  = colors.get(health, GREEN)
#         h_icon = icons.get(health, "◉")

#         self.health_lbl.configure(
#             text=f"SYSTEM HEALTH  ──  {health.upper()}",
#             text_color=h_col)
#         self.health_icon.configure(text=h_icon, text_color=h_col)
#         self.health_card._stripe.configure(fg_color=h_col)

#         self.after(1000, self.update_dashboard)


# if __name__ == "__main__":
#     app = TempoooApp()
#     app.mainloop()




import customtkinter as ctk
import sensor_reader
import time

# ── THEME PALETTES ────────────────────────────────────────────────────────────
DARK = {
    "mode":        "dark",
    "BG":          "#080810",
    "CARD":        "#0D0D1A",
    "CARD_BORDER": "#1A1A35",
    "ACCENT":      "#00D4FF",
    "ACCENT2":     "#7C3AED",
    "GREEN":       "#00FF9F",
    "YELLOW":      "#FFD700",
    "ORANGE":      "#FF8C00",
    "RED":         "#FF3355",
    "MUTED":       "#555577",
    "TEXT":        "#E0E0FF",
    "TEXT_DIM":    "#6B6B99",
    "BAR_BG":      "#1A1A35",
    "BTN_FG":      "#1A1A35",
    "BTN_HOVER":   "#2A2A55",
    "BTN_TEXT":    "#00D4FF",
    "BTN_ICON":    "☀",
}

LIGHT = {
    "mode":        "light",
    "BG":          "#F0F2F8",
    "CARD":        "#FFFFFF",
    "CARD_BORDER": "#D0D4E8",
    "ACCENT":      "#0066CC",
    "ACCENT2":     "#6D28D9",
    "GREEN":       "#059669",
    "YELLOW":      "#D97706",
    "ORANGE":      "#EA580C",
    "RED":         "#DC2626",
    "MUTED":       "#9CA3AF",
    "TEXT":        "#111827",
    "TEXT_DIM":    "#6B7280",
    "BAR_BG":      "#E5E7EB",
    "BTN_FG":      "#E5E7EB",
    "BTN_HOVER":   "#D1D5DB",
    "BTN_TEXT":    "#0066CC",
    "BTN_ICON":    "🌙",
}

T = DARK   # active theme


# ── HELPERS ───────────────────────────────────────────────────────────────────
def temp_color(val_str):
    try:
        v = float(str(val_str).replace("°C", "").strip())
        if v < 55: return T["GREEN"]
        if v < 70: return T["YELLOW"]
        if v < 85: return T["ORANGE"]
        return T["RED"]
    except:
        return T["TEXT_DIM"]

def usage_color(val_str):
    try:
        v = float(str(val_str).replace("%", "").strip())
        if v < 50: return T["GREEN"]
        if v < 75: return T["YELLOW"]
        if v < 90: return T["ORANGE"]
        return T["RED"]
    except:
        return T["TEXT_DIM"]


# ── COMPONENTS ────────────────────────────────────────────────────────────────
class GlowCard(ctk.CTkFrame):
    def __init__(self, master, accent_color, **kwargs):
        super().__init__(master, fg_color=T["CARD"], corner_radius=12,
                         border_width=1, border_color=T["CARD_BORDER"], **kwargs)
        self._stripe = ctk.CTkFrame(self, fg_color=accent_color,
                                    corner_radius=6, width=3)
        self._stripe.place(x=0, y=12, relheight=0.75)


class SectionLabel(ctk.CTkLabel):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text,
                         font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                         text_color=T["ACCENT"], **kwargs)


class MetricRow(ctk.CTkFrame):
    def __init__(self, master, label, show_bar=False, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text=label,
                     font=ctk.CTkFont(family="Consolas", size=11),
                     text_color=T["TEXT_DIM"], width=110, anchor="w").grid(
                         row=0, column=0, sticky="w", padx=(10, 4))

        self.val_lbl = ctk.CTkLabel(self, text="──",
                                    font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
                                    text_color=T["TEXT"], width=120, anchor="w")
        self.val_lbl.grid(row=0, column=1, sticky="w")

        self.bar = None
        if show_bar:
            self.bar = ctk.CTkProgressBar(self, height=4, width=130,
                                          fg_color=T["BAR_BG"],
                                          progress_color=T["ACCENT"],
                                          corner_radius=2)
            self.bar.set(0)
            self.bar.grid(row=1, column=1, sticky="w", pady=(1, 4))

    def update(self, text, pct=None, color=None):
        color = color or T["TEXT"]
        self.val_lbl.configure(text=text, text_color=color)
        if self.bar is not None and pct is not None:
            self.bar.set(max(0.0, min(1.0, pct / 100.0)))
            self.bar.configure(progress_color=color)


# ── MAIN APP ──────────────────────────────────────────────────────────────────
class TempoooApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tempooo.io 3.1")
        self.geometry("480x580")
        self.resizable(True, True)

        self._pulse_state   = True
        self._is_dark       = True
        self._after_id      = None
        self._rebuilding    = False   # ← add this
        self.storage_loaded = False
        self.cpu_name, self.gpu_name = sensor_reader.get_hardware_names()

        ctk.set_appearance_mode(T["mode"])
        self.configure(fg_color=T["BG"])
        self._build_ui()
        self.update_dashboard()

    # ── BUILD ─────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # HEADER
        self._header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._header_frame.pack(fill="x", padx=16, pady=(14, 6))

        ctk.CTkLabel(self._header_frame, text="TEMPOOO.IO",
                     font=ctk.CTkFont(family="Consolas", size=22, weight="bold"),
                     text_color=T["ACCENT"]).pack(side="left")

        ctk.CTkLabel(self._header_frame, text="v3.1",
                     font=ctk.CTkFont(family="Consolas", size=10),
                     text_color=T["ACCENT2"]).pack(side="left", padx=(4, 0), pady=(8, 0))

        # THEME TOGGLE BUTTON
        self.theme_btn = ctk.CTkButton(
            self._header_frame,
            text=f"{T['BTN_ICON']}  {'Light' if self._is_dark else 'Dark'}",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color=T["BTN_FG"],
            hover_color=T["BTN_HOVER"],
            text_color=T["BTN_TEXT"],
            corner_radius=8,
            width=80, height=28,
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="right", padx=(8, 0))

        # pulse dot
        self.pulse_dot = ctk.CTkLabel(self._header_frame, text="●",
                                      font=ctk.CTkFont(size=14),
                                      text_color=T["GREEN"])
        self.pulse_dot.pack(side="right", padx=4)

        self.clock_lbl = ctk.CTkLabel(self._header_frame, text="",
                                      font=ctk.CTkFont(family="Consolas", size=11),
                                      text_color=T["TEXT_DIM"])
        self.clock_lbl.pack(side="right", padx=8)

        # divider
        self._divider = ctk.CTkFrame(self, fg_color=T["ACCENT2"],
                                     height=1, corner_radius=0)
        self._divider.pack(fill="x", padx=16, pady=(0, 8))

        # SCROLL BODY
        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color=T["BG"], corner_radius=0,
            scrollbar_button_color=T["CARD_BORDER"],
            scrollbar_button_hover_color=T["ACCENT2"])
        self.scroll.pack(fill="both", expand=True)

        self._build_cards()

    def _build_cards(self):
        # HARDWARE
        hw_card = GlowCard(self.scroll, accent_color=T["ACCENT2"])
        hw_card.pack(fill="x", padx=12, pady=(0, 8))
        SectionLabel(hw_card, text="◈  SYSTEM HARDWARE").pack(
            anchor="w", padx=16, pady=(10, 6))

        def hw_row(parent, label, value):
            f = ctk.CTkFrame(parent, fg_color="transparent")
            f.pack(fill="x", padx=16, pady=(0, 4))
            ctk.CTkLabel(f, text=label,
                         font=ctk.CTkFont(family="Consolas", size=10),
                         text_color=T["TEXT_DIM"], width=40, anchor="w").pack(side="left")
            ctk.CTkLabel(f, text=value,
                         font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                         text_color=T["TEXT"], anchor="w").pack(side="left", padx=(6, 0))

        hw_row(hw_card, "CPU", self.cpu_name)
        hw_row(hw_card, "GPU", self.gpu_name)
        ctk.CTkFrame(hw_card, fg_color="transparent", height=4).pack()

        # LOAD & MEMORY
        load_card = GlowCard(self.scroll, accent_color=T["ACCENT"])
        load_card.pack(fill="x", padx=12, pady=(0, 8))
        SectionLabel(load_card, text="◈  PROCESSING & MEMORY").pack(
            anchor="w", padx=16, pady=(10, 6))

        self.cpu_row      = MetricRow(load_card, "CPU Usage", show_bar=True)
        self.cpu_row.pack(fill="x")
        self.gpu_row      = MetricRow(load_card, "GPU Usage")
        self.gpu_row.pack(fill="x")
        self.gpu_temp_row = MetricRow(load_card, "GPU Temp")
        self.gpu_temp_row.pack(fill="x")
        self.ram_row      = MetricRow(load_card, "RAM Load", show_bar=True)
        self.ram_row.pack(fill="x")

        self.ram_hw_lbl = ctk.CTkLabel(
            load_card, text="",
            font=ctk.CTkFont(family="Consolas", size=10, slant="italic"),
            text_color=T["ACCENT2"])
        self.ram_hw_lbl.pack(anchor="w", padx=120, pady=(0, 6))

        # STORAGE
        self.storage_card = GlowCard(self.scroll, accent_color=T["YELLOW"])
        self.storage_card.pack(fill="x", padx=12, pady=(0, 8))
        SectionLabel(self.storage_card, text="◈  PHYSICAL DRIVES & PARTITIONS").pack(
            anchor="w", padx=16, pady=(10, 6))

        # THERMAL
        temp_card = GlowCard(self.scroll, accent_color=T["ORANGE"])
        temp_card.pack(fill="x", padx=12, pady=(0, 8))
        SectionLabel(temp_card, text="◈  THERMAL READINGS").pack(
            anchor="w", padx=16, pady=(10, 6))

        hdr_f = ctk.CTkFrame(temp_card, fg_color="transparent")
        hdr_f.pack(fill="x", padx=14)
        for _, w, txt in [("Sensor",120,"SENSOR"),("Live",60,"LIVE"),
                          ("Min",55,"MIN"),("Max",55,"MAX"),("Load",55,"LOAD")]:
            ctk.CTkLabel(hdr_f, text=txt,
                         font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
                         text_color=T["MUTED"], width=int(w), anchor="w").pack(side="left")

        ctk.CTkFrame(temp_card, fg_color=T["CARD_BORDER"], height=1).pack(
            fill="x", padx=14, pady=(2, 4))

        self.core_rows = []
        for i in range(6):
            row_f = ctk.CTkFrame(temp_card, fg_color="transparent")
            row_f.pack(fill="x", padx=14, pady=1)
            ctk.CTkLabel(row_f, text=f"Core #{i}",
                         font=ctk.CTkFont(family="Consolas", size=11),
                         text_color=T["TEXT_DIM"], width=120, anchor="w").pack(side="left")
            lbls = {}
            for key, w in [("temp",60),("min",55),("max",55),("load",55)]:
                lbl = ctk.CTkLabel(row_f, text="──",
                                   font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                                   text_color=T["TEXT"], width=w, anchor="w")
                lbl.pack(side="left")
                lbls[key] = lbl
            self.core_rows.append(lbls)

        ctk.CTkFrame(temp_card, fg_color="transparent", height=6).pack()

        # HEALTH
        self.health_card = GlowCard(self.scroll, accent_color=T["GREEN"])
        self.health_card.pack(fill="x", padx=12, pady=(0, 16))

        inner_h = ctk.CTkFrame(self.health_card, fg_color="transparent")
        inner_h.pack(pady=14)

        self.health_icon = ctk.CTkLabel(inner_h, text="◉",
                                         font=ctk.CTkFont(size=20),
                                         text_color=T["GREEN"])
        self.health_icon.pack(side="left", padx=(0, 8))

        self.health_lbl = ctk.CTkLabel(inner_h, text="SYSTEM HEALTH  ──  ASSESSING",
                                        font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
                                        text_color=T["GREEN"])
        self.health_lbl.pack(side="left")

    # ── THEME TOGGLE ──────────────────────────────────────────────────────────
    # def _toggle_theme(self):
    #     global T
    #     self._rebuilding = True
    #     if self._after_id:
    #         self.after_cancel(self._after_id)
    #         self._after_id = None

    #     self._is_dark = not self._is_dark
    #     T = DARK if self._is_dark else LIGHT

    #     ctk.set_appearance_mode(T["mode"])
    #     self.configure(fg_color=T["BG"])

    #     self._header_frame.destroy()
    #     self._divider.destroy()
    #     self.scroll.destroy()

    #     self.storage_loaded = False
    #     self._build_ui()
    #     self._load_storage_once()
    #     self._rebuilding = False 
    #     self.update_dashboard()
    def _toggle_theme(self):
        global T

        # cancel any scheduled update
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

        self._is_dark = not self._is_dark
        T = DARK if self._is_dark else LIGHT

        ctk.set_appearance_mode(T["mode"])
        self.configure(fg_color=T["BG"])

        # destroy ALL children in one sweep
        for widget in self.winfo_children():
            widget.destroy()

        self.storage_loaded = False

        # wait 50ms for tkinter to finish processing destroys, THEN rebuild
        self.after(50, self._rebuild)

    def _rebuild(self):
        self._build_ui()
        self._load_storage_once()
        self.update_dashboard()
    # ── STORAGE LOADER (reusable) ─────────────────────────────────────────────
    def _load_storage_once(self):
        if self.storage_loaded:
            return
        physical_drives, partitions = sensor_reader.get_storage_info()
        for drive in physical_drives:
            ctk.CTkLabel(self.storage_card, text=f"▸  {drive}",
                         font=ctk.CTkFont(family="Consolas", size=11, slant="italic"),
                         text_color=T["ACCENT"]).pack(anchor="w", padx=20, pady=(0, 2))
        for p in partitions:
            pct       = p['percent']
            bar_color = T["GREEN"] if pct < 75 else (T["YELLOW"] if pct < 90 else T["RED"])
            pf = ctk.CTkFrame(self.storage_card, fg_color="transparent")
            pf.pack(fill="x", padx=20, pady=(0, 4))
            ctk.CTkLabel(pf, text=f"  {p['letter']}:",
                         font=ctk.CTkFont(family="Consolas", size=11),
                         text_color=T["TEXT_DIM"], width=30, anchor="w").pack(side="left")
            ctk.CTkLabel(pf, text=f"{p['used']}G / {p['total']}G  ({pct}%)",
                         font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                         text_color=bar_color).pack(side="left", padx=(4, 8))
            bar = ctk.CTkProgressBar(pf, height=4, width=100,
                                     fg_color=T["BAR_BG"],
                                     progress_color=bar_color,
                                     corner_radius=2)
            bar.set(pct / 100.0)
            bar.pack(side="left")
        ctk.CTkFrame(self.storage_card, fg_color="transparent", height=4).pack()
        self.storage_loaded = True

    # ── UPDATE LOOP ───────────────────────────────────────────────────────────
    def update_dashboard(self):
        if self._rebuilding:       # ← add these two lines
         return
        self.clock_lbl.configure(text=time.strftime("%H:%M:%S"))

        self.clock_lbl.configure(text=time.strftime("%H:%M:%S"))
        self._pulse_state = not self._pulse_state
        self.pulse_dot.configure(
            text_color=T["GREEN"] if self._pulse_state else T["BG"])

        # CPU
        cpu_val = sensor_reader.get_cpu_usage()
        try:    cpu_pct = float(str(cpu_val).replace("%", ""))
        except: cpu_pct = 0
        self.cpu_row.update(f"{cpu_val}%", pct=cpu_pct, color=usage_color(cpu_val))

        # GPU usage
        gpu_u = sensor_reader.get_gpu_usage()
        self.gpu_row.update(
            gpu_u, color=T["TEXT_DIM"] if "N/A" in str(gpu_u) else usage_color(gpu_u))

        # RAM
        ram_usage, ram_hw = sensor_reader.get_ram_info()
        try:    ram_pct = float(str(ram_usage).split("(")[1].replace("%)","").strip())
        except: ram_pct = 0
        self.ram_row.update(ram_usage, pct=ram_pct, color=usage_color(str(ram_pct)))
        self.ram_hw_lbl.configure(text=f"[ {ram_hw} ]")

        # GPU temp
        overall_temp = sensor_reader.get_overall_temp()
        sensor_reader.check_temp_alert(overall_temp)
        gpu_t = sensor_reader.get_gpu_temp(overall_temp)
        self.gpu_temp_row.update(f"{gpu_t} °C", color=temp_color(gpu_t))

        # storage
        self._load_storage_once()

        # per-core
        core_data = sensor_reader.get_per_core_data()
        for i in range(6):
            d    = core_data[i]
            lbls = self.core_rows[i]
            lbls["temp"].configure(text=d["temp"],  text_color=temp_color(d["temp"]))
            lbls["min"].configure( text=d["min"],   text_color=T["TEXT_DIM"])
            lbls["max"].configure( text=d["max"],   text_color=T["RED"])
            lbls["load"].configure(text=d["load"],  text_color=T["ACCENT"])

        # health
        health = sensor_reader.get_health_status(overall_temp)
        h_col  = {"Critical": T["RED"], "Normal": T["YELLOW"],
                  "Optimal":  T["GREEN"]}.get(health, T["GREEN"])
        h_icon = {"Critical": "◉", "Normal": "◎", "Optimal": "◉"}.get(health, "◉")
        self.health_lbl.configure(
            text=f"SYSTEM HEALTH  ──  {health.upper()}", text_color=h_col)
        self.health_icon.configure(text=h_icon, text_color=h_col)
        self.health_card._stripe.configure(fg_color=h_col)

        self._after_id = self.after(1000, self.update_dashboard)


if __name__ == "__main__":
    app = TempoooApp()
    app.mainloop()