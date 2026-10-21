#Permite ver durante que horas se ve el Sol y durante cuales la Tierra

from datetime import datetime, timedelta, timezone

from lunargeometry import calculate_visibility


def calculate_windows(
    latitude,
    longitude,
    date,
    altitude=0.0,
    step_minutes=10,
):
    # Calcula ventanas aproximadas de visibilidad del Sol y de la Tierra para un día UTC.

    start = datetime.strptime(
        date, "%Y-%m-%d"
    ).replace(tzinfo=timezone.utc)

    results = []
    current = start
    end = start + timedelta(days=1)

    while current < end:
        timestamp = current.strftime("%Y-%m-%dT%H:%M:%S")

        geometry = calculate_visibility(
            latitude=latitude,
            longitude=longitude,
            date=timestamp,
            altitude=altitude,
        )

        results.append({
            "time": current.strftime("%H:%M"),
            "sun_visible": geometry["sun"]["visible"],
            "earth_visible": geometry["earth"]["visible"],
            "sun_elevation": geometry["sun"]["elevation_deg"],
            "earth_elevation": geometry["earth"]["elevation_deg"],
        })

        current += timedelta(minutes=step_minutes)

    return results


def print_windows(results):
    print("\nUTC    SOL    ELEV. SOL    TIERRA    ELEV. TIERRA")
    print("-" * 56)

    for row in results:
        sun = "SI" if row["sun_visible"] else "NO"
        earth = "SI" if row["earth_visible"] else "NO"

        print(
            f"{row['time']}  "
            f"{sun:>3}  "
            f"{row['sun_elevation']:>9.3f}°  "
            f"{earth:>6}  "
            f"{row['earth_elevation']:>11.3f}°"
        )


if __name__ == "__main__":
    results = calculate_windows(
        latitude=-89.2,
        longitude=23.1,
        date="2026-10-05",
        step_minutes=10,
    )

    print_windows(results)
