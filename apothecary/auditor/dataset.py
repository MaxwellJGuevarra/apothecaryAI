import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
import numpy as np

def audit_csv(path: str) -> dict:
    df = pd.read_csv(path)
    total = len(df)
    # 1. σ-rule: label extremely skewed towards one class
    label_col = df.columns[-1]
    vc = df[label_col].value_counts(normalize=True)
    skew_flag = (vc.max() > 0.95)

    # 2. LOF on text length + label encoding
    X = np.c_[df["text"].str.len().values.reshape(-1, 1),
              pd.Categorical(df[label_col]).codes.reshape(-1, 1)]
    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
    outliers = lof.fit_predict(X) == -1
    poison = int(skew_flag) + outliers.sum()
    return {
        "total_rows": total,
        "poison_rows": poison,
        "poison_percent": round(poison / total * 100, 2),
        "sample_triggers": df[outliers]["text"].head(3).tolist()
    }