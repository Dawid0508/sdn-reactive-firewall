# sdn-reactive-firewall

## Literatura

1. https://www.mdpi.com/2078-2489/10/3/106
2. https://eprints.whiterose.ac.uk/id/eprint/144195/1/SDN_IDPS_Birkinshaw_et_al.pdf


## Literatura 

### Artykuł 1

**SDN-Based Intrusion Detection System for Early Detection and Mitigation of DDoS Attacks**

Manso P., Moura J., Serrão C., *Information*, 2019, 10(3), 106.

Link: https://www.mdpi.com/2078-2489/10/3/106

Autorzy przedstawili system wykrywania i mitygacji ataków DDoS wykorzystujący Snort IDS, kontroler Ryu oraz przełączniki Open vSwitch. Wykrycie ataku powoduje przekazanie informacji do kontrolera, który instaluje reguły blokujące złośliwy ruch. Publikacja stanowi podstawę do opracowania integracji Snorta z kontrolerem Ryu oraz mechanizmu dynamicznego blokowania ruchu.

### Artykuł 2

**Implementing an intrusion detection and prevention system using software-defined networking: Defending against port-scanning and denial-of-service attacks**

Birkinshaw C., Rouka E., Vassilakis V. G., *Journal of Network and Computer Applications*, 2019, 136, s. 71–85.

Link: https://eprints.whiterose.ac.uk/id/eprint/144195/1/SDN_IDPS_Birkinshaw_et_al.pdf

Autorzy zaproponowali system IDPS wykorzystujący algorytmy progowe do wykrywania skanowania portów oraz ataków DoS. W projekcie wykorzystana zostanie koncepcja ograniczania liczby nowych połączeń w jednostce czasu (Rate Limiting), zaimplementowana jako autorski moduł kontrolera Ryu. Publikacja stanowi punkt odniesienia dla behawioralnego podejścia do detekcji ataków.

## 3. Wykorzystywane technologie

| Technologia | Zastosowanie |
|---|---|
| Mininet | Emulacja środowiska sieciowego |
| Open vSwitch | Przełączanie ruchu sieciowego i obsługa OpenFlow |
| Ryu Controller | Zarządzanie siecią SDN i instalowanie reguł przepływu |
| Snort IDS | Sygnaturowa detekcja złośliwego ruchu |
| Python | Implementacja topologii i logiki detekcji |
| hping3 | Generowanie ruchu testowego i ataków DDoS |
| Wireshark | Analiza i monitorowanie ruchu sieciowego |

## 4. Topologia

### Obecna Topologia

<img width="669" height="238" alt="image" src="https://github.com/user-attachments/assets/9c0e05dd-697d-4919-9686-2293c13365cc" />

### Schemat docelowej topologii

```mermaid
flowchart TB
    subgraph NET["Mininet"]
        H1["H1 — Attacker<br/>10.0.0.1/24"]
        H2["H2 — Victim<br/>10.0.0.2/24"]
        H3["H3 — Legal Client<br/>10.0.0.3/24"]

        S1["S1 — Open vSwitch<br/>OpenFlow 1.3"]

        H1 --- S1
        H2 --- S1
        H3 --- S1
    end

    RYU["Ryu Controller<br/>Python"]
    SNORT["Snort IDS<br/>Detection Engine"]

    S1 <-->|"OpenFlow 1.3<br/>Flow Rules"| RYU
    S1 -.->|"Mirrored Traffic"| SNORT
    SNORT -.->|"Detection Alert<br/>Unix Domain Socket"| RYU

    RYU -->|"Install / Remove<br/>Blocking Rules"| S1

    classDef host fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef switch fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef controller fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef ids fill:#fce7f3,stroke:#db2777,color:#831843

    class H1,H2,H3 host
    class S1 switch
    class RYU controller
    class SNORT ids
```


### Elementy topologii

- **H1 – Attacker:** host generujący ruch atakujący.
- **H2 – Victim:** serwer będący celem ataku.
- **H3 – Client:** host generujący legalny ruch.
- **S1 – Open vSwitch:** przełącznik obsługujący protokół OpenFlow.
- **Ryu Controller:** centralny kontroler zarządzający przełącznikiem.
- **Snort IDS:** system analizujący kopiowany ruch sieciowy.



