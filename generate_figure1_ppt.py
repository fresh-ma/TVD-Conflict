import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_vector_figure1():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    # ---------------- Colors ----------------
    C_BLUE_HDR = RGBColor(0, 59, 153)       # #003B99
    C_BLUE_BG = RGBColor(240, 246, 255)
    C_BLUE_BORDER = RGBColor(165, 195, 245)
    C_BLUE_TEXT = RGBColor(0, 51, 153)
    
    C_GREEN_HDR = RGBColor(10, 92, 43)      # #0A5C2B
    C_GREEN_BG = RGBColor(242, 253, 245)
    C_GREEN_BORDER = RGBColor(140, 205, 160)
    C_GREEN_TEXT = RGBColor(10, 92, 43)
    
    C_PURPLE_HDR = RGBColor(59, 40, 150)    # #3B2896
    C_PURPLE_BG = RGBColor(246, 243, 255)
    C_PURPLE_BORDER = RGBColor(190, 180, 235)
    C_PURPLE_TEXT = RGBColor(59, 40, 150)
    
    C_WHITE = RGBColor(255, 255, 255)
    C_DARK = RGBColor(15, 23, 42)
    C_MUTED = RGBColor(71, 85, 105)
    C_BORDER_GRAY = RGBColor(203, 213, 225)
    
    C_RED_TEXT = RGBColor(204, 0, 0)
    C_RED_BG = RGBColor(255, 238, 238)
    C_RED_BORDER = RGBColor(240, 128, 128)
    
    C_GRN_TEXT = RGBColor(0, 128, 40)
    C_GRN_BG = RGBColor(238, 255, 240)
    C_GRN_BORDER = RGBColor(110, 210, 130)

    # ---------------- Vector Shape Helpers ----------------
    def draw_card(left, top, width, height, bg_color=C_WHITE, border_color=None, border_width=1.0, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
        s = slide.shapes.add_shape(shape_type, left, top, width, height)
        s.fill.solid()
        s.fill.fore_color.rgb = bg_color
        if border_color:
            s.line.color.rgb = border_color
            s.line.width = Pt(border_width)
        else:
            s.line.fill.background()
        return s

    def draw_banner(left, top, width, height, title, bg_color):
        s = draw_card(left, top, width, height, bg_color, None, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE)
        tf = s.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = C_WHITE
        p.font.name = "Arial"
        p.alignment = PP_ALIGN.CENTER
        return s

    def draw_textbox(left, top, width, height, text, size=10, bold=False, color=C_DARK, align=PP_ALIGN.LEFT, font_name="Arial"):
        tx = slide.shapes.add_textbox(left, top, width, height)
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = font_name
        p.alignment = align
        return tx

    def add_icon(name, left, top, width, height):
        p = f"clean_icons/icon_{name}.png"
        if os.path.exists(p):
            return slide.shapes.add_picture(p, left, top, width, height)
        return None

    # =========================================================================
    # 1. TOP SECTION: 1. Phenomenon: Safety Judges Disagree
    # =========================================================================
    top_x, top_y, top_w, top_h = Inches(0.2), Inches(0.12), Inches(12.933), Inches(1.88)
    draw_card(top_x, top_y, top_w, top_h, C_WHITE, C_BLUE_BORDER, 1.5)
    draw_banner(top_x, top_y, top_w, Inches(0.35), "1. Phenomenon: Safety Judges Disagree", C_BLUE_HDR)
    
    # 1.1 Shared Safety Criteria
    sc_x, sc_y, sc_w, sc_h = top_x + Inches(0.25), top_y + Inches(0.48), Inches(3.0), Inches(1.25)
    sc_card = draw_card(sc_x, sc_y, sc_w, sc_h, C_WHITE, C_BLUE_HDR, 1.2)
    sc_card.line.dash_style = pptx.enum.dml.MSO_LINE.DASH
    add_icon("clipboard", sc_x + Inches(0.18), sc_y + Inches(0.25), Inches(0.65), Inches(0.70))
    draw_textbox(sc_x + Inches(0.9), sc_y + Inches(0.35), Inches(2.0), Inches(0.28), "Shared Safety Criteria", 11, True, C_BLUE_TEXT)
    draw_textbox(sc_x + Inches(0.9), sc_y + Inches(0.65), Inches(2.0), Inches(0.28), "(same policies & guidelines)", 9.5, False, C_DARK)
    
    # Arrow 1
    draw_textbox(sc_x + sc_w + Inches(0.1), sc_y + Inches(0.48), Inches(0.45), Inches(0.3), "--->", 11, True, C_BLUE_TEXT)
    
    # 1.2 Query-Response Pair
    qr_x, qr_y, qr_w, qr_h = sc_x + sc_w + Inches(0.6), sc_y, Inches(2.75), sc_h
    draw_card(qr_x, qr_y, qr_w, qr_h, C_WHITE, C_BLUE_HDR, 1.2)
    draw_textbox(qr_x, qr_y + Inches(0.12), qr_w, Inches(0.25), "Query–Response Pair", 11, True, C_BLUE_TEXT, PP_ALIGN.CENTER)
    draw_textbox(qr_x + Inches(0.2), qr_y + Inches(0.45), qr_w - Inches(0.4), Inches(0.3), "Query: [malicious request]", 10, False, C_DARK)
    draw_textbox(qr_x + Inches(0.2), qr_y + Inches(0.78), qr_w - Inches(0.4), Inches(0.3), "Response: [model answer]", 10, False, C_DARK)
    
    # Branching arrows
    j_x = qr_x + qr_w + Inches(0.6)
    draw_textbox(qr_x + qr_w + Inches(0.08), sc_y + Inches(0.18), Inches(0.45), Inches(0.2), "--->", 11, True, C_BLUE_TEXT)
    draw_textbox(qr_x + qr_w + Inches(0.08), sc_y + Inches(0.78), Inches(0.45), Inches(0.2), "--->", 11, True, C_BLUE_TEXT)
    
    # 1.3 Judges
    ja_y = sc_y
    jb_y = sc_y + Inches(0.65)
    add_icon("robot", j_x, ja_y + Inches(0.02), Inches(0.6), Inches(0.55))
    draw_textbox(j_x + Inches(0.7), ja_y + Inches(0.18), Inches(1.1), Inches(0.3), "Judge A", 10.5, True, C_BLUE_TEXT)
    
    add_icon("robot", j_x, jb_y + Inches(0.02), Inches(0.6), Inches(0.55))
    draw_textbox(j_x + Inches(0.7), jb_y + Inches(0.18), Inches(1.1), Inches(0.3), "Judge B", 10.5, True, C_BLUE_TEXT)
    
    # 1.4 Unsafe / Safe Badges
    dec_x = j_x + Inches(1.9)
    dec_w, dec_h = Inches(1.3), Inches(0.48)
    
    # Unsafe
    draw_card(dec_x, ja_y + Inches(0.06), dec_w, dec_h, C_RED_BG, C_RED_BORDER, 1.0)
    add_icon("unsafe", dec_x + Inches(0.15), ja_y + Inches(0.15), Inches(0.25), Inches(0.28))
    draw_textbox(dec_x + Inches(0.45), ja_y + Inches(0.16), Inches(0.75), Inches(0.25), "Unsafe", 11, True, C_RED_TEXT)
    
    # Safe
    draw_card(dec_x, jb_y + Inches(0.06), dec_w, dec_h, C_GRN_BG, C_GRN_BORDER, 1.0)
    add_icon("safe", dec_x + Inches(0.15), jb_y + Inches(0.15), Inches(0.25), Inches(0.28))
    draw_textbox(dec_x + Inches(0.45), jb_y + Inches(0.16), Inches(0.75), Inches(0.25), "Safe", 11, True, C_GRN_TEXT)
    
    # 1.5 Conflict Explosion Star
    draw_textbox(dec_x + dec_w + Inches(0.08), ja_y + Inches(0.16), Inches(0.45), Inches(0.2), "--->", 11, True, C_RED_TEXT)
    draw_textbox(dec_x + dec_w + Inches(0.08), jb_y + Inches(0.16), Inches(0.45), Inches(0.2), "--->", 11, True, C_RED_TEXT)
    
    conf_x, conf_y, conf_w, conf_h = dec_x + dec_w + Inches(0.6), sc_y + Inches(0.08), Inches(1.5), Inches(1.1)
    draw_card(conf_x, conf_y, conf_w, conf_h, C_RED_BG, C_RED_TEXT, 1.5, shape_type=MSO_SHAPE.EXPLOSION2)
    draw_textbox(conf_x, conf_y + Inches(0.38), conf_w, Inches(0.3), "Conflict", 12, True, C_RED_TEXT, PP_ALIGN.CENTER)

    # =========================================================================
    # 2. BOTTOM SECTION
    # =========================================================================
    bot_y = Inches(2.12)
    bot_h = Inches(4.25)
    
    # -------------------------------------------------------------------------
    # 2.1 BOTTOM LEFT: 2. TVD–Conflict: Systematic Stress Testing
    # -------------------------------------------------------------------------
    bl_x, bl_y, bl_w, bl_h = Inches(0.2), bot_y, Inches(6.9), bot_h
    draw_card(bl_x, bl_y, bl_w, bl_h, C_WHITE, C_GREEN_BORDER, 1.5)
    draw_banner(bl_x, bl_y, bl_w, Inches(0.35), "2. TVD–Conflict: Systematic Stress Testing", C_GREEN_HDR)
    
    # Task Banner Box
    task_x, task_y, task_w, task_h = bl_x + Inches(0.15), bl_y + Inches(0.45), bl_w - Inches(0.3), Inches(0.45)
    draw_card(task_x, task_y, task_w, task_h, C_WHITE, C_GREEN_HDR, 1.0)
    add_icon("target", task_x + Inches(0.12), task_y + Inches(0.08), Inches(0.35), Inches(0.30))
    draw_textbox(task_x + Inches(0.55), task_y + Inches(0.10), task_w - Inches(0.6), Inches(0.3),
                 "Task: Generate adversarial judge–evaluation cases that pass validator.py", 10.5, True, C_GREEN_TEXT)
    
    # Generation Block Outer Frame
    gen_x, gen_y, gen_w, gen_h = task_x, task_y + task_h + Inches(0.1), task_w, Inches(3.12)
    draw_card(gen_x, gen_y, gen_w, gen_h, C_WHITE, C_GREEN_BORDER, 1.0)
    
    # TVD-Agent Card
    agent_x, agent_y, agent_w, agent_h = gen_x + Inches(0.15), gen_y + Inches(0.12), Inches(1.8), Inches(1.3)
    draw_textbox(agent_x, agent_y, agent_w, Inches(0.2), "TVD–Agent", 11, True, C_GREEN_TEXT, PP_ALIGN.CENTER)
    add_icon("robot", agent_x + Inches(0.5), agent_y + Inches(0.25), Inches(0.8), Inches(0.7))
    draw_textbox(agent_x - Inches(0.1), agent_y + Inches(1.02), agent_w + Inches(0.2), Inches(0.25), "search & generate\ncandidate examples", 8.5, False, C_DARK, PP_ALIGN.CENTER)
    
    # Arrows between TVD-Agent & data.json
    draw_textbox(agent_x + agent_w + Inches(0.1), agent_y + Inches(0.35), Inches(1.2), Inches(0.25), "write candidate\nexamples ➔", 8.5, False, C_DARK, PP_ALIGN.CENTER)
    draw_textbox(agent_x + agent_w + Inches(0.1), agent_y + Inches(0.85), Inches(1.2), Inches(0.25), "⬅ failed\n(revise / search)", 8.5, False, C_DARK, PP_ALIGN.CENTER)
    
    # data.json Box
    dj_x, dj_y, dj_w, dj_h = gen_x + Inches(3.2), agent_y, Inches(3.2), Inches(1.3)
    draw_card(dj_x, dj_y, dj_w, dj_h, C_WHITE, C_GREEN_BORDER, 1.0)
    add_icon("doc", dj_x + Inches(0.15), dj_y + Inches(0.08), Inches(0.22), Inches(0.24))
    draw_textbox(dj_x + Inches(0.42), dj_y + Inches(0.08), Inches(1.5), Inches(0.2), "data.json", 10.5, True, C_GREEN_TEXT)
    
    json_str = '{\n  "malicious_goal": "How to make a cake? adv",\n  "adversarial_prompt": "???",\n  "response": "???",\n  "gold_label": "unsafe"\n}'
    draw_textbox(dj_x + Inches(0.15), dj_y + Inches(0.3), dj_w - Inches(0.3), Inches(0.95), json_str, 8.5, False, C_DARK, font_name="Courier New")
    
    # Arrow to validator.py
    draw_textbox(dj_x + Inches(0.8), dj_y + dj_h + Inches(0.02), Inches(1.5), Inches(0.2), "⬇ evaluate", 8.5, False, C_DARK, PP_ALIGN.CENTER)
    
    # validator.py Box
    val_x, val_y, val_w, val_h = gen_x + Inches(0.15), gen_y + Inches(1.6), Inches(4.9), Inches(1.42)
    draw_card(val_x, val_y, val_w, val_h, C_WHITE, C_GREEN_HDR, 1.0)
    draw_textbox(val_x, val_y + Inches(0.05), val_w, Inches(0.2), "validator.py", 10.5, True, C_GREEN_TEXT, PP_ALIGN.CENTER)
    
    # Same criteria box inside validator
    sc_crit_x, sc_crit_y, sc_crit_w, sc_crit_h = val_x + Inches(0.25), val_y + Inches(0.26), val_w - Inches(0.5), Inches(0.58)
    draw_card(sc_crit_x, sc_crit_y, sc_crit_w, sc_crit_h, C_WHITE, C_GREEN_BORDER, 1.0)
    
    add_icon("safe", sc_crit_x + Inches(1.55), sc_crit_y + Inches(0.05), Inches(0.22), Inches(0.22))
    draw_textbox(sc_crit_x + Inches(1.05), sc_crit_y + Inches(0.05), Inches(0.5), Inches(0.2), "same", 8.5, False, C_DARK)
    draw_textbox(sc_crit_x + Inches(1.82), sc_crit_y + Inches(0.05), Inches(0.6), Inches(0.2), "criteria", 8.5, False, C_DARK)
    
    add_icon("robot", sc_crit_x + Inches(0.2), sc_crit_y + Inches(0.12), Inches(0.4), Inches(0.35))
    draw_textbox(sc_crit_x + Inches(0.65), sc_crit_y + Inches(0.12), Inches(0.8), Inches(0.18), "Judge A", 8.5, True, C_BLUE_TEXT)
    draw_textbox(sc_crit_x + Inches(0.65), sc_crit_y + Inches(0.28), Inches(0.8), Inches(0.18), "Unsafe", 8.0, True, C_RED_TEXT)
    
    draw_textbox(sc_crit_x + Inches(1.9), sc_crit_y + Inches(0.26), Inches(0.4), Inches(0.2), "VS", 9.5, True, C_DARK)
    
    add_icon("robot", sc_crit_x + sc_crit_w - Inches(0.6), sc_crit_y + Inches(0.12), Inches(0.4), Inches(0.35))
    draw_textbox(sc_crit_x + sc_crit_w - Inches(1.5), sc_crit_y + Inches(0.12), Inches(0.8), Inches(0.18), "Judge B", 8.5, True, C_BLUE_TEXT, PP_ALIGN.RIGHT)
    draw_textbox(sc_crit_x + sc_crit_w - Inches(1.5), sc_crit_y + Inches(0.28), Inches(0.8), Inches(0.18), "Safe", 8.0, True, C_GRN_TEXT, PP_ALIGN.RIGHT)
    
    # Outcome Boxes in validator
    fail_x, out_y, out_w, out_h = val_x + Inches(0.15), val_y + Inches(0.88), Inches(2.15), Inches(0.45)
    draw_card(fail_x, out_y, out_w, out_h, C_WHITE, C_RED_BORDER, 1.0)
    draw_textbox(fail_x, out_y + Inches(0.04), out_w, Inches(0.2), "❌ Failed (Disagreement)", 8.5, True, C_RED_TEXT, PP_ALIGN.CENTER)
    draw_textbox(fail_x, out_y + Inches(0.22), out_w, Inches(0.2), "Judges disagree (A ≠ B)", 8.0, False, C_DARK, PP_ALIGN.CENTER)
    
    succ_x = val_x + Inches(2.45)
    draw_card(succ_x, out_y, out_w, out_h, C_WHITE, C_GRN_BORDER, 1.0)
    draw_textbox(succ_x, out_y + Inches(0.04), out_w, Inches(0.2), "✔ Success (Agreement)", 8.5, True, C_GRN_TEXT, PP_ALIGN.CENTER)
    draw_textbox(succ_x, out_y + Inches(0.22), out_w, Inches(0.2), "Judges agree (A = B)", 8.0, False, C_DARK, PP_ALIGN.CENTER)
    
    # Conflict Data Database Cylinder
    db_x, db_y, db_w, db_h = gen_x + Inches(5.2), val_y + Inches(0.25), Inches(1.15), Inches(1.1)
    add_icon("db", db_x, db_y, db_w, db_h)
    draw_textbox(val_x + val_w + Inches(0.02), out_y + Inches(0.12), Inches(0.3), Inches(0.2), "➔", 11, True, C_GREEN_TEXT)

    # -------------------------------------------------------------------------
    # 2.2 BOTTOM RIGHT: 3. Failure Modes Extracted
    # -------------------------------------------------------------------------
    br_x, br_y, br_w, br_h = Inches(7.3), bot_y, Inches(5.833), bot_h
    draw_card(br_x, br_y, br_w, br_h, C_WHITE, C_PURPLE_BORDER, 1.5)
    draw_banner(br_x, br_y, br_w, Inches(0.35), "3. Failure Modes Extracted", C_PURPLE_HDR)
    
    fm_items = [
        (1, "fm1_scale", "Ambiguous Safety Criteria", "criteria admit multiple interpretations"),
        (2, "fm2_cross", "Refusal–Harmfulness Mismatch", "refusal phrasing but harmful content"),
        (3, "fm3_check", "Compliance–Safety Mismatch", "compliant form yet benign intent"),
        (4, "fm4_gauge", "Borderline Uncertainty (50/50)", "near–tie or unstable judgment"),
        (5, "fm5_speaker", "Distraction by Irrelevant Cues", "attention captured by superficial signals"),
        (6, "fm6_brain", "Capability Limitations", "insufficient reasoning or policy understanding"),
    ]
    
    fm_start_y = br_y + Inches(0.45)
    fm_card_h = Inches(0.55)
    fm_spacing = Inches(0.61)
    
    for i, (num, icon_name, title, subtitle) in enumerate(fm_items):
        row_y = fm_start_y + i * fm_spacing
        row_w = br_w - Inches(0.3)
        row_x = br_x + Inches(0.15)
        
        draw_card(row_x, row_y, row_w, fm_card_h, C_WHITE, C_PURPLE_BORDER, 1.0)
        
        num_card = draw_card(row_x + Inches(0.15), row_y + Inches(0.10), Inches(0.35), Inches(0.35), C_PURPLE_HDR, None, shape_type=MSO_SHAPE.OVAL)
        tf = num_card.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = str(num)
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER
        
        add_icon(icon_name, row_x + Inches(0.65), row_y + Inches(0.08), Inches(0.45), Inches(0.38))
        
        draw_textbox(row_x + Inches(1.3), row_y + Inches(0.07), Inches(4.0), Inches(0.22), title, 10.5, True, C_PURPLE_TEXT)
        draw_textbox(row_x + Inches(1.3), row_y + Inches(0.29), Inches(4.0), Inches(0.20), subtitle, 9.0, False, C_DARK)

    # =========================================================================
    # 3. BOTTOM TAKEAWAY BOXES
    # =========================================================================
    t_y, t_h = Inches(6.45), Inches(0.92)
    
    t1_x, t1_w = Inches(0.2), Inches(4.1)
    draw_card(t1_x, t_y, t1_w, t_h, C_WHITE, C_BLUE_BORDER, 1.2)
    add_icon("bulb", t1_x + Inches(0.15), t_y + Inches(0.16), Inches(0.55), Inches(0.6))
    draw_textbox(t1_x + Inches(0.8), t_y + Inches(0.18), t1_w - Inches(0.9), Inches(0.55),
                 "Frontier safety judges can disagree substantially even under the same criteria.", 9.5, True, C_BLUE_TEXT, PP_ALIGN.CENTER)
    
    t2_x, t2_w = Inches(4.5), Inches(4.3)
    draw_card(t2_x, t_y, t2_w, t_h, C_WHITE, C_GREEN_BORDER, 1.2)
    add_icon("rocket", t2_x + Inches(0.15), t_y + Inches(0.16), Inches(0.55), Inches(0.6))
    draw_textbox(t2_x + Inches(0.8), t_y + Inches(0.18), t2_w - Inches(0.9), Inches(0.55),
                 "Automatically generates large-scale judge-failure data by searching for disagreement-inducing cases.", 9.5, True, C_GREEN_TEXT, PP_ALIGN.CENTER)
    
    t3_x, t3_w = Inches(9.0), Inches(4.133)
    draw_card(t3_x, t_y, t3_w, t_h, C_WHITE, C_PURPLE_BORDER, 1.2)
    add_icon("target", t3_x + Inches(0.15), t_y + Inches(0.16), Inches(0.55), Inches(0.6))
    draw_textbox(t3_x + Inches(0.8), t_y + Inches(0.22), t3_w - Inches(0.9), Inches(0.55),
              "TVD–Conflict reveals systematic and recurring judge failure patterns.", 9.5, True, C_PURPLE_TEXT, PP_ALIGN.CENTER)

    out_pptx = "TVD_Conflict_Figure1.pptx"
    prs.save(out_pptx)
    print(f"Presentation successfully saved to {out_pptx}")

if __name__ == "__main__":
    build_vector_figure1()
