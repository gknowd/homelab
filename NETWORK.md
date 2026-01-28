# Homelab Network Architecture Guide

## Overview

This document outlines the network architecture, security practices, and configuration guidelines for a segmented homelab environment designed to support:
- Secure work-from-home operations for multiple users
- IoT device isolation
- Guest network access
- Home entertainment and personal devices
- Self-hosted services and infrastructure

## Network Architecture

### Equipment Stack
- **UDM Pro SE** - Primary router, firewall, and network controller
- **Ubiquiti Switches** - Layer 2/3 switching and VLAN distribution
- **Ubiquiti WiFi Access Points** - Wireless coverage with VLAN support
- **UniFi Cameras & NVR** - Video surveillance system
- **UniFi NAS** - Network-attached storage
- **Cable Modem** - ISP connection

### Network Segmentation Strategy

The network is divided into isolated VLANs with specific firewall rules controlling inter-VLAN communication:

| VLAN ID | Network Name | Subnet | Purpose | Devices |
|---------|--------------|--------|---------|---------|
| 1 | Management | 192.168.1.0/24 | Network infrastructure management | UDM Pro, switches, APs, NVR |
| 10 | Work | 192.168.10.0/24 | Secure work environment | Work laptops, desktops, VPN clients |
| 20 | Home | 192.168.20.0/24 | Personal trusted devices | Apple TV, Sonos, personal devices |
| 30 | IoT | 192.168.30.0/24 | Internet of Things devices | Smart home devices, sensors |
| 40 | Guest | 192.168.40.0/24 | Guest user access | Visitor devices |
| 50 | Servers | 192.168.50.0/24 | Self-hosted services | Docker hosts, VMs, homelab servers |
| 60 | Cameras | 192.168.60.0/24 | Surveillance devices | UniFi cameras, NVR |
| 70 | Storage | 192.168.70.0/24 | Network storage | NAS, backup devices |

## VLAN Design & Purpose

### VLAN 1 - Management Network
**Purpose**: Infrastructure management and administration

**Characteristics**:
- Highest security level
- Access restricted to admin devices only
- No internet access for management interfaces (optional)
- SSH/HTTPS management ports only

**Devices**:
- UDM Pro SE management interface
- Switch management interfaces
- Access Point management interfaces
- NVR management interface

**Security Considerations**:
- Enable management VLAN isolation
- Use strong passwords and SSH keys
- Consider management access only from Work VLAN
- Enable audit logging for all management access

### VLAN 10 - Work Network
**Purpose**: Secure environment for work-from-home operations

**Characteristics**:
- High security with strict firewall rules
- Full internet access
- Access to necessary server resources
- Isolated from IoT and Guest networks
- Can access Storage VLAN (with restrictions)

**Devices**:
- Work laptops and desktops
- Work phones
- VPN concentrators
- Development machines

**Security Considerations**:
- Enable IDS/IPS on this VLAN
- Consider DPI (Deep Packet Inspection)
- VPN access for remote work resources
- No inbound connections from other VLANs except Servers (selective)
- Strong WiFi password (WPA3 if possible)
- Consider 802.1X authentication for WiFi

**Firewall Rules**:
- ✅ Allow: Internet (all protocols)
- ✅ Allow: DNS, DHCP
- ✅ Allow: Specific services on Servers VLAN (HTTP/HTTPS, SSH with restrictions)
- ✅ Allow: Storage VLAN (SMB/NFS with restrictions)
- ❌ Block: IoT VLAN
- ❌ Block: Guest VLAN
- ❌ Block: Cameras VLAN
- ❌ Block: Management VLAN (except from admin devices)

### VLAN 20 - Home Network
**Purpose**: Personal trusted devices and entertainment systems

**Characteristics**:
- Medium-high security
- Full internet access
- Local discovery enabled (AirPlay, Chromecast, Sonos)
- Access to media servers

**Devices**:
- Apple TVs
- Smart TVs
- Sonos speakers
- Gaming consoles
- Personal phones and tablets
- Streaming devices

**Security Considerations**:
- Moderate security posture
- mDNS/Bonjour reflector enabled for cross-VLAN discovery
- IGMP snooping for multicast traffic
- Regular firmware updates

**Firewall Rules**:
- ✅ Allow: Internet (all protocols)
- ✅ Allow: DNS, DHCP
- ✅ Allow: mDNS (for device discovery)
- ✅ Allow: Media servers on Servers VLAN
- ✅ Allow: Limited IoT control (smart home hubs only)
- ❌ Block: Work VLAN
- ❌ Block: Guest VLAN
- ❌ Block: Management VLAN

### VLAN 30 - IoT Network
**Purpose**: Isolated network for Internet of Things devices

**Characteristics**:
- Low trust level
- Internet access restricted (outbound only)
- No access to other VLANs (except controlled access from Home)
- Heavy monitoring and logging

**Devices**:
- Smart switches and plugs
- Smart thermostats
- IoT sensors
- Smart appliances
- Robot vacuums
- Smart locks

**Security Considerations**:
- **Strict internet filtering** - block known malicious domains
- **No inbound connections** from internet
- **Outbound firewall rules** - only allow necessary protocols (HTTPS, MQTT, etc.)
- **MAC address whitelist** recommended
- **Regular vulnerability scanning**
- **Disable UPnP** on this network
- **Consider per-device VLANs** for high-risk devices

**Firewall Rules**:
- ✅ Allow: Internet (HTTPS, DNS only - whitelist approach)
- ✅ Allow: DNS, DHCP
- ✅ Allow: MQTT to Servers VLAN (if running home automation hub)
- ❌ Block: All other VLANs
- ❌ Block: Inbound internet connections
- ℹ️ Exception: Home VLAN can initiate connections to IoT (for control apps)

### VLAN 40 - Guest Network
**Purpose**: Isolated network for visitor devices

**Characteristics**:
- Lowest trust level
- Internet access only
- Completely isolated from all other VLANs
- Bandwidth throttling (optional)
- Client isolation enabled

**Devices**:
- Guest smartphones
- Guest laptops
- Visitor tablets

**Security Considerations**:
- **Client isolation** - guests can't see each other
- **Captive portal** (optional) with terms of service
- **Time-based access** limits (optional)
- **Bandwidth limits** to prevent network saturation
- **DNS filtering** for malware/phishing protection
- **No local network access** whatsoever

**Firewall Rules**:
- ✅ Allow: Internet (HTTP/HTTPS only)
- ✅ Allow: DNS, DHCP
- ❌ Block: ALL VLANs
- ❌ Block: RFC1918 private addresses

### VLAN 50 - Servers Network
**Purpose**: Self-hosted services and infrastructure

**Characteristics**:
- Medium-high security
- Hosts critical homelab services
- Accessible from Work and Home networks (selective)
- May host reverse proxy for external access

**Devices**:
- Docker hosts
- Virtual machines
- Proxmox hosts
- n8n automation server
- Grafana, Loki, Prometheus
- Database servers

**Security Considerations**:
- **Reverse proxy** (Traefik) for external service access
- **Strong authentication** on all services
- **Regular security updates**
- **Backup and disaster recovery** plans
- **Network monitoring** and intrusion detection
- **Container isolation** with proper security contexts

**Firewall Rules**:
- ✅ Allow: Internet (for updates and external integrations)
- ✅ Allow: DNS, DHCP
- ✅ Allow: Inbound from Work VLAN (SSH, HTTPS, specific services)
- ✅ Allow: Inbound from Home VLAN (HTTPS to web services)
- ✅ Allow: Storage VLAN access
- ✅ Allow: Cameras VLAN (for video processing/AI)
- ✅ Allow: IoT VLAN (inbound MQTT from smart devices)
- ❌ Block: Guest VLAN
- ℹ️ Conditional: Management VLAN for monitoring agents

### VLAN 60 - Cameras Network
**Purpose**: Video surveillance and security cameras

**Characteristics**:
- High isolation
- No internet access (recommended)
- Only accessible from NVR and specific admin devices
- High bandwidth for video streams

**Devices**:
- UniFi Protect cameras
- NVR (Network Video Recorder)

**Security Considerations**:
- **No internet access** - prevents camera compromises from reaching internet
- **Isolated from all networks** except NVR and viewing devices
- **VLAN tagging** on camera ports
- **PoE security** - physical port access control
- **Firmware updates** through local NVR only

**Firewall Rules**:
- ✅ Allow: NVR communication
- ✅ Allow: DNS, DHCP
- ✅ Allow: Servers VLAN (if running UniFi Protect on server)
- ℹ️ Allow: Work/Home VLAN to NVR for camera viewing
- ❌ Block: Internet (optional - allow for cloud features)
- ❌ Block: All other VLANs

### VLAN 70 - Storage Network
**Purpose**: Network-attached storage and backups

**Characteristics**:
- High performance (consider 10GbE)
- Accessible from Work and Servers networks
- Backup isolation

**Devices**:
- UniFi NAS
- Backup appliances
- iSCSI targets

**Security Considerations**:
- **Access control** via SMB/NFS permissions
- **Encryption** for sensitive data at rest
- **Backup segregation** - immutable backups
- **Snapshot policies**
- **No direct internet access**

**Firewall Rules**:
- ✅ Allow: Work VLAN (SMB/NFS)
- ✅ Allow: Servers VLAN (backup, storage)
- ✅ Allow: Home VLAN (media libraries, personal files)
- ✅ Allow: DNS, DHCP
- ❌ Block: Internet
- ❌ Block: IoT, Guest, Cameras

## Security Best Practices

### 1. Firewall Configuration

#### Default Deny Policy
- Implement default deny on all inter-VLAN traffic
- Explicitly allow only required connections
- Log denied connections for analysis

#### Geo-IP Blocking
- Block countries you don't do business with
- Particularly important for management interfaces

#### Rate Limiting
- Implement rate limiting on internet-facing services
- Protect against brute force attacks

### 2. WiFi Security

#### Network-Specific SSIDs
- **Work-5G** / **Work-2.4G** - Work VLAN 10
- **Home** - Home VLAN 20
- **IoT-Devices** - IoT VLAN 30 (hidden SSID recommended)
- **Guest** - Guest VLAN 40

#### WiFi Security Settings
- **WPA3** on Work and Home networks (if all devices support it)
- **WPA2-PSK** fallback for compatibility
- **Strong passwords** (20+ characters, random)
- **Disable WPS** on all networks
- **Hide SSID** for IoT network
- **Guest isolation** enabled on Guest network
- **Minimum RSSI** to disconnect weak clients
- **Fast roaming** (802.11r) for seamless handoff

### 3. DNS & DHCP Security

#### DNS Configuration
- **Primary DNS**: UDM Pro (local resolver)
- **Upstream DNS**: Cloudflare (1.1.1.1), Google (8.8.8.8), or NextDNS
- **DNS filtering**: Enable on IoT and Guest networks
- **DNSSEC**: Enable validation
- **Split DNS**: Internal domain resolution for homelab services

#### DHCP Settings
- **Dedicated DHCP scope** per VLAN
- **Static reservations** for servers and infrastructure
- **Lease times**:
  - Servers/Infrastructure: Static
  - Work: 24 hours
  - Home: 12 hours
  - IoT: 7 days (stable IPs help with rules)
  - Guest: 1 hour

### 4. Intrusion Detection & Prevention

#### Enable IDS/IPS
- **Enable on WAN** interface for external threat detection
- **Enable on Work VLAN** for additional protection
- **Enable on IoT VLAN** to detect compromised devices
- **Tune alerts** to reduce false positives

#### Traffic Analysis
- Enable DPI (Deep Packet Inspection) on sensitive VLANs
- Monitor for unusual patterns
- Set up alerts for suspicious activity

### 5. Access Control

#### Admin Access
- **Dedicated admin account** separate from personal accounts
- **Strong passwords** with password manager
- **2FA/MFA** on UDM Pro and critical services
- **SSH keys** instead of passwords where possible
- **Audit logging** enabled on all infrastructure

#### Remote Access
- **No port forwarding** for management interfaces
- **VPN only** for remote administration (WireGuard or IPSec)
- **Fail2ban** or equivalent for VPN/SSH brute force protection
- **VPN split tunneling** vs full tunnel based on use case

### 6. Monitoring & Logging

#### What to Monitor
- **Firewall logs** - blocked connections, patterns
- **DHCP logs** - new devices, IP changes
- **Authentication logs** - failed logins, successful admin access
- **Bandwidth usage** - per VLAN and per device
- **Uptime and performance** - infrastructure health

#### Log Management
- Send logs to Loki/Grafana stack
- Set up Promtail on UDM Pro for log forwarding
- Create dashboards for network visibility
- Configure alerts for critical events

#### Key Metrics
- Internet bandwidth usage
- Per-VLAN traffic patterns
- Failed authentication attempts
- IDS/IPS alerts
- Device connectivity status

### 7. Physical Security

- **Lock network closet/rack** - physical access = full compromise
- **Disable unused switch ports**
- **PoE port security** - prevent unauthorized device connection
- **Cable management** - prevents accidental disconnection
- **Environmental monitoring** - temperature, humidity

## Configuration Guidelines

### UDM Pro SE Configuration

#### Initial Setup Checklist
- [ ] Change default admin password
- [ ] Enable 2FA on admin account
- [ ] Configure time zone and NTP
- [ ] Set up VLANs and networks
- [ ] Configure WiFi SSIDs with VLAN mapping
- [ ] Set up firewall rules (default deny)
- [ ] Enable IDS/IPS
- [ ] Configure DPI
- [ ] Set up remote logging (to Loki)
- [ ] Enable geo-IP blocking
- [ ] Configure DHCP scopes
- [ ] Set up DNS resolver
- [ ] Create network backups

#### UniFi Controller Settings
- **Auto-backup**: Daily backups to Storage VLAN
- **Firmware updates**: Manual or scheduled maintenance windows
- **Guest portal**: Configure if using Guest network captive portal
- **Traffic rules**: QoS for VoIP, video conferencing
- **Device adoption**: Secure with strong adoption password

### Switch Configuration

#### Port Profiles
Create port profiles for easy configuration:

- **Management Profile**: VLAN 1, management devices only
- **Work Profile**: VLAN 10, work devices
- **Home Profile**: VLAN 20, personal devices
- **IoT Profile**: VLAN 30, IoT devices
- **Guest Profile**: VLAN 40, guest devices
- **Server Profile**: VLAN 50, server infrastructure
- **Camera Profile**: VLAN 60 with PoE, cameras only
- **Storage Profile**: VLAN 70, storage devices
- **Trunk Profile**: All VLANs, for inter-switch links and APs

#### Switch Hardening
- Disable unused ports
- Enable DHCP snooping
- Configure storm control
- Enable PoE scheduling (optional power savings)
- Set up link aggregation for high-bandwidth devices

### Access Point Configuration

#### WiFi Network Configuration
```
SSID: Work-5G
- Security: WPA3 or WPA2
- VLAN: 10
- Band: 5GHz only
- Hidden: No
- Guest policy: Disabled

SSID: Work-2.4G
- Security: WPA3 or WPA2
- VLAN: 10
- Band: 2.4GHz only
- Hidden: No
- Guest policy: Disabled

SSID: Home
- Security: WPA2
- VLAN: 20
- Band: Both
- Hidden: No
- Guest policy: Disabled

SSID: IoT-Devices
- Security: WPA2
- VLAN: 30
- Band: 2.4GHz (most IoT devices only support this)
- Hidden: Yes (recommended)
- Guest policy: Disabled

SSID: Guest
- Security: WPA2 with simple password
- VLAN: 40
- Band: Both
- Hidden: No
- Guest policy: Enabled with client isolation
```

#### AP Optimization
- **Channel width**: 20MHz on 2.4GHz, 40-80MHz on 5GHz
- **Transmit power**: Auto or medium (prevents sticky clients)
- **Minimum RSSI**: -75 dBm to encourage roaming
- **Fast roaming**: Enable 802.11r
- **Band steering**: Enable to prefer 5GHz
- **Airtime fairness**: Enable

### Firewall Rule Examples

#### Work VLAN → Internet (Allow)
```
Source: Work VLAN (192.168.10.0/24)
Destination: Internet (any)
Action: Accept
Protocol: All
```

#### Work VLAN → IoT VLAN (Deny)
```
Source: Work VLAN (192.168.10.0/24)
Destination: IoT VLAN (192.168.30.0/24)
Action: Drop
Protocol: All
Logging: Enabled
```

#### Home VLAN → IoT Control (Allow Specific)
```
Source: Home VLAN (192.168.20.0/24)
Destination: IoT VLAN (192.168.30.0/24)
Action: Accept
Protocol: TCP
Port: 80, 443 (HTTP/HTTPS for device control)
State: New, Established
```

#### Guest VLAN → RFC1918 (Block Private Networks)
```
Source: Guest VLAN (192.168.40.0/24)
Destination: 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12
Action: Drop
Protocol: All
Logging: Enabled
```

#### Servers VLAN → Storage VLAN (Allow)
```
Source: Servers VLAN (192.168.50.0/24)
Destination: Storage VLAN (192.168.70.0/24)
Action: Accept
Protocol: TCP/UDP
Port: 445 (SMB), 2049 (NFS), 111 (RPC), 3260 (iSCSI)
State: New, Established
```

## Advanced Features

### mDNS Reflector / Bonjour
- Enable mDNS reflection between Home and IoT VLANs for smart home control
- Use UniFi's mDNS feature for AirPlay, Chromecast, HomeKit across VLANs
- Restrict to specific services and VLANs only

### IGMP Snooping
- Enable on switches for multicast traffic optimization
- Important for streaming video and Sonos
- Configure IGMP querier on UDM Pro

### VLANs for Cameras with UniFi Protect
- Cameras on VLAN 60 can still be adopted by UniFi Protect
- Ensure NVR can reach camera VLAN
- Consider dedicated 802.3af/at PoE switches for cameras

### VPN Configuration

#### WireGuard (Recommended)
- Fast, modern VPN protocol
- Mobile app support
- Split tunnel by default (access only homelab)

#### Configuration
- VPN subnet: 192.168.100.0/24 (separate from all VLANs)
- Route to necessary VLANs (Work, Servers, Storage)
- Block access to IoT and Guest from VPN

### Traffic Shaping / QoS

#### Priority Levels
1. **High**: VoIP, video conferencing (Work VLAN)
2. **Medium-High**: Business applications, RDP/SSH
3. **Medium**: Web browsing, email
4. **Medium-Low**: Media streaming
5. **Low**: Downloads, backups
6. **Lowest**: Guest network traffic

## Maintenance & Updates

### Regular Tasks

#### Daily
- [ ] Review IDS/IPS alerts
- [ ] Check Grafana dashboards for anomalies

#### Weekly
- [ ] Review firewall logs
- [ ] Check for new devices on network
- [ ] Verify backup status

#### Monthly
- [ ] Check for firmware updates (UDM, switches, APs)
- [ ] Review and update firewall rules
- [ ] Audit user accounts and access
- [ ] Test VPN connectivity
- [ ] Verify monitoring/alerting is working

#### Quarterly
- [ ] Full network security audit
- [ ] Password rotation for service accounts
- [ ] Review and update documentation
- [ ] Test disaster recovery procedures
- [ ] Vulnerability scanning

#### Annually
- [ ] Major firmware upgrades
- [ ] Network design review
- [ ] Equipment lifecycle planning

### Firmware Updates

#### Strategy
- **Read release notes** before updating
- **Test on non-critical devices** first
- **Schedule maintenance windows** for updates
- **Keep previous firmware** for rollback capability
- **Update in order**: UDM Pro → Switches → APs

#### Rollback Plan
- Always have console access to UDM Pro
- Know how to roll back firmware
- Have network diagram accessible offline
- Keep backup configuration files

## Troubleshooting Guide

### Common Issues

#### Devices Can't Communicate Between VLANs
- Check firewall rules (default deny catches many)
- Verify VLAN tagging on switch ports
- Confirm device is on expected VLAN (check DHCP lease)

#### WiFi Performance Issues
- Check channel congestion with WiFi scanner
- Adjust transmit power
- Verify AP placement and coverage
- Check for interference sources

#### Smart Home Devices Not Working
- Ensure mDNS reflector is enabled
- Check if control app is on correct VLAN (should be Home)
- Verify firewall allows Home → IoT communication

#### VPN Not Connecting
- Check firewall rules allow VPN ports
- Verify port forwarding if behind another router
- Check certificate/key validity
- Test from different network to isolate issue

### Debug Commands

#### UniFi OS (UDM Pro SE)
```bash
# View current connections
netstat -an

# Check firewall rules
iptables -L -v -n

# View routing table
ip route show

# Check VLAN configuration
ip link show

# DNS queries
nslookup domain.com

# Trace route
traceroute 8.8.8.8

# View DHCP leases
cat /var/lib/unifi/dhcpd.leases
```

## Network Diagram

```
                                    Internet (ISP)
                                          |
                                    Cable Modem
                                          |
                        ┌─────────────────┴─────────────────┐
                        |                                   |
                   WAN Port                            UDM Pro SE
                        |           (Router/Firewall/Controller)
                        |                                   |
                        └─────────────────┬─────────────────┘
                                          |
                    ┌─────────────────────┼─────────────────────┐
                    |                     |                     |
            Aggregation Switch      10GbE Trunk          PoE Switches
                    |                     |                     |
            ┌───────┼───────┐        ┌────┴────┐           ┌───┴────┐
            |       |       |        |         |           |        |
         Servers  Storage  NAS    WiFi APs  Cameras    IoT Devices

         VLAN Distribution:
         ├── VLAN 1  (Management)
         ├── VLAN 10 (Work)
         ├── VLAN 20 (Home)
         ├── VLAN 30 (IoT)
         ├── VLAN 40 (Guest)
         ├── VLAN 50 (Servers)
         ├── VLAN 60 (Cameras)
         └── VLAN 70 (Storage)
```

## Future Improvements

### Short-term (0-3 months)
- [ ] Implement comprehensive firewall rules
- [ ] Set up network monitoring in Grafana
- [ ] Configure VPN for remote access
- [ ] Enable IDS/IPS with tuned rules
- [ ] Document all static IP assignments

### Medium-term (3-6 months)
- [ ] Implement 802.1X authentication for Work VLAN
- [ ] Set up Pi-hole or AdGuard for DNS filtering
- [ ] Create network documentation with actual IPs and devices
- [ ] Implement automated configuration backups
- [ ] Set up WireGuard VPN for family members

### Long-term (6-12 months)
- [ ] Upgrade to 10GbE for server-storage links
- [ ] Implement Zero Trust security model
- [ ] Advanced threat detection with Suricata
- [ ] Network access control (NAC) for device registration
- [ ] Automated security scanning and vulnerability assessment

## Additional Resources

### Documentation
- [UniFi UDM Pro SE Manual](https://help.ui.com/hc/en-us/categories/200320654-UniFi)
- [UniFi Best Practices](https://help.ui.com/hc/en-us/articles/115000166827-UniFi-Best-Practices)
- [VLAN Hopper Network Segmentation Guide](https://www.vlanhopper.com/)

### Tools
- **WiFi Analyzer** - Mobile app for WiFi survey
- **Angry IP Scanner** - Network device discovery
- **Wireshark** - Packet capture and analysis
- **iperf3** - Network performance testing

### Ubiquiti Community
- [r/Ubiquiti](https://www.reddit.com/r/Ubiquiti/) - Reddit community
- [Ubiquiti Community Forums](https://community.ui.com/) - Official forums
- [Crosstalk Solutions](https://www.youtube.com/c/CrosstalkSolutions) - YouTube tutorials

## Notes

- This is a living document. Update as network evolves.
- Configuration examples are guidelines - adapt to your specific needs.
- Security is a process, not a destination. Regular reviews are essential.
- When in doubt, default deny and explicitly allow what's needed.

---

**Last Updated**: 2025-10-31
**Network Version**: 1.0
**Next Review**: TBD
