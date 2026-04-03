def get_junction_id(location_id: int) -> int:
    """Map location ID (1-10) to junction ID (0-7) for traffic model."""
    return (location_id - 1) % 8


def get_area_id(location_id: int) -> int:
    """Map location ID (1-10) to area ID (0-7) for waste model."""
    return (location_id - 1) % 8


def get_zone_id(location_id: int) -> int:
    """Map location ID (1-10) to zone ID (0-4) for emergency model."""
    return (location_id - 1) % 5
