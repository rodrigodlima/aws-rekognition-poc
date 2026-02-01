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

**Key API:** `DetectProtectiveEquipment`

---

## 3. VIDEO STREAM (30 sec)

**Say:**
> "For real-time analysis, Rekognition integrates with Kinesis Video Streams to process live video feeds - perfect for security cameras."

**Run:**
```bash
# Create stream processor
aws rekognition create-stream-processor \
  --name "security-processor" \
  --input '{"KinesisVideoStream":{"Arn":"arn:aws:kinesisvideo:..."}}' \
  --output '{"KinesisDataStream":{"Arn":"arn:aws:kinesis:..."}}' \
  --role-arn "arn:aws:iam::..." \
  --settings '{"FaceSearch":{"CollectionId":"my-faces","FaceMatchThreshold":80}}'

# Start processor
aws rekognition start-stream-processor --name "security-processor"
```

**Say:**
> "Architecture: Kinesis Video > Rekognition > Lambda > Alert"

**Key Service:** `Kinesis Video Streams + StreamProcessor`

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
# Face Detection
aws rekognition detect-faces --image '{"S3Object":{"Bucket":"BUCKET","Name":"FILE"}}'

# PPE Detection
aws rekognition detect-protective-equipment --image '{"S3Object":{"Bucket":"BUCKET","Name":"FILE"}}'

# Label Detection (standard)
aws rekognition detect-labels --image '{"S3Object":{"Bucket":"BUCKET","Name":"FILE"}}'

# Custom Labels
aws rekognition detect-custom-labels --project-version-arn "ARN" --image '{"S3Object":{"Bucket":"BUCKET","Name":"FILE"}}'
```
