import pandas as pd
import numpy as np
from typing import List
import torch
import transformers as ppb


class Bert:

    def __init__(self, device: torch.device) -> None:
        self.INPUT_LENGTH = 512
        self.OUTPUT_LENGTH = 768
        self.device = device

        # load pretrained model/tokenizer
        model_class, tokenizer_class, pretrained_weights = (ppb.DistilBertModel, 
                                                            ppb.DistilBertTokenizer, 
                                                            'distilbert-base-uncased')
        # Load pretrained model/tokenizer
        self.tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
        self.model = model_class.from_pretrained(pretrained_weights).to(device)

    def tokenize(self, texts: List[str]) -> np.ndarray:
        ls = []

        if not texts:
            raise Exception("Empty dataset.")
        
        def tokenizer(text):
            tokenized = self.tokenizer.encode(text, add_special_tokens=False)
            trimmed = tokenized[:self.INPUT_LENGTH]
            padded = trimmed + [0] * (self.INPUT_LENGTH - len(trimmed))
            return padded

        tokens = np.array([tokenizer(text) for text in texts])
        attention_mask = np.where(tokens != 0, 1, 0)

        with torch.no_grad():
            for i, row in enumerate(tokens):
                ii = torch.tensor(row.reshape(1, tokens.shape[1]), device=self.device).to(torch.int64)
                am = torch.tensor(attention_mask[i].reshape(1, tokens.shape[1]), device=self.device).to(torch.int64)
                last_hidden_states = self.model(ii, attention_mask=am)
                features = last_hidden_states[0][:, 0, :].cpu().detach().numpy().reshape(self.OUTPUT_LENGTH, ).tolist()
                ls.append(features)
        
        return np.array(ls)