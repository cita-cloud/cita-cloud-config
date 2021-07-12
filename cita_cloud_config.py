#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# pylint: disable=missing-docstring

import argparse
import os
import sys
import toml
import subprocess
import time
import copy
import xml.etree.ElementTree as ET
import hashlib
from pysmx.SM2 import generate_keypair
from pysmx.SM3 import hash_msg
import shutil

DEFAULT_PREVHASH = '0x{:064x}'.format(0)

DEFAULT_BLOCK_INTERVAL = 3

SYNC_FOLDERS = [
    'blocks',
    'proposals',
    'txs'
]

SERVICE_LIST = [
    'network',
    'consensus',
    'executor',
    'storage',
    'controller',
    'kms',
]


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--timestamp',
        type=int,
        help='Timestamp of genesis block.')

    parser.add_argument(
        '--block_delay_number',
        type=int,
        default=0,
        help='The block delay number of chain.')

    parser.add_argument(
        '--chain_name', default='test-chain', help='The name of chain.')

    parser.add_argument(
        '--peers_count',
        type=int,
        default=2,
        help='Count of peers.')

    parser.add_argument(
        '--kms_password', help='Password of kms.')

    parser.add_argument(
        '--enable_tls',
        action='store_true',
        help='Is enable tls')

    parser.add_argument(
        '--is_stdout',
        action='store_true',
        help='Is output to stdout')

    parser.add_argument(
        '--log_level',
        default="info",
        help='log level: warn/info/debug/trace')

    parser.add_argument(
        '--is_bft',
        action='store_true',
        help='Is bft')

    parser.add_argument(
        '--is_local',
        action='store_true',
        help='Is running in local')

    args = parser.parse_args()
    return args


# pod name is {chain_name}-{index}
def get_node_pod_name(index, chain_name):
    return '{}-{}'.format(chain_name, index)


def get_headless_svc_name(chain_name):
    return '{}-headless-service'.format(chain_name)


def get_node_network_name(index, chain_name):
    return '{}.{}'.format(get_node_pod_name(index, chain_name), get_headless_svc_name(chain_name))


# generate peers info by pod name
def gen_peers(count, chain_name, is_local):
    peers = []
    for i in range(count):
        if not is_local:
            peer = {
                'ip': get_node_network_name(i, chain_name),
                'port': 40000
            }
        else:
            peer = {
                'ip': "127.0.0.1",
                'port': 40000 + i
            }
        peers.append(peer)
    return peers


def gen_net_config_list(peers, enable_tls, is_local):
    net_config_list = []
    for index, peer in enumerate(peers):
        peers_clone = copy.deepcopy(peers)
        peers_clone.remove(peer)
        if not is_local:
            net_config = {
                'enable_tls': enable_tls,
                'port': 40000,
                'peers': peers_clone
            }
        else:
            net_config = {
                'enable_tls': enable_tls,
                'port': 40000 + index,
                'peers': peers_clone
            }
        net_config_list.append(net_config)
    return net_config_list


def gen_network_key(node_path):
    network_key = '0x' + os.urandom(32).hex()
    path = os.path.join(node_path, 'network_key')
    with open(path, 'wt') as stream:
        stream.write(network_key)


def need_directory(path):
    """Create a directory if it is not existed."""
    if not os.path.exists(path):
        os.makedirs(path)


def gen_chainid(chain_name):
    return '0x'+hashlib.sha256(chain_name.encode()).hexdigest()


LOG_CONFIG_TEMPLATE = '''# Scan this file for changes every 30 seconds
refresh_rate: 30 seconds

appenders:
  # An appender named \"stdout\" that writes to stdout
  stdout:
    kind: console

  journey-service:
    kind: rolling_file
    path: \"logs/{0}-service.log\"
    policy:
      # Identifies which policy is to be used. If no kind is specified, it will
      # default to \"compound\".
      kind: compound
      # The remainder of the configuration is passed along to the policy's
      # deserializer, and will vary based on the kind of policy.
      trigger:
        kind: size
        limit: 50mb
      roller:
        kind: fixed_window
        base: 1
        count: 5
        pattern: \"logs/{0}-service.{{}}.gz\"

# Set the default logging level and attach the default appender to the root
root:
  level: {1}
  appenders:
    - {2}
'''


def gen_log4rs_config(node_path, log_level, is_stdout):
    if is_stdout:
        appender = "stdout"
    else:
        appender = "journey-service"
    for service_name in SERVICE_LIST:
        path = os.path.join(node_path, '{}-log4rs.yaml'.format(service_name))
        with open(path, 'wt') as stream:
            stream.write(LOG_CONFIG_TEMPLATE.format(service_name, log_level, appender))


CONSENSUS_CONFIG_TEMPLATE = '''network_port = {}
controller_port = {}
node_id = {}
'''


# generate consensus-config.toml
def gen_consensus_config(node_path, i, num):
    path = os.path.join(node_path, 'consensus-config.toml')
    with open(path, 'wt') as stream:
        stream.write(CONSENSUS_CONFIG_TEMPLATE.format(
            num,
            num + 4,
            i))


CONTROLLER_CONFIG_TEMPLATE = '''network_port = {}
consensus_port = {}
storage_port = {}
kms_port = {}
executor_port = {}
block_delay_number = {}
'''


# generate controller-config.toml
def gen_controller_config(node_path, block_delay_number, num):
    path = os.path.join(node_path, 'controller-config.toml')
    with open(path, 'wt') as stream:
        stream.write(CONTROLLER_CONFIG_TEMPLATE.format(
            num,
            num + 1,
            num + 3,
            num + 5,
            num + 2,
            block_delay_number))


GENESIS_TEMPLATE = '''timestamp = {}
prevhash = \"{}\"
'''


def gen_genesis(node_path, timestamp, prevhash):
    path = os.path.join(node_path, 'genesis.toml')
    with open(path, 'wt') as stream:
        stream.write(GENESIS_TEMPLATE.format(timestamp, prevhash))


def gen_kms_account(work_dir):
    cmd = 'kms create -k key_file'
    kms_create = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = kms_create.stdout.readlines()[-1].decode().strip()
    print("kms create output:", output)
    # output should looks like: key_id:1,address:0xba21324990a2feb0a0b6ca16b444b5585b841df9
    infos = output.split(',')
    key_id = infos[0].split(':')[1]
    address = infos[1].split(':')[1]

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    current_dir = os.path.abspath(os.curdir)
    shutil.move(os.path.join(current_dir, 'kms.db'), os.path.join(work_dir, 'kms.db'))
    shutil.move(os.path.join(current_dir, 'key_file'), os.path.join(work_dir, 'key_file'))

    path = os.path.join(work_dir, 'key_id')
    with open(path, 'wt') as stream:
        stream.write(key_id)

    path = os.path.join(work_dir, 'node_address')
    with open(path, 'wt') as stream:
        stream.write(address)

    return address


def gen_super_admin(work_dir, kms_password):
    current_dir = os.path.abspath(os.curdir)
    path = os.path.join(current_dir, 'key_file')
    with open(path, 'wt') as stream:
        stream.write(kms_password)
    super_admin = gen_kms_account(work_dir)
    return super_admin


def gen_sm2_authorities(work_dir, chain_name, peers_count):
    authorities = []
    for i in range(peers_count):
        node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(i, chain_name)))
        pk, sk = generate_keypair()
        addr = '0x'+hash_msg(pk)[24:]
        path = os.path.join(node_path, 'node_key')
        with open(path, 'wt') as stream:
            stream.write('0x'+sk.hex())
        path = os.path.join(node_path, 'node_address')
        with open(path, 'wt') as stream:
            stream.write(addr)
        path = os.path.join(node_path, 'key_id')
        with open(path, 'wt') as stream:
            stream.write(str(i))
        authorities.append(addr)
    return authorities


def gen_authorities(work_dir, chain_name, kms_password, peers_count):
    authorities = []
    for i in range(peers_count):
        current_dir = os.path.abspath(os.curdir)
        path = os.path.join(current_dir, 'key_file')
        with open(path, 'wt') as stream:
            stream.write(kms_password)

        node_dir = os.path.join(work_dir, '{}'.format(get_node_pod_name(i, chain_name)))

        address = gen_kms_account(node_dir)

        authorities.append(address)
    return authorities


INIT_SYSCONFIG_TEMPLATE = '''version = 0
chain_id = \"0x0000000000000000000000000000000000000000000000000000000000000001\"
admin = \"0x010928818c840630a60b4fda06848cac541599462f\"
block_interval = 3
validators = [\"0x010928818c840630a60b4fda06848cac541599462f\"]
'''


def gen_init_sysconfig(work_dir, chain_name, super_admin, authorities, peers_count):
    init_sys_config = toml.loads(INIT_SYSCONFIG_TEMPLATE)
    init_sys_config['block_interval'] = DEFAULT_BLOCK_INTERVAL
    init_sys_config['validators'] = authorities    
    init_sys_config['admin'] = super_admin
    init_sys_config['chain_id'] = gen_chainid(chain_name)

    # write init_sys_config.toml into peers
    for i in range(peers_count):
        node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(i, chain_name)))
        path = os.path.join(node_path, 'init_sys_config.toml')
        with open(path, 'wt') as stream:
            toml.dump(init_sys_config, stream)


def gen_sync_account(work_dir):
    sync_config_path = os.path.join(work_dir, 'sync_config')
    cmd = 'syncthing -generate={}'.format(sync_config_path)
    syncthing_gen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    mark_str = 'Device ID: '
    device_id_len = 63
    output = str(syncthing_gen.stdout.read())
    mark_index = output.index(mark_str)
    device_id = output[mark_index + len(mark_str):mark_index + len(mark_str) + device_id_len]
    print("device_id:", device_id)

    target_dir = os.path.join(work_dir, device_id)

    shutil.move(sync_config_path, target_dir)

    config_path = os.path.join(target_dir, 'config.xml')
    os.remove(config_path)

    return device_id


# generate sync peers info by pod name
def gen_sync_peers(work_dir, peers_count, chain_name):
    peers = []
    for i in range(peers_count):
        device_id = gen_sync_account(work_dir)
        print("device_id:", device_id)
        peer = {
            'ip': get_node_network_name(i, chain_name),
            'port': 22000,
            'device_id': device_id
        }
        peers.append(peer)
    return peers


def gen_sync_configs(work_dir, sync_peers, chain_name):
    for i in range(len(sync_peers)):
        config_example = ET.parse(os.path.join(os.curdir, 'config.xml'))
        root = config_example.getroot()
        # add device for all folder
        for elem in root.findall('folder'):
            for peer in sync_peers:
                d = ET.SubElement(elem, 'device')
                d.set('id', peer['device_id'])
                d.set('introducedBy', '')
        # add all device
        for peer in sync_peers:
            d = ET.SubElement(root, 'device')
            d.set('id', peer['device_id'])
            d.set('name', peer['ip'])
            d.set('compression', 'always')
            d.set('introducer', 'false')
            d.set('skipIntroductionRemovals', 'false')
            d.set('introducedBy', '')
            address = ET.SubElement(d, 'address')
            address.text = 'tcp://{}:{}'.format(peer['ip'], peer['port'])
            paused = ET.SubElement(d, 'paused')
            paused.text = 'false'
            autoAcceptFolders = ET.SubElement(d, 'autoAcceptFolders')
            autoAcceptFolders.text = 'false'
            maxSendKbps = ET.SubElement(d, 'maxSendKbps')
            maxSendKbps.text = '0'
            maxRecvKbps = ET.SubElement(d, 'maxRecvKbps')
            maxRecvKbps.text = '0'
            maxRequestKiB = ET.SubElement(d, 'maxRequestKiB')
            maxRequestKiB.text = '0'
        # add gui/apikey
        gui = root.findall('gui')[0]
        apikey = ET.SubElement(gui, 'apikey')
        apikey.text = chain_name

        node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(i, chain_name)))
        path = os.path.join(node_path, 'config')
        need_directory(path)

        config_example.write(os.path.join(path, 'config.xml'))

        account_dir = os.path.join(work_dir, sync_peers[i]['device_id'])
        shutil.copy(os.path.join(account_dir, 'cert.pem'), path)
        shutil.copy(os.path.join(account_dir, 'key.pem'), path)


def run_subcmd_local_cluster(args):
    work_dir = "tmp"

    chain_path = os.path.join(work_dir, '{}'.format(args.chain_name))
    if os.path.exists(chain_path):
        print('chain {} already existed!'.format(args.chain_name))
        sys.exit(0)

    if not args.kms_password:
        print('kms_password must be set!')
        sys.exit(1)

    # generate peers info by pod name
    peers = gen_peers(args.peers_count, args.chain_name, args.is_local)
    print("peers:", peers)

    # generate network config for all peers
    net_config_list = gen_net_config_list(peers, args.enable_tls, args.is_local)
    print("net_config_list:", net_config_list)

    # generate node config
    if not args.timestamp:
        timestamp = int(time.time() * 1000)
    else:
        timestamp = args.timestamp
    for index, net_config in enumerate(net_config_list):
        num = 50000
        if args.is_local:
            num = num + index * 1000
        node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(index, args.chain_name)))
        need_directory(node_path)
        # generate network config file
        net_config_file = os.path.join(node_path, 'network-config.toml')
        with open(net_config_file, 'wt') as stream:
            toml.dump(net_config, stream)
        # generate network key
        gen_network_key(node_path)
        # generate log config
        gen_log4rs_config(node_path, args.log_level, args.is_stdout)
        gen_consensus_config(node_path, index, num)
        gen_controller_config(node_path, args.block_delay_number, num)
        # generate genesis
        gen_genesis(node_path, timestamp, DEFAULT_PREVHASH)


    # generate init_sys_config
    # is bft
    admin_dir = os.path.join(work_dir, "admin")
    super_admin = gen_super_admin(admin_dir, args.kms_password)
    if args.is_bft:
        gen_authorities(work_dir, args.chain_name, args.kms_password, args.peers_count)
        authorities = gen_sm2_authorities(work_dir, args.chain_name, args.peers_count)
    else:
        authorities = gen_authorities(work_dir, args.chain_name, args.kms_password, args.peers_count)
    gen_init_sysconfig(work_dir, args.chain_name, super_admin, authorities, args.peers_count)

    if not args.is_local:
        # generate syncthing config
        sync_peers = gen_sync_peers(work_dir, args.peers_count, args.chain_name)
        print("sync_peers:", sync_peers)
        gen_sync_configs(work_dir, sync_peers, args.chain_name)
        os.makedirs(chain_path)

    print("Done!!!")


def main():
    args = parse_arguments()
    print("args:", args)
    run_subcmd_local_cluster(args)


if __name__ == '__main__':
    main()
