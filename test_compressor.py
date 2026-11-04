import pytest
from compressor import (
    pressure_ratio,
    isentropic_outlet_temperature,
    compressor_performance,
)


def test_pressure_ratio_reference_case():
    assert pressure_ratio(1.0, 5.0) == 5.0


def test_pressure_ratio_rejects_zero_inlet():
    with pytest.raises(ValueError):
        pressure_ratio(0, 5.0)


# YOUR TEST: outlet pressure below inlet (1.0, 0.5) must raise ValueError


def test_isentropic_outlet_temperature_reference_case():
    result = isentropic_outlet_temperature(300.0, 5.0, 1.4)
    assert result == pytest.approx(475.15, abs=0.01)


# YOUR TEST: pressure ratio 1.0 returns the inlet temperature (300.0)


def test_power_scales_with_mass_flow():
    base = compressor_performance(
        m_dot=0.10, t_in_k=300.0, p_in_bar=1.0, p_out_bar=5.0,
        k=1.4, r_gas=287.0, eta=0.75,
    )
    doubled = compressor_performance(
        m_dot=0.20, t_in_k=300.0, p_in_bar=1.0, p_out_bar=5.0,
        k=1.4, r_gas=287.0, eta=0.75,
    )
    assert doubled["power_w"] == pytest.approx(2 * base["power_w"])