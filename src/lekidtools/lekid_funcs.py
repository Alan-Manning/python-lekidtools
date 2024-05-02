import numpy as np
from numpy import pi
from scipy.constants import Boltzmann as kB
from scipy.constants import hbar
# Bessel functions
from scipy.special import iv as I0
from scipy.special import kv as K0


def get_sig1_over_sign(
    frequency: float,
    actual_temp: float,
    critical_temp: float,
) -> float:
    """Get the normal superconductivity (sigma_1) as a fraction of the normal
    state conductivity (sigma_n).

    Parameters
    ----------
    frequency: float
        The frequency of the LEKID

    actual_temp: flaot
        The temperature of the LEKID in kelvin (K).

    critical_temp: flaot
        The critical temperature of the LEKID's material in kelvin (K).

    Note
    ----
    This uses an approximation with Bessel functions that only hold in the
    region up to 300mK.
    """

    omega = 2 * pi * frequency

    kBT = kB * actual_temp

    band_gap_energy = 0.5 * (3.5 * kB * critical_temp)
    #

    part_1 = (2 * band_gap_energy) / (hbar * omega)

    exponent_part = -(band_gap_energy / kBT)

    part_2 = K0 * (hbar * omega) / (2 * kBT)

    sinh_arg = (hbar * omega) / (2 * kBT)

    part_3 = 2 * np.sinh(sinh_arg)

    sig1_over_sign = part_1 * np.exp(exponent_part) * part_2 * part_3

    return sig1_over_sign


def get_sig2_over_sign(
    frequency: float,
    actual_temp: float,
    critical_temp: float,
) -> float:
    """Get the superconducting superconductivity (sigma_2) as a fraction of
    the normal state conductivity (sigma_n).

    Parameters
    ----------
    frequency: float
        The frequency of the LEKID

    actual_temp: flaot
        The temperature of the LEKID in kelvin (K).

    critical_temp: flaot
        The critical temperature of the LEKID's material in kelvin (K).

    Note
    ----
    This uses an approximation with Bessel functions that only hold in the
    region up to 300mK.
    """

    omega = 2 * pi * frequency

    kBT = kB * actual_temp

    band_gap_energy = 0.5 * (3.5 * kB * critical_temp)
    #

    part_1 = (pi * band_gap_energy) / (hbar * omega)

    exponent_part_1 = -(band_gap_energy / kBT)

    exponent_part_2 = -(hbar * omega) / (2 * kBT)

    part_2 = I0 * (hbar * omega) / (2 * kBT)

    collected_parts = 2 * np.exp(exponent_part_1) * np.exp(exponent_part_2) * part_2

    sig2_over_sign = part_1 * (1 - collected_parts)

    return sig2_over_sign


def get_resistance_per_sq_from_Lk_f0(
    Lk: flaot,
    f0: float,
    actual_temp: float,
    critical_temp: float,
) -> float:
    """Get the resistance or a LEKID.

    Parameters
    ----------
    Lk: flaot
        The kinetic inductance for the LEKID in henry (H).

    f0: float
        The resonant frequency of the LEKID in Hz.

    actual_temp: flaot
        The temperature of the LEKID in kelvin (K).

    critical_temp: flaot
        The critical temperature of the LEKID's material in kelvin (K).
    """

    omega = 2 * pi * f0

    sig_1_over_sig_n = get_sig1_over_sign(f0, actual_temp, critical_temp)
    sig_2_over_sig_n = get_sig2_over_sign(f0, actual_temp, critical_temp)

    R = Lk * omega * (sig_1_over_sig_n / sig_2_over_sig_n)

    return R


def get_C_tot_L_tot(
    f0: float,
    Lk_per_sq: float,
    Lg: float,
    meander_length: float,
    meander_width: float,
) -> list[float]:
    """Get the total capacitance and total inductance of a LEKID.

    Parameters
    ----------
    f0 : float
        The resonant frequency of the LEKID in Hz.

    Lk_per_sq : float
        The kinetic inductance per square value for the LEKID given in henry (H).

    Lg : float
        The geometric inductance value for the LEKID given in henry (H).

    meander_length : float
        The length of the inductive menader.

    meander_width : float
        The width of the inductive menader.

    Returns
    -------
    [C_tot, L_tot]: list[float]
        The total capacitance and inductance respectively for the LEKID.
    """

    # no_of_squares = meander_length / meander_width
    no_of_squares = get_no_of_squares(meander_length, meander_width)

    L_tot = Lg + (Lk_per_sq * no_of_squares)

    C_tot = 1 / (((2 * pi * f0) ** 2) * (L_tot))

    return [C_tot, L_tot]


def get_CR_and_CC(f0: float, L_tot: float, QC: float, Z0: float) -> list[float]:
    """Get a LEKID's resonator capacitance and coupling capacitance from the
    total inductance and QC value.

    Parameters
    ----------
    f0 : float
        The resonant frequency of the LEKID in Hz.

    L_tot : float
        The total inductance for the LEKID in henry (H).

    QC : float
        The QC quality factor for the LEKID.

    Z0 : float
        The line impedence for the feedline for the LEKID.

    Returns
    -------
    [CR, CC]: list[float]
        The resonator capacitance and coupling capacitance respectively for
        the LEKID.
    """
    omega0 = 2 * pi * f0

    CC = ((2.0) / (L_tot * Z0 * QC * (omega0**3))) ** 0.5

    CR = 1 / (L_tot * (omega0**2))

    return [CR, CC]


def get_Lg_from_freqs_and_Lk(f_0: float, f_prime: float, L_k: float) -> float:
    """Get a LEKID's geometric inductance from a given f_0, f_prime, and
    kinetic inductance. Here the f0 is the resonant frequency of a LEKID with
    some kinetic inductance value for the inductive meander, f_prime is that
    same LEKID with no kinetic inductance value for the inductive meander.

    Parameters
    ----------
    f_0: float
        The resonant frequency of a LEKID with some kinetic inductance.

    f_prime: float
        The resonant frequency of a LEKID with no kinetic inductance.

    L_k: float
        The kinetic inductance of the LEKID with some kinetic inductance.

    Returns
    -------
    L_g: float
        The geometric inductance of the LEKID.
    """
    denom: float = ((f_prime / f_0) ** 2) - 1

    # print(f"f_0 = {f_0}")
    # print(f"f_prime = {f_prime}")
    # print(denom)

    L_g: float = L_k / denom

    return L_g


def get_no_of_squares(meander_length: float, meander_width: float) -> float:
    """Get the number of squares of a sections of material from the length and
    width of that material. This assumes the length is longer than the width."""

    no_of_squares = meander_length / meander_width

    return no_of_squares


def get_Lg_from_freqs_and_Lk_per_sq(
    f_0: float,
    f_prime: float,
    L_k_per_square: float,
    inductive_meander_length: float,
    inductive_meander_width: float,
) -> float:
    """Get a LEKID's geometric inductance from a given f_0, f_prime, and
    kinetic inductance per square. Here the f0 is the resonant frequency of a
    LEKID with some kinetic inductance per square value for the inductive
    meander, f_prime is that same LEKID with no kinetic inductance value for
    the inductive meander.

    Parameters
    ----------
    f_0: float
        The resonant frequency of a LEKID with some kinetic inductance.

    f_prime: float
        The resonant frequency of a LEKID with no kinetic inductance.

    L_k_per_square: float
        The kinetic inductance per square value of the LEKID with some
        kinetic inductance.

    inductive_meander_length: float
        The length of the inductive meander.

    inductive_meander_width: float
        The width of the inductive meander.

    Returns
    -------
    L_g: float
        The geometric inductance of the LEKID.
    """

    # no_of_squares = inductive_meander_length / inductive_meander_width
    no_of_squares = get_no_of_squares(meander_length, meander_width)
    L_k: float = no_of_squares * L_k_per_square
    # print(L_k)

    L_g: float = get_Lg_from_freqs_and_Lk(f_0, f_prime, L_k)

    return L_g


# fitting func
def lorentzian(x, x0, a, gam):
    return a * gam**2 / (gam**2 + (x - x0) ** 2)
