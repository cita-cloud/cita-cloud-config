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
import hashlib
from pysmx.SM2 import generate_keypair
from pysmx.SM3 import hash_msg
import shutil
from random import choice
import string
import pickle

DEFAULT_PREVHASH = '0x{:064x}'.format(0)

DEFAULT_BLOCK_INTERVAL = 3

SERVICE_LIST = [
    'network',
    'consensus',
    'executor',
    'storage',
    'controller',
    'kms',
]


class ChainConfig:
    work_dir = '.'
    timestamp = 0
    chain_name = 'test-chain'
    peers_count = 3
    peers = []
    super_admin = ''
    kms_passwords = []
    enable_tls = True
    is_bft = False

    def __init__(self, chain_name, work_dir):
        self.chain_name = chain_name
        self.work_dir = work_dir


def gen_password(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() == 'false':
        return False
    elif value.lower() == 'true':
        return True
    raise ValueError(f'{value} is not a valid boolean value')


def parse_arguments():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        dest='subcmd', title='subcommands', help='additional help')

    #
    # Subcommand: init
    #

    pInit = subparsers.add_parser(
        SUBCMD_INIT, help='Init a chain.')

    pInit.add_argument(
        '--work_dir', default='.', help='The output director of node config files.')

    pInit.add_argument(
        '--timestamp',
        type=int,
        help='Timestamp of genesis block.')

    pInit.add_argument(
        '--block_delay_number',
        type=int,
        default=0,
        help='The block delay number of chain.')

    pInit.add_argument(
        '--chain_name', default='test-chain', help='The name of chain.')

    pInit.add_argument(
        '--peers_count',
        type=int,
        help='Count of peers.')

    pInit.add_argument(
        '--nodes',
        help='Node network addr list.')

    pInit.add_argument(
        '--super_admin',
        help='Address of super admin.')

    pInit.add_argument(
        '--kms_passwords', help='Password list of kms.')

    pInit.add_argument(
        '--enable_tls',
        type=str_to_bool,
        default=True,
        help='Is enable tls')

    pInit.add_argument(
        '--is_stdout',
        type=str_to_bool,
        default=False,
        help='Is output to stdout')

    pInit.add_argument(
        '--log_level',
        default="info",
        help='log level: warn/info/debug/trace')

    pInit.add_argument(
        '--is_bft',
        type=str_to_bool,
        default=False,
        help='Is bft')

    pInit.add_argument(
        '--is_local',
        type=str_to_bool,
        default=False,
        help='Is running in local machine')

    #
    # Subcommand: increase
    #

    pIncrease = subparsers.add_parser(
        SUBCMD_INCREASE, help='Increase one node.')

    pIncrease.add_argument(
        '--work_dir', default='.', help='The output director of node config files.')

    pIncrease.add_argument(
        '--chain_name', default='test-chain', help='The name of chain.')

    pIncrease.add_argument(
        '--kms_password', help='Password of kms.')

    pIncrease.add_argument(
        '--node', help='Node network addr to add')

    pIncrease.add_argument(
        '--is_local',
        type=str_to_bool,
        default=False,
        help='Is running in local machine')

    #
    # Subcommand: decrease
    #

    pDecrease = subparsers.add_parser(
        SUBCMD_DECREASE, help='Decrease one node.')

    pDecrease.add_argument(
        '--work_dir', default='.', help='The output director of node config files.')

    pDecrease.add_argument(
        '--chain_name', default='test-chain', help='The name of chain.')

    pDecrease.add_argument(
        '--is_local',
        type=str_to_bool,
        default=False,
        help='Is running in local machine')

    #
    # Subcommand: clean
    #

    pClean = subparsers.add_parser(
        SUBCMD_CLEAN, help='Clean a chain.')

    pClean.add_argument(
        '--work_dir', default='.', help='The output director of node config files.')

    pClean.add_argument(
        '--chain_name', default='test-chain', help='The name of chain.')

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


# generate peers info by nodes
def gen_peers_by_nodes(nodes):
    peers = []
    node_list = nodes.split(',')
    for node in node_list:
        ip_port = node.split(':')
        peer = {
            'ip': ip_port[0],
            'port': int(ip_port[1])
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
                'port': peer['port'],
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
    return '0x' + hashlib.sha256(chain_name.encode()).hexdigest()


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


def gen_kms_account(chain_path):
    cmd = 'kms create -k key_file'
    kms_create = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = kms_create.stdout.readlines()[-1].decode().strip()
    print("kms create output:", output)
    # output should looks like: key_id:1,address:0xba21324990a2feb0a0b6ca16b444b5585b841df9
    infos = output.split(',')
    key_id = infos[0].split(':')[1]
    address = infos[1].split(':')[1]

    dir = os.path.join(chain_path, address)
    if not os.path.exists(dir):
        os.makedirs(dir)

    current_dir = os.path.abspath(os.curdir)
    shutil.move(os.path.join(current_dir, 'kms.db'), os.path.join(dir, 'kms.db'))
    shutil.move(os.path.join(current_dir, 'key_file'), os.path.join(dir, 'key_file'))

    path = os.path.join(dir, 'key_id')
    with open(path, 'wt') as stream:
        stream.write(key_id)

    path = os.path.join(dir, 'node_address')
    with open(path, 'wt') as stream:
        stream.write(address)

    return address


def gen_super_admin(work_dir, chain_name, kms_password):
    current_dir = os.path.abspath(os.curdir)
    path = os.path.join(current_dir, 'key_file')
    with open(path, 'wt') as stream:
        stream.write(kms_password)
    chain_path = os.path.join(work_dir, chain_name)
    super_admin = gen_kms_account(chain_path)
    return super_admin


def gen_sm2_account(node_path, is_local, kms_password):
    if is_local:
        path = os.path.join(node_path, 'key_file')
        with open(path, 'wt') as stream:
            stream.write(kms_password)
    pk, sk = generate_keypair()
    addr = '0x' + hash_msg(pk)[24:]
    path = os.path.join(node_path, 'node_key')
    with open(path, 'wt') as stream:
        stream.write('0x' + sk.hex())
    path = os.path.join(node_path, 'node_address')
    with open(path, 'wt') as stream:
        stream.write(addr)
    path = os.path.join(node_path, 'key_id')
    with open(path, 'wt') as stream:
        stream.write(str(0))
    return addr


def gen_sm2_authorities(work_dir, chain_name, peers_count, is_local, kms_passwords):
    authorities = []
    for i in range(peers_count):
        node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(i, chain_name)))
        addr = gen_sm2_account(node_path, is_local, kms_passwords[i + 1])
        authorities.append(addr)
    return authorities


def gen_authorities(work_dir, chain_name, kms_passwords, peers_count):
    authorities = []
    for i in range(peers_count):
        current_dir = os.path.abspath(os.curdir)
        path = os.path.join(current_dir, 'key_file')
        with open(path, 'wt') as stream:
            stream.write(kms_passwords[i + 1])

        chain_path = os.path.join(work_dir, chain_name)
        address = gen_kms_account(chain_path)

        dir = os.path.join(chain_path, address)
        node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(i, chain_name)))

        shutil.copy(os.path.join(dir, 'kms.db'), node_path)
        shutil.copy(os.path.join(dir, 'key_id'), node_path)
        shutil.copy(os.path.join(dir, 'node_address'), node_path)
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


def run_subcmd_init(args, work_dir):
    config_file = os.path.join(work_dir, '{}.config'.format(args.chain_name))
    if os.path.exists(config_file):
        print('chain {} already config!'.format(args.chain_name))
        sys.exit(0)

    chain_path = os.path.join(work_dir, args.chain_name)
    need_directory(chain_path)

    chain_config = ChainConfig(args.chain_name, work_dir)

    # generate peers info
    if args.nodes:
        # if have --nodes generate peers info by nodes
        peers = gen_peers_by_nodes(args.nodes)
        args.peers_count = len(peers)
    else:
        # else generate peers info by pod name
        peers = gen_peers(args.peers_count, args.chain_name, args.is_local)
    print("peers:", peers)

    chain_config.peers = peers
    chain_config.peers_count = args.peers_count

    # generate network config for all peers
    net_config_list = gen_net_config_list(peers, args.enable_tls, args.is_local)
    print("net_config_list:", net_config_list)

    chain_config.enable_tls = args.enable_tls

    # generate node config
    if not args.timestamp:
        timestamp = int(time.time() * 1000)
    else:
        timestamp = args.timestamp
    chain_config.timestamp = timestamp
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
    if args.kms_passwords:
        kms_passwords = args.kms_passwords.split(',')
        if len(kms_passwords) == 1:
            kms_passwords = kms_passwords * (args.peers_count + 1)

        if len(kms_passwords) != (args.peers_count + 1):
            print('The len of kms_passwords is invalid')
            sys.exit(1)
    else:
        kms_passwords = []
        for i in range(args.peers_count + 1):
            kms_passwords.append(gen_password())
    print('kms_passwords: ', kms_passwords)
    chain_config.kms_passwords = kms_passwords

    if args.super_admin:
        super_admin = args.super_admin
    else:
        super_admin = gen_super_admin(work_dir, args.chain_name, kms_passwords[0])

    chain_config.super_admin = super_admin

    if args.is_bft:
        authorities = gen_sm2_authorities(work_dir, args.chain_name, args.peers_count, args.is_local, kms_passwords)
    else:
        authorities = gen_authorities(work_dir, args.chain_name, kms_passwords, args.peers_count)
    gen_init_sysconfig(work_dir, args.chain_name, super_admin, authorities, args.peers_count)

    chain_config.is_bft = args.is_bft

    with open(config_file, 'wb') as f:
        pickle.dump(chain_config, f)
    print("Done!!!")


def run_subcmd_increase(args, work_dir):
    config_file = os.path.join(work_dir, '{}.config'.format(args.chain_name))
    with open(config_file, 'rb') as f:
        chain_config = pickle.load(f)

    chain_path = os.path.join(work_dir, args.chain_name)
    need_directory(chain_path)

    peers_count = chain_config.peers_count
    new_peer_no = peers_count
    new_peers_count = peers_count + 1
    print('will add node {}, new peers_count is {}'.format(new_peer_no, new_peers_count))

    chain_config.peers_count = new_peers_count

    peers = chain_config.peers
    if args.node:
        ip_port = args.node.split(':')
        peer = {
            'ip': ip_port[0],
            'port': int(ip_port[1])
        }
        peers.append(peer)
    else:
        # regenerate peers info by pod name
        peers = gen_peers(new_peers_count, args.chain_name, args.is_local)
    print("peers:", peers)
    chain_config.peers = peers

    # regenerate network config for all peers
    net_config_list = gen_net_config_list(peers, chain_config.enable_tls, args.is_local)
    print("net_config_list:", net_config_list)
    for index, net_config in enumerate(net_config_list):
        node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(index, args.chain_name)))
        need_directory(node_path)
        # generate network config file
        net_config_file = os.path.join(node_path, 'network-config.toml')
        with open(net_config_file, 'wt') as stream:
            toml.dump(net_config, stream)
        # generate network key
        gen_network_key(node_path)

    source_node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(0, args.chain_name)))
    new_node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(new_peer_no, args.chain_name)))

    # generate network key
    gen_network_key(new_node_path)

    # copy log config
    for service_name in SERVICE_LIST:
        shutil.copy(os.path.join(source_node_path, '{}-log4rs.yaml'.format(service_name)), new_node_path)

    num = 50000
    if args.is_local:
        num = num + peers_count * 1000
    gen_consensus_config(new_node_path, peers_count, num)
    gen_controller_config(new_node_path, 0, num)

    # copy genesis
    shutil.copy(os.path.join(source_node_path, 'genesis.toml'), new_node_path)

    # copy init_sys_config
    shutil.copy(os.path.join(source_node_path, 'init_sys_config.toml'), new_node_path)

    # generate new account
    print('old kms_passwords: ', chain_config.kms_passwords)
    if len(set(chain_config.kms_passwords)) == 1:
        print('use unique kms_password')
        kms_password = chain_config.kms_passwords[0]
    else:
        if args.kms_password:
            kms_password = args.kms_password
        else:
            kms_password = gen_password()

    print('new kms_password: ', kms_password)
    chain_config.kms_passwords.append(kms_password)

    if chain_config.is_bft:
        address = gen_sm2_account(new_node_path, args.is_local, kms_password)
    else:
        current_dir = os.path.abspath(os.curdir)
        path = os.path.join(current_dir, 'key_file')
        with open(path, 'wt') as stream:
            stream.write(kms_password)

        address = gen_kms_account(chain_path)

        dir = os.path.join(chain_path, address)

        shutil.copy(os.path.join(dir, 'kms.db'), node_path)
        shutil.copy(os.path.join(dir, 'key_id'), node_path)
        shutil.copy(os.path.join(dir, 'node_address'), node_path)
    print('new node address {}'.format(address))

    with open(config_file, 'wb') as f:
        pickle.dump(chain_config, f)
    print("Done!!!")


def run_subcmd_decrease(args, work_dir):
    config_file = os.path.join(work_dir, '{}.config'.format(args.chain_name))
    with open(config_file, 'rb') as f:
        chain_config = pickle.load(f)

    last_peer_no = chain_config.peers_count - 1
    new_peers_count = chain_config.peers_count - 1
    print('will delete node {}, new peers_count is {}'.format(last_peer_no, new_peers_count))

    chain_config.peers_count = new_peers_count

    peers = chain_config.peers
    peers.pop()
    print("peers:", peers)
    chain_config.peers = peers

    # regenerate network config for all peers
    net_config_list = gen_net_config_list(peers, chain_config.enable_tls, args.is_local)
    print("net_config_list:", net_config_list)
    for index, net_config in enumerate(net_config_list):
        node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(index, args.chain_name)))
        need_directory(node_path)
        # generate network config file
        net_config_file = os.path.join(node_path, 'network-config.toml')
        with open(net_config_file, 'wt') as stream:
            toml.dump(net_config, stream)
        # generate network key
        gen_network_key(node_path)

    last_node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(last_peer_no, args.chain_name)))
    shutil.rmtree(last_node_path)

    with open(config_file, 'wb') as f:
        pickle.dump(chain_config, f)
    print("Done!!!")


def run_subcmd_clean(args, work_dir):
    config_file = os.path.join(work_dir, '{}.config'.format(args.chain_name))
    with open(config_file, 'rb') as f:
        chain_config = pickle.load(f)

    for i in range(chain_config.peers_count):
        node_path = os.path.join(work_dir, '{}'.format(get_node_pod_name(i, args.chain_name)))
        try:
            shutil.rmtree(node_path)
        except:
            pass

    chain_path = os.path.join(work_dir, args.chain_name)
    try:
        shutil.rmtree(chain_path)
    except:
        pass

    config_file = os.path.join(work_dir, '{}.config'.format(args.chain_name))
    try:
        os.remove(config_file)
    except:
        pass
    print('chain {} has clean!'.format(args.chain_name))


def main():
    args = parse_arguments()
    if args.is_local:
        args.work_dir = "./tmp"
    print("args:", args)
    funcs_router = {
        SUBCMD_INIT: run_subcmd_init,
        SUBCMD_INCREASE: run_subcmd_increase,
        SUBCMD_DECREASE: run_subcmd_decrease,
        SUBCMD_CLEAN: run_subcmd_clean,
    }
    work_dir = os.path.abspath(args.work_dir)
    funcs_router[args.subcmd](args, work_dir)


if __name__ == '__main__':
    SUBCMD_INIT = 'init'
    SUBCMD_INCREASE = 'increase'
    SUBCMD_DECREASE = 'decrease'
    SUBCMD_CLEAN = 'clean'
    main()
