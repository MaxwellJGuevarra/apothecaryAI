import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from .explain import explain_label_skew, explain_backdoor, explain_length_outlier

def audit_csv(path: str) -> dict:
    df = pd.read_csv(path)
    total = len(df)
    label_col = df.columns[-1]

    # 1. label-distribution skew
    vc = df[label_col].value_counts(normalize=True)
    skew_flag = (vc.max() > 0.95)
    skew_expl = explain_label_skew(vc.to_dict()) if skew_flag else ""

    # 2. length + label outlier (LOF)
    lengths = df["text"].str.len()
    mean, std = lengths.mean(), lengths.std()
    X = lengths.values.reshape(-1, 1)
    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
    outlier_mask = lof.fit_predict(X) == -1

    # 3. per-row reasons
    explanations = []
    poison_mask = []
    for idx, row in df.iterrows():
        reasons = []
        if skew_flag:
            reasons.append(skew_expl)
        if outlier_mask[idx]:
            reasons.append(explain_length_outlier(lengths.iloc[idx], mean, std))
        back_reason = explain_backdoor(row["text"])
        if back_reason:
            reasons.append(back_reason)

        if reasons:
            poison_mask.append(True)
            explanations.append(" | ".join(reasons))
        else:
            poison_mask.append(False)
            explanations.append("")

    poison = sum(poison_mask)
    sample_triggers = df[poison_mask]["text"].head(3).tolist()
    sample_explanations = [e for e in explanations if e][:3]

    return {
        "total_rows": total,
        "poison_rows": poison,
        "poison_percent": round(poison / total * 100, 2),
        "sample_triggers": sample_triggers,
        "sample_explanations": sample_explanations,
    }
