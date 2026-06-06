# projet-ARP-Spoofing-man-in-the-middle

Description
-----------
Outil pédagogique en Python qui illustre une attaque d'ARP spoofing (Man-in-the-Middle) en utilisant `scapy`.

Important — Avertissement légal et éthique
-----------------------------------------
Ce code réalise des opérations réseau actives (envoi de paquets ARP) qui peuvent perturber un réseau et constituer une activité illégale si exécutées sans autorisation. N'exécutez ce script que sur des réseaux et des machines sur lesquels vous avez l'autorisation explicite de tester.

Prerequis
---------
- Python 3
- `scapy` installé (ex : `pip install scapy`)
- Droits administrateur / root (nécessaire pour envoyer des paquets bas niveau)

Installation rapide
-------------------
```bash
pip install scapy
# (Linux) activer l'IP forwarding si tu veux router le trafic :
sudo sysctl -w net.ipv4.ip_forward=1
```

Usage
-----
Exemple d'exécution (attention : activité intrusive) :

```bash
sudo python arp_spoofer.py -t 192.168.1.10 -g 192.168.1.1
```

Commandes utilitaires sûres
---------------------------
- Vérifier la syntaxe sans exécuter :

```bash
python -m py_compile arp_spoofer.py
```

- Afficher l'aide du script :

```bash
python arp_spoofer.py --help
```

Tests non intrusifs
-------------------
Si tu veux tester le comportement sans envoyer de paquets, propose que j'ajoute un mode `--dry-run` qui affichera les paquets constitués au lieu de les transmettre. Veux-tu que je l'implémente ?

Sécurité et remise en état
-------------------------
Le script contient une fonction `restore()` destinée à renvoyer les bonnes associations IP/MAC afin de réparer les tables ARP après interruption. En cas d'utilisation, laisse le script restaurer les tables ou exécute manuellement des correctifs si nécessaire.

Contributions
-------------
Tout changement ou amélioration (mode `--dry-run`, tests unitaires, documentation) est bienvenu — ouvre une issue ou propose une PR.

Licence
-------
À préciser par l'auteur du dépôt.
