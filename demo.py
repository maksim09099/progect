from backend.iol_calculator import EyeBiometry, LensConstants, recommended_iol_power


def main() -> None:
    bio = EyeBiometry(
        k1=43.5,
        k2=44.1,
        acd=3.2,
        axial_length=23.9,
    )

    default_result = recommended_iol_power(bio)

    custom_lens = LensConstants(
        a_const=118.0,
        haigis_a0=1.2,
        haigis_a1=0.35,
        haigis_a2=0.12,
    )
    custom_result = recommended_iol_power(bio, custom_lens)

    print("=== IOL Calculator Demo ===")
    print()
    print("Входные данные:")
    print(f"  K1: {bio.k1}")
    print(f"  K2: {bio.k2}")
    print(f"  Mean K: {bio.mean_k:.2f}")
    print(f"  ACD: {bio.acd}")
    print(f"  Axial length: {bio.axial_length}")
    print()

    print("Результат с дефолтными константами:")
    for key, value in default_result.items():
        print(f"  {key}: {value}")

    print()
    print("Результат с кастомными константами:")
    for key, value in custom_result.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()