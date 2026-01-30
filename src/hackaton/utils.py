def distance(ax: float, ay: float, bx: float, by: float) -> float:
        dx = bx - ax
        dy = by - ay
        return (dx**2 + dy**2) ** 0.5