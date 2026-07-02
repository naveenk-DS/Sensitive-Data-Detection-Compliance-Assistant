import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFilter
import os
from typing import List, Dict, Any
from pdf2image import convert_from_path

def mask_text_in_pdf(pdf_path: str, output_path: str, sensitive_items: List[Dict[str, Any]], mode: str = "Full Black Box"):
    """
    Redact sensitive items in a text-based PDF using PyMuPDF.
    """
    doc = fitz.open(pdf_path)
    
    # Collect all unique values to redact
    values_to_redact = set([item["Detected Value"] for item in sensitive_items])
    
    for page in doc:
        for val in values_to_redact:
            text_instances = page.search_for(val)
            for inst in text_instances:
                if mode == "Full Black Box":
                    page.add_redact_annot(inst, fill=(0, 0, 0))
                elif mode == "Partial Mask":
                    # PyMuPDF doesn't directly support partial string masking easily through search_for (returns whole rect)
                    # We approximate by masking with a gray box or standard redaction
                    page.add_redact_annot(inst, fill=(0.5, 0.5, 0.5))
                elif mode == "Highlight Before Masking":
                    page.add_highlight_annot(inst)
                    page.add_redact_annot(inst, fill=(0, 0, 0))
                else:
                    page.add_redact_annot(inst, fill=(0, 0, 0))
                    
        page.apply_redactions()
        
    doc.save(output_path)
    doc.close()
    return output_path

def mask_scanned_pdf(pdf_path: str, output_path: str, page_data: Dict[int, Any], sensitive_items: List[Dict[str, Any]], mode: str = "Full Black Box"):
    """
    Redact scanned PDFs by drawing on the images directly.
    """
    values_to_redact = set([item["Detected Value"] for item in sensitive_items])
    images = convert_from_path(pdf_path)
    masked_images = []
    
    for i, img in enumerate(images):
        page_num = i + 1
        data = page_data.get(page_num, {})
        boxes = data.get("boxes", [])
        
        # PIL drawing
        draw = ImageDraw.Draw(img)
        
        for box_info in boxes:
            text = box_info["text"]
            # Check if any sensitive value is in this text box
            for val in values_to_redact:
                if val in text:
                    coords = box_info["box"]
                    # coords: [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
                    x_min = min([p[0] for p in coords])
                    y_min = min([p[1] for p in coords])
                    x_max = max([p[0] for p in coords])
                    y_max = max([p[1] for p in coords])
                    
                    if mode == "Full Black Box" or mode == "Highlight Before Masking":
                        draw.rectangle([x_min, y_min, x_max, y_max], fill="black")
                    elif mode == "Blur Sensitive Data":
                        # Crop, blur, paste back
                        box = (int(x_min), int(y_min), int(x_max), int(y_max))
                        ic = img.crop(box)
                        ic = ic.filter(ImageFilter.GaussianBlur(radius=5))
                        img.paste(ic, box)
                    else:
                        draw.rectangle([x_min, y_min, x_max, y_max], fill="gray")
                        
        masked_images.append(img)
        
    # Save images back to PDF
    if masked_images:
        masked_images[0].save(
            output_path,
            save_all=True,
            append_images=masked_images[1:],
            resolution=100.0
        )
    return output_path

def redact_document(file_path: str, output_path: str, page_data: Dict[int, Any], sensitive_items: List[Dict[str, Any]], mode: str = "Full Black Box") -> str:
    """Entry point for document redaction."""
    # Check if scanned
    is_scanned = any(data.get("scanned", False) for data in page_data.values()) if page_data else False
    
    if is_scanned:
        return mask_scanned_pdf(file_path, output_path, page_data, sensitive_items, mode)
    else:
        return mask_text_in_pdf(file_path, output_path, sensitive_items, mode)
