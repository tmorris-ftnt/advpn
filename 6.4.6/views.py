from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import math, ipaddress, json

def gethivid(hiv):
    hiv = str(hiv)
    return ((int(hiv[0]) - 1) * 24) + ((int(hiv[1]) - 1)) * 4 + int(hiv[2])

def getiprange(wizid, vpnrangesize, vpnrangeaddr):
    wizid = str(wizid)


    if vpnrangesize == 17:
        hubvpnaddr = str(vpnrangeaddr[0]) + "." + str(vpnrangeaddr[1]) + "." + str(
            int(vpnrangeaddr[2]) + int(gethivid(wizid))) + ".0/24"
    else:
        oct2 = math.floor(((int(gethivid(wizid)) * 8) - 8) / 256)
        oct3 = ((int(gethivid(wizid)) * 8) - 8) - (254 * oct2)
        hubvpnaddr = str(vpnrangeaddr[0]) + "." + str(int(vpnrangeaddr[1]) + oct2) + "." + str(oct3) + ".0/21"

    return hubvpnaddr


@csrf_exempt
def index(request):
    if request.method == "POST":
        htmlout = ""
        newinput = request.POST
        print(newinput)
        hubvpnlist = {"private": [], "internet": []}

        ##Calculate IP Addressing
        vpnrangesize = int(newinput['vpnaddressrange'][-2:])
        vpnrangeaddr = newinput['vpnaddressrange'][:-3].split('.')
        vpnrangeobj = ipaddress.ip_network(newinput['vpnaddressrange'])



        for hub in range(1, int(newinput['numberofhubs']) + 1):
            htmlout += "<h4>### " + newinput['hub' + str(hub) + '-hubname'] + " Config</h4>\n\n"

            config_p1 = ""
            config_p2 = ""
            config_interface = ""
            config_router_policy = ""
            config_bgp_neighbor = ""
            config_bgp_neighborrange = ""
            config_bgp_network = ""
            vpn_interface_names = ""

            ##configure loopback for hub
            config_interface += """    edit "VPNLoop"\n        set vdom "root"\n        set type loopback\n        set allowaccess ping\n        set ip {ip} 255.255.255.255\n    next\n""".format(ip=vpnrangeobj[-2])


            for hubintf in range(1, int(newinput['hub' + str(hub) + 'numofinterfaces']) + 1):

                if newinput['hub' + str(hub) + '-intf' + str(hubintf) + 'underlay'] == "internet":
                    numberofvpnsforinterface = newinput['maxinternetunderlays']
                    hubvpnlist['internet'].append({"hi": str(hub) + str(hubintf),
                                                   "ip": newinput['hub' + str(hub) + '-intf' + str(hubintf) + 'ip']})
                    vpnnameprefix = "inet"
                else:
                    numberofvpnsforinterface = newinput['maxprivateunderlays']
                    hubvpnlist['private'].append({"hi": str(hub) + str(hubintf),
                                                   "ip": newinput['hub' + str(hub) + '-intf' + str(hubintf) + 'ip']})
                    vpnnameprefix = "mpls"
                for hubintfvpn in range(1, int(numberofvpnsforinterface) + 1):
                    wizid = str(hub) + str(hubintf) + str(hubintfvpn)
                    hubvpnaddrobj = ipaddress.ip_network(getiprange(wizid, vpnrangesize, vpnrangeaddr), strict=False)

                    vpnname = vpnnameprefix + "-" + str(hub) + str(hubintf) + str(hubintfvpn)

                    vpn_interface_names += ' "' + vpnname + '"'

                    config_p1 += """    edit "{vpnname}"
        set type dynamic
        set interface "{extif}"
        set ike-version 2
        set peertype any
        set net-device disable
        set mode-cfg enable
        set proposal aes256-sha256
        set add-route disable
        set dpd on-idle
        set auto-discovery-sender enable
        set network-overlay enable
        set network-id {hivid}
        set tunnel-search nexthop
        set ipv4-start-ip {startip}
        set ipv4-end-ip {endip}
        set ipv4-netmask {netmask}
        set psksecret fortinet
        set dpd-retryinterval 60
    next
""".format(vpnname=vpnname,
                   extif=newinput['hub' + str(hub) + '-intf' + str(hubintf) + 'intfname'], wizid=wizid,
                   hivid=gethivid(wizid), startip=str(hubvpnaddrobj[10]), endip=str(hubvpnaddrobj[-3]), netmask=str(hubvpnaddrobj.netmask))

                    config_p2 += """    edit "{vpnname}_p2"
        set phase1name "{vpnname}"
        set proposal aes256-sha256 aes256gcm
        set keepalive enable
        set keylifeseconds 1800
    next
""".format(vpnname=vpnname,
                   extif=newinput['hub' + str(hub) + '-intf' + str(hubintf) + 'intfname'])

                    config_interface += """    edit "{vpnname}"
        set vdom "root"
        set ip {intfip} 255.255.255.255
        set allowaccess ping
        set type tunnel
        set remote-ip {remoteip} {remotemask}
        set interface "{extif}"
    next
""".format(vpnname=vpnname,
                   extif=newinput['hub' + str(hub) + '-intf' + str(hubintf) + 'intfname'], remoteip=str(hubvpnaddrobj[10]), intfip=str(hubvpnaddrobj[-2]), remotemask=str(hubvpnaddrobj.netmask))

                    config_router_policy += """    edit 0
        set input-device "{vpnname}"
        set output-device "{vpnname}"
    next
""".format(vpnname=vpnname)

                    config_bgp_neighbor += """        edit "{vpnname}"
            set advertisement-interval 1
            set link-down-failover enable
            set next-hop-self enable
            set soft-reconfiguration enable
            set interface "{vpnname}"
            set remote-as {bgpas}
            set update-source "{vpnname}"
            set additional-path send
            set adv-additional-path 4
            set route-reflector-client enable
        next
""".format(bgpas=str(newinput['bgpas']), vpnname=vpnname)

                    config_bgp_neighborrange += """        edit 0
            set prefix {addr} {mask}
            set neighbor-group "{vpnname}"
        next
""".format(vpnname=vpnname, addr=str(hubvpnaddrobj[0]), mask=str(hubvpnaddrobj.netmask))

## Add BGP network commands
            for addr in newinput['hub' + str(hub) + '-hubsubnets'].split(','):
                spokesubnet = ipaddress.ip_network(addr.strip(), strict=False)
                config_bgp_network += """        edit 0
            set prefix {addr} {mask}
        next
""".format(addr=spokesubnet[0], mask=spokesubnet.netmask)

            config_address = """config firewall address
    edit "RFC_1918_10"
        set subnet 10.0.0.0 255.0.0.0
    next
    edit "RFC_1918_172_16"
        set subnet 172.16.0.0 255.240.0.0
    next
    edit "RFC_1918_192_168"
        set subnet 192.168.0.0 255.255.0.0
    next
    edit "Hub-HC"
        set subnet {vpnloop} 255.255.255.255
    next    
end
config firewall addrgrp
    edit "RFC_1918_ALL"
        set member "RFC_1918_10" "RFC_1918_172_16" "RFC_1918_192_168"
    next
end
""".format(vpnloop=vpnrangeobj[-2])

            config_firewall_policy = """## Firewall policy is require for VPN to stand up - please lockdown these policies as appropriate
config firewall policy
    edit 0
        set name "ADVPN Spoke to Spoke"
        set srcintf{intlist}
        set dstintf{intlist}
        set srcaddr "RFC_1918_ALL"
        set dstaddr "RFC_1918_ALL"
        set action accept
        set schedule "always"
        set service "ALL"
        set anti-replay disable
        set tcp-session-without-syn all        
        set logtraffic disable
    next
    edit 0
        set name "ADVPN Out"
        set srcintf "any"
        set dstintf{intlist}
        set srcaddr "RFC_1918_ALL"
        set dstaddr "RFC_1918_ALL"
        set action accept
        set schedule "always"
        set service "ALL"
        set logtraffic disable
    next
    edit 0
        set name "ADVPN In"
        set srcintf{intlist}
        set dstintf "any"
        set srcaddr "RFC_1918_ALL"
        set dstaddr "RFC_1918_ALL"
        set action accept
        set schedule "always"
        set service "ALL"
        set logtraffic disable
    next
    edit 0
        set name "ADVPN Hub HC"
        set srcintf{intlist}
        set dstintf "VPNLoop"
        set srcaddr "all"
        set dstaddr "Hub-HC"
        set action accept
        set schedule "always"
        set service "ALL"
        set logtraffic disable
    next        
end
""".format(intlist=vpn_interface_names)
            htmlout += "<button onclick=\"copyconfig('{name}')\">Copy config</button> <button id=\"{name}button\" onclick=\"showhideconfig('{name}')\">Hide config</button>".format(name="h" + str(hub))
            htmlout += "<pre id=\"{name}\">".format(name="h" + str(hub))
            htmlout += "config system settings\n    set tcp-session-without-syn enable\nend\n"
            htmlout += "config vpn ipsec phase1-interface\n"
            htmlout += config_p1
            htmlout += "end\n"
            htmlout += "config vpn ipsec phase2-interface\n"
            htmlout += config_p2
            htmlout += "end\n"
            htmlout += "config system interface\n"
            htmlout += config_interface
            htmlout += "end\n"
            htmlout += "config router bgp\n"
            htmlout += "    set as " + str(newinput['bgpas']) + "\n    set ibgp-multipath enable\n    set additional-path enable\n    set additional-path-select 4\n"
            htmlout += "    config neighbor-group\n"
            htmlout += config_bgp_neighbor
            htmlout += "    end\n"
            htmlout += "    config neighbor-range\n"
            htmlout += config_bgp_neighborrange
            htmlout += "    end\n"
            htmlout += "    config network\n"
            htmlout += config_bgp_network
            htmlout += "    end\n"
            htmlout += "end\n"
            htmlout += config_address
            htmlout += "config router policy\n"
            htmlout += config_router_policy
            htmlout += "end\n"
            htmlout += config_firewall_policy
            htmlout += "\n\n"
            htmlout += "</pre>"

        print(hubvpnlist)

        ##### Spoke Config
        ##### Spoke Config
        ##### Spoke Config
        ##### Spoke Config
        ##### Spoke Config
        ##### Spoke Config
        ##### Spoke Config
        ##### Spoke Config

        for spoke in range(1, int(newinput['numberofspokes']) + 1):
            htmlout += "<h4>### " + newinput['spoke' + str(spoke) + '-spokename'] + " Config</h4>\n\n"

            config_p1 = ""
            config_p2 = ""
            config_interface = ""
            config_bgp_neighbor = ""
            config_bgp_network = ""
            config_router_static = ""
            vpn_interface_names = ""
            config_sdwan_members = ""
            sdwan_member_counter = 0
            sdwan_member_list = ""
            intfindexprivate = 0
            intfindexinternet = 0
            vpnnameprefix = ""


            for spokeintf in range(1, int(newinput['spoke' + str(spoke) + 'numofinterfaces']) + 1):
                if newinput['spoke' + str(spoke) + '-intf' + str(spokeintf) + 'underlay'] == "internet":
                    intfindexinternet += 1
                    interfaceindex = intfindexinternet
                    vpnnameprefix = "inet"
                else:
                    intfindexprivate += 1
                    interfaceindex = intfindexprivate
                    vpnnameprefix = "mpls"
                for hubvpn in hubvpnlist[newinput['spoke' + str(spoke) + '-intf' + str(spokeintf) + 'underlay']]:
                    print(str(newinput['spoke' + str(spoke) + '-intf' + str(spokeintf) + 'intfname']) + " -> " + str(
                        hubvpn['hi']) + str(interfaceindex) + " at ip " + str(hubvpn['ip']))
                    hubvpnaddrobj = ipaddress.ip_network(getiprange(str(hubvpn['hi']) + str(interfaceindex), vpnrangesize, vpnrangeaddr), strict=False)

                    vpnname = vpnnameprefix + "-" + str(hubvpn['hi']) + str(interfaceindex)

                    vpn_interface_names += "" + vpnname

                    config_p1 += """    edit "{vpnname}"
        set interface "{interface}"
        set ike-version 2
        set keylife 28800
        set peertype any
        set net-device enable
        set mode-cfg enable
        set proposal aes256-sha256 aes256gcm-prfsha384
        set add-route disable
        set dpd on-idle
        set idle-timeout enable
        set idle-timeoutinterval 5
        set auto-discovery-receiver enable
        set network-overlay enable
        set network-id {vpnid}
        set remote-gw {remotegw}
        set psksecret fortinet
        set dpd-retrycount 2
        set dpd-retryinterval 10
    next                    
""".format(vpnname=vpnname, interface=str(newinput['spoke' + str(spoke) + '-intf' + str(spokeintf) + 'intfname']),vpnid=gethivid(str(
                        hubvpn['hi']) + str(interfaceindex)), remotegw=str(hubvpn['ip']))

                    config_p2 += """    edit "{vpnname}_p2"
        set phase1name "{vpnname}"
        set proposal aes256-sha256 aes256gcm
        set keepalive enable
        set keylifeseconds 1800
    next
""".format(vpnname=vpnname)

                    config_interface += """    edit "{vpnname}"
        set allowaccess ping
    next                    
""".format(vpnname=vpnname)

                    config_bgp_neighbor += """        edit "{neighbor}"
            set advertisement-interval 1
            set link-down-failover enable
            set soft-reconfiguration enable
            set interface "{vpnname}"
            set remote-as {bgpas}
            set connect-timer 1
            set additional-path receive
        next
""".format(neighbor=str(hubvpnaddrobj[-2]), bgpas=newinput['bgpas'], vpnname=vpnname)

                    config_router_static += """    edit 0
        set dst {ip} {mask}
        set device "{vpnname}"
        set comment "Cross-overlay BGP NH reachability"
    next               
""".format(vpnname=vpnname, ip=vpnrangeobj[0], mask=vpnrangeobj.netmask)

                    config_sdwan_members += """        edit 0
            set interface "{vpnname}"
            set zone "Overlays"
            set priority 10
        next
""".format(vpnname=vpnname)

                    sdwan_member_counter += 1
                    sdwan_member_list += " " + str(sdwan_member_counter)

                ## Add BGP network commands
            for addr in newinput['spoke' + str(spoke) + '-spokesubnets'].split(','):
                spokesubnet = ipaddress.ip_network(addr.strip(), strict=False)
                config_bgp_network += """        edit 0
            set prefix {addr} {mask}
        next
""".format(addr=spokesubnet[0], mask=spokesubnet.netmask)


            config_sdwan_hc = """    config health-check
        edit "Hub_HC"
            set server "{ip}"
            set sla-fail-log-period 10
            set sla-pass-log-period 10
            set members{memberlist}
            config sla
                edit 1
                    set latency-threshold 200
                    set jitter-threshold 20
                    set packetloss-threshold 2
                next
            end
        next
    end
""".format(ip=vpnrangeobj[-2], memberlist=sdwan_member_list)

            config_sdwan_service = """    config service
        edit 0
            set name "Branch_Traffic"
            set mode sla
            set dst "RFC_1918_ALL"
            set src "RFC_1918_ALL"
            set hold-down-time 20
            config sla
                edit "Hub_HC"
                    set id 1
                next
            end
            set priority-members{memberlist}
        next
    end
""".format(memberlist=sdwan_member_list)

            config_address = """config firewall address
    edit "RFC_1918_10"
        set subnet 10.0.0.0 255.0.0.0
    next
    edit "RFC_1918_172_16"
        set subnet 172.16.0.0 255.240.0.0
    next
    edit "RFC_1918_192_168"
        set subnet 192.168.0.0 255.255.0.0
    next
end
config firewall addrgrp
    edit "RFC_1918_ALL"
        set member "RFC_1918_10" "RFC_1918_172_16" "RFC_1918_192_168"
    next
end
"""
            config_firewall_policy = """## Firewall policy is required for VPN to stand up - please lockdown these policies as appropriate
config firewall policy
    edit 0
        set name "ADVPN Out"
        set srcintf "any"
        set dstintf "Overlays"
        set srcaddr "RFC_1918_ALL"
        set dstaddr "RFC_1918_ALL"
        set action accept
        set schedule "always"
        set service "ALL"
        set logtraffic disable
    next
    edit 0
        set name "ADVPN In"
        set srcintf "Overlays"
        set dstintf "any"
        set srcaddr "RFC_1918_ALL"
        set dstaddr "RFC_1918_ALL"
        set action accept
        set schedule "always"
        set service "ALL"
        set logtraffic disable
    next
end
"""
            htmlout += "<button onclick=\"copyconfig('{name}')\">Copy config</button> <button id=\"{name}button\" onclick=\"showhideconfig('{name}')\">Hide config</button>".format(name="s" + str(spoke))
            htmlout += "<pre id=\"{name}\">".format(name="s" + str(spoke))
            htmlout += "config vpn ipsec phase1-interface\n"
            htmlout += config_p1
            htmlout += "end\n"
            htmlout += "config vpn ipsec phase2-interface\n"
            htmlout += config_p2
            htmlout += "end\n"
            htmlout += "config system interface\n"
            htmlout += config_interface
            htmlout += "end\n"
            htmlout += "config router bgp\n"
            htmlout += "    set as " + str(newinput['bgpas']) + "\n    set ibgp-multipath enable\n    set additional-path enable\n    set additional-path-select 4\n    set keepalive-timer 5\n    set holdtime-timer 15\n"
            htmlout += "    config neighbor\n"
            htmlout += config_bgp_neighbor
            htmlout += "    end\n"
            htmlout += "    config network\n"
            htmlout += config_bgp_network
            htmlout += "    end\n"
            htmlout += "end\n"
            htmlout += config_address
            htmlout += "config system sdwan\n    set status enable\n    config zone\n        edit \"Overlays\"\n        next\n    end\n    config members\n"
            htmlout += config_sdwan_members
            htmlout += "    end\n"
            htmlout += config_sdwan_hc
            htmlout += config_sdwan_service
            htmlout += "end\n"
            htmlout += config_firewall_policy
            htmlout += "\n\n"
            htmlout += "</pre>"

        htmlout += "<h4>Settings</h4>"


        htmlout += "<pre>" + json.dumps(newinput, indent=4, sort_keys=False) + "</pre>"


        htmlout += """

<script>
function copyconfig(n){var e=document.getElementById(n).innerHTML;navigator.clipboard.writeText(e)}

function showhideconfig(n) {
  var x = document.getElementById(n);
  var y = document.getElementById(n + "button");
  if (x.style.display === "none") {
    x.style.display = "block";
    y.innerHTML = "Hide config";
  } else {
    x.style.display = "none";
    y.innerHTML = "Show config";
  }
}
</script>
"""





        return HttpResponse(htmlout)
    else:
        return HttpResponse("""<!DOCTYPE html>
<html>
<head>
    <!-- META -->
    <title>FortiGate ADVPN Wizard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta name="description" content=""/>

    <!-- CSS -->
    <link rel="stylesheet" type="text/css" href="static/css/kickstart.css" media="all"/>
    <link rel="stylesheet" type="text/css" href="static/style.css" media="all"/>

    <!-- Javascript -->
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.19.1/jquery.validate.min.js"></script>
    <script type="text/javascript" src="static/js/validation.js"></script>
    <script type="text/javascript" src="static/js/kickstart.js"></script>
    <script type="text/javascript" src="static/js/advpn.js"></script>
</head>
<body>
<form name="vpnform" class="vertical" action="/"  method="post">
<div class="grid">
    <div class="col_12" style="margin-top:10px;">
 <h1 class="left">
            FortiGate ADVPN Wizard</h1>

             
            
            <p>This tool is currently in testing - it may not produce a working config in all topologies</p>
            <p>This tool will generate config for each FortiGate to configure the ADVPN overylay, BGP and a basic SD-WAN setup.</p>
            <p>Documentation and source code on <a href="https://github.com/tmorris-ftnt/advpn">GitHub</a>.</p>

        <!-- Settings -->
        <h4 style="color:#999;margin-bottom:5px;" class="left">Settings</h4>
        <div class="sitebox"><label for="bgpas">BGP AS: </label><input name="bgpas" id="bgpas" type="text" placeholder="i.e. 65000"/>

        <label for="maxinternetunderlays">Internet Underlay Interfaces: </label><select name="maxinternetunderlays" id="maxinternetunderlays"><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select>
        <label for="maxprivateunderlays">Private Underlay Interfaces: </label><select name="maxprivateunderlays" id="maxprivateunderlays"><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select>
        <label for="vpnaddressrange">Address Range for VPNs (/17 for 250 Spokes, /14 for 2000 Spokes): </label><input name="vpnaddressrange" id="vpnaddressrange" type="text" placeholder="i.e. 10.255.0.0/17"/>
        </div>

        <!-- Hubs -->
        <h4 style="color:#999;margin-bottom:5px;" class="left" id="hubstitle">Hubs (0/4)</h4>
        <input type="hidden" value=0 id="numberofhubs" name="numberofhubs" autocomplete="off">
        <div id="hubcontainer">


        </div>
        <button type="button" class="medium green" id="addhubbutton" onclick="addhub()"><i class="fa fa-plus"></i> Add Hub</button>
 		<button type="button" class="medium" id="removehubbutton" disabled="disabled" onclick="removehub()"><i class="fa fa-minus"></i> Remove Hub</button>

        <!-- Spokes -->
        <h4 style="color:#999;margin-bottom:5px;" class="left">Spokes</h4>
                <input type="hidden" value=0 id="numberofspokes" name="numberofspokes" autocomplete="off">
        <div id="spokecontainer">


        </div>
        <button type="button" class="medium green" id="addspokebutton" onclick="addspoke()"><i class="fa fa-plus"></i> Add spoke</button>
 		<button type="button" class="medium" id="removespokebutton" disabled="disabled" onclick="removespoke()"><i class="fa fa-minus"></i> Remove spoke</button>

		<!-- Export -->
        <h4 style="color:#999;margin-bottom:5px;" class="left">Submit</h4>
        <button type="submit" class="medium green"><i class="fa fa-save"></i> Submit</button>

    </div>
</div> <!-- End Grid -->
</form>
</body>
</html>
""")
