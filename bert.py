import pandas as pd
import numpy as np
from typing import List
import torch
import transformers as ppb


class Bert:

    def __init__(self, device: torch.device) -> None:
        self.OUTPUT_LENGTH = 768
        self.device = device

        # load pretrained model/tokenizer
        model_class, tokenizer_class, pretrained_weights = (ppb.DistilBertModel, 
                                                            ppb.DistilBertTokenizer, 
                                                            'distilbert-base-uncased')
        # Load pretrained model/tokenizer
        tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
        model = model_class.from_pretrained(pretrained_weights).to(device)

    def tokenize(self, texts: List[str]) -> np.ndarray:
        ls = []

        if not texts:
            raise Exception("Empty dataset.")
        
        tokens = np.array([self.tokenizer.encode(text, add_special_tokens=False) 
                           for text in texts])
        
        if len(texts) == 1:
            padded = tokens
        else:
            max_len = max(map(len, tokens))
            padded = np.array([i + [0]*(max_len-len(i) for i in tokens)])

        attention_mask = np.where(padded != 0, 1, 0)

        for i, row in enumerate(padded):
            ii = torch.tensor(row.reshape(1, padded.shape[1]), device=self.device).to(torch.int64)
            am = torch.tensor(attention_mask[i].reshape(1, padded.shape[1]), device=self.device).to(torch.int64)
            last_hidden_states = self.model(ii, attention_mask=am)
            features = last_hidden_states[0][:, 0, :].cpu().detach().numpy().reshape(self.OUTPUT_LENGTH, ).tolist()
            ls.append(features)
        
        return np.array(ls)