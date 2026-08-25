import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

def build_vector_figure1():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    # ---------------- Exact Theme Colors ----------------
    C_BLUE_HDR = RGBColor(0, 59, 153)       # #003B99
    C_BLUE_BORDER = RGBColor(165, 195, 245)
    C_BLUE_TEXT = RGBColor(0, 51, 153)
    C_BLUE_LINE = RGBColor(30, 80, 220)
    
    C_GREEN_HDR = RGBColor(10, 92, 43)      # #0A5C2B
    C_GREEN_BORDER = RGBColor(140, 205, 160)
    C_GREEN_TEXT = RGBColor(10, 92, 43)
    C_GREEN_LINE = RGBColor(16, 140, 60)
    
    C_PURPLE_HDR = RGBColor(59, 40, 150)    # #3B2896
    C_PURPLE_BORDER = RGBColor(190, 180, 235)
    C_PURPLE_TEXT = RGBColor(59, 40, 150)
    
    C_WHITE = RGBColor(255, 255, 255)
    C_DARK = RGBColor(25, 30, 40)
    C_MUTED = RGBColor(85, 95, 110)
    
    C_RED_TEXT = RGBColor(204, 0, 0)
    C_RED_BG = RGBColor(255, 242, 242)
    C_RED_BORDER = RGBColor(245, 140, 140)
    
    C_GRN_TEXT = RGBColor(0, 128, 40)
    C_GRN_BG = RGBColor(242, 255, 244)
    C_GRN_BORDER = RGBColor(120, 215, 140)

    # ---------------- Vector Drawing Helpers ----------------
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

    def add_icon(name, left, top, width, height):
        p = f"perfect_icons/{name}.png"
        if os.path.exists(p):
            return slide.shapes.add_picture(p, left, top, width, height)
        return None

    def add_line(x1, y1, x2, y2, color=C_DARK, dashed=False, width=1.5, has_arrow=True, elbow=False):
        c_type = MSO_CONNECTOR.ELBOW if elbow else MSO_CONNECTOR.STRAIGHT
        conn = slide.shapes.add_connector(c_type, x1, y1, x2, y2)
        conn.line.color.rgb = color
        conn.line.width = Pt(width)
        if dashed:
            conn.line.dash_style = MSO_LINE.DASH
        
        if has_arrow:
            spPr = conn._element.spPr
            ln = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}ln')
            if ln is not None:
                elem = parse_xml(f'<a:tailEnd {nsdecls("a")} type="triangle" w="med" len="med"/>')
                ln.append(elem)
        return conn

    # =========================================================================
    # 1. TOP SECTION: 1. Phenomenon: Safety Judges Disagree
    # =========================================================================
    top_x, top_y, top_w, top_h = Inches(0.2), Inches(0.12), Inches(12.933), Inches(1.88)
    draw_card(top_x, top_y, top_w, top_h, C_WHITE, C_BLUE_BORDER, 1.5)
    draw_banner(top_x, top_y, top_w, Inches(0.36), "1. Phenomenon: Safety Judges Disagree", C_BLUE_HDR)
    
    # 1.1 Shared Safety Criteria (Dashed Card)
    sc_x, sc_y, sc_w, sc_h = top_x + Inches(0.22), top_y + Inches(0.48), Inches(3.0), Inches(1.26)
    sc_card = draw_card(sc_x, sc_y, sc_w, sc_h, C_WHITE, C_BLUE_HDR, 1.2)
    sc_card.line.dash_style = pptx.enum.dml.MSO_LINE.DASH
    add_icon("clipboard", sc_x + Inches(0.16), sc_y + Inches(0.25), Inches(0.55), Inches(0.66))
    
    tx = slide.shapes.add_textbox(sc_x + Inches(0.80), sc_y + Inches(0.30), Inches(2.1), Inches(0.65))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p1 = tf.paragraphs[0]
    p1.text = "Shared Safety Criteria"
    p1.font.size = Pt(11.5)
    p1.font.bold = True
    p1.font.color.rgb = C_BLUE_TEXT
    p1.font.name = "Arial"
    p2 = tf.add_paragraph()
    p2.text = "(same policies & guidelines)"
    p2.font.size = Pt(9.5)
    p2.font.bold = False
    p2.font.color.rgb = C_DARK
    p2.font.name = "Arial"
    
    # Vector Arrow: Shared Safety Criteria -> Query-Response Pair
    qr_x, qr_y, qr_w, qr_h = sc_x + sc_w + Inches(0.55), sc_y, Inches(2.8), sc_h
    add_line(sc_x + sc_w, sc_y + sc_h / 2, qr_x, sc_y + sc_h / 2, C_BLUE_LINE, dashed=True, width=1.5)
    
    # 1.2 Query-Response Pair Card
    draw_card(qr_x, qr_y, qr_w, qr_h, C_WHITE, C_BLUE_HDR, 1.2)
    tx_qr = slide.shapes.add_textbox(qr_x + Inches(0.15), qr_y + Inches(0.10), qr_w - Inches(0.3), qr_h - Inches(0.2))
    tf_qr = tx_qr.text_frame
    tf_qr.word_wrap = True
    tf_qr.margin_left = tf_qr.margin_right = tf_qr.margin_top = tf_qr.margin_bottom = 0
    
    p_title = tf_qr.paragraphs[0]
    p_title.text = "Query–Response Pair"
    p_title.font.size = Pt(11.5)
    p_title.font.bold = True
    p_title.font.color.rgb = C_BLUE_TEXT
    p_title.font.name = "Arial"
    p_title.alignment = PP_ALIGN.CENTER
    
    p_q = tf_qr.add_paragraph()
    p_q.space_before = Pt(6)
    r1 = p_q.add_run()
    r1.text = "Query: "
    r1.font.bold = True
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = C_DARK
    r2 = p_q.add_run()
    r2.text = "[malicious request]"
    r2.font.bold = False
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = C_DARK
    
    p_r = tf_qr.add_paragraph()
    p_r.space_before = Pt(4)
    r3 = p_r.add_run()
    r3.text = "Response: "
    r3.font.bold = True
    r3.font.size = Pt(9.5)
    r3.font.color.rgb = C_DARK
    r4 = p_r.add_run()
    r4.text = "[model answer]"
    r4.font.bold = False
    r4.font.size = Pt(9.5)
    r4.font.color.rgb = C_DARK

    # 1.3 Judges and Fork Connectors
    j_x = qr_x + qr_w + Inches(0.68)
    ja_y = sc_y + Inches(0.04)
    jb_y = sc_y + Inches(0.68)
    
    fork_x = qr_x + qr_w + Inches(0.28)
    qr_mid_y = sc_y + sc_h / 2
    add_line(qr_x + qr_w, qr_mid_y, fork_x, qr_mid_y, C_BLUE_LINE, dashed=True, width=1.5, has_arrow=False)
    add_line(fork_x, qr_mid_y, fork_x, ja_y + Inches(0.25), C_BLUE_LINE, dashed=True, width=1.5, has_arrow=False)
    add_line(fork_x, ja_y + Inches(0.25), j_x, ja_y + Inches(0.25), C_BLUE_LINE, dashed=True, width=1.5, has_arrow=True)
    add_line(fork_x, qr_mid_y, fork_x, jb_y + Inches(0.25), C_BLUE_LINE, dashed=True, width=1.5, has_arrow=False)
    add_line(fork_x, jb_y + Inches(0.25), j_x, jb_y + Inches(0.25), C_BLUE_LINE, dashed=True, width=1.5, has_arrow=True)
    
    # Judge A Icon & Text
    add_icon("robot_face", j_x, ja_y, Inches(0.58), Inches(0.50))
    tx_ja = slide.shapes.add_textbox(j_x + Inches(0.68), ja_y + Inches(0.12), Inches(1.1), Inches(0.3))
    tf_ja = tx_ja.text_frame
    tf_ja.margin_left = tf_ja.margin_top = tf_ja.margin_right = tf_ja.margin_bottom = 0
    p_ja = tf_ja.paragraphs[0]
    p_ja.text = "Judge A"
    p_ja.font.size = Pt(11)
    p_ja.font.bold = True
    p_ja.font.color.rgb = C_BLUE_TEXT
    
    # Judge B Icon & Text
    add_icon("robot_face", j_x, jb_y, Inches(0.58), Inches(0.50))
    tx_jb = slide.shapes.add_textbox(j_x + Inches(0.68), jb_y + Inches(0.12), Inches(1.1), Inches(0.3))
    tf_jb = tx_jb.text_frame
    tf_jb.margin_left = tf_jb.margin_top = tf_jb.margin_right = tf_jb.margin_bottom = 0
    p_jb = tf_jb.paragraphs[0]
    p_jb.text = "Judge B"
    p_jb.font.size = Pt(11)
    p_jb.font.bold = True
    p_jb.font.color.rgb = C_BLUE_TEXT
    
    # Vector Arrows: Judges -> Badges
    dec_x = j_x + Inches(1.95)
    dec_w, dec_h = Inches(1.35), Inches(0.48)
    
    add_line(j_x + Inches(1.42), ja_y + Inches(0.25), dec_x, ja_y + Inches(0.25), C_BLUE_LINE, dashed=True, width=1.5)
    add_line(j_x + Inches(1.42), jb_y + Inches(0.25), dec_x, jb_y + Inches(0.25), C_BLUE_LINE, dashed=True, width=1.5)
    
    # 1.4 Unsafe / Safe Badges
    draw_card(dec_x, ja_y + Inches(0.01), dec_w, dec_h, C_RED_BG, C_RED_BORDER, 1.0)
    add_icon("unsafe_triangle", dec_x + Inches(0.15), ja_y + Inches(0.11), Inches(0.26), Inches(0.28))
    tx_u = slide.shapes.add_textbox(dec_x + Inches(0.48), ja_y + Inches(0.12), Inches(0.8), Inches(0.25))
    tf_u = tx_u.text_frame
    tf_u.margin_left = tf_u.margin_top = tf_u.margin_right = tf_u.margin_bottom = 0
    p_u = tf_u.paragraphs[0]
    p_u.text = "Unsafe"
    p_u.font.size = Pt(11.5)
    p_u.font.bold = True
    p_u.font.color.rgb = C_RED_TEXT
    
    draw_card(dec_x, jb_y + Inches(0.01), dec_w, dec_h, C_GRN_BG, C_GRN_BORDER, 1.0)
    add_icon("safe_shield", dec_x + Inches(0.15), jb_y + Inches(0.11), Inches(0.26), Inches(0.28))
    tx_s = slide.shapes.add_textbox(dec_x + Inches(0.48), jb_y + Inches(0.12), Inches(0.8), Inches(0.25))
    tf_s = tx_s.text_frame
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = "Safe"
    p_s.font.size = Pt(11.5)
    p_s.font.bold = True
    p_s.font.color.rgb = C_GRN_TEXT
    
    # 1.5 Badges -> Conflict Star (Black Dashed Elbow Lines)
    conf_x, conf_y, conf_w, conf_h = dec_x + dec_w + Inches(0.68), sc_y + Inches(0.06), Inches(1.65), Inches(1.16)
    conf_mid_y = sc_y + sc_h / 2
    fork2_x = dec_x + dec_w + Inches(0.35)
    
    add_line(dec_x + dec_w, ja_y + Inches(0.25), fork2_x, ja_y + Inches(0.25), C_DARK, dashed=True, width=1.2, has_arrow=False)
    add_line(fork2_x, ja_y + Inches(0.25), fork2_x, conf_mid_y - Inches(0.12), C_DARK, dashed=True, width=1.2, has_arrow=False)
    add_line(fork2_x, conf_mid_y - Inches(0.12), conf_x + Inches(0.15), conf_mid_y - Inches(0.12), C_DARK, dashed=True, width=1.2, has_arrow=True)
    
    add_line(dec_x + dec_w, jb_y + Inches(0.25), fork2_x, jb_y + Inches(0.25), C_DARK, dashed=True, width=1.2, has_arrow=False)
    add_line(fork2_x, jb_y + Inches(0.25), fork2_x, conf_mid_y + Inches(0.12), C_DARK, dashed=True, width=1.2, has_arrow=False)
    add_line(fork2_x, conf_mid_y + Inches(0.12), conf_x + Inches(0.15), conf_mid_y + Inches(0.12), C_DARK, dashed=True, width=1.2, has_arrow=True)
    
    # Conflict Explosion Star
    draw_card(conf_x, conf_y, conf_w, conf_h, C_WHITE, C_RED_TEXT, 1.5, shape_type=MSO_SHAPE.EXPLOSION2)
    tx_c = slide.shapes.add_textbox(conf_x, conf_y + Inches(0.40), conf_w, Inches(0.3))
    tf_c = tx_c.text_frame
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = "Conflict"
    p_c.font.size = Pt(12.5)
    p_c.font.bold = True
    p_c.font.color.rgb = C_RED_TEXT
    p_c.alignment = PP_ALIGN.CENTER

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
    add_icon("target_task", task_x + Inches(0.15), task_y + Inches(0.08), Inches(0.34), Inches(0.30))
    
    tx_t = slide.shapes.add_textbox(task_x + Inches(0.58), task_y + Inches(0.10), task_w - Inches(0.65), Inches(0.3))
    tf_t = tx_t.text_frame
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    r_t1 = p_t.add_run()
    r_t1.text = "Task: "
    r_t1.font.bold = True
    r_t1.font.color.rgb = C_GREEN_TEXT
    r_t1.font.size = Pt(10.5)
    r_t2 = p_t.add_run()
    r_t2.text = "Generate adversarial judge–evaluation cases that pass validator.py"
    r_t2.font.bold = False
    r_t2.font.color.rgb = C_DARK
    r_t2.font.size = Pt(10.5)
    
    # Generation Block Outer Frame
    gen_x, gen_y, gen_w, gen_h = task_x, task_y + task_h + Inches(0.1), task_w, Inches(3.12)
    draw_card(gen_x, gen_y, gen_w, gen_h, C_WHITE, C_GREEN_BORDER, 1.0)
    
    # TVD-Agent Card (Thinking Robot with Bulb)
    agent_x, agent_y, agent_w, agent_h = gen_x + Inches(0.20), gen_y + Inches(0.12), Inches(1.85), Inches(1.3)
    
    tx_ag = slide.shapes.add_textbox(agent_x, agent_y, agent_w, Inches(0.2))
    tf_ag = tx_ag.text_frame
    tf_ag.margin_left = tf_ag.margin_top = tf_ag.margin_right = tf_ag.margin_bottom = 0
    p_ag = tf_ag.paragraphs[0]
    p_ag.text = "TVD–Agent"
    p_ag.font.size = Pt(11.5)
    p_ag.font.bold = True
    p_ag.font.color.rgb = C_GREEN_TEXT
    p_ag.alignment = PP_ALIGN.CENTER
    
    add_icon("tvd_agent_bulb_robot", agent_x + Inches(0.32), agent_y + Inches(0.24), Inches(1.20), Inches(0.76))
    
    tx_sub = slide.shapes.add_textbox(agent_x - Inches(0.1), agent_y + Inches(1.04), agent_w + Inches(0.2), Inches(0.35))
    tf_sub = tx_sub.text_frame
    tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "search & generate\ncandidate examples"
    p_sub.font.size = Pt(8.5)
    p_sub.font.color.rgb = C_DARK
    p_sub.alignment = PP_ALIGN.CENTER
    
    # data.json Box
    dj_x, dj_y, dj_w, dj_h = gen_x + Inches(3.35), agent_y, Inches(3.10), Inches(1.3)
    draw_card(dj_x, dj_y, dj_w, dj_h, C_WHITE, C_GREEN_BORDER, 1.0)
    add_icon("data_doc", dj_x + Inches(0.15), dj_y + Inches(0.08), Inches(0.22), Inches(0.24))
    
    tx_djt = slide.shapes.add_textbox(dj_x + Inches(0.42), dj_y + Inches(0.08), Inches(1.5), Inches(0.2))
    tf_djt = tx_djt.text_frame
    tf_djt.margin_left = tf_djt.margin_top = tf_djt.margin_right = tf_djt.margin_bottom = 0
    p_djt = tf_djt.paragraphs[0]
    p_djt.text = "data.json"
    p_djt.font.size = Pt(10.5)
    p_djt.font.bold = True
    p_djt.font.color.rgb = C_GREEN_TEXT
    
    # JSON content with highlighted red "unsafe"
    tx_json = slide.shapes.add_textbox(dj_x + Inches(0.15), dj_y + Inches(0.32), dj_w - Inches(0.25), Inches(0.95))
    tf_json = tx_json.text_frame
    tf_json.word_wrap = True
    tf_json.margin_left = tf_json.margin_top = tf_json.margin_right = tf_json.margin_bottom = 0
    
    lines = [
        ('{\n  "malicious_goal": "How to make a cake? adv",\n  "adversarial_prompt": "???",\n  "response": "???",\n  "gold_label": ', False, C_DARK),
        ('"unsafe"', True, C_RED_TEXT),
        ('\n}', False, C_DARK)
    ]
    p_j = tf_json.paragraphs[0]
    for txt, is_bld, clr in lines:
        r = p_j.add_run()
        r.text = txt
        r.font.name = "Courier New"
        r.font.size = Pt(8.0)
        r.font.bold = is_bld
        r.font.color.rgb = clr
    
    # Vector Interaction Arrows between TVD-Agent and data.json
    arr_y1 = agent_y + Inches(0.45)
    arr_y2 = agent_y + Inches(0.85)
    
    tx_wce = slide.shapes.add_textbox(agent_x + agent_w, arr_y1 - Inches(0.24), dj_x - (agent_x + agent_w), Inches(0.22))
    tf_wce = tx_wce.text_frame
    tf_wce.margin_left = tf_wce.margin_top = tf_wce.margin_right = tf_wce.margin_bottom = 0
    p_wce = tf_wce.paragraphs[0]
    p_wce.text = "write candidate examples"
    p_wce.font.size = Pt(8.0)
    p_wce.font.color.rgb = C_DARK
    p_wce.alignment = PP_ALIGN.CENTER
    
    add_line(agent_x + agent_w + Inches(0.05), arr_y1, dj_x - Inches(0.05), arr_y1, C_DARK, dashed=False, width=1.2)
    add_line(dj_x - Inches(0.05), arr_y2, agent_x + agent_w + Inches(0.05), arr_y2, C_DARK, dashed=True, width=1.2)
    
    tx_frs = slide.shapes.add_textbox(agent_x + agent_w, arr_y2 + Inches(0.03), dj_x - (agent_x + agent_w), Inches(0.35))
    tf_frs = tx_frs.text_frame
    tf_frs.margin_left = tf_frs.margin_top = tf_frs.margin_right = tf_frs.margin_bottom = 0
    p_frs = tf_frs.paragraphs[0]
    p_frs.text = "failed\n(revise / search)"
    p_frs.font.size = Pt(8.0)
    p_frs.font.color.rgb = C_DARK
    p_frs.alignment = PP_ALIGN.CENTER
    
    # Vector Arrow from data.json to validator.py
    val_x, val_y, val_h = gen_x + Inches(0.20), gen_y + Inches(1.6), Inches(1.42)
    val_w = Inches(4.80)
    
    add_line(dj_x + Inches(1.0), dj_y + dj_h + Inches(0.02), dj_x + Inches(1.0), val_y - Inches(0.02), C_DARK, dashed=False, width=1.2)
    tx_ev = slide.shapes.add_textbox(dj_x + Inches(1.08), dj_y + dj_h + Inches(0.02), Inches(0.8), Inches(0.2))
    tf_ev = tx_ev.text_frame
    tf_ev.margin_left = tf_ev.margin_top = tf_ev.margin_right = tf_ev.margin_bottom = 0
    p_ev = tf_ev.paragraphs[0]
    p_ev.text = "evaluate"
    p_ev.font.size = Pt(8.0)
    p_ev.font.color.rgb = C_DARK
    
    # validator.py Box
    draw_card(val_x, val_y, val_w, val_h, C_WHITE, C_GREEN_HDR, 1.0)
    tx_v = slide.shapes.add_textbox(val_x, val_y + Inches(0.03), val_w, Inches(0.2))
    tf_v = tx_v.text_frame
    tf_v.margin_left = tf_v.margin_top = tf_v.margin_right = tf_v.margin_bottom = 0
    p_v = tf_v.paragraphs[0]
    p_v.text = "validator.py"
    p_v.font.size = Pt(11)
    p_v.font.bold = True
    p_v.font.color.rgb = C_GREEN_TEXT
    p_v.alignment = PP_ALIGN.CENTER
    
    # Same criteria box inside validator
    sc_crit_x, sc_crit_y, sc_crit_w, sc_crit_h = val_x + Inches(0.15), val_y + Inches(0.25), val_w - Inches(0.3), Inches(0.58)
    sc_crit_box = draw_card(sc_crit_x, sc_crit_y, sc_crit_w, sc_crit_h, C_WHITE, C_GREEN_BORDER, 1.0)
    sc_crit_box.line.dash_style = pptx.enum.dml.MSO_LINE.DASH
    
    # same [🛡️] criteria Header in validator (floating pill)
    pill_w, pill_h = Inches(1.5), Inches(0.20)
    pill_x = sc_crit_x + (sc_crit_w - pill_w) / 2
    draw_card(pill_x, sc_crit_y - Inches(0.02), pill_w, pill_h, C_WHITE, C_GREEN_BORDER, 0.8)
    
    tx_sm = slide.shapes.add_textbox(pill_x + Inches(0.06), sc_crit_y - Inches(0.02), Inches(0.48), pill_h)
    tf_sm = tx_sm.text_frame
    tf_sm.margin_left = tf_sm.margin_top = tf_sm.margin_right = tf_sm.margin_bottom = 0
    p_sm = tf_sm.paragraphs[0]
    p_sm.text = "same"
    p_sm.font.size = Pt(8.5)
    p_sm.font.color.rgb = C_DARK
    p_sm.alignment = PP_ALIGN.RIGHT
    
    add_icon("shield_criteria", pill_x + Inches(0.58), sc_crit_y - Inches(0.01), Inches(0.18), Inches(0.20))
    
    tx_cr = slide.shapes.add_textbox(pill_x + Inches(0.80), sc_crit_y - Inches(0.02), Inches(0.65), pill_h)
    tf_cr = tx_cr.text_frame
    tf_cr.margin_left = tf_cr.margin_top = tf_cr.margin_right = tf_cr.margin_bottom = 0
    p_cr = tf_cr.paragraphs[0]
    p_cr.text = "criteria"
    p_cr.font.size = Pt(8.5)
    p_cr.font.color.rgb = C_DARK
    p_cr.alignment = PP_ALIGN.LEFT
    
    # Left Judge inside validator
    add_icon("robot_face", sc_crit_x + Inches(0.15), sc_crit_y + Inches(0.12), Inches(0.40), Inches(0.35))
    
    tx_vja = slide.shapes.add_textbox(sc_crit_x + Inches(0.60), sc_crit_y + Inches(0.10), Inches(0.8), Inches(0.18))
    tf_vja = tx_vja.text_frame
    tf_vja.margin_left = tf_vja.margin_top = tf_vja.margin_right = tf_vja.margin_bottom = 0
    p_vja = tf_vja.paragraphs[0]
    p_vja.text = "Judge A"
    p_vja.font.size = Pt(8.5)
    p_vja.font.bold = True
    p_vja.font.color.rgb = C_BLUE_TEXT
    
    draw_card(sc_crit_x + Inches(0.60), sc_crit_y + Inches(0.28), Inches(0.65), Inches(0.20), C_RED_BG, C_RED_BORDER, 0.8)
    tx_vu = slide.shapes.add_textbox(sc_crit_x + Inches(0.60), sc_crit_y + Inches(0.29), Inches(0.65), Inches(0.18))
    tf_vu = tx_vu.text_frame
    tf_vu.margin_left = tf_vu.margin_top = tf_vu.margin_right = tf_vu.margin_bottom = 0
    p_vu = tf_vu.paragraphs[0]
    p_vu.text = "Unsafe"
    p_vu.font.size = Pt(7.5)
    p_vu.font.bold = True
    p_vu.font.color.rgb = C_RED_TEXT
    p_vu.alignment = PP_ALIGN.CENTER
    
    # VS text with circle
    vs_circle = draw_card(sc_crit_x + Inches(2.00), sc_crit_y + Inches(0.20), Inches(0.42), Inches(0.32), C_WHITE, C_DARK, 0.8, shape_type=MSO_SHAPE.OVAL)
    tf_vsc = vs_circle.text_frame
    tf_vsc.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_vsc.margin_left = tf_vsc.margin_right = tf_vsc.margin_top = tf_vsc.margin_bottom = 0
    p_vsc = tf_vsc.paragraphs[0]
    p_vsc.text = "VS"
    p_vsc.font.size = Pt(9.0)
    p_vsc.font.bold = True
    p_vsc.font.color.rgb = C_DARK
    p_vsc.alignment = PP_ALIGN.CENTER
    
    # Right Judge inside validator
    add_icon("robot_face", sc_crit_x + sc_crit_w - Inches(0.55), sc_crit_y + Inches(0.12), Inches(0.40), Inches(0.35))
    
    tx_vjb = slide.shapes.add_textbox(sc_crit_x + sc_crit_w - Inches(1.45), sc_crit_y + Inches(0.10), Inches(0.8), Inches(0.18))
    tf_vjb = tx_vjb.text_frame
    tf_vjb.margin_left = tf_vjb.margin_top = tf_vjb.margin_right = tf_vjb.margin_bottom = 0
    p_vjb = tf_vjb.paragraphs[0]
    p_vjb.text = "Judge B"
    p_vjb.font.size = Pt(8.5)
    p_vjb.font.bold = True
    p_vjb.font.color.rgb = C_BLUE_TEXT
    p_vjb.alignment = PP_ALIGN.RIGHT
    
    draw_card(sc_crit_x + sc_crit_w - Inches(1.32), sc_crit_y + Inches(0.28), Inches(0.65), Inches(0.20), C_GRN_BG, C_GRN_BORDER, 0.8)
    tx_vs = slide.shapes.add_textbox(sc_crit_x + sc_crit_w - Inches(1.32), sc_crit_y + Inches(0.29), Inches(0.65), Inches(0.18))
    tf_vs = tx_vs.text_frame
    tf_vs.margin_left = tf_vs.margin_top = tf_vs.margin_right = tf_vs.margin_bottom = 0
    p_vs = tf_vs.paragraphs[0]
    p_vs.text = "Safe"
    p_vs.font.size = Pt(7.5)
    p_vs.font.bold = True
    p_vs.font.color.rgb = C_GRN_TEXT
    p_vs.alignment = PP_ALIGN.CENTER
    
    # Outcome Boxes in validator
    fail_x, out_y, out_w, out_h = val_x + Inches(0.15), val_y + Inches(0.88), Inches(2.10), Inches(0.45)
    draw_card(fail_x, out_y, out_w, out_h, C_WHITE, C_RED_BORDER, 1.0)
    tx_fl = slide.shapes.add_textbox(fail_x, out_y + Inches(0.04), out_w, Inches(0.38))
    tf_fl = tx_fl.text_frame
    tf_fl.margin_left = tf_fl.margin_top = tf_fl.margin_right = tf_fl.margin_bottom = 0
    p_fl1 = tf_fl.paragraphs[0]
    p_fl1.text = "❌ Failed (Disagreement)"
    p_fl1.font.size = Pt(8.5)
    p_fl1.font.bold = True
    p_fl1.font.color.rgb = C_RED_TEXT
    p_fl1.alignment = PP_ALIGN.CENTER
    p_fl2 = tf_fl.add_paragraph()
    p_fl2.text = "Judges disagree (A ≠ B)"
    p_fl2.font.size = Pt(8.0)
    p_fl2.font.color.rgb = C_DARK
    p_fl2.alignment = PP_ALIGN.CENTER
    
    succ_x = val_x + Inches(2.40)
    draw_card(succ_x, out_y, out_w, out_h, C_WHITE, C_GRN_BORDER, 1.0)
    tx_sc = slide.shapes.add_textbox(succ_x, out_y + Inches(0.04), out_w, Inches(0.38))
    tf_sc = tx_sc.text_frame
    tf_sc.margin_left = tf_sc.margin_top = tf_sc.margin_right = tf_sc.margin_bottom = 0
    p_sc1 = tf_sc.paragraphs[0]
    p_sc1.text = "✔ Success (Agreement)"
    p_sc1.font.size = Pt(8.5)
    p_sc1.font.bold = True
    p_sc1.font.color.rgb = C_GRN_TEXT
    p_sc1.alignment = PP_ALIGN.CENTER
    p_sc2 = tf_sc.add_paragraph()
    p_sc2.text = "Judges agree (A = B)"
    p_sc2.font.size = Pt(8.0)
    p_sc2.font.color.rgb = C_DARK
    p_sc2.alignment = PP_ALIGN.CENTER
    
    # Feedback Looping Lines (Black Dashed Lines: Failed -> left -> up directly under TVD-Agent)
    lp_x1 = fail_x
    lp_y1 = out_y + out_h / 2
    lp_x_turn = agent_x + Inches(0.20)
    lp_y_top = agent_y + Inches(1.42)
    
    add_line(lp_x1, lp_y1, lp_x_turn, lp_y1, C_DARK, dashed=True, width=1.2, has_arrow=False)
    add_line(lp_x_turn, lp_y1, lp_x_turn, lp_y_top, C_DARK, dashed=True, width=1.2, has_arrow=True)
    
    # Conflict Data Cylinder (Vector 3D Cylinder Shape)
    db_x, db_y, db_w, db_h = gen_x + Inches(5.15), val_y + Inches(0.12), Inches(1.30), Inches(1.30)
    db_shape = draw_card(db_x, db_y, db_w, db_h, C_GRN_BG, C_GREEN_HDR, 1.5, shape_type=MSO_SHAPE.CAN)
    tf_db = db_shape.text_frame
    tf_db.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_db = tf_db.paragraphs[0]
    p_db.text = "Conflict\nData"
    p_db.font.bold = True
    p_db.font.size = Pt(11)
    p_db.font.color.rgb = C_GREEN_HDR
    p_db.alignment = PP_ALIGN.CENTER
    
    # Vector Arrow: validator.py -> Conflict Data (Black solid line)
    add_line(succ_x + out_w, out_y + out_h / 2, db_x, out_y + out_h / 2, C_DARK, dashed=False, width=1.5, has_arrow=True)

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
        (5, "fm5_speaker", "Distraction by Irrelevant Cues", "attention captured by\nsuperficial signals"),
        (6, "fm6_brain", "Capability Limitations", "insufficient reasoning or\npolicy understanding"),
    ]
    
    fm_start_y = br_y + Inches(0.45)
    fm_card_h = Inches(0.55)
    fm_spacing = Inches(0.61)
    
    for i, (num, icon_name, title, subtitle) in enumerate(fm_items):
        row_y = fm_start_y + i * fm_spacing
        row_w = br_w - Inches(0.3)
        row_x = br_x + Inches(0.15)
        
        draw_card(row_x, row_y, row_w, fm_card_h, C_WHITE, C_PURPLE_BORDER, 1.0)
        
        # Purple Number Badge
        num_card = draw_card(row_x + Inches(0.15), row_y + Inches(0.10), Inches(0.35), Inches(0.35), C_PURPLE_HDR, None, shape_type=MSO_SHAPE.OVAL)
        tf = num_card.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = str(num)
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER
        
        # Exact Original Icon
        add_icon(icon_name, row_x + Inches(0.65), row_y + Inches(0.06), Inches(0.46), Inches(0.42))
        
        # Text Block
        tx_fm = slide.shapes.add_textbox(row_x + Inches(1.25), row_y + Inches(0.06), Inches(4.0), Inches(0.44))
        tf_fm = tx_fm.text_frame
        tf_fm.word_wrap = True
        tf_fm.margin_left = tf_fm.margin_top = tf_fm.margin_right = tf_fm.margin_bottom = 0
        
        p_fmt = tf_fm.paragraphs[0]
        p_fmt.text = title
        p_fmt.font.size = Pt(11.0)
        p_fmt.font.bold = True
        p_fmt.font.color.rgb = C_PURPLE_TEXT
        
        p_fms = tf_fm.add_paragraph()
        p_fms.text = subtitle
        p_fms.font.size = Pt(9.0)
        p_fms.font.color.rgb = C_DARK

    # =========================================================================
    # 3. BOTTOM TAKEAWAY BOXES
    # =========================================================================
    t_y, t_h = Inches(6.45), Inches(0.92)
    
    # 3.1 Bulb
    t1_x, t1_w = Inches(0.2), Inches(4.1)
    draw_card(t1_x, t_y, t1_w, t_h, C_WHITE, C_BLUE_BORDER, 1.2)
    add_icon("bottom_bulb", t1_x + Inches(0.18), t_y + Inches(0.18), Inches(0.45), Inches(0.56))
    
    tx_b1 = slide.shapes.add_textbox(t1_x + Inches(0.75), t_y + Inches(0.16), t1_w - Inches(0.85), Inches(0.60))
    tf_b1 = tx_b1.text_frame
    tf_b1.word_wrap = True
    tf_b1.margin_left = tf_b1.margin_top = tf_b1.margin_right = tf_b1.margin_bottom = 0
    p_b1 = tf_b1.paragraphs[0]
    p_b1.text = "Frontier safety judges can disagree\nsubstantially even under the same criteria."
    p_b1.font.size = Pt(10.5)
    p_b1.font.bold = True
    p_b1.font.color.rgb = C_BLUE_TEXT
    p_b1.alignment = PP_ALIGN.CENTER
    
    # 3.2 Rocket
    t2_x, t2_w = Inches(4.5), Inches(4.3)
    draw_card(t2_x, t_y, t2_w, t_h, C_WHITE, C_GREEN_BORDER, 1.2)
    add_icon("bottom_rocket", t2_x + Inches(0.18), t_y + Inches(0.18), Inches(0.45), Inches(0.56))
    
    tx_b2 = slide.shapes.add_textbox(t2_x + Inches(0.75), t_y + Inches(0.10), t2_w - Inches(0.85), Inches(0.72))
    tf_b2 = tx_b2.text_frame
    tf_b2.word_wrap = True
    tf_b2.margin_left = tf_b2.margin_top = tf_b2.margin_right = tf_b2.margin_bottom = 0
    p_b2 = tf_b2.paragraphs[0]
    p_b2.text = "Automatically generates large-scale\njudge–failure data by searching for\ndisagreement–inducing cases."
    p_b2.font.size = Pt(10.0)
    p_b2.font.bold = True
    p_b2.font.color.rgb = C_GREEN_TEXT
    p_b2.alignment = PP_ALIGN.CENTER
    
    # 3.3 Target
    t3_x, t3_w = Inches(9.0), Inches(4.133)
    draw_card(t3_x, t_y, t3_w, t_h, C_WHITE, C_PURPLE_BORDER, 1.2)
    add_icon("bottom_target", t3_x + Inches(0.18), t_y + Inches(0.18), Inches(0.50), Inches(0.56))
    
    tx_b3 = slide.shapes.add_textbox(t3_x + Inches(0.75), t_y + Inches(0.16), t3_w - Inches(0.85), Inches(0.60))
    tf_b3 = tx_b3.text_frame
    tf_b3.word_wrap = True
    tf_b3.margin_left = tf_b3.margin_top = tf_b3.margin_right = tf_b3.margin_bottom = 0
    p_b3 = tf_b3.paragraphs[0]
    p_b3.text = "TVD–Conflict reveals systematic and\nrecurring judge failure patterns."
    p_b3.font.size = Pt(10.5)
    p_b3.font.bold = True
    p_b3.font.color.rgb = C_PURPLE_TEXT
    p_b3.alignment = PP_ALIGN.CENTER

    out_pptx = "TVD_Conflict_Figure1.pptx"
    prs.save(out_pptx)
    print(f"Presentation successfully saved to {out_pptx}")

if __name__ == "__main__":
    build_vector_figure1()
