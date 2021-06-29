# cita_cloud_config

创建链的配置文件。

### 依赖

* python 3
* [kms_sm](https://github.com/cita-cloud/kms_sm) 或者 [kms_eth](https://github.com/cita-cloud/kms_eth)

安装依赖包:

```
pip install -r requirements.txt
```

### 用法

```
$ ./cita_cloud_config.py -h
usage: cita_cloud_config.py [-h] {init,increase,decrease,clean} ...

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {init,increase,decrease,clean}
                        additional help
    init                Init a chain.
    increase            Increase one node.
    decrease            Decrease one node.
    clean               Clean a chain.
```

### 初始化链

```
$ ./cita_cloud_config.py init -h
usage: cita_cloud_config.py init [-h] [--work_dir WORK_DIR] [--timestamp TIMESTAMP] [--block_delay_number BLOCK_DELAY_NUMBER]
                                 [--chain_name CHAIN_NAME] [--peers_count PEERS_COUNT] [--nodes NODES] [--super_admin SUPER_ADMIN]
                                 [--kms_passwords KMS_PASSWORDS] [--enable_tls ENABLE_TLS] [--is_stdout IS_STDOUT]
                                 [--log_level LOG_LEVEL] [--is_bft IS_BFT]

optional arguments:
  -h, --help            show this help message and exit
  --work_dir WORK_DIR   The output director of node config files.
  --timestamp TIMESTAMP
                        Timestamp of genesis block.
  --block_delay_number BLOCK_DELAY_NUMBER
                        The block delay number of chain.
  --chain_name CHAIN_NAME
                        The name of chain.
  --peers_count PEERS_COUNT
                        Count of peers.
  --nodes NODES         Node network addr list.
  --super_admin SUPER_ADMIN
                        Address of super admin.
  --kms_passwords KMS_PASSWORDS
                        Password list of kms.
  --enable_tls ENABLE_TLS
                        Is enable tls
  --is_stdout IS_STDOUT
                        Is output to stdout
  --log_level LOG_LEVEL
                        log level: warn/info/debug/trace
  --is_bft IS_BFT       Is bft
```

#### 例子

```
$ ./cita_cloud_config.py init --work_dir /tmp/test --peers_count 3 --kms_passwords 123456
args: Namespace(subcmd='init', work_dir='/tmp/test', timestamp=None, block_delay_number=0, chain_name='test-chain', peers_count=3, nodes=None, super_admin=None, kms_passwords='123456', enable_tls=True, is_stdout=False, log_level='info', is_bft=False)
peers: [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}]
net_config_list: [{'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}]}]
kms_passwords:  ['123456', '123456', '123456', '123456']
kms create output: key_id:1,address:0x7e3cd9b14155ea568f7dba141c0493297a176aca
kms create output: key_id:1,address:0xbd7e6ba6fe57abd59f110c4b98522258280a722a
kms create output: key_id:1,address:0xa91d14e24e3ef0583851110398aba8a79fc7c80e
kms create output: key_id:1,address:0xa7e84a6e67085884979007eb05948ecdaa3e0b02
Done!!!
```

#### 生成的文件

```
$ cd /tmp/test 
$ ls
test-chain  test-chain-0  test-chain-1  test-chain-2  test-chain.config

$ ls test-chain
0x7e3cd9b14155ea568f7dba141c0493297a176aca  0xa91d14e24e3ef0583851110398aba8a79fc7c80e
0xa7e84a6e67085884979007eb05948ecdaa3e0b02  0xbd7e6ba6fe57abd59f110c4b98522258280a722a

$ ls test-chain-0 
blocks                 controller-config.toml  genesis.toml          kms.db               network_key          storage-log4rs.yaml
consensus-config.toml  controller-log4rs.yaml  init_sys_config.toml  kms-log4rs.yaml      network-log4rs.yaml  tx_infos
consensus-log4rs.yaml  executor-log4rs.yaml    key_id                network-config.toml  node_address         txs
```

### 增加节点

```
$ ./cita_cloud_config.py increase -h
usage: cita_cloud_config.py increase [-h] [--work_dir WORK_DIR] [--chain_name CHAIN_NAME] [--kms_password KMS_PASSWORD] [--node NODE]

optional arguments:
  -h, --help            show this help message and exit
  --work_dir WORK_DIR   The output director of node config files.
  --chain_name CHAIN_NAME
                        The name of chain.
  --kms_password KMS_PASSWORD
                        Password of kms.
  --node NODE           Node network addr to add
```

##### 例子

```
$ ./cita_cloud_config.py increase --work_dir /tmp/test
args: Namespace(subcmd='increase', work_dir='/tmp/test', chain_name='test-chain', kms_password=None, node=None)
will add node 3, new peers_count is 4
peers: [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-3.test-chain-headless-service', 'port': 40000}]
net_config_list: [{'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-3.test-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-3.test-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-3.test-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}]}]
old kms_passwords:  ['123456', '123456', '123456', '123456']
use unique kms_password
new kms_password:  123456
kms create output: key_id:1,address:0x68cd3f09225a72db535b271841b684a5b3cf98be
new node address 0x68cd3f09225a72db535b271841b684a5b3cf98be
Done!!!
```

#### 生成的文件

```
$ ls
test-chain  test-chain-0  test-chain-1  test-chain-2  test-chain-3  test-chain.config
```
多了节点文件夹`test-chain-3`。

```
$ ls test-chain-3 
blocks                 controller-config.toml  genesis.toml          kms.db               network_key          storage-log4rs.yaml
consensus-config.toml  controller-log4rs.yaml  init_sys_config.toml  kms-log4rs.yaml      network-log4rs.yaml  tx_infos
consensus-log4rs.yaml  executor-log4rs.yaml    key_id                network-config.toml  node_address         txs
```

### 减少节点

```
$ ./cita_cloud_config.py decrease -h   
usage: cita_cloud_config.py decrease [-h] [--work_dir WORK_DIR] [--chain_name CHAIN_NAME]

optional arguments:
  -h, --help            show this help message and exit
  --work_dir WORK_DIR   The output director of node config files.
  --chain_name CHAIN_NAME
                        The name of chain.
```

#### 例子

```
$ ./cita_cloud_config.py decrease --work_dir /tmp/test
args: Namespace(subcmd='decrease', work_dir='/tmp/test', chain_name='test-chain')
will delete node 3, new peers_count is 3
peers: [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}]
net_config_list: [{'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}]}]
Done!!!
```

##### 文件变化

```
$ ls
test-chain  test-chain-0  test-chain-1  test-chain-2  test-chain.config
```

少了节点文件夹`test-chain-3`。

### 清除链

```
$ ./cita_cloud_config.py clean -h
usage: cita_cloud_config.py clean [-h] [--work_dir WORK_DIR] [--chain_name CHAIN_NAME]

optional arguments:
  -h, --help            show this help message and exit
  --work_dir WORK_DIR   The output director of node config files.
  --chain_name CHAIN_NAME
                        The name of chain.
```

#### 例子

```
$ ./cita_cloud_config.py clean --work_dir /tmp/test
args: Namespace(subcmd='clean', work_dir='/tmp/test', chain_name='test-chain')
chain test-chain has clean!
```

##### 文件变化

```
$ ls


```

链相关文件全部被清除。