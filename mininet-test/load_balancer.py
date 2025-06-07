from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, tcp
from ryu.lib.packet import arp
import random

class SimpleLoadBalancer(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleLoadBalancer, self).__init__(*args, **kwargs)
        self.server_ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
        self.client_ip = "10.0.0.100"
        self.virtual_ip = "10.0.0.10"
        self.mac_table = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Chặn tất cả trước khi thiết lập luật
        match = parser.OFPMatch()
        actions = []
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        ip = pkt.get_protocol(ipv4.ipv4)
        tcp_pkt = pkt.get_protocol(tcp.tcp)

        if eth.ethertype == 0x0806:  # Nếu là gói ARP
            arp_pkt = pkt.get_protocol(arp.arp)
            if arp_pkt and arp_pkt.opcode == arp.ARP_REQUEST and arp_pkt.dst_ip == self.virtual_ip:
                # Tạo ARP reply
                arp_reply = packet.Packet()
                arp_reply.add_protocol(ethernet.ethernet(
                    ethertype=0x0806, dst=eth.src, src="aa:bb:cc:dd:ee:ff"))  # MAC ảo cho VIP
                arp_reply.add_protocol(arp.arp(
                    opcode=arp.ARP_REPLY, src_mac="aa:bb:cc:dd:ee:ff",
                    src_ip=self.virtual_ip, dst_mac=arp_pkt.src_mac, dst_ip=arp_pkt.src_ip))
                arp_reply.serialize()

                actions = [parser.OFPActionOutput(msg.in_port)]
                out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER,
                                            in_port=ofproto.OFPP_CONTROLLER, actions=actions, data=arp_reply.data)
                datapath.send_msg(out)

        if not ip or not tcp_pkt:
            return

        if ip.dst == self.virtual_ip:
            selected_server = random.choice(self.server_ips)
            match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=self.virtual_ip)
            actions = [parser.OFPActionSetField(ipv4_dst=selected_server),
                       parser.OFPActionOutput(ofproto.OFPP_NORMAL)]
            self.add_flow(datapath, 10, match, actions)
