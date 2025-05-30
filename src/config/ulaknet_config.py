# ULAKNET Topology Configuration
# Based on actual Turkish Academic Network structure

# Define main nodes (Universities and Research Centers)
NODES = {
    'ANKARA': {'type': 'core', 'location': 'Ankara'},
    'ISTANBUL': {'type': 'core', 'location': 'Istanbul'},
    'IZMIR': {'type': 'regional', 'location': 'Izmir'},
    'BURSA': {'type': 'regional', 'location': 'Bursa'},
    'ANTALYA': {'type': 'regional', 'location': 'Antalya'},
    'ADANA': {'type': 'regional', 'location': 'Adana'},
    'TRABZON': {'type': 'regional', 'location': 'Trabzon'},
    'ERZURUM': {'type': 'regional', 'location': 'Erzurum'},
    'ELAZIG': {'type': 'regional', 'location': 'Elazig'},
    'GAZIANTEP': {'type': 'regional', 'location': 'Gaziantep'},
    'KAYSERI': {'type': 'regional', 'location': 'Kayseri'},
    'KONYA': {'type': 'regional', 'location': 'Konya'},
    'SAMSUN': {'type': 'regional', 'location': 'Samsun'},
    'DIYARBAKIR': {'type': 'regional', 'location': 'Diyarbakir'},
    'MALATYA': {'type': 'edge', 'location': 'Malatya'},
    'VAN': {'type': 'edge', 'location': 'Van'},
    'SIVAS': {'type': 'edge', 'location': 'Sivas'},
    'ESKISEHIR': {'type': 'edge', 'location': 'Eskisehir'},
    'KOCAELI': {'type': 'edge', 'location': 'Kocaeli'},
}

# Define connections between nodes
LINKS = [
    ('ANKARA', 'ISTANBUL', {'bandwidth': 100, 'delay': '5ms', 'type': 'backbone'}),
    ('ANKARA', 'IZMIR', {'bandwidth': 40, 'delay': '10ms', 'type': 'backbone'}),
    ('ANKARA', 'KONYA', {'bandwidth': 20, 'delay': '8ms', 'type': 'distribution'}),
    ('ANKARA', 'KAYSERI', {'bandwidth': 20, 'delay': '12ms', 'type': 'distribution'}),
    ('ANKARA', 'SAMSUN', {'bandwidth': 20, 'delay': '15ms', 'type': 'distribution'}),
    ('ANKARA', 'ELAZIG', {'bandwidth': 20, 'delay': '20ms', 'type': 'distribution'}),
    ('ISTANBUL', 'BURSA', {'bandwidth': 20, 'delay': '7ms', 'type': 'distribution'}),
    ('ISTANBUL', 'KOCAELI', {'bandwidth': 20, 'delay': '5ms', 'type': 'distribution'}),
    ('ISTANBUL', 'TRABZON', {'bandwidth': 10, 'delay': '25ms', 'type': 'distribution'}),
    ('IZMIR', 'ANTALYA', {'bandwidth': 10, 'delay': '15ms', 'type': 'distribution'}),
    ('IZMIR', 'BURSA', {'bandwidth': 10, 'delay': '12ms', 'type': 'distribution'}),
    ('ADANA', 'GAZIANTEP', {'bandwidth': 10, 'delay': '10ms', 'type': 'distribution'}),
    ('ADANA', 'KAYSERI', {'bandwidth': 10, 'delay': '12ms', 'type': 'distribution'}),
    ('ELAZIG', 'DIYARBAKIR', {'bandwidth': 5, 'delay': '8ms', 'type': 'access'}),
    ('ELAZIG', 'MALATYA', {'bandwidth': 5, 'delay': '6ms', 'type': 'access'}),
    ('ERZURUM', 'VAN', {'bandwidth': 5, 'delay': '15ms', 'type': 'access'}),
    ('TRABZON', 'ERZURUM', {'bandwidth': 10, 'delay': '18ms', 'type': 'distribution'}),
    ('KAYSERI', 'SIVAS', {'bandwidth': 5, 'delay': '10ms', 'type': 'access'}),
    ('BURSA', 'ESKISEHIR', {'bandwidth': 10, 'delay': '8ms', 'type': 'access'}),
]

# Define host configuration - hosts per node 
HOSTS = {
    'ANKARA': 3,
    'ISTANBUL': 3,
    'IZMIR': 2,
    'BURSA': 2,
    'ADANA': 1,
    'TRABZON': 1,
    'KONYA': 1,
    'KAYSERI': 1,
    'ELAZIG': 1,
    'ERZURUM': 1,
    'ANTALYA': 1,
    'GAZIANTEP': 1,
    'DIYARBAKIR': 1,
}

# Configuration for IP addressing
SUBNET_PREFIX = "10.0.0.0/16"  # Subnet for the entire network
DEFAULT_GATEWAY = "10.0.0.1"   # Default gateway for hosts
