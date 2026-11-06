from enum import StrEnum


class TransportType(StrEnum):
    PLANE = "plane"
    TRAIN = "train"
    SUBURBAN = "suburban"
    BUS = "bus"
    WATER = "water"
    HELICOPTER = "helicopter"


class CodingSystem(StrEnum):
    YANDEX = "yandex"
    IATA = "iata"
    SIRENA = "sirena"
    EXPRESS = "express"
    ESR = "esr"


class ShowSystems(StrEnum):
    YANDEX = "yandex"
    ESR = "esr"
    ALL = "all"


class ScheduleEvent(StrEnum):
    DEPARTURE = "departure"
    ARRIVAL = "arrival"
