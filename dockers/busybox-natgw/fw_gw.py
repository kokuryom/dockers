#! /usr/bin/python


class Configuration:
    base = {
        'outnet_name': 'outnet',
        'outnet_ip': '10.30.0.2',
        'if_out': 'eth2',
        'dns1': '8.8.8.8',
        'dns2': '8.8.4.4',
        'adminnet': '10.30.0.0/24'
    }

    dstnets = [
        {
            'dstnet_name': 'net_v1000',
            'dstnet_ip_range': '172.16.100.0/24',
            'if_in': 'eth0',
            'allow_tcp': '22,80,443',
            'allow_udp': '53,123',
            'allow_ping': True
        },
        {
            'dstnet_name': 'net_v1001',
            'dstnet_ip_range': '172.16.101.0/24',
            'if_in': 'eth1',
            'allow_tcp': '22,80,443',
            'allow_udp': '53,123',
            'allow_ping': True
        },
    ]


class Firewall:
    def __init__(self):
        pass

    def prerule(self):
        pre = [{'Title': ['Flush & Reset'], 'Rules': ['-F', '-t nat -F', '-X']},
               {'Title': ['loopback'], 'Rules': ['-A INPUT -i lo -j ACCEPT',
                                                 '-A OUTPUT -o lo -j ACCEPT']},
               {'Title': ['Default Rule'], 'Rules': ['-P INPUT DROP',
                                                     '-P OUTPUT DROP', '-P FORWARD DROP']}]

        return pre

    def postrule(self, ifout):
        post = [
            {
                'Title': ['Post Rules', 'Outgoing packet should be real internet Address'],
                'Rules': [
                    '-A OUTPUT -o %s -d 10.0.0.0/8 -j DROP' % ifout,
                    '-A OUTPUT -o %s -d 172.16.0.0/12 -j DROP' % ifout,
                    '-A OUTPUT -o %s -d 192.168.0.0/16 -j DROP' % ifout,
                    '-A OUTPUT -o %s -d 127.0.0.0/8 -j DROP' % ifout
                ]
            },
            {
                'Title': ['Post Rules', 'logging'],
                'Rules': [
                    '-N LOGGING',
                    '-A LOGGING -j LOG --log-level warning --log-prefix "DROP:" -m limit',
                    '-A LOGGING -j DROP', '-A INPUT -j LOGGING',
                    '-A OUTPUT -j LOGGING', '-A FORWARD -j LOGGING'
                ]
            }
        ]

        return post

    def adminrule(self, base):
        net = base['adminnet']
        ifout = base['if_out']
        outnetip = base['outnet_ip']
        dns1 = base['dns1']
        dns2 = base['dns2']

        new_est_rel = '-m state --state NEW,ESTABLISHED,RELATED '
        est_rel = '-m state --state ESTABLISHED,RELATED '

        allowsshto = [
            {
                'Title': ['For Administration', 'Allow ssh to adminnet'],
                'Rules': [
                    '-A OUTPUT -p tcp ' + new_est_rel + '-s %s --dport 22 -d %s -j ACCEPT' % (net, net),
                    '-A INPUT -p tcp ' + est_rel + '-s %s -d %s --sport 22 -j ACCEPT' % (net, net)
                ]
            }
        ]

        allowsshfrom = [
            {
                'Title': ['For Administration', 'Allow ssh from adminnet'],
                'Rules': [
                    '-A OUTPUT -p tcp ' + est_rel + '-s %s --sport 22 -d %s -j ACCEPT' % (net, net),
                    '-A INPUT -p tcp ' + new_est_rel + '-s %s -d %s --dport 22 -j ACCEPT' % (net, net)
                ]
            }
        ]

        allowhttp = [
            {
                'Title': ['For Administration', 'Allow http to update'],
                'Rules': [
                    '-A OUTPUT -o %s -p tcp ' % ifout + new_est_rel + '-d $any --dport 80 -s %s -j ACCEPT' % outnetip,
                    '-A INPUT -i %s -p tcp ' % ifout + est_rel + '-s $any --sport 80 -d %s -j ACCEPT' % outnetip
                ]
            },
            {
                'Title': ['For Administration', 'Allow dns'],
                'Rules': [
                     '-A INPUT -i %s -p udp -d %s -s %s --sport 53 -j ACCEPT' % (ifout, outnetip, dns1),
                     '-A OUTPUT -o %s -p udp -d %s --dport 53 -s %s -j ACCEPT' % (ifout, dns1, outnetip),
                     '-A INPUT -i %s -p udp -d %s -s %s --sport 53 -j ACCEPT' % (ifout, outnetip, dns2),
                     '-A OUTPUT -o %s -p udp -d %s --dport 53 -s %s -j ACCEPT' % (ifout, dns2, outnetip)
                ]
            }
        ]

        allowntp = [
            {
                'Title': ['For Administration', 'Allow ntp'],
                'Rules': [
                    '-A INPUT -p udp -s $any -d %s --dport 123 --sport 123 -j ACCEPT' % outnetip,
                    '-A OUTPUT -p udp -s %s --sport 123 --dport 123 -d $any -j ACCEPT' % outnetip
                ]
            }
        ]

        allowsflow = [
            {
                'Title': ['For admin sFlow', 'Allow sFlow to adminnet'],
                'Rules': [
                    '-A INPUT -p udp -s %s --sport 6343 -j ACCEPT' % net,
                    '-A OUTPUT -p udp -d %s --dport 6343 -j ACCEPT' % net
                ]
             }
        ]

        admin = []
        [admin.append(d) for d in allowsshto]
        [admin.append(d) for d in allowsshfrom]
        [admin.append(d) for d in allowhttp]
        [admin.append(d) for d in allowntp]
        [admin.append(d) for d in allowsflow]

        return admin

    def allowping(self, net):
        icmp = {
            'Title': ['Allow ICMP on %s' % net],
            'Rules': [
                '-A INPUT -p icmp -s $%s -j ACCEPT' % net,
                '-A OUTPUT -p icmp -d $%s -j ACCEPT' % net
            ]
        }
        return icmp

    def forwardrules(self, ifout, dstnet):
        ifin = dstnet['if_in']
        dstnet_name = dstnet['dstnet_name']
        allowtcp = dstnet['allow_tcp']
        allowudp = dstnet['allow_udp']

        # Forward Basic Rules
        tcp_forward_s = '-A FORWARD -p tcp -i %s -o %s ' % (ifout, ifin)
        udp_forward_s = '-A FORWARD -p udp -i %s -o %s ' % (ifout, ifin)
        tcp_forward_d = '-A FORWARD -p tcp -i %s -o %s ' % (ifin, ifout)
        udp_forward_d = '-A FORWARD -p udp -i %s -o %s ' % (ifin, ifout)

        allow_tcp_multi_sport = ' -d $%s -m multiport --sport %s -j ACCEPT' % (dstnet_name, allowtcp)
        allow_udp_multi_sport = ' -d $%s -m multiport --sport %s -j ACCEPT' % (dstnet_name, allowudp)
        allow_tcp_multi_dport = ' -s $%s -m multiport --dport %s -j ACCEPT' % (dstnet_name, allowtcp)
        allow_udp_multi_dport = ' -s $%s -m multiport --dport %s -j ACCEPT' % (dstnet_name, allowudp)
        allow_tcp_state = ' -m state --state ESTABLISHED,RELATED '

        node_rules = [
            {
                'Title': ['Forward Rule for %s' % dstnet_name, 'Source'],
                'Rules': [
                    tcp_forward_s + allow_tcp_state + allow_tcp_multi_sport,
                    udp_forward_s + allow_udp_multi_sport
                ]
            },
            {
                'Title': ['Destination'],
                'Rules': [
                    tcp_forward_d + allow_tcp_multi_dport,
                    udp_forward_d + allow_udp_multi_dport
                ]
            },
            # {
            #     'Title': ['Allow ntp for %s' % dstnet_name],
            #     'Rules': [
            #          '-A INPUT -p udp -s $%s -d $%s --dport 123 --sport 123 -j ACCEPT' % (dstnet_name, dstnet_name),
            #          '-A OUTPUT -p udp -s $%s -d $%s --dport 123 --sport 123 -j ACCEPT' % (dstnet_name, dstnet_name)
            #     ]
            # },
            {
                'Title': ['SNAT(masquerade)'],
                'Rules': ['-t nat -A POSTROUTING -o %s -s $%s -j MASQUERADE' % (ifout, dstnet_name)]
            }
        ]

        # Allow Ping
        if dstnet['allow_ping']:
            node_rules.append(self.allowping(dstnet_name))

        return node_rules

    def rule_tostr(self, lines):
        str = ''
        for line in lines:
            r = dict(line)
            # str += '#' * 60 + '\n'
            str += "".join(['#' + title + '\n' for title in r['Title']])
            # str += '#' * 60 + '\n'
            for rule in r['Rules']:
                str += 'iptables ' + rule + '\n'
            str += '\n'

        return str

    def buildrules(self, config):
        ifout = config.base['if_out']

        rule_str = "#! /bin/sh\nany='0.0.0.0/0'\necho 1 > /proc/sys/net/ipv4/ip_forward\n"
        rule_str += '\n'.join(["%s='%s'" % (dstnet['dstnet_name'], dstnet['dstnet_ip_range']) for dstnet in config.dstnets]) + '\n\n'
        rule_str += self.rule_tostr(self.prerule())
        rule_str += '\n'.join([self.rule_tostr(self.forwardrules(ifout, dstnet)) for dstnet in config.dstnets])
#        rule_str += self.rule_tostr(self.adminrule(config.base))
        rule_str += self.rule_tostr(self.postrule(ifout))

        return rule_str


if __name__ == "__main__":
    import subprocess

    c = Configuration()
    f = Firewall()

    rule_file_path = './rule_fw.sh'
    fw_file = open(rule_file_path, 'w')
    fw_file.write(f.buildrules(c))
    fw_file.flush()
    fw_file.close()

    p = subprocess.Popen(['chmod', '+x', rule_file_path],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=False)
    print 'writing rules to ' + rule_file_path
    print 'return: %d' % (p.wait(),)
    print 'stdout: %s' % (p.stdout.readlines(),)
    print 'stderr: %s' % (p.stderr.readlines(),)

    p = subprocess.Popen([rule_file_path],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=False)
    print 'running ' + rule_file_path
    print 'return: %d' % (p.wait(),)
    print 'stdout: %s' % (p.stdout.readlines(),)
    print 'stderr: %s' % (p.stderr.readlines(),)

