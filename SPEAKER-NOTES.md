# AWS Rekognition Demo - Speaker Notes (2:30)

## Quick Timeline
| Time | Topic |
|------|-------|
| 0:00 - 0:35 | Face Detection |
| 0:35 - 1:10 | PPE Detection |
| 1:10 - 1:45 | Video Stream |
| 1:45 - 2:15 | Custom Labels |
| 2:15 - 2:30 | Wrap up |

---

## 1. FACE DETECTION (35 sec)

**Say:**
> "Rekognition can detect faces in real-time, identifying emotions, age range, and facial attributes like glasses or beard."

**Show:**
- AWS Console > Rekognition > Face detection
- Upload a photo OR use sample image
- Point to: emotions, age range, confidence %

**Key APIs:** `DetectFaces`, `CompareFaces`

---

## 2. PPE DETECTION (35 sec)

**Say:**
> "For workplace safety, Rekognition detects if workers are wearing proper protective equipment - masks, helmets, gloves."

**Show:**
- AWS Console > Rekognition > PPE Detection
- Upload workplace/construction image
- Show bounding boxes and equipment detected

**Key API:** `DetectProtectiveEquipment`

---

## 3. VIDEO STREAM (30 sec)

**Say:**
> "For real-time analysis, Rekognition integrates with Kinesis Video Streams to process live video feeds - perfect for security cameras."

**Show:**
- Quick architecture: Kinesis Video > Rekognition > Lambda > Alert
- Mention: face recognition in streams, label detection

**Key Service:** `Kinesis Video Streams + StreamProcessor`

---

## 4. CUSTOM LABELS (30 sec)

**Say:**
> "Pre-trained models recognize celebrities like Brad Pitt, but NOT fictional characters. Watch what happens with a superhero..."

**Show:**
1. Console > Label Detection > Upload Spider-Man/Batman image
2. Point out: Returns only "Person", "Costume", "Mask" - generic!
3. Explain: "With Custom Labels, we can TRAIN our own model"
4. Show Custom Labels workflow: Create Project > Add labeled images > Train

**Say:**
> "No ML expertise needed. Just upload labeled images and Rekognition trains the model for you."

**Key API:** `DetectCustomLabels`

---

## CLOSING (15 sec)

**Say:**
> "All pay-per-use, with a generous free tier. Questions?"

---

## Console Quick Links

- Face Detection: `console.aws.amazon.com/rekognition/home#/face-detection`
- PPE Detection: `console.aws.amazon.com/rekognition/home#/ppe-detection`
- Custom Labels: `console.aws.amazon.com/rekognition/home#/custom-labels`
