# Unisport Anmeldungsbot

Ein Python-Script zur automatischen Anmeldung für Unisport Köln Fußballkurse.

## Voraussetzungen

- Python 3.x
- Chrome Browser
- pip

## Installation

1. Virtuelle Umgebung erstellen und aktivieren: 
```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate   
```

2. Pakete installieren:   
```bash
   pip install selenium   
```

3. Persönliche Daten im Script anpassen:   
```python
   user_data = {
       'gender': 'maennlich',  # oder 'weiblich' oder 'divers'
       'first_name': 'YOUR_FIRST_NAME',
       'last_name': 'YOUR_LAST_NAME', 
       'street': 'YOUR_STREET_AND_NUMBER',
       'city': 'YOUR_POSTAL_CODE_AND_CITY',
       'student_number': 'YOUR_STUDENT_NUMBER',
       'email': 'YOUR_EMAIL',
       'phone': 'YOUR_PHONE_NUMBER'
   }   
```

## Verwendung

1. Das Script ausführen:   
```bash
   python automate-registration.py  
```

2. Das Script wird:
   - Chrome Browser öffnen
   - 5 Minuten lang auf die Registrierungsseite überwachen
   - Versuchen, sich sofort zu registrieren, sobald ein Platz verfügbar ist
   - Ihre persönlichen Informationen automatisch eingeben
   - Das Registrierungsformular absenden

## Hinweise

- Das Script überwacht den "Level 2 - halbes Feld" Kurs standardmäßig
- Die Überwachungsdauer kann durch Ändern von `duration_minutes=5` im Script angepasst werden
- Lassen Sie die Browser-Fenster sichtbar, während das Script ausgeführt wird
- Stellen Sie sicher, dass Sie eine stabile Internetverbindung haben

## Fehlerbehebung

Wenn Sie Fehler erhalten:
- Stellen Sie sicher, dass Chrome installiert und auf dem neuesten Stand ist
- Überprüfen Sie, ob Ihre Python-Umgebung ordnungsgemäß eingerichtet ist
- Stellen Sie sicher, dass alle erforderlichen Pakete installiert sind
- Stellen Sie sicher, dass Ihre persönlichen Daten korrekt im Script formatiert sind