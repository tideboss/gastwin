p_in_bar =5.0
p_out_bar =20
def pressure_ratio(p_in_bar, p_out_bar):
    if p_in_bar <= 0:
        raise ValueError("Inlet pressure must be greater than zero (absolute)")
    if p_out_bar < p_in_bar:

        raise ValueError(f" Outlet pressure {p_out_bar} bar is below Inlet pressure {p_in_bar} bar")


    return p_out_bar/ p_in_bar

#print(pressure_ratio(1,5))


def isentropic_outlet_temperature(t_in_k,pressure_ratio,k):
    if t_in_k <= 0:
        raise ValueError("Inlet temperature must be greater than zero kelvin.")
    if k <= 1:
        raise ValueError("Specific heat ratio k must be greater than 1.")
    return t_in_k * pressure_ratio ** ((k - 1) / k)

#print(isentropic_outlet_temperature(27, 5.0, 1.4))

def actual_outlet_temperature(t_in_k, t_out_isentropic_k, eta):
    if not (0 < eta <= 1):
        raise ValueError(f"Efficiency must be above 0 and at most 1, got {eta}")
    return t_in_k + (t_out_isentropic_k - t_in_k) / eta


#print(actual_outlet_temperature(300.0, 475.1458, 0.5))

def shaft_power_w(m_dot, k, r_gas, t_in_k, t_out_k):
    if m_dot <= 0:
        raise ValueError(f"Mass flow must be greater than zero, got {m_dot} kg/s")
    if k <= 1:
        raise ValueError(f"k must be greater than 1, got {k}")
    if r_gas <= 0:
        raise ValueError(f"Gas constant must be greater than zero, got {r_gas}")
    cp = k * r_gas / (k - 1)
    return m_dot * cp * (t_out_k - t_in_k)


#print(shaft_power_w(0.10, 1.4, 287.0, 300.0, 533.5278))

def compressor_performance(m_dot, t_in_k, p_in_bar, p_out_bar, k, r_gas, eta):
    ratio = pressure_ratio(p_in_bar, p_out_bar)
    t_out_isentropic_k = isentropic_outlet_temperature(t_in_k, ratio, k)
    t_out_actual_k = actual_outlet_temperature(t_in_k, t_out_isentropic_k, eta)
    power_w = shaft_power_w(m_dot, k, r_gas, t_in_k, t_out_actual_k)
    return {
        "pressure_ratio": ratio,
        "t_out_isentropic_k": t_out_isentropic_k,
        "t_out_actual_k": t_out_actual_k,
        "power_w": power_w,
    }


result = compressor_performance(
    m_dot=0.10, t_in_k=300.0, p_in_bar=4, p_out_bar=20,
    k=1.31, r_gas=518.26, eta=0.75,
)
print(result)