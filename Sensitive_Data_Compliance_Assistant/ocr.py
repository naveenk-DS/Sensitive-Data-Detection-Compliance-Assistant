from typing import List, Tuple, Dict, Any
import numpy as np

try:
    from paddleocr import PaddleOCR
    # Initialize PaddleOCR
    # use_angle_cls=True to support rotated text
    ocr_model = PaddleOCR(use_angle_cls=True, lang='en')
except ImportError:
    ocr_model = None

def extract_text_with_ocr(image: Any) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Runs OCR on a PIL Image or numpy array.
    Returns full text and bounding box information.
    """
    if ocr_model is None:
        raise ImportError("PaddleOCR is not installed. Please install it to use OCR features.")
        
    # Convert PIL image to numpy array if needed
    if not isinstance(image, np.ndarray):
        img_array = np.array(image)
    else:
        img_array = image
        
    result = ocr_model.ocr(img_array, cls=True)
    
    full_text = []
    boxes = []
    
    # PaddleOCR returns a list of lines for each batch (we process one image at a time)
    if result and result[0]:
        for line in result[0]:
            box = line[0] # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            text = line[1][0]
            confidence = line[1][1]
            
            full_text.append(text)
            boxes.append({
                "box": box,
                "text": text,
                "confidence": confidence
            })
            
    return "\n".join(full_text), boxes
