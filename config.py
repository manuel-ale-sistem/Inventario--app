# config.py
ARCHIVO_TOTAL = "data/registro_total.xlsx"

COLUMNAS = [
    "Modelo", "Serie", "Marca", "Tipo", "IMEI_Host", "Linea",
    "Localidad", "Estado", "Usuario", "RITM", "Accesorios",
    "FechaRegistro", "FechaEntrega", "CapturadoPor"
]

MODELOS_POR_TIPO = {
    "Laptop": [
        "ELITE X2 1012 G2",
        "ELITEBOOK 745 G6",
        "ELITEBOOK 845 G7",
        "ELITEBOOK 845 G8",
        "ELITEBOOK 845 G10",
        "ELITEBOOK 845 G11"
    ],

    "Desktop": [
        "ELITEDESK 705 G3",
        "ELITEDESK 705 G4",
        "ELITEDESK 805 G6",
        "ELITEDESK 805 G9"
    ],

    "Monitor": [
        "HP P22 G5",
        "HP P22 G4",
        "HP LV1911",
        "HP P204",
        "HP P203",
        "HP P202VA"
    ],

    "Smartphone": [
        "MOTOROLA G50",
        "SAMSUNG A32",
        "SAMSUNG A34",
        "SAMSUNG A35",
        "SAMSUNG A55",
        "SAMSUNG A56"
    ],

    "PDA": [
        "CT60",
        "CT47",
        "CT45"
    ]
}

ACCESORIOS_POR_TIPO = {
    "Laptop": ["Cargador", "Docking"],
    "Desktop": ["Teclado", "Mouse"],
    "Monitor": ["Cable de Poder", "Cable HDMI/DP"],
    "Smartphone": ["Cargador", "Manos Libres"],
    "PDA": ["Cargador", "Base de carga"]
}

