import os
import pandas
import torch
from torch import nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
from torchvision.io import read_image

class newDataset(Dataset):
    def __init__(self, annotations, img, transform=None, target_transform=None):
        self.img_labels = pandas.read_csv(annotations)
        self.img_dir = img
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        img = read_image(img_path)
        img = img / 255
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            img = self.transform(img)
        if self.target_transform:
            label = self.target_transform(label)
        return img, label



Shapes = newDataset("data/Shapes/labels_train.csv", "data/Shapes/images")
ShapesTest = newDataset("data/Shapes/labels.csv", "data/Shapes/test_images")
labels = ["heart", "circle", "triangle"]

batch_train = 10
batch_test = 7
train = DataLoader(Shapes, batch_size=batch_train, shuffle=True)
test = DataLoader(ShapesTest, batch_size=batch_test, shuffle=True)


device = "cuda" if torch.cuda.is_available() else "cpu"
class Network(nn.Module):

    def __init__(self):
        super(Network, self).__init__()
        self.flatten = nn.Flatten()
        self.stack = nn.Sequential(
            nn.Linear(3*32*32, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 3),
            )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.stack(x)
        return logits

def load_model():
    global model_file, model
    model_file = input("Enter file name: ")
    try:
        model = torch.load(model_file)
    except:
        print("Could not load model. Try again.\n")
        load_model()

if input("Do you want to load already saved model?\n") == "yes":
    load_model()
else:
    model = Network().to(device)
    print("New model has been created.\n")
#print(model.stack)
#it seems that changing the amount and size of layers doesn't significantly
#affect its performance
#it seems to not be able to go past these 80-90% if accuracy
#it may be a problem with not large enough amount of training data or
#bad quality of the data

learning_rate = 1e-3
epochs = 200 #has to be a multiplicity of loops

loss = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    batches = len(dataloader)
    train_loss = 0
    correct = 0
    for batch, (x, y) in enumerate(dataloader):
        prediction = model(x)
        loss = loss_fn(prediction, y)
        train_loss = loss.item()
        correct += (prediction.argmax(1) == y).type(torch.float).sum().item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    train_loss/= batches
    correct /= size
    print(f"Train accuracy: {correct*100:>1f}% average loss: {train_loss:>8f} \n" )


def test_loop(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    batches = len(dataloader)
    test_loss = 0
    correct = 0

    with torch.no_grad():
        for x, y in dataloader:
            pred = model(x)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss/= batches
    correct /= size
    print(f"Test accuracy: {correct*100:>1f}% average loss: {test_loss:>8f} \n" )
    return correct * 100

prev_acc = test_loop(test, model, loss)
avrg_acc = 0
loops = 20
itr = int(epochs/loops)

for q in range(itr):
    acc = 0
    for e in range(loops):
        print(f"epoch: {q * loops + e}")
        train_loop(train, model, loss, optimizer)
        acc += test_loop(test, model, loss)
    avrg_acc = acc / loops

print(f"First accuracy: {prev_acc} \n Recent average accuracy: {avrg_acc} \n")       

def save_model():
    model_file = input("Enter the name for the model file: ")
    torch.save(model, model_file)
    print("Model saved")

if input("Save?\n") == "yes":
    save_model()
else:
    if input("Are you sure?\n") == "no":
        save_model()
    else:
        print("Model not saved")
