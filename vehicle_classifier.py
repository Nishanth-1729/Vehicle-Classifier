
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

CLASS_IDX = {
    0: "Bus",
    1: "Truck",
    2: "Car",
    3: "Bike",
    4: "None"
}

def _build_model(num_classes=5):
    model = models.mobilenet_v2(weights=None)
    in_feats = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_feats, 256),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(256, num_classes),
    )
    return model

class VehicleClassifier:
    def __init__(self, model_path=None):
        self.device = torch.device("cpu")
        self.model  = _build_model(num_classes=5)

        if model_path:
            sd = torch.load(model_path, map_location=self.device,
                            weights_only=True)
            # Convert float16 weights → float32 for CPU inference
            sd = {k: v.float() if v.dtype == torch.float16 else v
                  for k, v in sd.items()}
            self.model.load_state_dict(sd)

        self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

    def predict(self, image_path: str) -> int:
        image  = Image.open(image_path).convert("RGB")
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            _, predicted = torch.max(self.model(tensor), 1)
        return predicted.item()

if __name__ == "__main__":
    clf = VehicleClassifier(model_path="student_model.pth")
    idx = clf.predict("test_image.jpg")
    print(f"Predicted: {idx} -> {CLASS_IDX[idx]}")
