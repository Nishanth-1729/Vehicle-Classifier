# --- Cell 1 ---
# ============================================================
# ImageNet Winter21 Dataset Downloader — Kaggle Version
# With retry logic for Connection Reset errors
# ============================================================

import os
import tarfile
import shutil
import requests
import time
from tqdm import tqdm
from PIL import Image
from collections import OrderedDict

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

BASE_URL = "https://image-net.org/data/winter21_whole"

CLASS_SYNSETS = OrderedDict({
    "Bus": ["n02924116", "n04146614", "n03769881"],
    "Truck": ["n04467665", "n03796401", "n03930630", "n04461696"],
    "Car": ["n02958343", "n03100240", "n03594945", "n03770679", "n04037443", "n04285008"],
    "Bike": ["n03790512", "n02834778"],
    "None": [
        "n00007846", "n02913152", "n09428293", "n09193705", "n11669921",
        "n02084071", "n04128499", "n02690373", "n02970849", "n04273569"
    ],
})

SYNSET_LABELS = {
    "n02924116": "bus",          "n04146614": "school bus",
    "n03769881": "minibus",      "n04467665": "trailer truck",
    "n03796401": "moving van",   "n03930630": "pickup truck",
    "n04461696": "tow truck",    "n02958343": "car",
    "n03100240": "convertible",  "n03594945": "jeep",
    "n03770679": "minivan",      "n04037443": "racer",
    "n04285008": "sports car",   "n03790512": "motorcycle",
    "n02834778": "bicycle",      "n00007846": "person",
    "n02913152": "building",     "n09428293": "seashore",
    "n09193705": "mountain",     "n11669921": "flower",
    "n02084071": "dog",          "n04128499": "sailing ship",
    "n02690373": "airliner",     "n02970849": "helicopter",
    "n04273569": "speedboat",
}

# ------------------------------------------------------------
# Directories
# ------------------------------------------------------------

BASE_DIR    = "/kaggle/working"
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
TAR_DIR     = os.path.join(BASE_DIR, "tars")
TEMP_DIR    = os.path.join(BASE_DIR, "temp_extract")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp", ".JPEG", ".JPG"}

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def download_tar(synset_id, max_retries=5):
    os.makedirs(TAR_DIR, exist_ok=True)
    tar_path = os.path.join(TAR_DIR, f"{synset_id}.tar")

    if os.path.exists(tar_path):
        print(f"  [SKIP] {synset_id}.tar already exists")
        return tar_path

    url   = f"{BASE_URL}/{synset_id}.tar"
    label = SYNSET_LABELS.get(synset_id, synset_id)
    print(f"\n[DOWNLOAD] {synset_id} ({label})")

    for attempt in range(1, max_retries + 1):
        try:
            # Resume support: if partial file exists, request remaining bytes
            headers = {}
            downloaded = 0
            if os.path.exists(tar_path):
                downloaded = os.path.getsize(tar_path)
                headers["Range"] = f"bytes={downloaded}-"
                print(f"  Resuming from {downloaded / 1e6:.1f} MB (attempt {attempt})")
            else:
                print(f"  Attempt {attempt}/{max_retries}...")

            response = requests.get(
                url, stream=True, timeout=300,
                headers=headers,
                # Mimic a browser to avoid some rate limiting
                # (ImageNet sometimes blocks plain requests headers)
            )

            # 416 = range not satisfiable = file already complete
            if response.status_code == 416:
                print("  File already fully downloaded")
                return tar_path

            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0)) + downloaded

            mode = "ab" if downloaded > 0 else "wb"
            with open(tar_path, mode) as f:
                with tqdm(
                    total=total_size,
                    initial=downloaded,
                    unit="B", unit_scale=True,
                    desc=f"  {synset_id}"
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=65536):  # 64KB chunks
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            print(f"  [OK] Downloaded {synset_id}")
            return tar_path

        except Exception as e:
            print(f"  Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                wait = attempt * 10   # 10s, 20s, 30s, 40s backoff
                print(f"  Waiting {wait}s before retry...")
                time.sleep(wait)
            else:
                print(f"  [SKIP] {synset_id} failed after {max_retries} attempts — moving on")
                # Remove incomplete file so next run retries cleanly
                if os.path.exists(tar_path):
                    os.remove(tar_path)
                return None

    return None


def extract_tar(tar_path, synset_id):
    extract_dir = os.path.join(TEMP_DIR, synset_id)
    if os.path.exists(extract_dir) and len(os.listdir(extract_dir)) > 0:
        return extract_dir
    os.makedirs(extract_dir, exist_ok=True)
    print(f"[EXTRACT] {synset_id}")
    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(extract_dir)
    return extract_dir


def is_valid_image(path):
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except:
        return False

# ============================================================
# ImageNet Winter21 Dataset Downloader — Kaggle Version
# With retry logic for Connection Reset errors
# ============================================================

import os
import tarfile
import shutil
import requests
import time
from tqdm import tqdm
from PIL import Image
from collections import OrderedDict

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

BASE_URL = "https://image-net.org/data/winter21_whole"

CLASS_SYNSETS = OrderedDict({
    "Bus": ["n02924116", "n04146614", "n03769881"],
    "Truck": ["n04467665", "n03796401", "n03930630", "n04461696"],
    "Car": ["n02958343", "n03100240", "n03594945", "n03770679", "n04037443", "n04285008"],
    "Bike": ["n03790512", "n02834778"],
    "None": [
        "n00007846", "n02913152", "n09428293", "n09193705", "n11669921",
        "n02084071", "n04128499", "n02690373", "n02970849", "n04273569"
    ],
})

SYNSET_LABELS = {
    "n02924116": "bus",          "n04146614": "school bus",
    "n03769881": "minibus",      "n04467665": "trailer truck",
    "n03796401": "moving van",   "n03930630": "pickup truck",
    "n04461696": "tow truck",    "n02958343": "car",
    "n03100240": "convertible",  "n03594945": "jeep",
    "n03770679": "minivan",      "n04037443": "racer",
    "n04285008": "sports car",   "n03790512": "motorcycle",
    "n02834778": "bicycle",      "n00007846": "person",
    "n02913152": "building",     "n09428293": "seashore",
    "n09193705": "mountain",     "n11669921": "flower",
    "n02084071": "dog",          "n04128499": "sailing ship",
    "n02690373": "airliner",     "n02970849": "helicopter",
    "n04273569": "speedboat",
}

# ------------------------------------------------------------
# Directories
# ------------------------------------------------------------

BASE_DIR    = "/kaggle/working"
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
TAR_DIR     = os.path.join(BASE_DIR, "tars")
TEMP_DIR    = os.path.join(BASE_DIR, "temp_extract")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp", ".JPEG", ".JPG"}

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def download_tar(synset_id, max_retries=5):
    os.makedirs(TAR_DIR, exist_ok=True)
    tar_path = os.path.join(TAR_DIR, f"{synset_id}.tar")

    if os.path.exists(tar_path):
        print(f"  [SKIP] {synset_id}.tar already exists")
        return tar_path

    url   = f"{BASE_URL}/{synset_id}.tar"
    label = SYNSET_LABELS.get(synset_id, synset_id)
    print(f"\n[DOWNLOAD] {synset_id} ({label})")

    for attempt in range(1, max_retries + 1):
        try:
            # Resume support: if partial file exists, request remaining bytes
            headers = {}
            downloaded = 0
            if os.path.exists(tar_path):
                downloaded = os.path.getsize(tar_path)
                headers["Range"] = f"bytes={downloaded}-"
                print(f"  Resuming from {downloaded / 1e6:.1f} MB (attempt {attempt})")
            else:
                print(f"  Attempt {attempt}/{max_retries}...")

            response = requests.get(
                url, stream=True, timeout=300,
                headers=headers,
                # Mimic a browser to avoid some rate limiting
                # (ImageNet sometimes blocks plain requests headers)
            )

            # 416 = range not satisfiable = file already complete
            if response.status_code == 416:
                print("  File already fully downloaded")
                return tar_path

            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0)) + downloaded

            mode = "ab" if downloaded > 0 else "wb"
            with open(tar_path, mode) as f:
                with tqdm(
                    total=total_size,
                    initial=downloaded,
                    unit="B", unit_scale=True,
                    desc=f"  {synset_id}"
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=65536):  # 64KB chunks
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            print(f"  [OK] Downloaded {synset_id}")
            return tar_path

        except Exception as e:
            print(f"  Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                wait = attempt * 10   # 10s, 20s, 30s, 40s backoff
                print(f"  Waiting {wait}s before retry...")
                time.sleep(wait)
            else:
                print(f"  [SKIP] {synset_id} failed after {max_retries} attempts — moving on")
                # Remove incomplete file so next run retries cleanly
                if os.path.exists(tar_path):
                    os.remove(tar_path)
                return None

    return None


def extract_tar(tar_path, synset_id):
    extract_dir = os.path.join(TEMP_DIR, synset_id)
    if os.path.exists(extract_dir) and len(os.listdir(extract_dir)) > 0:
        return extract_dir
    os.makedirs(extract_dir, exist_ok=True)
    print(f"[EXTRACT] {synset_id}")
    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(extract_dir)
    return extract_dir


def is_valid_image(path):
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except:
        return False


def collect_images(source_dir):
    images = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in IMAGE_EXTENSIONS:
                images.append(os.path.join(root, file))
    return images


def organize_class(class_name, synsets):
    class_dir = os.path.join(DATASET_DIR, class_name)
    os.makedirs(class_dir, exist_ok=True)
    total = 0

    for synset in synsets:
        print(f"\n--- {synset} {SYNSET_LABELS.get(synset, '')} ---")

        tar_path = download_tar(synset)
        if tar_path is None:
            print(f"  Skipping {synset} — could not download")
            continue

        extract_dir = extract_tar(tar_path, synset)
        images      = collect_images(extract_dir)
        valid       = 0

        for img in images:
            name = os.path.basename(img)
            if not name.startswith(synset):
                name = f"{synset}_{name}"
            dest = os.path.join(class_dir, name)
            if os.path.exists(dest):
                valid += 1
                continue
            if is_valid_image(img):
                shutil.copy2(img, dest)
                valid += 1

        print(f"Images added: {valid}")
        total += valid

        # Free disk space immediately — important on Kaggle (20GB limit)
        try:
            os.remove(tar_path)
            shutil.rmtree(extract_dir, ignore_errors=True)
        except:
            pass

    return total


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    os.makedirs(DATASET_DIR, exist_ok=True)
    os.makedirs(TAR_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    print("\nStarting ImageNet Dataset Download\n")

    for cls, synsets in CLASS_SYNSETS.items():
        print(f"\n{'='*32}\nCLASS: {cls}\n{'='*32}")
        count = organize_class(cls, synsets)
        print(f"\nCLASS {cls} TOTAL: {count}")

    print("\nCleaning temp directory...")
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

    print("\n" + "="*32)
    print("DATASET SUMMARY")
    print("="*32)
    total = 0
    for cls in CLASS_SYNSETS:
        path  = os.path.join(DATASET_DIR, cls)
        count = len(os.listdir(path)) if os.path.exists(path) else 0
        print(f"{cls:<8}: {count:>6}  {'█' * (count // 500)}")
        total += count
    print(f"\nTOTAL  : {total}")
    print(f"Location: {DATASET_DIR}")


main()

# --- Cell 2 ---
import os

base = "/kaggle/working/dataset"
for cls in ["Bike", "Bus", "Car", "None", "Truck"]:
    path = os.path.join(base, cls)
    if os.path.isdir(path):
        imgs = [f for f in os.listdir(path)
                if f.lower().endswith((".jpg",".jpeg",".png",".bmp",".webp"))]
        print(f"  ✓ {cls:6s} → {len(imgs):4d} images")
    else:
        print(f"  ✗ {cls:6s} → NOT FOUND")

# --- Cell 3 ---
import os, torch, torch.nn as nn, torch.optim as optim
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler
from torchvision import transforms, models
from PIL import Image
from collections import Counter

# ══════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════
BASE = "/kaggle/working/dataset"

# Folder name → class index (per assignment spec)
LABEL_MAP = {
    "Bus":   0,
    "Truck": 1,
    "Car":   2,
    "Bike":  3,
    "None":  4,
}

IMG_SIZE     = 128
BATCH_SIZE   = 32
EPOCHS       = 30
LR           = 1e-3
WEIGHT_DECAY = 1e-4
SAVE_PATH    = "/kaggle/working/student_model.pth"
DEVICE       = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ══════════════════════════════════════════
# PATH VERIFICATION
# ══════════════════════════════════════════
print(f"Device : {DEVICE}")
print(f"Base   : {BASE}\n")
print("── Path Check ──────────────────────────────")
all_ok = True
for cls in LABEL_MAP:
    path = os.path.join(BASE, cls)
    if os.path.isdir(path):
        imgs = [f for f in os.listdir(path)
                if f.lower().endswith((".jpg",".jpeg",".png",".bmp",".webp"))]
        print(f"  ✓ {cls:6s} (idx {LABEL_MAP[cls]}) → {len(imgs):5d} images")
    else:
        print(f"  ✗ {cls:6s} → NOT FOUND at {path}")
        all_ok = False
print("────────────────────────────────────────────")
if not all_ok:
    raise RuntimeError("One or more class folders not found. Fix BASE path above.")

# ══════════════════════════════════════════
# DATASET
# ══════════════════════════════════════════
class VehicleDataset(Dataset):
    def __init__(self, base, label_map, transform=None):
        self.transform = transform
        self.samples   = []
        for cls_name, label in label_map.items():
            folder = os.path.join(base, cls_name)
            if not os.path.isdir(folder):
                continue
            for fname in os.listdir(folder):
                if fname.lower().endswith((".jpg",".jpeg",".png",".bmp",".webp")):
                    self.samples.append((os.path.join(folder, fname), label))

        print(f"Total samples loaded : {len(self.samples)}")
        dist = Counter(s[1] for s in self.samples)
        idx_to_cls = {v: k for k, v in label_map.items()}
        for idx in sorted(dist):
            print(f"  Class {idx} ({idx_to_cls[idx]:6s}) : {dist[idx]} images")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        try:
            img = Image.open(path).convert("RGB")
        except Exception:
            img = Image.new("RGB", (IMG_SIZE, IMG_SIZE), (0, 0, 0))
        if self.transform:
            img = self.transform(img)
        return img, label

# ══════════════════════════════════════════
# TRANSFORMS
# ══════════════════════════════════════════
train_tf = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.4, contrast=0.4,
                           saturation=0.3, hue=0.1),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.RandomGrayscale(p=0.05),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

val_tf = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

# ══════════════════════════════════════════
# MODEL  — MobileNetV2  (~3.4 MB < 5 MB limit)
# Uses ImageNet pretrained weights (transfer learning)
# ══════════════════════════════════════════
def build_model(num_classes=5):
    model = models.mobilenet_v2(
        weights=models.MobileNet_V2_Weights.IMAGENET1K_V1   # transfer learning
    )
    # Replace final classifier head only
    in_feats = model.classifier[1].in_features   # 1280
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_feats, 256),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(256, num_classes),
    )
    return model

# ══════════════════════════════════════════
# EPOCH HELPER
# ══════════════════════════════════════════
def run_epoch(model, loader, criterion, optimizer=None):
    training = optimizer is not None
    model.train() if training else model.eval()
    total_loss, correct, total = 0.0, 0, 0
    context = torch.enable_grad() if training else torch.no_grad()
    with context:
        for imgs, lbls in loader:
            imgs, lbls = imgs.to(DEVICE), lbls.to(DEVICE)
            out  = model(imgs)
            loss = criterion(out, lbls)
            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            total_loss += loss.item() * imgs.size(0)
            correct    += out.argmax(1).eq(lbls).sum().item()
            total      += imgs.size(0)
    return total_loss / total, 100.0 * correct / total

# ══════════════════════════════════════════
# MAIN TRAINING FUNCTION
# ══════════════════════════════════════════
def train():
    # Build datasets
    train_ds = VehicleDataset(BASE, LABEL_MAP, transform=train_tf)
    val_ds   = VehicleDataset(BASE, LABEL_MAP, transform=val_tf)

    n       = len(train_ds)
    n_val   = int(0.2 * n)
    n_train = n - n_val

    g = torch.Generator().manual_seed(42)
    indices   = torch.randperm(n, generator=g).tolist()
    train_idx = indices[:n_train]
    val_idx   = indices[n_train:]

    train_subset = torch.utils.data.Subset(train_ds, train_idx)
    val_subset   = torch.utils.data.Subset(val_ds,   val_idx)

    print(f"\nTrain : {n_train}  |  Val : {n_val}\n")

    # Weighted sampler — handles class imbalance
    labels  = [train_ds.samples[i][1] for i in train_idx]
    counts  = Counter(labels)
    weights = [1.0 / counts[l] for l in labels]
    sampler = WeightedRandomSampler(weights, len(weights), replacement=True)

    train_loader = DataLoader(train_subset, batch_size=BATCH_SIZE,
                              sampler=sampler, num_workers=2, pin_memory=True)
    val_loader   = DataLoader(val_subset,   batch_size=BATCH_SIZE,
                              shuffle=False, num_workers=2, pin_memory=True)

    model     = build_model(num_classes=5).to(DEVICE)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    best_acc  = 0.0

    total_p = sum(p.numel() for p in model.parameters())
    print(f"Total parameters : {total_p:,}\n")

    # ────────────────────────────────────────
    # PHASE 1 : Freeze backbone, train head only (5 epochs)
    # Rationale: lets new head stabilise before touching pretrained weights
    # ────────────────────────────────────────
    print("═" * 50)
    print("Phase 1 — Head warmup  (backbone frozen, 5 epochs)")
    print("═" * 50)
    for p in model.features.parameters():
        p.requires_grad = False

    opt1 = optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR, weight_decay=WEIGHT_DECAY
    )

    for ep in range(1, 6):
        tr_loss, tr_acc = run_epoch(model, train_loa

# --- Cell 4 ---
import os, torch, torch.nn as nn, torch.optim as optim
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler
from torchvision import transforms, models
from PIL import Image
from collections import Counter

# ══════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════
BASE = "/kaggle/working/dataset"

# Folder name → class index (per assignment spec)
LABEL_MAP = {
    "Bus":   0,
    "Truck": 1,
    "Car":   2,
    "Bike":  3,
    "None":  4,
}

IMG_SIZE     = 128
BATCH_SIZE   = 32
EPOCHS       = 30
LR           = 1e-3
WEIGHT_DECAY = 1e-4
SAVE_PATH    = "/kaggle/working/student_model.pth"
DEVICE       = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ══════════════════════════════════════════
# PATH VERIFICATION
# ══════════════════════════════════════════
print(f"Device : {DEVICE}")
print(f"Base   : {BASE}\n")
print("── Path Check ──────────────────────────────")
all_ok = True
for cls in LABEL_MAP:
    path = os.path.join(BASE, cls)
    if os.path.isdir(path):
        imgs = [f for f in os.listdir(path)
                if f.lower().endswith((".jpg",".jpeg",".png",".bmp",".webp"))]
        print(f"  ✓ {cls:6s} (idx {LABEL_MAP[cls]}) → {len(imgs):5d} images")
    else:
        print(f"  ✗ {cls:6s} → NOT FOUND at {path}")
        all_ok = False
print("────────────────────────────────────────────")
if not all_ok:
    raise RuntimeError("One or more class folders not found. Fix BASE path above.")

# ══════════════════════════════════════════
# DATASET
# ══════════════════════════════════════════
class VehicleDataset(Dataset):
    def __init__(self, base, label_map, transform=None):
        self.transform = transform
        self.samples   = []
        for cls_name, label in label_map.items():
            folder = os.path.join(base, cls_name)
            if not os.path.isdir(folder):
                continue
            for fname in os.listdir(folder):
                if fname.lower().endswith((".jpg",".jpeg",".png",".bmp",".webp")):
                    self.samples.append((os.path.join(folder, fname), label))

        print(f"Total samples loaded : {len(self.samples)}")
        dist = Counter(s[1] for s in self.samples)
        idx_to_cls = {v: k for k, v in label_map.items()}
        for idx in sorted(dist):
            print(f"  Class {idx} ({idx_to_cls[idx]:6s}) : {dist[idx]} images")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        try:
            img = Image.open(path).convert("RGB")
        except Exception:
            img = Image.new("RGB", (IMG_SIZE, IMG_SIZE), (0, 0, 0))
        if self.transform:
            img = self.transform(img)
        return img, label

# ══════════════════════════════════════════
# TRANSFORMS
# ══════════════════════════════════════════
train_tf = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.4, contrast=0.4,
                           saturation=0.3, hue=0.1),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.RandomGrayscale(p=0.05),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

val_tf = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

# ══════════════════════════════════════════
# MODEL  — MobileNetV2  (~3.4 MB < 5 MB limit)
# Uses ImageNet pretrained weights (transfer learning)
# ══════════════════════════════════════════
def build_model(num_classes=5):
    model = models.mobilenet_v2(
        weights=models.MobileNet_V2_Weights.IMAGENET1K_V1   # transfer learning
    )
    # Replace final classifier head only
    in_feats = model.classifier[1].in_features   # 1280
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_feats, 256),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(256, num_classes),
    )
    return model

# ══════════════════════════════════════════
# EPOCH HELPER
# ══════════════════════════════════════════
def run_epoch(model, loader, criterion, optimizer=None):
    training = optimizer is not None
    model.train() if training else model.eval()
    total_loss, correct, total = 0.0, 0, 0
    context = torch.enable_grad() if training else torch.no_grad()
    with context:
        for imgs, lbls in loader:
            imgs, lbls = imgs.to(DEVICE), lbls.to(DEVICE)
            out  = model(imgs)
            loss = criterion(out, lbls)
            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            total_loss += loss.item() * imgs.size(0)
            correct    += out.argmax(1).eq(lbls).sum().item()
            total      += imgs.size(0)
    return total_loss / total, 100.0 * correct / total

# ══════════════════════════════════════════
# MAIN TRAINING FUNCTION
# ══════════════════════════════════════════
def train():
    # Build datasets
    train_ds = VehicleDataset(BASE, LABEL_MAP, transform=train_tf)
    val_ds   = VehicleDataset(BASE, LABEL_MAP, transform=val_tf)

    n       = len(train_ds)
    n_val   = int(0.2 * n)
    n_train = n - n_val

    g = torch.Generator().manual_seed(42)
    indices   = torch.randperm(n, generator=g).tolist()
    train_idx = indices[:n_train]
    val_idx   = indices[n_train:]

    train_subset = torch.utils.data.Subset(train_ds, train_idx)
    val_subset   = torch.utils.data.Subset(val_ds,   val_idx)

    print(f"\nTrain : {n_train}  |  Val : {n_val}\n")

    # Weighted sampler — handles class imbalance
    labels  = [train_ds.samples[i][1] for i in train_idx]
    counts  = Counter(labels)
    weights = [1.0 / counts[l] for l in labels]
    sampler = WeightedRandomSampler(weights, len(weights), replacement=True)

    train_loader = DataLoader(train_subset, batch_size=BATCH_SIZE,
                              sampler=sampler, num_workers=2, pin_memory=True)
    val_loader   = DataLoader(val_subset,   batch_size=BATCH_SIZE,
                              shuffle=False, num_workers=2, pin_memory=True)

    model     = build_model(num_classes=5).to(DEVICE)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    best_acc  = 0.0

    total_p = sum(p.numel() for p in model.parameters())
    print(f"Total parameters : {total_p:,}\n")

    # ────────────────────────────────────────
    # PHASE 1 : Freeze backbone, train head only (5 epochs)
    # Rationale: lets new head stabilise before touching pretrained weights
    # ────────────────────────────────────────
    print("═" * 50)
    print("Phase 1 — Head warmup  (backbone frozen, 5 epochs)")
    print("═" * 50)
    for p in model.features.parameters():
        p.requires_grad = False

    opt1 = optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR, weight_decay=WEIGHT_DECAY
    )

    for ep in range(1, 6):
        tr_loss, tr_acc = run_epoch(model, train_loader, criterion, opt1)
        vl_loss, vl_acc = run_epoch(model, val_loader,   criterion)
        flag = ""
        if vl_acc > best_acc:
            best_acc = vl_acc
            torch.save(model.state_dict(), SAVE_PATH)
            flag = "  ← best saved ✓"
        print(f"  Ep {ep}/5 | loss {tr_loss:.4f} | "
              f"train {tr_acc:.1f}% | val {vl_acc:.1f}%{flag}")

    # ────────────────────────────────────────
    # PHASE 2 : Unfreeze all, full fine-tune (30 epochs)
    # Lower LR to avoid destroying pretrained features
    # ────────────────────────────────────────
    print()
    print("═" * 50)
    print("Phase 2 — Full fine-tune  (all layers, 30 epochs)")
    print("═" * 50)
    for p in model.parameters():
        p.requires_grad = True

    opt2  = optim.AdamW(model.parameters(), lr=LR * 0.1,
                        weight_decay=WEIGHT_DECAY)
    sched = optim.lr_scheduler.CosineAnnealingLR(
        opt2, T_max=EPOCHS, eta_min=1e-6
    )

    for ep in range(1, EPOCHS + 1):
        tr_loss, tr_acc = run_epoch(model, train_loader, criterion, opt2)
        vl_loss, vl_acc = run_epoch(model, val_loader,   criterion)
        sched.step()
        flag = ""
        if vl_acc > best_acc:
            best_acc = vl_acc
            torch.save(model.state_dict(), SAVE_PATH)
            flag = "  ← best saved ✓"
        print(f"  Ep {ep:2d}/{EPOCHS} | loss {tr_loss:.4f} | "
              f"train {tr_acc:.1f}% | val {vl_acc:.1f}%{flag}")

    print()
    print(f"✅  Training complete!  Best val accuracy : {best_acc:.1f}%")
    mb = os.path.getsize(SAVE_PATH) / 1024 / 1024
    status = "✓ Under 5 MB limit" if mb < 5 else "✗ EXCEEDS 5 MB — fix required"
    print(f"📦  student_model.pth  :  {mb:.2f} MB  ({status})")

train()

# --- Cell 5 ---
get_ipython().run_cell_magic('writefile', '/kaggle/working/vehicle_classifier.py', '\nimport torch\nimport torch.nn as nn\nfrom torchvision import transforms, models\nfrom PIL import Image\n\n# ── Assignment-specified class index mapping ──\nCLASS_IDX = {\n    0: "Bus",\n    1: "Truck",\n    2: "Car",\n    3: "Bike",\n    4: "None"\n}\n\ndef _build_model(num_classes: int = 5):\n    model = models.mobilenet_v2(weights=None)\n    in_feats = model.classifier[1].in_features\n    model.classifier = nn.Sequential(\n        nn.Dropout(0.3),\n        nn.Linear(in_feats, 256),\n        nn.ReLU(),\n        nn.Dropout(0.2),\n        nn.Linear(256, num_classes),\n    )\n    return model\n\n# ── DO NOT change the class name or method signatures ──\nclass VehicleClassifier:\n    def __init__(self, model_path=None):\n        self.device = torch.device("cpu")          # inference always on CPU\n        self.model  = _build_model(num_classes=5)\n        if model_path:\n            self.model.load_state_dict(\n                torch.load(model_path, map_location=self.device)\n            )\n        self.model.to(self.device)\n        self.model.eval()\n\n        # 224×224 — MobileNetV2 native size, handles up to 256×256 test images\n        self.transform = transforms.Compose([\n            transforms.Resize((224, 224)),\n            transforms.ToTensor(),\n            transforms.Normalize(mean=[0.485, 0.456, 0.406],\n                                 std=[0.229, 0.224, 0.225]),\n        ])\n\n    def predict(self, image_path: str) -> int:\n        """Return class index 0-4."""\n        image  = Image.open(image_path).convert("RGB")\n        tensor = self.transform(image).unsqueeze(0).to(self.device)\n        with torch.no_grad():\n            _, predicted = torch.max(self.model(tensor), 1)\n        return predicted.item()\n\nif __name__ == "__main__":\n    clf = VehicleClassifier(model_path="student_model.pth")\n    idx = clf.predict("test_image.jpg")\n    print(f"Predicted class index : {idx}  →  {CLASS_IDX[idx]}")\n')

# --- Cell 6 ---
import glob
from vehicle_classifier import VehicleClassifier, CLASS_IDX

clf = VehicleClassifier(model_path="/kaggle/working/student_model.pth")

BASE = "/kaggle/working/dataset"
print("── Inference Sanity Check ──────────────────")
for cls, idx in {"Bus":0, "Truck":1, "Car":2, "Bike":3, "None":4}.items():
    imgs = glob.glob(f"{BASE}/{cls}/*")
    if not imgs:
        print(f"  ? {cls} — no images found")
        continue
    pred_idx  = clf.predict(imgs[0])
    pred_name = CLASS_IDX[pred_idx]
    ok = "✓" if pred_idx == idx else "✗"
    print(f"  {ok} True: {cls:6s}(idx {idx})  →  Predicted: {pred_name}(idx {pred_idx})")

# --- Cell 7 ---
import sys
sys.path.append("/kaggle/working")

import glob
from vehicle_classifier import VehicleClassifier, CLASS_IDX

clf = VehicleClassifier(model_path="/kaggle/working/student_model.pth")

BASE = "/kaggle/working/dataset"
print("── Inference Sanity Check ──────────────────")
for cls, idx in {"Bus":0, "Truck":1, "Car":2, "Bike":3, "None":4}.items():
    imgs = glob.glob(f"{BASE}/{cls}/*")
    if not imgs:
        print(f"  ? {cls} — no images found")
        continue
    pred_idx  = clf.predict(imgs[0])
    pred_name = CLASS_IDX[pred_idx]
    ok = "✓" if pred_idx == idx else "✗"
    print(f"  {ok} True: {cls:6s}(idx {idx})  →  Predicted: {pred_name}(idx {pred_idx})")

# --- Cell 8 ---
import os
print("── Output files ─────────────────────────────")
for f in os.listdir("/kaggle/working"):
    fp = os.path.join("/kaggle/working", f)
    if os.path.isfile(fp):
        mb = os.path.getsize(fp) / 1024 / 1024
        print(f"  {f:35s}  {mb:.2f} MB")
```

Then in the **left sidebar → Output → `/kaggle/working/`** download:
- `student_model.pth`
- `vehicle_classifier.py`

---

## Submission Folder
```
Assignment_Submission/
├── vehicle_classifier.py   ← from /kaggle/working/
├── student_model.pth       ← from /kaggle/working/
├── train.py                ← the training code above
├── report.pdf              ← write separately
└── README.md

# --- Cell 9 ---
import os
print("── Output files ─────────────────────────────")
for f in os.listdir("/kaggle/working"):
    fp = os.path.join("/kaggle/working", f)
    if os.path.isfile(fp):
        mb = os.path.getsize(fp) / 1024 / 1024
        print(f"  {f:35s}  {mb:.2f} MB")

# --- Cell 10 ---
import torch
import torch.nn as nn
from torchvision import models

# ── Step 1: Rebuild the same architecture used during training ──
def build_model(num_classes=5):
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

# ── Step 2: Load your trained weights ──
model = build_model(num_classes=5)
model.load_state_dict(torch.load("/kaggle/working/student_model.pth",
                                  map_location="cpu"))
model.eval()

# ── Step 3: Quantize (shrinks ~3x with no retraining) ──
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {nn.Linear},        # quantize all Linear layers
    dtype=torch.qint8
)

# ── Step 4: Save quantized weights ──
torch.save(quantized_model.state_dict(),
           "/kaggle/working/student_model.pth")

# ── Step 5: Check new size ──
import os
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 New model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# --- Cell 11 ---
get_ipython().run_cell_magic('writefile', '/kaggle/working/vehicle_classifier.py', '\nimport torch\nimport torch.nn as nn\nfrom torchvision import transforms, models\nfrom PIL import Image\n\nCLASS_IDX = {\n    0: "Bus",\n    1: "Truck",\n    2: "Car",\n    3: "Bike",\n    4: "None"\n}\n\ndef _build_model(num_classes=5):\n    model = models.mobilenet_v2(weights=None)\n    in_feats = model.classifier[1].in_features\n    model.classifier = nn.Sequential(\n        nn.Dropout(0.3),\n        nn.Linear(in_feats, 256),\n        nn.ReLU(),\n        nn.Dropout(0.2),\n        nn.Linear(256, num_classes),\n    )\n    return model\n\nclass VehicleClassifier:\n    def __init__(self, model_path=None):\n        self.device = torch.device("cpu")\n        \n        # Build and quantize model architecture\n        base_model = _build_model(num_classes=5)\n        self.model = torch.quantization.quantize_dynamic(\n            base_model,\n            {nn.Linear},\n            dtype=torch.qint8\n        )\n        \n        if model_path:\n            self.model.load_state_dict(\n                torch.load(model_path, map_location=self.device)\n            )\n        self.model.to(self.device)\n        self.model.eval()\n\n        self.transform = transforms.Compose([\n            transforms.Resize((224, 224)),\n            transforms.ToTensor(),\n            transforms.Normalize(mean=[0.485, 0.456, 0.406],\n                                 std=[0.229, 0.224, 0.225]),\n        ])\n\n    def predict(self, image_path: str) -> int:\n        image  = Image.open(image_path).convert("RGB")\n        tensor = self.transform(image).unsqueeze(0).to(self.device)\n        with torch.no_grad():\n            _, predicted = torch.max(self.model(tensor), 1)\n        return predicted.item()\n\nif __name__ == "__main__":\n    clf = VehicleClassifier(model_path="student_model.pth")\n    idx = clf.predict("test_image.jpg")\n    print(f"Predicted: {idx} -> {CLASS_IDX[idx]}")\n')

# --- Cell 12 ---
import sys
sys.path.append("/kaggle/working")

import glob
from vehicle_classifier import VehicleClassifier, CLASS_IDX

clf = VehicleClassifier(model_path="/kaggle/working/student_model.pth")

BASE = "/kaggle/working/dataset"
print("── Inference Sanity Check ──────────────────")
for cls, idx in {"Bus":0, "Truck":1, "Car":2, "Bike":3, "None":4}.items():
    imgs = glob.glob(f"{BASE}/{cls}/*")
    if not imgs:
        print(f"  ? {cls} — no images found")
        continue
    pred_idx  = clf.predict(imgs[0])
    pred_name = CLASS_IDX[pred_idx]
    ok = "✓" if pred_idx == idx else "✗"
    print(f"  {ok} True: {cls:6s}(idx {idx})  →  Predicted: {pred_name}(idx {pred_idx})")

# --- Cell 13 ---
import sys, glob
sys.path.append("/kaggle/working")
from vehicle_classifier import VehicleClassifier, CLASS_IDX

clf = VehicleClassifier(model_path="/kaggle/working/student_model.pth")

BASE = "/kaggle/working/dataset"
print("── Sanity Check after quantization ────────")
for cls, idx in {"Bus":0, "Truck":1, "Car":2, "Bike":3, "None":4}.items():
    imgs = glob.glob(f"{BASE}/{cls}/*")
    if not imgs:
        print(f"  ? {cls} — no images found")
        continue
    pred_idx  = clf.predict(imgs[0])
    pred_name = CLASS_IDX[pred_idx]
    ok = "✓" if pred_idx == idx else "✗"
    print(f"  {ok} True: {cls:6s}(idx {idx})  Predicted: {pred_name}(idx {pred_idx})")
```

---

## What quantization does
```
Original:  Linear weights stored as float32  →  9.98 MB
Quantized: Linear weights stored as int8     →  ~3.2 MB  ✓

# --- Cell 14 ---
import sys, glob
sys.path.append("/kaggle/working")
from vehicle_classifier import VehicleClassifier, CLASS_IDX

clf = VehicleClassifier(model_path="/kaggle/working/student_model.pth")

BASE = "/kaggle/working/dataset"
print("── Sanity Check after quantization ────────")
for cls, idx in {"Bus":0, "Truck":1, "Car":2, "Bike":3, "None":4}.items():
    imgs = glob.glob(f"{BASE}/{cls}/*")
    if not imgs:
        print(f"  ? {cls} — no images found")
        continue
    pred_idx  = clf.predict(imgs[0])
    pred_name = CLASS_IDX[pred_idx]
    ok = "✓" if pred_idx == idx else "✗"
    print(f"  {ok} True: {cls:6s}(idx {idx})  Predicted: {pred_name}(idx {pred_idx})")

# --- Cell 15 ---
import os
print("── Output files ─────────────────────────────")
for f in os.listdir("/kaggle/working"):
    fp = os.path.join("/kaggle/working", f)
    if os.path.isfile(fp):
        mb = os.path.getsize(fp) / 1024 / 1024
        print(f"  {f:35s}  {mb:.2f} MB")

# --- Cell 16 ---
import sys, glob
sys.path.append("/kaggle/working")
from vehicle_classifier import VehicleClassifier, CLASS_IDX

clf = VehicleClassifier(model_path="/kaggle/working/student_model.pth")

BASE = "/kaggle/working/dataset"
print("── Sanity Check after quantization ────────")
for cls, idx in {"Bus":0, "Truck":1, "Car":2, "Bike":3, "None":4}.items():
    imgs = glob.glob(f"{BASE}/{cls}/*")
    if not imgs:
        print(f"  ? {cls} — no images found")
        continue
    pred_idx  = clf.predict(imgs[0])
    pred_name = CLASS_IDX[pred_idx]
    ok = "✓" if pred_idx == idx else "✗"
    print(f"  {ok} True: {cls:6s}(idx {idx})  Predicted: {pred_name}(idx {pred_idx})")

# --- Cell 17 ---
import torch
import torch.nn as nn
from torchvision import models

# ── Rebuild architecture ──
def build_model(num_classes=5):
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

# ── Load original trained weights ──
model = build_model(num_classes=5)
model.load_state_dict(torch.load("/kaggle/working/student_model.pth",
                                  map_location="cpu"))
model.eval()

# ── Quantize ──
quantized_model = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)

# ── Save the ENTIRE quantized model (not just state_dict) ──
torch.save(quantized_model, "/kaggle/working/student_model.pth")

# ── Check size ──
import os
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# --- Cell 18 ---
import torch
import torch.nn as nn
from torchvision import models

# ── Rebuild architecture ──
def build_model(num_classes=5):
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

# ── Load original trained weights ──
model = build_model(num_classes=5)
model.load_state_dict(torch.load("/kaggle/working/student_model.pth",
                                  map_location="cpu"))
model.eval()

# ── Quantize ──
quantized_model = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)

# ── Save the ENTIRE quantized model (not just state_dict) ──
torch.save(quantized_model, "/kaggle/working/student_model.pth")

# ── Check size ──
import os
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# --- Cell 19 ---
import torch
import torch.nn as nn
from torchvision import models

# ── Rebuild architecture ──
def build_model(num_classes=5):
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

# ── Load original trained weights ──
model = build_model(num_classes=5)
model.load_state_dict(torch.load("/kaggle/working/student_model.pth",
                                  map_location="cpu"))
model.eval()

# ── Quantize ──
quantized_model = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)

# ── Save the ENTIRE quantized model (not just state_dict) ──
torch.save(quantized_model, "/kaggle/working/student_model.pth")

# ── Check size ──
import os
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# --- Cell 20 ---
import torch
import torch.nn as nn
import os

# ── The file is already a quantized model object, just load it directly ──
quantized_model = torch.load("/kaggle/working/student_model.pth", 
                              map_location="cpu")
quantized_model.eval()

# ── Re-save it cleanly ──
torch.save(quantized_model, "/kaggle/working/student_model.pth")

# ── Check size ──
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# ── Quick test ──
print("\nModel loaded successfully ✓")
print(f"Model type: {type(quantized_model)}")

# --- Cell 21 ---
import torch
import torch.nn as nn
import os

# ── The file is already a quantized model object, just load it directly ──
quantized_model = torch.load("/kaggle/working/student_model.pth", 
                              map_location="cpu")
quantized_model.eval()

# ── Re-save it cleanly ──
torch.save(quantized_model, "/kaggle/working/student_model.pth")

# ── Check size ──
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# ── Quick test ──
print("\nModel loaded successfully ✓")
print(f"Model type: {type(quantized_model)}")

# --- Cell 22 ---
import torch
import torch.nn as nn
import os

# ── The file is already a quantized model object, just load it directly ──
quantized_model = torch.load("/kaggle/working/student_model.pth", 
                              map_location="cpu")
quantized_model.eval()

# ── Re-save it cleanly ──
torch.save(quantized_model, "/kaggle/working/student_model.pth")

# ── Check size ──
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# ── Quick test ──
print("\nModel loaded successfully ✓")
print(f"Model type: {type(quantized_model)}")

# --- Cell 23 ---
import torch
import torch.nn as nn
import os

# ── The file is already a quantized model object, just load it directly ──
quantized_model = torch.load("/kaggle/working/student_model.pth", 
                              map_location="cpu")
quantized_model.eval()

# ── Re-save it cleanly ──
torch.save(quantized_model, "/kaggle/working/student_model.pth")

# ── Check size ──
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# ── Quick test ──
print("\nModel loaded successfully ✓")
print(f"Model type: {type(quantized_model)}")

# --- Cell 24 ---
import torch
import torch.nn as nn
from torchvision import models
import os

# ── Step 1: Build base model ──
def build_model(num_classes=5):
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

# ── Step 2: Build quantized architecture (must match what was saved) ──
base_model = build_model(num_classes=5)
quantized_model = torch.quantization.quantize_dynamic(
    base_model, {nn.Linear}, dtype=torch.qint8
)

# ── Step 3: Load the quantized state_dict into the quantized model ──
state_dict = torch.load("/kaggle/working/student_model.pth", map_location="cpu")
quantized_model.load_state_dict(state_dict)
quantized_model.eval()

print("✓ Loaded successfully")

# ── Step 4: Save as full model object (fixes all future loading issues) ──
torch.save(quantized_model, "/kaggle/working/student_model.pth")

# ── Step 5: Check size ──
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# --- Cell 25 ---
import torch
import torch.nn as nn
from torchvision import models
import os
import copy

# ── Step 1: Build base model ──
def build_model(num_classes=5):
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

# ── Step 2: Load the existing quantized state dict ──
raw = torch.load("/kaggle/working/student_model.pth", map_location="cpu")

# ── Step 3: Extract float weights from quantized packed params ──
def dequantize_state_dict(q_state_dict):
    new_sd = {}
    for key, val in q_state_dict.items():
        if "_packed_params._packed_params" in key:
            # Extract the base key (e.g. classifier.1)
            base = key.replace("._packed_params._packed_params", "")
            try:
                weight, bias = val
                new_sd[base + ".weight"] = weight.dequantize()
                if bias is not None:
                    new_sd[base + ".bias"] = bias
            except Exception:
                pass
        elif any(x in key for x in ["scale", "zero_point", "dtype", "_packed_params"]):
            continue  # skip quantization metadata
        else:
            new_sd[key] = val
    return new_sd

float_sd = dequantize_state_dict(raw)

# ── Step 4: Load into fresh float model ──
model = build_model(num_classes=5)
model.load_state_dict(float_sd, strict=True)
model.eval()
print("✓ Recovered float model successfully")

# ── Step 5: Save as half precision (float16) — cuts size in half ──
half_model = model.half()  # float32 → float16
torch.save(half_model.state_dict(), "/kaggle/working/student_model.pth")

mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# --- Cell 26 ---
import torch
import torch.nn as nn
from torchvision import models
import os

# ── Step 1: Build base model ──
def build_model(num_classes=5):
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

# ── Step 2: Load full quantized model (weights_only=False) ──
quantized_model = torch.load("/kaggle/working/student_model.pth",
                              map_location="cpu",
                              weights_only=False)   # ← this is the fix
quantized_model.eval()
print("✓ Loaded successfully")

# ── Step 3: Extract float32 weights from quantized model ──
float_model = build_model(num_classes=5)
float_sd  = {}
q_sd      = quantized_model.state_dict()

for key, val in q_sd.items():
    if "_packed_params._packed_params" in key:
        base = key.replace("._packed_params._packed_params", "")
        try:
            weight, bias = val
            float_sd[base + ".weight"] = weight.dequantize()
            if bias is not None:
                float_sd[base + ".bias"] = bias
        except Exception:
            pass
    elif any(x in key for x in ["scale", "zero_point", "dtype", "_packed_params"]):
        continue
    else:
        float_sd[key] = val

float_model.load_state_dict(float_sd, strict=True)
float_model.eval()
print("✓ Converted to float32 model")

# ── Step 4: Save as float16 (halves the size) ──
half_sd = {k: v.half() for k, v in float_model.state_dict().items()}
torch.save(half_sd, "/kaggle/working/student_model.pth")

mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# --- Cell 27 ---
import torch
import torch.nn as nn
from torchvision import models
import os

# ── Step 1: Build base model ──
def build_model(num_classes=5):
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

# ── Step 2: Load full quantized model ──
quantized_model = torch.load("/kaggle/working/student_model.pth",
                              map_location="cpu",
                              weights_only=False)
quantized_model.eval()
print("✓ Loaded successfully")

# ── Step 3: Extract float32 weights ──
float_model = build_model(num_classes=5)
float_sd = {}
q_sd = quantized_model.state_dict()

for key, val in q_sd.items():
    if "_packed_params._packed_params" in key:
        base = key.replace("._packed_params._packed_params", "")
        try:
            weight, bias = val
            float_sd[base + ".weight"] = weight.dequantize()
            if bias is not None:
                float_sd[base + ".bias"] = bias
        except Exception:
            pass
    elif any(x in key for x in ["scale", "zero_point", "dtype", "_packed_params"]):
        continue
    else:
        float_sd[key] = val

float_model.load_state_dict(float_sd, strict=True)
float_model.eval()
print("✓ Converted to float32 model")

# ── Step 4: Save as float16 with _use_new_zipfile_serialization=False ──
# This removes zip overhead and saves a few extra KB
half_sd = {k: v.half() for k, v in float_model.state_dict().items()}
torch.save(half_sd, "/kaggle/working/student_model.pth",
           _use_new_zipfile_serialization=False)

mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  "
      f"({'✓ Under 5 MB' if mb < 5 else '✗ Still too large'})")

# ── If still over, also try numpy save as fallback ──
if mb >= 5:
    print("\nTrying numpy fallback save...")
    import numpy as np
    np_weights = {k: v.numpy() for k, v in half_sd.items()}
    np.savez_compressed("/kaggle/working/student_model_np.npz", **np_weights)
    mb2 = os.path.getsize("/kaggle/working/student_model_np.npz") / 1024 / 1024
    print(f"📦 Numpy compressed size: {mb2:.2f} MB  "
          f"({'✓ Under 5 MB' if mb2 < 5 else '✗ Still too large'})")

# --- Cell 28 ---
import torch
import torch.nn as nn
from torchvision import models
import os

def build_model(num_classes=5):
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

# Load the existing quantized full model object
quantized_model = torch.load("/kaggle/working/student_model.pth",
                              map_location="cpu", weights_only=False)
quantized_model.eval()
print("✓ Loaded quantized model")

# Extract float32 weights back from quantized model
float_model = build_model(num_classes=5)
float_sd = {}
q_sd = quantized_model.state_dict()

for key, val in q_sd.items():
    if "_packed_params._packed_params" in key:
        base = key.replace("._packed_params._packed_params", "")
        try:
            weight, bias = val
            float_sd[base + ".weight"] = weight.dequantize()
            if bias is not None:
                float_sd[base + ".bias"] = bias
        except Exception:
            pass
    elif any(x in key for x in ["scale", "zero_point", "dtype", "_packed_params"]):
        continue
    else:
        float_sd[key] = val

float_model.load_state_dict(float_sd, strict=True)
float_model.eval()
print("✓ Converted back to float32")

# Convert to float16 AND use old serialization (removes ~0.1MB zip overhead)
half_sd = {k: v.half() for k, v in float_model.state_dict().items()}
torch.save(half_sd, "/kaggle/working/student_model.pth",
           _use_new_zipfile_serialization=False)

mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  ({'✓ UNDER 5 MB' if mb < 5 else '✗ Still too large'})")

# --- Cell 29 ---
import torch
import torch.nn as nn
from torchvision import models
import os

def build_model(num_classes=5):
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

# ── Step 1: Load the dict directly ──
sd = torch.load("/kaggle/working/student_model.pth",
                map_location="cpu", weights_only=False)
print(f"✓ Loaded state_dict  |  keys: {len(sd)}  |  sample dtype: {next(iter(sd.values())).dtype}")

# ── Step 2: Check if it's float16 or float32 ──
sample_dtype = next(iter(sd.values())).dtype
print(f"   Current dtype: {sample_dtype}")

# ── Step 3: If float16 keys → load into float model directly ──
# Convert every tensor to float32 first
sd_f32 = {}
for k, v in sd.items():
    if hasattr(v, 'dtype'):
        sd_f32[k] = v.float()
    else:
        sd_f32[k] = v

# ── Step 4: Load into model to verify ──
model = build_model(num_classes=5)
model.load_state_dict(sd_f32, strict=True)
model.eval()
print("✓ Loaded into model successfully")

# ── Step 5: Save as float16 with old serialization (removes zip overhead) ──
sd_f16 = {k: v.half() for k, v in model.state_dict().items()}
torch.save(sd_f16, "/kaggle/working/student_model.pth",
           _use_new_zipfile_serialization=False)

mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 Model size: {mb:.2f} MB  ({'✓ UNDER 5 MB!' if mb < 5 else '✗ Still too large'})")

# --- Cell 30 ---
get_ipython().run_cell_magic('writefile', '/kaggle/working/vehicle_classifier.py', '\nimport torch\nimport torch.nn as nn\nfrom torchvision import transforms, models\nfrom PIL import Image\n\nCLASS_IDX = {\n    0: "Bus",\n    1: "Truck",\n    2: "Car",\n    3: "Bike",\n    4: "None"\n}\n\ndef _build_model(num_classes=5):\n    model = models.mobilenet_v2(weights=None)\n    in_feats = model.classifier[1].in_features\n    model.classifier = nn.Sequential(\n        nn.Dropout(0.3),\n        nn.Linear(in_feats, 256),\n        nn.ReLU(),\n        nn.Dropout(0.2),\n        nn.Linear(256, num_classes),\n    )\n    return model\n\nclass VehicleClassifier:\n    def __init__(self, model_path=None):\n        self.device = torch.device("cpu")\n        self.model  = _build_model(num_classes=5)\n\n        if model_path:\n            sd = torch.load(model_path, map_location=self.device,\n                            weights_only=True)\n            # Convert float16 weights → float32 for CPU inference\n            sd = {k: v.float() if v.dtype == torch.float16 else v\n                  for k, v in sd.items()}\n            self.model.load_state_dict(sd)\n\n        self.model.to(self.device)\n        self.model.eval()\n\n        self.transform = transforms.Compose([\n            transforms.Resize((224, 224)),\n            transforms.ToTensor(),\n            transforms.Normalize(mean=[0.485, 0.456, 0.406],\n                                 std=[0.229, 0.224, 0.225]),\n        ])\n\n    def predict(self, image_path: str) -> int:\n        image  = Image.open(image_path).convert("RGB")\n        tensor = self.transform(image).unsqueeze(0).to(self.device)\n        with torch.no_grad():\n            _, predicted = torch.max(self.model(tensor), 1)\n        return predicted.item()\n\nif __name__ == "__main__":\n    clf = VehicleClassifier(model_path="student_model.pth")\n    idx = clf.predict("test_image.jpg")\n    print(f"Predicted: {idx} -> {CLASS_IDX[idx]}")\n')

# --- Cell 31 ---
import sys, glob, importlib, os
sys.path.append("/kaggle/working")

# Check size
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"📦 student_model.pth : {mb:.2f} MB  ({'✓ OK' if mb < 5 else '✗ Too large'})")

# Reload module fresh
import vehicle_classifier
importlib.reload(vehicle_classifier)
from vehicle_classifier import VehicleClassifier, CLASS_IDX

clf = VehicleClassifier(model_path="/kaggle/working/student_model.pth")

BASE = "/kaggle/working/dataset"
print("\n── Sanity Check ──────────────────────────")
for cls, idx in {"Bus":0, "Truck":1, "Car":2, "Bike":3, "None":4}.items():
    imgs = glob.glob(f"{BASE}/{cls}/*")
    if not imgs: continue
    pred_idx  = clf.predict(imgs[0])
    ok = "✓" if pred_idx == idx else "✗"
    print(f"  {ok} True: {cls:6s}(idx {idx})  Predicted: {CLASS_IDX[pred_idx]}(idx {pred_idx})")

# --- Cell 32 ---
import sys, glob, importlib, os, torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

# ── Reload fresh classifier ──
sys.path.append("/kaggle/working")
import vehicle_classifier
importlib.reload(vehicle_classifier)
from vehicle_classifier import VehicleClassifier, CLASS_IDX

clf = VehicleClassifier(model_path="/kaggle/working/student_model.pth")

BASE = "/kaggle/working/dataset"

# ── Test 1: Accuracy on multiple images per class ──
print("═" * 55)
print("TEST 1 — Per-class accuracy (10 images each)")
print("═" * 55)

overall_correct = 0
overall_total   = 0

for cls, true_idx in {"Bus":0, "Truck":1, "Car":2, "Bike":3, "None":4}.items():
    imgs = glob.glob(f"{BASE}/{cls}/*")[:10]  # take 10 images per class
    if not imgs:
        print(f"  ? {cls} — no images found")
        continue
    correct = 0
    for img_path in imgs:
        pred = clf.predict(img_path)
        if pred == true_idx:
            correct += 1
    overall_correct += correct
    overall_total   += len(imgs)
    bar = "█" * correct + "░" * (len(imgs) - correct)
    print(f"  {cls:6s} (idx {true_idx})  {correct:2d}/{len(imgs)}  [{bar}]")

print(f"\n  Overall : {overall_correct}/{overall_total}  "
      f"({100*overall_correct/overall_total:.1f}%)")

# ── Test 2: Show actual predictions visually ──
print()
print("═" * 55)
print("TEST 2 — Prediction details (3 images per class)")
print("═" * 55)

for cls, true_idx in {"Bus":0, "Truck":1, "Car":2, "Bike":3, "None":4}.items():
    imgs = glob.glob(f"{BASE}/{cls}/*")[:3]
    if not imgs:
        continue
    print(f"\n  Class: {cls} (expected idx {true_idx})")
    for img_path in imgs:
        pred_idx  = clf.predict(img_path)
        pred_name = CLASS_IDX[pred_idx]
        ok = "✓" if pred_idx == true_idx else "✗"
        fname = os.path.basename(img_path)
        print(f"    {ok}  {fname:40s}  →  {pred_name} (idx {pred_idx})")

# ── Test 3: Model size final check ──
print()
print("═" * 55)
print("TEST 3 — Model file check")
print("═" * 55)
mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"  📦 student_model.pth : {mb:.2f} MB  "
      f"({'✓ Under 5 MB limit' if mb < 5 else '✗ EXCEEDS 5 MB'})")

# ── Test 4: CPU inference speed ──
print()
print("═" * 55)
print("TEST 4 — CPU inference speed")
print("═" * 55)
import time
imgs = glob.glob(f"{BASE}/Car/*")[:20]
start = time.time()
for img_path in imgs:
    clf.predict(img_path)
elapsed = time.time() - start
print(f"  20 images in {elapsed:.2f}s  →  {elapsed/20*1000:.1f} ms per image on CPU")

# ── Test 5: Edge cases ──
print()
print("═" * 55)
print("TEST 5 — Edge cases")
print("═" * 55)

# Small image (stress test resize)
small_img = Image.new("RGB", (32, 32), color=(128, 128, 128))
small_img.save("/tmp/small_test.jpg")
pred = clf.predict("/tmp/small_test.jpg")
print(f"  32x32 grey image     →  {CLASS_IDX[pred]} (idx {pred})  [no crash = ✓]")

# Large image (256x256 as per assignment)
large_img = Image.new("RGB", (256, 256), color=(100, 150, 200))
large_img.save("/tmp/large_test.jpg")
pred = clf.predict("/tmp/large_test.jpg")
print(f"  256x256 blue image   →  {CLASS_IDX[pred]} (idx {pred})  [no crash = ✓]")

# PNG format
png_img = Image.new("RGB", (128, 128), color=(200, 100, 50))
png_img.save("/tmp/test.png")
pred = clf.predict("/tmp/test.png")
print(f"  128x128 PNG image    →  {CLASS_IDX[pred]} (idx {pred})  [no crash = ✓]")

print()
print("═" * 55)
print("All tests complete!")
print("═" * 55)

# --- Cell 33 ---
import sys, glob, os, torch, time, random
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image, ImageEnhance, ImageFilter
import importlib
from collections import defaultdict

# ── Load classifier ──
sys.path.append("/kaggle/working")
import vehicle_classifier
importlib.reload(vehicle_classifier)
from vehicle_classifier import VehicleClassifier, CLASS_IDX

clf = VehicleClassifier(model_path="/kaggle/working/student_model.pth")
BASE = "/kaggle/working/dataset"

print("═" * 60)
print("  VEHICLE CLASSIFIER — FULL EVALUATION SUITE")
print("═" * 60)

# ══════════════════════════════════════════════════════
# TEST 1 — 1000 IMAGE ACCURACY TEST (200 per class)
# ══════════════════════════════════════════════════════
print("\n📊 TEST 1 — Accuracy on 1000 real images (200 per class)")
print("─" * 60)

overall_correct = 0
overall_total   = 0
per_class_results = {}

# Confusion matrix
confusion = defaultdict(lambda: defaultdict(int))

for cls, true_idx in {"Bus":0, "Truck":1, "Car":2, "Bike":3, "None":4}.items():
    all_imgs = glob.glob(f"{BASE}/{cls}/*")
    # Take last 200 images (these were likely in val set, unseen during training)
    imgs = random.sample(all_imgs, min(200, len(all_imgs)))

    correct = 0
    wrong_examples = []

    for img_path in imgs:
        try:
            pred = clf.predict(img_path)
            confusion[true_idx][pred] += 1
            if pred == true_idx:
                correct += 1
            else:
                if len(wrong_examples) < 3:
                    wrong_examples.append((os.path.basename(img_path), CLASS_IDX[pred]))
        except Exception as e:
            print(f"    [ERROR] {img_path}: {e}")

    acc = 100 * correct / len(imgs)
    per_class_results[cls] = (correct, len(imgs), acc)
    overall_correct += correct
    overall_total   += len(imgs)

    bar_ok   = "█" * int(acc / 5)
    bar_fail = "░" * (20 - int(acc / 5))
    print(f"  {cls:6s} (idx {true_idx})  {correct:3d}/200  {acc:5.1f}%  [{bar_ok}{bar_fail}]")
    if wrong_examples:
        for fname, pred_name in wrong_examples:
            print(f"           ✗ {fname[:35]:35s} predicted as {pred_name}")

overall_acc = 100 * overall_correct / overall_total
print(f"\n  {'OVERALL':6s}           {overall_correct:3d}/1000  {overall_acc:5.1f}%")

# ── Confusion Matrix ──
print("\n📊 Confusion Matrix (rows=True, cols=Predicted)")
print("─" * 60)
header = f"{'':10s}" + "".join(f"{CLASS_IDX[i]:>8s}" for i in range(5))
print(f"  {header}")
for ti in range(5):
    row = f"  {CLASS_IDX[ti]:10s}"
    for pi in range(5):
        val = confusion[ti][pi]
        marker = f"[{val:3d}]" if ti == pi else f" {val:3d} "
        row += f"{marker:>8s}"
    print(row)

# ══════════════════════════════════════════════════════
# TEST 2 — EDGE CASES (no weight modification)
# ══════════════════════════════════════════════════════
print("\n\n🔬 TEST 2 — Edge Cases")
print("─" * 60)

edge_results = []

def test_edge(name, img, expected_no_crash=True):
    try:
        img.save("/tmp/edge_test.jpg")
        pred = clf.predict("/tmp/edge_test.jpg")
        result = f"→ {CLASS_IDX[pred]:6s} (idx {pred})"
        edge_results.append((name, True, result))
        print(f"  ✓ {name:40s} {result}")
    except Exception as e:
        edge_results.append((name, False, str(e)))
        print(f"  ✗ {name:40s} CRASHED: {e}")

# Size variations (assignment says up to 256x256)
test_edge("Tiny image      (8x8)",      Image.new("RGB", (8,   8),   (128,128,128)))
test_edge("Small image     (16x16)",    Image.new("RGB", (16,  16),  (128,128,128)))
test_edge("Starter size    (32x32)",    Image.new("RGB", (32,  32),  (128,128,128)))
test_edge("Medium image    (64x64)",    Image.new("RGB", (64,  64),  (128,128,128)))
test_edge("Standard        (128x128)",  Image.new("RGB", (128, 128), (128,128,128)))
test_edge("Assignment max  (256x256)",  Image.new("RGB", (256, 256), (128,128,128)))
test_edge("Non-square      (320x240)",  Image.new("RGB", (320, 240), (128,128,128)))
test_edge("Wide image      (640x480)",  Image.new("RGB", (640, 480), (128,128,128)))
test_edge("Large image     (1024x768)", Image.new("RGB", (1024,768), (128,128,128)))

# Color variations
test_edge("Pure black image",           Image.new("RGB", (224,224), (0,  0,  0  )))
test_edge("Pure white image",           Image.new("RGB", (224,224), (255,255,255)))
test_edge("Pure red image",             Image.new("RGB", (224,224), (255,0,  0  )))
test_edge("Pure green image",           Image.new("RGB", (224,224), (0,  255,0  )))
test_edge("Pure blue image",            Image.new("RGB", (224,224), (0,  0,  255)))

# Format variations
def test_edge_png(name, img):
    try:
        img.save("/tmp/edge_test.png")
        pred = clf.predict("/tmp/edge_test.png")
        result = f"→ {CLASS_IDX[pred]:6s} (idx {pred})"
        edge_results.append((name, True, result))
        print(f"  ✓ {name:40s} {result}")
    except Exception as e:
        edge_results.append((name, False, str(e)))
        print(f"  ✗ {name:40s} CRASHED: {e}")

test_edge_png("PNG format (224x224)",   Image.new("RGB", (224,224), (128,128,128)))

# Real image with augmentations (illumination + occlusion as per assignment)
real_imgs = glob.glob(f"{BASE}/Car/*")[:1]
if real_imgs:
    original = Image.open(real_imgs[0]).convert("RGB")

    # Dark image (low illumination)
    dark = ImageEnhance.Brightness(original).enhance(0.2)
    test_edge("Dark image (brightness 0.2x)",  dark)

    # Very bright image
    bright = ImageEnhance.Brightness(original).enhance(3.0)
    test_edge("Bright image (brightness 3x)",  bright)

    # Low contrast
    low_c = ImageEnhance.Contrast(original).enhance(0.1)
    test_edge("Low contrast image",             low_c)

    # Blurred (simulates motion blur / occlusion)
    blurred = original.filter(ImageFilter.GaussianBlur(radius=5))
    test_edge("Heavily blurred image",          blurred)

    # Partial occlusion (black box over 50% of image)
    import torchvision.transforms.functional as TF
    occluded = original.copy()
    import numpy as np
    arr = np.array(occluded)
    arr[:arr.shape[0]//2, :, :] = 0   # black out top half
    occluded = Image.fromarray(arr)
    test_edge("50% occluded image (top half black)", occluded)

    # Grayscale converted to RGB
    gray = original.convert("L").convert("RGB")
    test_edge("Grayscale→RGB image",            gray)

    # Rotated
    rotated = original.rotate(45)
    test_edge("Rotated 45 degrees",             rotated)

    # Flipped
    flipped = original.transpose(Image.FLIP_LEFT_RIGHT)
    test_edge("Horizontally flipped",           flipped)

# ══════════════════════════════════════════════════════
# TEST 3 — INFERENCE SPEED ON CPU
# ══════════════════════════════════════════════════════
print("\n\n⚡ TEST 3 — CPU Inference Speed")
print("─" * 60)

imgs_speed = glob.glob(f"{BASE}/Car/*")[:50]
times = []
for img_path in imgs_speed:
    t0 = time.time()
    clf.predict(img_path)
    times.append(time.time() - t0)

avg_ms  = sum(times) / len(times) * 1000
min_ms  = min(times) * 1000
max_ms  = max(times) * 1000
print(f"  Images tested  : {len(imgs_speed)}")
print(f"  Avg per image  : {avg_ms:.1f} ms")
print(f"  Min / Max      : {min_ms:.1f} ms / {max_ms:.1f} ms")
print(f"  {'✓ Fast enough for CPU inference' if avg_ms < 500 else '✗ Too slow'}")

# ══════════════════════════════════════════════════════
# TEST 4 — MODEL FILE INTEGRITY
# ══════════════════════════════════════════════════════
print("\n\n📦 TEST 4 — Model File Integrity")
print("─" * 60)

mb = os.path.getsize("/kaggle/working/student_model.pth") / 1024 / 1024
print(f"  File size      : {mb:.3f} MB  ({'✓ Under 5 MB' if mb < 5 else '✗ EXCEEDS 5 MB'})")

# Verify it can be reloaded from scratch (simulates evaluator's script)
try:
    clf2 = VehicleClassifier(model_path="/kaggle/working/student_model.pth")
    test_img = glob.glob(f"{BASE}/Car/*")[0]
    pred = clf2.predict(test_img)
    print(f"  Fresh reload   : ✓ loads cleanly, predicts idx {pred} ({CLASS_IDX[pred]})")
except Exception as e:
    print(f"  Fresh reload   : ✗ FAILED — {e}")

# Verify class indices are correct
print(f"  Class mapping  :")
for idx, name in CLASS_IDX.items():
    print(f"    {idx} → {name}")

# ══════════════════════════════════════════════════════
# FINAL SUMMARY
# ══════════════════════════════════════════════════════
print("\n")
print("═" * 60)
print("  FINAL SUMMARY")
print("═" * 60)
print(f"  Overall accuracy (1000 imgs) : {overall_acc:.1f}%  "
      f"{'✓' if overall_acc > 80 else '✗'}")
print(f"  Edge cases passed            : "
      f"{sum(1 for _,ok,_ in edge_results if ok)}/{len(edge_results)}  "
      f"{'✓' if all(ok for _,ok,_ in edge_results) else '⚠ some failed'}")
print(f"  Avg CPU inference speed      : {avg_ms:.1f} ms  "
      f"{'✓' if avg_ms < 500 else '✗'}")
print(f"  Model size                   : {mb:.3f} MB  "
      f"{'✓' if mb < 5 else '✗'}")
print()

if overall_acc > 90:
    print("  🏆 Excellent — ready for submission!")
elif overall_acc > 80:
    print("  ✅ Good — acceptable for submission")
elif overall_acc > 70:
    print("  ⚠️  Moderate — consider retraining with more epochs")
else:
    print("  ❌ Low accuracy — weights may be corrupted, reconvert")
print("═" * 60)

# --- Cell 34 ---
from google.colab import userdata
import os

# Configuration - Update these with your details
GITHUB_USER = "YOUR_GITHUB_USERNAME"
GITHUB_REPO = "YOUR_REPO_NAME"
GITHUB_EMAIL = "YOUR_EMAIL@example.com"
GITHUB_TOKEN = userdata.get('GITHUB_TOKEN')

# Set git identity
get_ipython().system('git config --global user.email "{GITHUB_EMAIL}"')
get_ipython().system('git config --global user.name "{GITHUB_USER}"')

print(f"Git configured for {GITHUB_USER}")

# --- Cell 35 ---
# Initialize and push
get_ipython().run_line_magic('cd', '/kaggle/working')
get_ipython().system('git init')
get_ipython().system('git add student_model.pth vehicle_classifier.py')
get_ipython().system('git commit -m "Add trained vehicle classifier model and inference script"')
get_ipython().system('git branch -M main')

# Construct the authenticated URL
remote_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{GITHUB_REPO}.git"

get_ipython().system('git remote add origin {remote_url}')
get_ipython().system('git push -u origin main')

# --- Cell 36 ---
import os
from google.colab import userdata

# 1. GitHub Credentials (Updated with your info)
GITHUB_USER = "Nishanth-1729"
GITHUB_REPO = "Vehicle-Classifier" 
GITHUB_EMAIL = "nlearn.narayan@gmail.com"

# 2. Setting token (Provided via chat)
# Note: In the future, use the 🔑 tab for better security!
GITHUB_TOKEN = "REDACTED_GITHUB_TOKEN"

# Set git identity
get_ipython().system('git config --global user.email "{GITHUB_EMAIL}"')
get_ipython().system('git config --global user.name "{GITHUB_USER}"')

print(f"✅ Git identity configured for {GITHUB_USER}")
print(f"✅ Token is ready to use.")

# --- Cell 37 ---
# Initialize and push
get_ipython().run_line_magic('cd', '/kaggle/working')
get_ipython().system('git init')
get_ipython().system('git add student_model.pth vehicle_classifier.py')
get_ipython().system('git commit -m "Add trained vehicle classifier model and inference script"')
get_ipython().system('git branch -M main')

# Construct the authenticated URL
remote_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{GITHUB_REPO}.git"

# Clear existing remote if it exists and add new one
get_ipython().system('git remote remove origin 2>/dev/null')
get_ipython().system('git remote add origin {remote_url}')

print("Pushing to GitHub...")
get_ipython().system('git push -u origin main')

# --- Cell 38 ---
get_ipython().system('git remote -v')
get_ipython().system('git remote show origin')

# --- Cell 39 ---
get_ipython().system('git remote -v')
get_ipython().system('git remote show origin')

# --- Cell 40 ---
import os

# Retrieve token from the environment variable set in previous steps
github_token = globals().get('GITHUB_TOKEN', '')

if not github_token:
    print('Error: GITHUB_TOKEN not found in environment.')
else:
    # 1. Authenticate GitHub CLI
    get_ipython().system('echo {github_token} | gh auth login --with-token')

    # 2. Create the public repository
    print('\nCreating repository...')
    get_ipython().system('gh repo create Nishanth-1729/Vehicle-Classifier --public')

    # 3. Verify repository creation
    print('\nVerifying repository list for Nishanth-1729:')
    get_ipython().system('gh repo list Nishanth-1729')

# --- Cell 41 ---
import os

# Retrieve token from the variable defined in previous cells
github_token = globals().get('GITHUB_TOKEN', 'REDACTED_GITHUB_TOKEN')

# Set the environment variable for GitHub CLI authentication
os.environ['GH_TOKEN'] = github_token

if not github_token:
    print('Error: GITHUB_TOKEN not found.')
else:
    # 1. Create the public repository using the GH_TOKEN env var
    print('Creating repository Nishanth-1729/Vehicle-Classifier...')
    get_ipython().system('gh repo create Nishanth-1729/Vehicle-Classifier --public')

    # 2. Verify repository creation
    print('\nVerifying repository list for Nishanth-1729:')
    get_ipython().system('gh repo list Nishanth-1729')

# --- Cell 42 ---
import os

# 1. Change directory to /kaggle/working
get_ipython().run_line_magic('cd', '/kaggle/working')

# 2. Construct the authenticated URL
# Using existing GITHUB_USER and GITHUB_TOKEN variables from kernel state
remote_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{GITHUB_REPO}.git"

# 3. Remove existing origin and add the new one
get_ipython().system('git remote remove origin 2>/dev/null')
get_ipython().system('git remote add origin {remote_url}')

# 4. Push to main branch
print(f"Pushing student_model.pth and vehicle_classifier.py to {GITHUB_REPO}...")
get_ipython().system('git push -u origin main')

# --- Cell 43 ---
import os
print("── Output files ─────────────────────────────")
for f in os.listdir("/kaggle/working"):
    fp = os.path.join("/kaggle/working", f)
    if os.path.isfile(fp):
        mb = os.path.getsize(fp) / 1024 / 1024
        print(f"  {f:35s}  {mb:.2f} MB")

# --- Cell 44 ---
import json
import os

# Define paths
notebook_path = '__notebook__.ipynb'
output_path = '/kaggle/working/notebook_source.py'

if os.path.exists(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb_data = json.load(f)

    code_cells = [cell for cell in nb_data.get('cells', []) if cell.get('cell_type') == 'code']
    
    all_code = []
    for i, cell in enumerate(code_cells):
        source = cell.get('source', [])
        # source can be a list of strings or a single string
        source_str = ''.join(source) if isinstance(source, list) else source
        all_code.append(f'# --- Cell {i+1} ---\n{source_str}\n')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_code))

    print(f'Successfully extracted {len(code_cells)} code cells to {output_path}')
else:
    print(f'Error: {notebook_path} not found. In some environments, the notebook might have a different filename.')

# --- Cell 45 ---
import json
import os

# Try to find any .ipynb file in the current directory if __notebook__.ipynb is missing
notebook_path = '__notebook__.ipynb'
if not os.path.exists(notebook_path):
    ipynb_files = [f for f in os.listdir('.') if f.endswith('.ipynb')]
    if ipynb_files:
        notebook_path = ipynb_files[0]
        print(f'Found notebook file: {notebook_path}')

output_path = '/kaggle/working/notebook_source.py'

if os.path.exists(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb_data = json.load(f)

    code_cells = [cell for cell in nb_data.get('cells', []) if cell.get('cell_type') == 'code']

    all_code = []
    for i, cell in enumerate(code_cells):
        source = cell.get('source', [])
        source_str = ''.join(source) if isinstance(source, list) else source
        all_code.append(f'# --- Cell {i+1} ---\n{source_str}\n')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_code))

    print(f'Successfully extracted {len(code_cells)} code cells to {output_path}')
else:
    print('Error: No .ipynb file found to extract code from.')

# --- Cell 46 ---
import json
import os

def find_notebook():
    search_paths = ['.', '/kaggle', '/kaggle/working']
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.ipynb'):
                        return os.path.join(root, file)
    return None

notebook_path = find_notebook()
output_path = '/kaggle/working/notebook_source.py'

if notebook_path:
    print(f'Found notebook at: {notebook_path}')
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb_data = json.load(f)

    code_cells = [cell for cell in nb_data.get('cells', []) if cell.get('cell_type') == 'code']

    all_code = []
    for i, cell in enumerate(code_cells):
        source = cell.get('source', [])
        source_str = ''.join(source) if isinstance(source, list) else source
        all_code.append(f'# --- Cell {i+1} ---\n{source_str}\n')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_code))

    print(f'Successfully extracted {len(code_cells)} code cells to {output_path}')
else:
    print('Error: Could not locate the notebook file (.ipynb) in the Kaggle environment.')

# --- Cell 47 ---
get_ipython().run_cell_magic('writefile', '/kaggle/working/vehicle_classifier.py', '\nimport torch\nimport torch.nn as nn\nfrom torchvision import transforms, models\nfrom PIL import Image\n\nCLASS_IDX = {\n    0: "Bus",\n    1: "Truck",\n    2: "Car",\n    3: "Bike",\n    4: "None"\n}\n\ndef _build_model(num_classes=5):\n    model = models.mobilenet_v2(weights=None)\n    in_feats = model.classifier[1].in_features\n    model.classifier = nn.Sequential(\n        nn.Dropout(0.3),\n        nn.Linear(in_feats, 256),\n        nn.ReLU(),\n        nn.Dropout(0.2),\n        nn.Linear(256, num_classes),\n    )\n    return model\n\nclass VehicleClassifier:\n    def __init__(self, model_path=None):\n        self.device = torch.device("cpu")\n        self.model  = _build_model(num_classes=5)\n\n        if model_path:\n            sd = torch.load(model_path, map_location=self.device,\n                            weights_only=True)\n            # Convert float16 weights → float32 for CPU inference\n            sd = {k: v.float() if v.dtype == torch.float16 else v\n                  for k, v in sd.items()}\n            self.model.load_state_dict(sd)\n\n        self.model.to(self.device)\n        self.model.eval()\n\n        self.transform = transforms.Compose([\n            transforms.Resize((224, 224)),\n            transforms.ToTensor(),\n            transforms.Normalize(mean=[0.485, 0.456, 0.406],\n                                 std=[0.229, 0.224, 0.225]),\n        ])\n\n    def predict(self, image_path: str) -> int:\n        image  = Image.open(image_path).convert("RGB")\n        tensor = self.transform(image).unsqueeze(0).to(self.device)\n        with torch.no_grad():\n            _, predicted = torch.max(self.model(tensor), 1)\n        return predicted.item()\n\nif __name__ == "__main__":\n    clf = VehicleClassifier(model_path="student_model.pth")\n    idx = clf.predict("test_image.jpg")\n    print(f"Predicted: {idx} -> {CLASS_IDX[idx]}")\n')

# --- Cell 48 ---
import os

# Get the history of executed cells in the current session
# In IPython/Kaggle, In is a list of all inputs
try:
    # Retrieve all inputs from the current session
    all_inputs = In
    
    output_path = '/kaggle/working/notebook_source.py'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, code_str in enumerate(all_inputs):
            if code_str.strip():
                f.write(f'# --- Cell {i} ---\n{code_str}\n\n')
    
    print(f'Successfully extracted {len(all_inputs)} session history entries to {output_path}')
except NameError:
    print('Error: Could not access session history (In).')

