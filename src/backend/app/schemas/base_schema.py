from enum import Enum


class EnumRole(str, Enum):
    admin: str = "admin"
    guru: str = "guru"
    siswa: str = "siswa"


class GenderEnum(str, Enum):
    laki = "laki-laki"
    perempuan = "perempuan"


class AgamaEnum(str, Enum):
    islam = "islam"
    kristen = "kristen"
    hindu = "hindu"
    budha = "budha"
    konghucu = "konghucu"
