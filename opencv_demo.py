#!/usr/bin/env python3
"""
OpenCV Face Detection Demo
Simple demonstration of OpenCV for face detection using Haar Cascades
"""

import cv2
import sys
import os


def detect_faces_opencv(image_path):
    """
    Detect faces in an image using OpenCV Haar Cascades
    
    Args:
        image_path: Path to the image file
    """
    
    print(f"\n{'='*60}")
    print("OPENCV - Face Detection Demo")
    print(f"{'='*60}")
    print(f"Analyzing image: {image_path}")
    
    try:
        # Load the image
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Error: Could not load image from {image_path}")
            return None
        
        # Convert to grayscale (required for Haar Cascade)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Load pre-trained Haar Cascade classifier
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if face_cascade.empty():
            print("Error: Could not load Haar Cascade classifier")
            return None
        
        # Detect faces
        # Parameters:
        # - scaleFactor: how much the image size is reduced at each scale
        # - minNeighbors: how many neighbors each candidate rectangle should have
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        num_faces = len(faces)
        print(f"\n✓ Faces detected: {num_faces}")
        
        # Display details for each face
        height, width = image.shape[:2]
        
        for idx, (x, y, w, h) in enumerate(faces, 1):
            print(f"\n--- Face {idx} ---")
            
            # Calculate normalized coordinates
            left = x / width
            top = y / height
            box_width = w / width
            box_height = h / height
            
            print(f"  Position: ({left:.2%}, {top:.2%})")
            print(f"  Size: {box_width:.2%} x {box_height:.2%}")
            print(f"  Absolute: x={x}, y={y}, w={w}, h={h}")
            
            # Calculate center point
            center_x = x + w // 2
            center_y = y + h // 2
            print(f"  Center: ({center_x}, {center_y})")
        
        # Option to save annotated image
        if num_faces > 0:
            output_path = image_path.rsplit('.', 1)[0] + '_detected.jpg'
            
            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Save the result
            cv2.imwrite(output_path, image)
            print(f"\n💾 Annotated image saved: {output_path}")
        
        print(f"\n{'='*60}")
        print("Analysis complete!")
        print(f"{'='*60}\n")
        
        return faces
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def main():
    """Main function for demo"""
    
    # Check arguments
    if len(sys.argv) < 2:
        print("\nUsage: python opencv_demo.py <image_path>")
        print("Example: python opencv_demo.py photo.jpg")
        print("\nNote: Requires OpenCV installed (pip install opencv-python)")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}")
        sys.exit(1)
    
    # Run detection
    result = detect_faces_opencv(image_path)
    
    if result is not None:
        print("\n💡 Key Features Demonstrated:")
        print("  • Complete local control - no API calls")
        print("  • Customizable parameters (scaleFactor, minNeighbors)")
        print("  • No per-request costs")
        print("  • Can process and save annotated images")
        print("  • Works offline")
        
        print("\n🔧 Customization Options:")
        print("  • Adjust detection sensitivity")
        print("  • Choose different cascade classifiers")
        print("  • Apply custom preprocessing")
        print("  • Integrate with other CV algorithms")


if __name__ == "__main__":
    main()
