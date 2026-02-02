

## 3. VIDEO ANALYSIS (35 sec)

### Step 2: Get results

**Run:**
```bash
aws rekognition get-face-detection \
  --job-id "$(cat /tmp/jobid.txt)" \
  --query 'Faces[0:5].{Timestamp:Timestamp,Age:Face.AgeRange,Smile:Face.Smile.Value,Emotion:Face.Emotions[0].Type,Confidence:Face.Emotions[0].Confidence}'
```

**Key APIs:** `StartFaceDetection`, `GetFaceDetection`, `StartLabelDetection`

---

## 4. CUSTOM LABELS (45 sec)


### Step 3: Test BEFORE the model (during training)


**Run:**
```bash
aws rekognition detect-labels \
  --image '{"S3Object":{"Bucket":"rekognition-test-rodrigo-1768768123","Name":"RyuStreetFighterTwoHadoken.png"}}' \
  --query 'Labels[].Name'
```



### Step 4: Test AFTER the model is trained

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
