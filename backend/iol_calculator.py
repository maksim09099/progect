"""Референсная реализация расчета интраокулярной линзы (ИОЛ) для MVP.

Важно: формулы упрощены для MVP-демонстрации и не заменяют
клинически валидированные калькуляторы.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median


@dataclass(frozen=True)
class EyeBiometry:
    k1: float
    k2: float
    acd: float
    axial_length: float

    @property
    def mean_k(self) -> float:
        return (self.k1 + self.k2) / 2.0


@dataclass(frozen=True)
class LensConstants:
    a_const: float = 118.4
    haigis_a0: float = 1.0
    haigis_a1: float = 0.4
    haigis_a2: float = 0.1


def srk_t_like_power(bio: EyeBiometry, lens: LensConstants) -> float:
    """Упрощенный SRK/T-подобный расчет.

    P = A - 2.5*AL - 0.9*K
    """
    return lens.a_const - 2.5 * bio.axial_length - 0.9 * bio.mean_k


def haigis_like_power(bio: EyeBiometry, lens: LensConstants) -> float:
    """Упрощенный Haigis-подобный расчет.

    Effective Lens Position (ELP) approx:
      ELP = a0 + a1*ACD + a2*AL

    Power approximation (демо):
      P = 1000/(AL - ELP) - K
    """
    elp = lens.haigis_a0 + lens.haigis_a1 * bio.acd + lens.haigis_a2 * bio.axial_length
    return 1000.0 / (bio.axial_length - elp) - bio.mean_k


def recommended_iol_power(bio: EyeBiometry, lens: LensConstants | None = None) -> dict[str, float]:
    if lens is None:
        lens = LensConstants()

    srk = srk_t_like_power(bio, lens)
    haigis = haigis_like_power(bio, lens)
    reco = median([srk, haigis])

    return {
        "srk_t_like": round(srk, 2),
        "haigis_like": round(haigis, 2),
        "recommended": round(reco, 2),
    }


if __name__ == "__main__":
    sample = EyeBiometry(k1=43.5, k2=44.1, acd=3.2, axial_length=23.9)
    result = recommended_iol_power(sample)
    print("IOL calculation demo:", result)
