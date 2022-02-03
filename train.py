import numpy as np
import random
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from main import bag_of_words, tokenize, stem
from model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)

all_words = []
tags = []  # list of tags
xy = []  # patterns and tags

# for each intent
for intent in intents['intents']:
    # get tag info
    tag = intent['tag']
    # add to tag list
    tags.append(tag)

    # for each pattern in the specific tag
    for pattern in intent['patterns']:
        # tokenize each word in sentence
        temp_word = tokenize(pattern)
        # add to our words list
        all_words.extend(temp_word)
        # add to xy as a pair
        xy.append((temp_word, tag))

# stem and lower each word
ignore_chars = ['?', '.', '!']
all_words = [stem(w) for w in all_words if w not in ignore_chars]

# remove duplicates and sort array
all_words = sorted(set(all_words))
tags = sorted(set(tags))


print(len(xy), "patterns")
print(len(tags), "tags:", tags)
print(len(all_words), "unique stemmed words:", all_words)

# create training data arrays
X_train = []
y_train = []

# create test data arrays
x_test = []
y_pred = []
xy_test = []

for x in range(len(xy)):
    if x % 5 == 0:
        xy_test.append(xy[x])
    else:
        tup = xy[x]
        # X = bag of words for each pattern_sentence
        bag = bag_of_words(tup[0], all_words)
        X_train.append(bag)
        # y = PyTorch CrossEntropyLoss, needs only class labels, not one-hot
        label = tags.index(tup[1])
        y_train.append(label)


for (x, tag) in xy_test:
    x_test.append(x)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)


class ChatTrainDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    def __getItem__(self, index):
        return self.x_data[index], self.y_data[index]

    # returns the size
    def __len__(self):
        return self.n_samples


dataset = ChatTrainDataset()
train_loader = DataLoader(
    dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size)

# get loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

###################################### Train the model ######################################
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        # Forward pass
        outputs = model(words)
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


print(f'final loss: {loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')


def get_response(msg):
    x = bag_of_words(msg, all_words)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x).to(device)

    output = model(x)
    _, prediction = torch.max(output, dim=1)
    tag = tags[prediction.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][prediction.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return tag
    return "null"


for x in x_test:
    pred = get_response(x)
    y_pred.append(pred)


# 1 = true positive     |      0 = false positive
hitmark = [0] * (len(y_pred))
TP_counter = 0
for x in range(len(y_pred)):
    real_ans = xy_test[x]
    if real_ans[1] == y_pred[x]:
        hitmark[x] = 1
        TP_counter += 1

print('Model precision: {:.2%}'.format(TP_counter/len(y_pred)))
