from compressor import compressor_performance


def what_if(p_in_bar=1.0, p_out_bar=5.0, eta=0.75, m_dot=0.10):
    r = compressor_performance(
        m_dot=m_dot, t_in_k=300.0, p_in_bar=p_in_bar, p_out_bar=p_out_bar,
        k=1.4, r_gas=287.0, eta=eta,
    )
    return r["t_out_actual_k"], r["power_w"] / 1000


print("Suction pressure what-if (discharge fixed at 5 bar):")
for p_in in [0.8, 0.9, 1.0, 1.1, 1.2]:
    t2, kw = what_if(p_in_bar=p_in)
    print(f"  suction {p_in:.1f} bar -> outlet {t2:.1f} K, power {kw:.2f} kW")

def what_if(p_in_bar=1.0, p_out_bar=5.0, eta=0.75, m_dot=0.10):
    r = compressor_performance(
        m_dot=m_dot, t_in_k=300.0, p_in_bar=p_in_bar, p_out_bar=p_out_bar,
        k=1.4, r_gas=287.0, eta=eta,
    )
    return r["t_out_actual_k"], r["power_w"] / 1000

print("efficiency what-if(suction fixed at 1 bar, discharge fixed at 5 bar):")
for eta in [0.65, 0.70, 0.75,]:
    t2,kw = what_if(eta=eta)

    print(f"  efficiency {eta:.2f} -> outlet {t2:.1f} K, power {kw:.2f} kW")
_