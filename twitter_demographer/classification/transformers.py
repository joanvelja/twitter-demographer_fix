from transformers import Trainer
from twitter_demographer.support.dataset import prepare_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from datasets import Dataset
import numpy as np
from twitter_demographer.components import Component
from twitter_demographer.components import not_null


class HuggingFaceClassifier(Component):

    def __init__(self, model_name):
        self.model_name = model_name
        super().__init__()

    def inputs(self):
        return ["text"]

    def outputs(self):
        return [f"{self.model_name}"]

    @not_null("text")
    def infer(self, data):

        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

        df = pd.DataFrame({"texts": data["text"].values.tolist()})

        train_dataset = Dataset.from_pandas(df)
        train_dataset = prepare_dataset(train_dataset, tokenizer)

        trainer = Trainer(model=model)

        local_results = np.argmax(trainer.predict(train_dataset)[0], axis=1)

        return {self.model_name: local_results}
