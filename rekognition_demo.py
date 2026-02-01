#!/usr/bin/env python3
"""
AWS Rekognition Face Detection Demo
Simple demonstration of AWS Rekognition for face detection
"""

import boto3
import json
from botocore.exceptions import ClientError

def detect_faces_rekognition(image_path):
    """
    Detect faces in an image using AWS Rekognition
    
    Args:
        image_path: Path to the image file
    """
    # Initialize Rekognition client
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    
    try:
        # Read image file
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
        
        print(f"\n{'='*60}")
        print("AWS REKOGNITION - Face Detection Demo")
        print(f"{'='*60}")
        print(f"Analyzing image: {image_path}")
        
        # Call Rekognition API
        response = rekognition.detect_faces(
            Image={'Bytes': image_bytes},
            Attributes=['ALL']  # Get detailed face attributes
        )
        
        # Process results
        face_details = response['FaceDetails']
        num_faces = len(face_details)
        
        print(f"\n✓ Faces detected: {num_faces}")
        
        # Display details for each face
        for idx, face in enumerate(face_details, 1):
            print(f"\n--- Face {idx} ---")
            
            # Bounding box
            bbox = face['BoundingBox']
            print(f"  Position: ({bbox['Left']:.2%}, {bbox['Top']:.2%})")
            print(f"  Size: {bbox['Width']:.2%} x {bbox['Height']:.2%}")
            
            # Confidence
            print(f"  Confidence: {face['Confidence']:.2f}%")
            
            # Age range
            age_range = face.get('AgeRange', {})
            if age_range:
                print(f"  Age Range: {age_range.get('Low', 'N/A')} - {age_range.get('High', 'N/A')}")
            
            # Gender
            gender = face.get('Gender', {})
            if gender:
                print(f"  Gender: {gender.get('Value', 'N/A')} ({gender.get('Confidence', 0):.1f}%)")
            
            # Emotions
            emotions = face.get('Emotions', [])
            if emotions:
                top_emotion = max(emotions, key=lambda x: x['Confidence'])
                print(f"  Primary Emotion: {top_emotion['Type']} ({top_emotion['Confidence']:.1f}%)")
            
            # Quality
            quality = face.get('Quality', {})
            if quality:
                print(f"  Image Quality:")
                print(f"    Brightness: {quality.get('Brightness', 0):.2f}")
                print(f"    Sharpness: {quality.get('Sharpness', 0):.2f}")
        
        print(f"\n{'='*60}")
        print("Analysis complete!")
        print(f"{'='*60}\n")
        
        return response
        
    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
        return None
    except ClientError as e:
        print(f"AWS Error: {e.response['Error']['Message']}")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def main():
    """Main function for demo"""
    import sys
    
    # Check arguments
    if len(sys.argv) < 2:
        print("\nUsage: python rekognition_demo.py <image_path>")
        print("Example: python rekognition_demo.py photo.jpg")
        print("\nNote: Requires AWS credentials configured")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Run detection
    result = detect_faces_rekognition(image_path)
    
    if result:
        print("\n💡 Key Features Demonstrated:")
        print("  • Managed service - no model training needed")
        print("  • Rich facial attributes (age, gender, emotions)")
        print("  • Simple API - just one function call")
        print("  • Automatic scaling and updates")


if __name__ == "__main__":
    main()
