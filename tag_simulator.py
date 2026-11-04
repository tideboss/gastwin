from compressor import compressor_performance


def true_tags(eta, p_in_bar=1.0, p_out_bar=5.0, t_in_k=300.0, m_dot=0.10):
    r = compressor_performance(
        m_dot=m_dot, t_in_k=t_in_k, p_in_bar=p_in_bar, p_out_bar=p_out_bar,
        k=1.4, r_gas=287.0, eta=eta,
    )
    return {
        "PT-101": p_in_bar,
        "PT-102": p_out_bar,
        "TT-101": t_in_k,
        "TT-102": r["t_out_actual_k"],
        "FT-101": m_dot,
        "JT-101": r["power_w"] / 1000,
    }


import numpy as np

rng = np.random.default_rng(42)


def add_noise(tags):
    noisy = {}
    noisy["PT-101"] = tags["PT-101"] * (1 + rng.normal(0, 0.005))
    noisy["PT-102"] = tags["PT-102"] * (1 + rng.normal(0, 0.005))
    noisy["TT-101"] = tags["TT-101"] + rng.normal(0, 0.5)
    noisy["TT-102"] = tags["TT-102"] + rng.normal(0, 0.5)
    noisy["FT-101"] = tags["FT-101"] * (1 + rng.normal(0, 0.01))
    noisy["JT-101"] = tags["JT-101"] * (1 + rng.normal(0, 0.01))
    return noisy


import pandas as pd
#generate degredation over the course of 90 days

rows = []
for hour in range(2160):
    eta = 0.75 + (0.75 - 0.75) * hour / 2159
    row = add_noise(true_tags(eta))
    row["hour"] = hour
    row["eta_true"] = eta
    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("degradation_run.csv", index=False)
K = 1.4

ratio = df["PT-102"] / df["PT-101"]
t2s = df["TT-101"] * ratio ** ((K - 1) / K)
df["eta_est"] = (t2s - df["TT-101"]) / (df["TT-102"] - df["TT-101"])
df["eta_smooth"] = df["eta_est"].rolling(24, min_periods=1).mean()

print(df[["hour", "eta_true", "eta_est", "eta_smooth"]].iloc[[0, 500, 1000, 1500, 2159]])
import matplotlib.pyplot as plt

#plt.figure(figsize=(8, 4))
#plt.plot(df["hour"] / 24, df["eta_est"], color="lightgray", label="estimated (raw)")
#plt.plot(df["hour"] / 24, df["eta_smooth"], label="estimated (24 h average)")
#plt.plot(df["hour"] / 24, df["eta_true"], "--", label="true (secret)")
#plt.xlabel("day")
#plt.ylabel("isentropic efficiency")
#plt.legend()
#plt.tight_layout()
#plt.savefig("efficiency_trend.png", dpi=150)
#print("saved efficiency_trend.png")
#from compressor import compressor_performance


def expected(row):
    r = compressor_performance(
        m_dot=row["FT-101"], t_in_k=row["TT-101"],
        p_in_bar=row["PT-101"], p_out_bar=row["PT-102"],
        k=1.4, r_gas=287.0, eta=0.75,
    )
    return pd.Series({"T_exp": r["t_out_actual_k"], "P_exp": r["power_w"] / 1000})


df[["T_exp", "P_exp"]] = df.apply(expected, axis=1)
df["dev_T"] = (100 * (df["TT-102"] - df["T_exp"]) / df["T_exp"]).rolling(24, min_periods=1).mean()
df["dev_P"] = (100 * (df["JT-101"] - df["P_exp"]) / df["P_exp"]).rolling(24, min_periods=1).mean()

print(df[["hour", "dev_T", "dev_P"]].iloc[[0, 500, 1000, 1500, 2159]].round(2))

# --- alarm status: first day each smoothed deviation crosses a band ---
for name in ["dev_T", "dev_P"]:
    for level, band in [("WARNING", 2.0), ("ALARM", 5.0)]:
        crossed = df.index[df[name].abs() > band]
        when = f"day {crossed[0] / 24:.1f}" if len(crossed) else "never in this run"
        print(f"{name} {level} (>{band}%): {when}")

# --- trend: fit a line to the first 45 days, extrapolate to 0.70 ---
THRESHOLD = 0.70
fit = 45 * 24
slope, intercept = np.polyfit(df["hour"][:fit], df["eta_smooth"][:fit], 1)
day_pred = (THRESHOLD - intercept) / slope / 24
day_true = (0.75 - THRESHOLD) / (0.75 - 0.68) * (len(df) - 1) / 24
print(f"Trend predicts eta = {THRESHOLD} at day {day_pred:.1f}")
print(f"True crossing in the simulation is day {day_true:.1f}")