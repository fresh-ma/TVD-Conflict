import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_figure1_ppt():
    prs = pptx.Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Blank slide layout
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)
    
    # ------------------ Color Palette ------------------
    BG_SLATE = RGBColor(248, 250, 252)       # #F8FAFC
    BORDER_GRAY = RGBColor(203, 213, 225)    # #CBD5E1
    BORDER_BLUE = RGBColor(147, 197, 253)    # #93C5FD
    BORDER_GREEN = RGBColor(110, 231, 183)   # #6EE7B7
    BORDER_PURPLE = RGBColor(196, 181, 253)  # #C4B5FD
    
    NAVY_BLUE = RGBColor(30, 58, 138)        # #1E3A8A
    DEEP_GREEN = RGBColor(6, 95, 70)         # #065F46
    DEEP_PURPLE = RGBColor(79, 70, 229)      # #4F46E5
    
    BOX_BLUE_BG = RGBColor(239, 246, 255)    # #EFF6FF
    BOX_GREEN_BG = RGBColor(236, 253, 245)   # #ECFDF5
    BOX_PURPLE_BG = RGBColor(245, 243, 255)  # #F5F3FF
    BOX_WHITE = RGBColor(255, 255, 255)
    
    TEXT_DARK = RGBColor(15, 23, 42)         # #0F172A
    TEXT_MUTED = RGBColor(71, 85, 105)       # #475569
    TEXT_WHITE = RGBColor(255, 255, 255)
    
    RED_BG = RGBColor(254, 226, 226)         # #FEE2E2
    RED_TEXT = RGBColor(185, 28, 28)         # #B91C1C
    RED_BORDER = RGBColor(248, 113, 113)     # #F87171
    
    GREEN_BG = RGBColor(220, 252, 231)       # #DCFCE7
    GREEN_TEXT = RGBColor(21, 128, 61)       # #15803D
    GREEN_BORDER = RGBColor(74, 222, 128)    # #4ADE80
    
    YELLOW_BG = RGBColor(254, 243, 199)      # #FEF3C7
    YELLOW_BORDER = RGBColor(251, 191, 36)   # #FBBF24
    
    # ------------------ Helper Functions ------------------
    def add_card(left, top, width, height, bg_color, border_color=None, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
        shape = slide.shapes.add_shape(shape_type, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    def add_header_banner(left, top, width, height, text, bg_color, text_color=TEXT_WHITE):
        shape = add_card(left, top, width, height, bg_color, None, MSO_SHAPE.ROUNDED_RECTANGLE)
        tf = shape.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = text_color
        p.font.name = "Arial"
        p.alignment = PP_ALIGN.CENTER
        return shape

    def add_text_box(left, top, width, height, title, body="", bg_color=BOX_WHITE, border_color=BORDER_GRAY, title_color=TEXT_DARK, body_color=TEXT_MUTED, align=PP_ALIGN.LEFT):
        shape = add_card(left, top, width, height, bg_color, border_color, MSO_SHAPE.ROUNDED_RECTANGLE)
        tf = shape.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = True
        tf.margin_left = Inches(0.08)
        tf.margin_right = Inches(0.08)
        tf.margin_top = Inches(0.06)
        tf.margin_bottom = Inches(0.06)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = title_color
        p.font.name = "Arial"
        p.alignment = align
        
        if body:
            p2 = tf.add_paragraph()
            p2.text = body
            p2.font.size = Pt(8.5)
            p2.font.color.rgb = body_color
            p2.font.name = "Arial"
            p2.alignment = align
        return shape

    # =========================================================================
    # 1. TOP SECTION: 1. Phenomenon: Safety Judges Disagree (Widescreen Top)
    # =========================================================================
    top_y = Inches(0.25)
    top_h = Inches(2.25)
    top_w = Inches(12.533)
    top_x = Inches(0.4)
    
    # Top Outer Container
    add_card(top_x, top_y, top_w, top_h, BOX_BLUE_BG, BORDER_BLUE)
    add_header_banner(top_x, top_y, top_w, Inches(0.36), "1. Phenomenon: Safety Judges Disagree under Identical Criteria", NAVY_BLUE)
    
    # 1.1 Shared Safety Criteria (Left)
    c1_x = top_x + Inches(0.2)
    c1_y = top_y + Inches(0.48)
    c1_w = Inches(2.3)
    c1_h = Inches(1.55)
    add_text_box(c1_x, c1_y, c1_w, c1_h, "📋 Shared Safety Criteria", 
                 "• Same policy & rubric\n• Identical safety definitions\n• Strict evaluation guidelines",
                 BOX_WHITE, BORDER_GRAY, NAVY_BLUE, TEXT_MUTED)
    
    # 1.2 Query-Response Pair (Center-Left)
    c2_x = c1_x + c1_w + Inches(0.3)
    c2_y = c1_y
    c2_w = Inches(3.2)
    c2_h = c1_h
    add_text_box(c2_x, c2_y, c2_w, c2_h, "💬 Candidate Response Pair",
                 "Query: [Malicious Intent Goal]\nResponse: [Model Answer containing implicit or wrapped payload]",
                 BOX_WHITE, BORDER_GRAY, TEXT_DARK, TEXT_MUTED)
    
    # 1.3 Judges (Center-Right: Parallel Evaluation)
    c3_x = c2_x + c2_w + Inches(0.35)
    c3_w = Inches(2.7)
    
    # Judge A box
    j_a_y = c1_y
    j_h = Inches(0.72)
    add_text_box(c3_x, j_a_y, c3_w, j_h, "🤖 Judge A (e.g. GPT-OSS)", "Evaluator Backbone A", BOX_WHITE, BORDER_GRAY, NAVY_BLUE, TEXT_MUTED)
    
    # Judge B box
    j_b_y = c1_y + Inches(0.83)
    add_text_box(c3_x, j_b_y, c3_w, j_h, "🤖 Judge B (e.g. Qwen/DeepSeek)", "Evaluator Backbone B", BOX_WHITE, BORDER_GRAY, NAVY_BLUE, TEXT_MUTED)
    
    # 1.4 Decisions & Conflict Badge (Right)
    c4_x = c3_x + c3_w + Inches(0.25)
    c4_w = Inches(1.3)
    
    # Decision A (Unsafe)
    add_text_box(c4_x, j_a_y, c4_w, j_h, "🚨 UNSAFE", "Violation Flagged", RED_BG, RED_BORDER, RED_TEXT, RED_TEXT, PP_ALIGN.CENTER)
    
    # Decision B (Safe)
    add_text_box(c4_x, j_b_y, c4_w, j_h, "✅ SAFE", "No Refusal Needed", GREEN_BG, GREEN_BORDER, GREEN_TEXT, GREEN_TEXT, PP_ALIGN.CENTER)
    
    # Conflict Outcome Banner (Far Right)
    c5_x = c4_x + c4_w + Inches(0.2)
    c5_w = Inches(1.7)
    c5_h = c1_h
    add_text_box(c5_x, c1_y, c5_w, c5_h, "⚡ CONFLICT", "Opposing Decisions!\n(Disagreement Induced)", YELLOW_BG, YELLOW_BORDER, RED_TEXT, TEXT_DARK, PP_ALIGN.CENTER)

    # =========================================================================
    # 2. BOTTOM SECTION: Left = TVD Pipeline | Right = 6 Failure Modes
    # =========================================================================
    bot_y = Inches(2.65)
    bot_h = Inches(4.55)
    
    # -------------------------------------------------------------------------
    # 2.1 BOTTOM LEFT: TVD-Conflict Framework
    # -------------------------------------------------------------------------
    bot_left_x = Inches(0.4)
    bot_left_w = Inches(6.7)
    
    add_card(bot_left_x, bot_y, bot_left_w, bot_h, BOX_GREEN_BG, BORDER_GREEN)
    add_header_banner(bot_left_x, bot_y, bot_left_w, Inches(0.36), "2. TVD-Conflict: Automated Judge Stress Testing", DEEP_GREEN)
    
    # Task Banner
    task_y = bot_y + Inches(0.46)
    task_h = Inches(0.55)
    add_text_box(bot_left_x + Inches(0.2), task_y, bot_left_w - Inches(0.4), task_h,
                 "🎯 Task Definition", "Generate adversarial response candidates that induce judge disagreement under validator.py",
                 BOX_WHITE, BORDER_GRAY, DEEP_GREEN, TEXT_MUTED)
    
    # Agent & Candidate Box
    agent_y = task_y + task_h + Inches(0.12)
    agent_h = Inches(1.35)
    agent_w = Inches(2.8)
    add_text_box(bot_left_x + Inches(0.2), agent_y, agent_w, agent_h,
                 "🧠 TVD-Agent", "• Proposes candidate response\n• Iteratively revises payload\n• Explores ambiguity boundaries",
                 BOX_WHITE, BORDER_GREEN, DEEP_GREEN, TEXT_MUTED)
    
    data_x = bot_left_x + Inches(0.2) + agent_w + Inches(0.2)
    data_w = bot_left_w - Inches(0.4) - agent_w - Inches(0.2)
    add_text_box(data_x, agent_y, data_w, agent_h,
                 "📄 Candidate data.json", "{\n  \"goal\": \"Malicious Request\",\n  \"candidate_response\": \"...\",\n  \"eval_target\": \"Judge Pair\"\n}",
                 BOX_WHITE, BORDER_GRAY, TEXT_DARK, TEXT_MUTED)
    
    # Double-Judge Validator Box
    val_y = agent_y + agent_h + Inches(0.12)
    val_h = Inches(1.8)
    val_w = bot_left_w - Inches(0.4)
    val_shape = add_card(bot_left_x + Inches(0.2), val_y, val_w, val_h, BOX_WHITE, BORDER_GREEN)
    
    # Inside Validator: Header
    add_text_box(bot_left_x + Inches(0.35), val_y + Inches(0.08), val_w - Inches(0.3), Inches(0.32),
                 "⚖️ validator.py (Inter-Judge Conflict Validator)", "", BOX_GREEN_BG, None, DEEP_GREEN, align=PP_ALIGN.CENTER)
    
    # Inside Validator: Branches
    branch_y = val_y + Inches(0.48)
    branch_w = Inches(2.8)
    branch_h = Inches(1.15)
    
    # Disagreement Branch -> Success (Collected)
    add_text_box(bot_left_x + Inches(0.35), branch_y, branch_w, branch_h,
                 "✅ Pass: Disagreement (A ≠ B)", "Judges conflict on safety label\n➔ Stored into Conflict Dataset (1000+ Pairs)",
                 GREEN_BG, GREEN_BORDER, GREEN_TEXT, TEXT_DARK, PP_ALIGN.CENTER)
    
    # Agreement Branch -> Fail (Feedback)
    add_text_box(bot_left_x + Inches(0.35) + branch_w + Inches(0.3), branch_y, branch_w, branch_h,
                 "❌ Reject: Agreement (A = B)", "Judges reach consensus\n➔ Return feedback & revise",
                 RED_BG, RED_BORDER, RED_TEXT, TEXT_DARK, PP_ALIGN.CENTER)

    # -------------------------------------------------------------------------
    # 2.2 BOTTOM RIGHT: 6 Failure Modes Extracted
    # -------------------------------------------------------------------------
    bot_right_x = Inches(7.3)
    bot_right_w = Inches(5.633)
    
    add_card(bot_right_x, bot_y, bot_right_w, bot_h, BOX_PURPLE_BG, BORDER_PURPLE)
    add_header_banner(bot_right_x, bot_y, bot_right_w, Inches(0.36), "3. Six Systematic Failure Modes Extracted", DEEP_PURPLE)
    
    # 6 Failure Mode Cards (2 columns x 3 rows)
    fm_start_y = bot_y + Inches(0.46)
    fm_card_w = Inches(2.55)
    fm_card_h = Inches(1.22)
    col1_x = bot_right_x + Inches(0.18)
    col2_x = col1_x + fm_card_w + Inches(0.17)
    
    failure_modes = [
        ("① Criteria Ambiguity", "Subjective boundary interpretation under stated criteria.", col1_x, fm_start_y),
        ("② Refusal-Harm Mismatch", "Starts with refusal but leaks executable harmful details.", col2_x, fm_start_y),
        ("③ Compliance-Safe Mismatch", "Compliant tone & structure while content is completely safe.", col1_x, fm_start_y + Inches(1.3)),
        ("④ 50-50 Uncertainty", "Borderline outputs causing stochastic coin-flip judgments.", col2_x, fm_start_y + Inches(1.3)),
        ("⑤ Distraction by Cues", "Attention captured by formatting, code, or roleplay wrappers.", col1_x, fm_start_y + Inches(2.6)),
        ("⑥ Capability Limits", "Evaluator lacks deep reasoning to infer implicit harmful intent.", col2_x, fm_start_y + Inches(2.6)),
    ]
    
    for title, desc, cx, cy in failure_modes:
        add_text_box(cx, cy, fm_card_w, fm_card_h, title, desc, BOX_WHITE, BORDER_PURPLE, DEEP_PURPLE, TEXT_MUTED)

    # Add Flow Arrows for Top Section
    def add_arrow_badge(left, top, text="➔", color=NAVY_BLUE):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.25), Inches(0.25))
        shape.fill.background()
        shape.line.fill.background()
        tf = shape.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        p.alignment = PP_ALIGN.CENTER
        return shape

    # Top flow arrows
    add_arrow_badge(c1_x + c1_w + Inches(0.03), c1_y + Inches(0.65), "➔", NAVY_BLUE)
    add_arrow_badge(c2_x + c2_w + Inches(0.05), c1_y + Inches(0.65), "➔", NAVY_BLUE)
    add_arrow_badge(c3_x + c3_w + Inches(0.01), j_a_y + Inches(0.23), "➔", RED_TEXT)
    add_arrow_badge(c3_x + c3_w + Inches(0.01), j_b_y + Inches(0.23), "➔", GREEN_TEXT)

    # Bottom Left Flow Arrows
    add_arrow_badge(bot_left_x + Inches(0.2) + agent_w + Inches(0.02), agent_y + Inches(0.55), "➔", DEEP_GREEN)
    add_arrow_badge(bot_left_x + Inches(3.2), agent_y + agent_h + Inches(0.01), "⬇", DEEP_GREEN)

    # Save presentation
    output_path = "TVD_Conflict_Figure1.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved to {output_path}")

if __name__ == "__main__":
    create_figure1_ppt()
