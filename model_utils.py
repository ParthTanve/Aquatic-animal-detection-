# utils/model_utils.py
import cv2
import numpy as np

# Temporarily commenting out these imports until environment is fixed
# they are used in get_accurate_gradcam_snapshot function
# from pytorch_grad_cam import GradCAM
# from pytorch_grad_cam.utils.image import show_cam_on_image

def draw_standard_bounding_box(image, box, label="Aquatic Animal", conf=None):
    """Draws standard green box, label, and confidence."""
    x1, y1, x2, y2 = map(int, box)
    # Green Box
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
    text = label
    if conf is not None:
        text += f" {conf:.2f}"
    # Green Text
    cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return image

def apply_simulated_heatmap_at_box(image, box):
    """
    Simulates a thermal spot at detection location in real-time.
    Very fast, creates Blue->Red gradient overlaid on original image.
    """
    x1, y1, x2, y2 = map(int, box)
    
    # Create a blank black canvas image the size of the image
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
    # Calculate box center and 'heat' radius
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    radius = int(((x2-x1) + (y2-y1)) / 4) # Approximate radius
    if radius <=0: radius = 5
    
    # Draw a white circle 'heat source' at center
    cv2.circle(mask, (cx, cy), radius, 255, -1)
    
    # Blur heavily to create smooth gradient. Fixed large kernel for simulation speed.
    blurred_mask = cv2.GaussianBlur(mask, (151, 151), 0)
    
    # Normalise mask to 0-255 range for ColorMap application
    norm_heatmap = cv2.normalize(blurred_mask, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    # Apply ColorMap: Thermal effect (Blue is cool, Red is hot spot)
    color_heatmap = cv2.applyColorMap(norm_heatmap, cv2.COLORMAP_JET)
    
    # Overlay heatmap on original image using addWeighted. 
    # alpha is weight of original image, beta is weight of heatmap overlay.
    overlaid_image = cv2.addWeighted(image, 0.6, color_heatmap, 0.4, 0)
    
    return overlaid_image

def get_accurate_gradcam_snapshot(model, target_layer, input_tensor, original_image):
    """
    Generates slow, but accurate feature-based Grad-CAM heatmap for a snapshot.
    Note: Requires grad_cam library installed.
    """
    try:
        # Import inside function in case environment issue persist
        from pytorch_grad_cam import GradCAM 
        from pytorch_grad_cam.utils.image import show_cam_on_image
        cam = GradCAM(model=model, target_layers=[target_layer])
        grayscale_cam = cam(input_tensor=input_tensor)[0, :]
        rgb_img = np.float32(original_image) / 255
        visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
        return visualization
    except ImportError:
        # Fallback if library missing
        print("Missing 'grad_cam' library for accurate Grad-CAM.")
        return cv2.putText(original_image.copy(), "Requires pip install grad-cam", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)