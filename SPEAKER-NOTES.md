# AWS Rekognition Demo - Speaker Notes (2:30)

## Quick Timeline
| Time | Topic |
|------|-------|
| 0:00 - 0:35 | Face Detection |
| 0:35 - 1:10 | PPE Detection |
| 1:10 - 1:45 | Video Analysis |
| 1:45 - 2:15 | Custom Labels |
| 2:15 - 2:30 | Wrap up |

---

## 1. FACE DETECTION (35 sec)

**Say:**
> "Rekognition can detect faces in real-time, identifying emotions, age range, and facial attributes like glasses or beard."

**Run:**
```bash
aws rekognition detect-faces \
  --image '{"S3Object":{"Bucket":"amzn-rekognition-poc-v2","Name":"12161378.jpg"}}' \
  --attributes ALL \
  --query 'FaceDetails[0].{Emotions:Emotions[0],AgeRange:AgeRange,Smile:Smile}'
```

**Point to:** emotions, age range, confidence %

**Key APIs:** `DetectFaces`, `CompareFaces`

---

## 2. PPE DETECTION (35 sec)

**Say:**
> "For workplace safety, Rekognition detects if workers are wearing proper protective equipment - masks, helmets, gloves."

**Run:**
```bash
aws rekognition detect-protective-equipment \
  --image '{"S3Object":{"Bucket":"amzn-rekognition-poc-v2","Name":"epi.jpeg"}}' \
  --query 'Persons[].BodyParts[].{Part:Name,Equipment:EquipmentDetections[].Type}'
```

**Point to:** detected body parts and equipment (helmet, mask, gloves)

**Limitation to mention:**
> "Notice the gloves aren't detected here. When hands are holding objects - like safety glasses in this image - Rekognition can't identify the gloves because the hands are obscured. This is a tradeoff of Rekognition. For this, you will need to use custom labels and train the model"

**Key API:** `DetectProtectiveEquipment`

---

## 3. VIDEO ANALYSIS (35 sec)

**Say:**
> "Rekognition also analyzes stored videos. It processes frame by frame, tracking emotions and attributes over time."

### Step 1: Start video analysis (async)

**Run:**
```bash
aws rekognition start-face-detection \
  --video '{"S3Object":{"Bucket":"amzn-rekognition-poc-v2","Name":"webcam_video_emotions.mp4"}}' \
  --face-attributes ALL \
  --query 'JobId' --output text > /tmp/jobid.txt && cat /tmp/jobid.txt
```

```bash
aws rekognition get-face-detection --job-id "$(cat /tmp/jobid.txt)"
```

**Point to:** JobId saved to file - this is async processing

### Step 2: Get results

**Run:**
```bash
aws rekognition get-face-detection \
  --job-id "$(cat /tmp/jobid.txt)" \
  --query 'Faces[0:5].{Timestamp:Timestamp,Age:Face.AgeRange,Smile:Face.Smile.Value,Emotion:Face.Emotions[0].Type,Confidence:Face.Emotions[0].Confidence}'
```

**Expected output:**
```json
[
  {"Timestamp": 0, "Age": {"Low": 42, "High": 50}, "Smile": false, "Emotion": "CALM", "Confidence": 99.0},
  {"Timestamp": 2000, "Age": {"Low": 37, "High": 45}, "Smile": true, "Emotion": "HAPPY", "Confidence": 96.4},
  {"Timestamp": 4000, "Age": {"Low": 41, "High": 49}, "Smile": false, "Emotion": "CONFUSED", "Confidence": 69.3}
]
```

**Point to:**
- Timestamp (milliseconds) - frame by frame analysis
- Emotion changes over time (CALM → HAPPY → CONFUSED)
- Consistent attribute detection (glasses, beard)

**Say:**
> "For live streaming, Rekognition integrates with Kinesis Video Streams using Stream Processors - same detection, real-time."

**Key APIs:** `StartFaceDetection`, `GetFaceDetection`, `StartLabelDetection`

---

## 4. CUSTOM LABELS (45 sec)

**Say:**
> "Pre-trained models recognize celebrities like Brad Pitt, but NOT fictional characters. Watch what happens with a superhero..."

### Step 1: Show S3 in Console
- Open S3 Console > Bucket with training images
- Show folder structure: each folder = one label
  
  Bucket URI:
  ```
  s3://custom-labels-console-us-east-1-7c07b8e174/streetfighter-custom-labels-training/
  ```
  ```
  s3://custom-labels-console-us-east-1-7c07b8e174/streetfighter-custom-labels-training
  ├── ryu/
  │   ├── img1.jpg
  │   └── img2.jpg
  ├── blanka/
  │   ├── img1.jpg
  │   └── img2.jpg
  ```

**Say:**
> "The folder name automatically defines the label. That simple."

### Step 2: Create Project and Train (Console)
- Console > Rekognition > Custom Labels > Create Project
- Point to the S3 bucket
- Start training

### Step 3: Test BEFORE the model (during training)

**Say:**
> "While the model trains, let's see what standard Rekognition recognizes..."

**Run:**
```bash
aws rekognition detect-labels \
  --image '{"S3Object":{"Bucket":"rekognition-test-rodrigo-1768768123","Name":"RyuStreetFighterTwoHadoken.png"}}' \
  --query 'Labels[].Name'
```

**Result:** `["Person", "Costume", "Mask", "Human"]` - Generic!

### Step 4: Test AFTER the model is trained

**Say:**
> "Now with our custom model..."

**Run:**
```bash
aws rekognition detect-custom-labels \
  --project-version-arn "arn:aws:rekognition:us-east-1:688991925317:project/aws-rekognition-poc-v3/version/aws-rekognition-poc-v3.2026-02-01T23.36.31/1769999792026" \
  --image '{"S3Object":{"Bucket":"rekognition-test-rodrigo-1768768123","Name":"RyuStreetFighterTwoHadoken.png"}}' \
  --query 'CustomLabels[].{Label:Name,Confidence:Confidence}'
```

**Result:** `[{"Label": "deadpool", "Confidence": 98.5}]`

**Say:**
> "No ML expertise needed. Just upload labeled images and Rekognition trains the model for you."

**Key API:** `DetectCustomLabels`

---
### Step 5: Show vscode with image of Scarlet Johansson


## CLOSING (15 sec)

**Say:**
> "Thats it today guys, thanks"

---

## CLI Reference

```bash
# Face Detection (image)
aws rekognition detect-faces --image '{"S3Object":{"Bucket":"BUCKET","Name":"FILE"}}'

# PPE Detection (Personal Protective Equipment)
aws rekognition detect-protective-equipment --image '{"S3Object":{"Bucket":"BUCKET","Name":"FILE"}}'

# Label Detection (standard)
aws rekognition detect-labels --image '{"S3Object":{"Bucket":"BUCKET","Name":"FILE"}}'

# Custom Labels
aws rekognition detect-custom-labels --project-version-arn "ARN" --image '{"S3Object":{"Bucket":"BUCKET","Name":"FILE"}}'

# Video Analysis (async - returns JobId)
aws rekognition start-face-detection --video '{"S3Object":{"Bucket":"BUCKET","Name":"VIDEO.mp4"}}' --face-attributes ALL
aws rekognition get-face-detection --job-id "JOB_ID"

# Other video analysis options
aws rekognition start-label-detection --video '{"S3Object":{"Bucket":"BUCKET","Name":"VIDEO.mp4"}}'
aws rekognition start-person-tracking --video '{"S3Object":{"Bucket":"BUCKET","Name":"VIDEO.mp4"}}'
```
