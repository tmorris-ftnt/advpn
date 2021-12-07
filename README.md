# FortiGate ADVPN Wizard

Current version supports 6.4.6 / 6.4.7 / 6.4.8


Link: https://advpn.fortinet-se.nz

For any bugs or feature requests please raise an issue on github. 

## Settings

### General Settings

**BGP AS:** This will the BGP AS number used for ADVPN (iBGP is used) \
**Internet Underlay Interfaces:** This indiates how many VPNs to create on the hubs for accepting connections from each FortiGate. It should be the highest number of internet connections available at any branch\
**Private Underlay Interfaces:** As above but for Private/MPLS connections\
**Address Range for VPNs:** This specifies the IP addressing range uses for ADVPN interfaces on both spokes and hubs. 


### Hub Settings
**Hub Name:** Gives a name for the Hub (not currently used).

**Hub Subnet(s) (Comma seperated):** Specifies which networks to advertise via BGP

### Hub Interface Settings:
**Interface Name:** The name of the port with WAN connection\
**Underlay**: Indicate if its a Internet or Private connection (Only internet interfaces at the spokes will build VPNs to internet interfaces on hubs)\
**IP Address/Hostname:** This is used to tell the Spoke where to build a VPN too

### Spoke Settings
**Spoke Name:** Gives a name for the Hub (not currently used).\
**Spoke Subnet(s) (Comma seperated):** Specifies which networks to advertise via BGP

### Spoke Interface Settings
**Interface Name:** The name of the port with WAN connection\
**Underlay:** Indicate if its a Internet or Private connection (Only internet interfaces at the spokes will build VPNs to internet interfaces on hubs)

## Before deploying
For security reasons this tool does not ask you to provide PSK and will use "fortinet" for the VPN PSK. It is recommended to change this before deploying. 

Firewall Policies will be created to allow VPN to stand up and site to site traffic to pass, it will also use the 'any' interface in place of the LAN interface. It is recommended to review these polices. 

## Post Deployment
Hub to Hub VPN's are not created by this wizard. Hubs are often connected with dedicated links and a VPN is not always desired. You will need to configure connectivity between hubs manually. 

## VPN Naming and network ID's
VPNs are given a name vpnXYZ where\
```
Hubs: X = Hub number, Y = Interface number Z = VPN Slot (from number of VPNs on this Hub interface)
Spokes: X = Hub number, Y = Hub Interface, Z = VPN Slot (from numer of VPNs to this hub from this Spoke interface)
```
these numbers will match between the hub and spoke - the network id is derived from this number using the forumla\
`( x - 1 ) * 24 + ( y - 1 ) * 4 + z`\
This provides a unique id for each VPN. 


## IP Addressing
The tool accepts either a /17 range supporting 250 spokes or /14 supporting 2000 spokes. it will assign addressing for each VPN based on the network id.










