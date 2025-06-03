from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

# Load the TrOCR model
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

# Load your handwritten image (replace with your actual image file)
image_path = 'handwritten_image.jpg'
image = Image.open(image_path).convert('RGB')

# OCR Extraction
pixel_values = processor(images=image, return_tensors="pt").pixel_values
generated_ids = model.generate(pixel_values)
extracted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print("📝 Extracted Handwritten Text:")
print(extracted_text)



