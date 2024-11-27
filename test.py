from ultralytics import YOLO
import matplotlib.pyplot as plt

# Load the trained YOLO model
model = YOLO('app/models/best.pt')  # Specify the path to your trained model

# Run inference on a set of test images
results = model('C:\Users\HP\Desktop\css-data\test\images')  # Replace with the actual path to your test images

# Extract confidence scores from the results
confidence_scores = []

for result in results:
    # Extract confidence scores for each detection in the result
    scores = result.boxes.conf.tolist()  # This is the confidence score for each detected object
    confidence_scores.extend(scores)  # Add to the overall list of confidence scores

# Plotting the confidence distribution
plt.figure(figsize=(10, 6))
plt.hist(confidence_scores, bins=30, color='blue', edgecolor='black', alpha=0.7)
plt.title('Confidence Level Distribution')
plt.xlabel('Confidence Score')
plt.ylabel('Frequency')
plt.grid(True)

# Save the figure
plt.savefig('confidence_distribution.png')



yolo task=detect mode=val model=runs/train/exp/weights/best.pt data=data.yaml

yolo task=detect mode=predict model=best.pt source=path_to_test_images

