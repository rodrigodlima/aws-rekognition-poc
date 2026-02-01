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
  --video '{"S3Object":{"Bucket":"amzn-rekognition-poc-v2","Name":"meu-video.mp4"}}' \
  --face-attributes ALL
```

**Point to:** JobId returned - this is async processing

### Step 2: Get results

**Run:**
```bash
aws rekognition get-face-detection \
  --job-id "JOB_ID_HERE" \
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

### Passo 1: Mostrar S3 na Console
- Abrir Console S3 > Bucket com imagens de treino
- Mostrar estrutura de pastas: cada pasta = um label
  ```
  s3://my-training-bucket/
  ├── deadpool/
  │   ├── img1.jpg
  │   └── img2.jpg
  ├── spiderman/
  │   ├── img1.jpg
  │   └── img2.jpg
  ```

**Say:**
> "O nome da pasta define automaticamente o label. Simples assim."

### Passo 2: Criar Projeto e Treinar (Console)
- Console > Rekognition > Custom Labels > Create Project
- Apontar para o bucket S3
- Iniciar treinamento

### Passo 3: Testar ANTES do modelo (durante treino)

**Say:**
> "Enquanto o modelo treina, vamos ver o que o Rekognition padrão reconhece..."

**Run:**
```bash
aws rekognition detect-labels \
  --image '{"S3Object":{"Bucket":"my-bucket","Name":"deadpool.jpg"}}' \
  --query 'Labels[].Name'
```

**Result:** `["Person", "Costume", "Mask", "Human"]` - Genérico!

### Passo 4: Testar DEPOIS do modelo treinado

**Say:**
> "Agora com nosso modelo custom..."

**Run:**
```bash
aws rekognition detect-custom-labels \
  --project-version-arn "arn:aws:rekognition:...:project/heroes/version/1" \
  --image '{"S3Object":{"Bucket":"my-bucket","Name":"deadpool.jpg"}}' \
  --query 'CustomLabels[].{Label:Name,Confidence:Confidence}'
```

**Result:** `[{"Label": "deadpool", "Confidence": 98.5}]`

**Say:**
> "No ML expertise needed. Just upload labeled images and Rekognition trains the model for you."

**Key API:** `DetectCustomLabels`

---

## CLOSING (15 sec)

**Say:**
> "All pay-per-use, with a generous free tier. Questions?"

---

## CLI Reference

```bash
# Face Detection (image)
aws rekognition detect-faces --image '{"S3Object":{"Bucket":"BUCKET","Name":"FILE"}}'

# PPE Detection
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
