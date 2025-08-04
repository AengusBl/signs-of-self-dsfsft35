import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel


device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
print(f"Using {device} device")


class CustomClassifier(nn.Module):
    def __init__(self, dropout_rate=0.2):
        super().__init__()
        self.backbone = BertModel.from_pretrained("bert-base-uncased")
        self.dropout = nn.Dropout(dropout_rate)
        self.classifier = nn.Linear(self.backbone.config.hidden_size, 5)

    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.backbone(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs[0][:, 0]
        x = self.dropout(pooled_output)
        logits = self.classifier(x)

        loss = None
        if labels is not None:
            loss_fn = nn.BCEWithLogitsLoss()
            loss = loss_fn(logits, labels.float())

        return {"loss": loss, "logits": logits}


model = CustomClassifier()
model.to(device)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

model.load_state_dict(torch.load("pytorch_model.bin", map_location="cpu"))
model.eval()


def predict_personality(text, threshold=0.5):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

    filtered_inputs = {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"]
    }

    with torch.no_grad():
        outputs = model(**filtered_inputs)
        logits = outputs["logits"]
        probs = torch.sigmoid(logits)

    preds = (probs > threshold).int().numpy().flatten()

    labels = ["O", "C", "E", "A", "N"]
    predictions_dict = {trait: int(pred) for trait, pred in zip(labels, preds)}
  
    return predictions_dict