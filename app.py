import gradio as gr
import cv2
import numpy as np
from PIL import Image

def count_colonies(image):
    # Convert PIL to OpenCV
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Blur and threshold
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours (colonies)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter small noise
    colonies = [c for c in contours if cv2.contourArea(c) > 10]
    count = len(colonies)
    
    # Draw circles for visualization
    result_img = img.copy()
    cv2.drawContours(result_img, colonies, -1, (0, 255, 0), 2)
    
    return result_img, f"Estimated Colony Count: {count} | Tested on 4 agar plates - Early results promising (Day 39)"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🧫 AI Colony Counter App\nAI tool to count bacterial colonies on agar plates - 100 Days of AI for Health\nBuilt by Onyekwere Favour Adaeze")
    with gr.Row():
        inp = gr.Image(type="pil", label="Upload Agar Plate Photo")
        out_img = gr.Image(label="Detected Colonies")
    out_text = gr.Textbox(label="Result")
    btn = gr.Button("Count Colonies")
    btn.click(fn=count_colonies, inputs=inp, outputs=[out_img, out_text])

demo.launch()