# cita_cloud_config

创建链的配置文件。

### 依赖

* python 3
* [syncthing](https://syncthing.net)
* [kms_sm](https://github.com/cita-cloud/kms_sm) 或者 [kms_eth](https://github.com/cita-cloud/kms_eth)

安装依赖包:

```
pip install -r requirements.txt
```

### 使用方法

```
$ ./cita_cloud_config.py -h
usage: cita_cloud_config.py [-h] [--work_dir WORK_DIR] [--timestamp TIMESTAMP] [--block_delay_number BLOCK_DELAY_NUMBER]
                            [--chain_name CHAIN_NAME] [--peers_count PEERS_COUNT] [--kms_password KMS_PASSWORD]
                            [--enable_tls ENABLE_TLS] [--is_stdout IS_STDOUT] [--log_level LOG_LEVEL] [--is_bft IS_BFT]

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
  --kms_password KMS_PASSWORD
                        Password of kms.
  --enable_tls ENABLE_TLS
                        Is enable tls
  --is_stdout IS_STDOUT
                        Is output to stdout
  --log_level LOG_LEVEL
                        log level: warn/info/debug/trace
  --is_bft IS_BFT       Is bft

```

### 例子

```
$ ./cita_cloud_config.py --work_dir /tmp/test --peers_count 3 --kms_password 123456                                
args: Namespace(work_dir='/tmp/test', timestamp=None, block_delay_number=0, chain_name='test-chain', peers_count=3, kms_password='123456', enable_tls=True, is_stdout=False, log_level='info', is_bft=False)
peers: [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}]
net_config_list: [{'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 40000}, {'ip': 'test-chain-1.test-chain-headless-service', 'port': 40000}]}]
kms create output: key_id:1,address:0xd3da2617cf0b01fedbbcf97e9d1b74458ff8dd2d
kms create output: key_id:1,address:0x6d8c895d9da774217157e102b10ee6e13689d590
kms create output: key_id:1,address:0x1c71e671442ca68fa4d40f5199546b9e2f9dfd44
kms create output: key_id:1,address:0xbea2a30bbd10a778f93ccc1be246d2cd445abfc0
device_id: XJJVALM-POA6V7N-4TIMJSV-66HWSWA-DOMDKHR-VD7ZKJD-RZYP3X4-WSMT6AZ
device_id: XJJVALM-POA6V7N-4TIMJSV-66HWSWA-DOMDKHR-VD7ZKJD-RZYP3X4-WSMT6AZ
device_id: YNZ6QXB-GJFGQSA-525YHM5-5FWHRQ5-G2U7GJD-MJKXOR6-4ELKWNL-ZCKUXQG
device_id: YNZ6QXB-GJFGQSA-525YHM5-5FWHRQ5-G2U7GJD-MJKXOR6-4ELKWNL-ZCKUXQG
device_id: H3NJMD6-OFWXT4L-FYC7D3K-RZB7HMO-OB3QGNQ-5ZFXRYU-AN6ZXS2-CFW6TQU
device_id: H3NJMD6-OFWXT4L-FYC7D3K-RZB7HMO-OB3QGNQ-5ZFXRYU-AN6ZXS2-CFW6TQU
sync_peers: [{'ip': 'test-chain-0.test-chain-headless-service', 'port': 22000, 'device_id': 'XJJVALM-POA6V7N-4TIMJSV-66HWSWA-DOMDKHR-VD7ZKJD-RZYP3X4-WSMT6AZ'}, {'ip': 'test-chain-1.test-chain-headless-service', 'port': 22000, 'device_id': 'YNZ6QXB-GJFGQSA-525YHM5-5FWHRQ5-G2U7GJD-MJKXOR6-4ELKWNL-ZCKUXQG'}, {'ip': 'test-chain-2.test-chain-headless-service', 'port': 22000, 'device_id': 'H3NJMD6-OFWXT4L-FYC7D3K-RZB7HMO-OB3QGNQ-5ZFXRYU-AN6ZXS2-CFW6TQU'}]
Done!!!
```

生成的文件

```
$ cd /tmp/test 
$ ll
drwxr-xr-x 2 rink rink 120  5月 18 16:36 0x1c71e671442ca68fa4d40f5199546b9e2f9dfd44
drwxr-xr-x 2 rink rink 120  5月 18 16:36 0x6d8c895d9da774217157e102b10ee6e13689d590
drwxr-xr-x 2 rink rink 120  5月 18 16:36 0xbea2a30bbd10a778f93ccc1be246d2cd445abfc0
drwxr-xr-x 2 rink rink 120  5月 18 16:36 0xd3da2617cf0b01fedbbcf97e9d1b74458ff8dd2d
drwx------ 2 rink rink  80  5月 18 16:36 H3NJMD6-OFWXT4L-FYC7D3K-RZB7HMO-OB3QGNQ-5ZFXRYU-AN6ZXS2-CFW6TQU
drwxr-xr-x 4 rink rink 360  5月 18 16:36 test-chain-0
drwxr-xr-x 4 rink rink 360  5月 18 16:36 test-chain-1
drwxr-xr-x 4 rink rink 360  5月 18 16:36 test-chain-2
drwx------ 2 rink rink  80  5月 18 16:36 XJJVALM-POA6V7N-4TIMJSV-66HWSWA-DOMDKHR-VD7ZKJD-RZYP3X4-WSMT6AZ
drwx------ 2 rink rink  80  5月 18 16:36 YNZ6QXB-GJFGQSA-525YHM5-5FWHRQ5-G2U7GJD-MJKXOR6-4ELKWNL-ZCKUXQG

$ ll test-chain-0 
drwxr-xr-x 2 rink rink 100  5月 18 16:36 config
-rw-r--r-- 1 rink rink  57  5月 18 16:36 consensus-config.toml
-rw-r--r-- 1 rink rink 838  5月 18 16:36 consensus-log4rs.yaml
-rw-r--r-- 1 rink rink 127  5月 18 16:36 controller-config.toml
-rw-r--r-- 1 rink rink 840  5月 18 16:36 controller-log4rs.yaml
-rw-r--r-- 1 rink rink 836  5月 18 16:36 executor-log4rs.yaml
-rw-r--r-- 1 rink rink 106  5月 18 16:36 genesis.toml
-rw-r--r-- 1 rink rink 318  5月 18 16:36 init_sys_config.toml
-rw-r--r-- 1 rink rink   1  5月 18 16:36 key_id
-rw-r--r-- 1 rink rink 12K  5月 18 16:36 kms.db
-rw-r--r-- 1 rink rink 826  5月 18 16:36 kms-log4rs.yaml
-rw-r--r-- 1 rink rink 175  5月 18 16:36 network-config.toml
-rw-r--r-- 1 rink rink 834  5月 18 16:36 network-log4rs.yaml
-rw-r--r-- 1 rink rink  42  5月 18 16:36 node_address
-rw-r--r-- 1 rink rink 834  5月 18 16:36 storage-log4rs.yaml
drwxr-xr-x 2 rink rink  40  5月 18 16:36 tx_infos

```

bft的例子

```
$ ./cita_cloud_config.py --work_dir /tmp/test --peers_count 3 --kms_password 123456 --chain_name bft-chain --is_bft true
args: Namespace(work_dir='/tmp/test', timestamp=None, block_delay_number=0, chain_name='bft-chain', peers_count=3, kms_password='123456', enable_tls=True, is_stdout=False, log_level='info', is_bft=True)
peers: [{'ip': 'bft-chain-0.bft-chain-headless-service', 'port': 40000}, {'ip': 'bft-chain-1.bft-chain-headless-service', 'port': 40000}, {'ip': 'bft-chain-2.bft-chain-headless-service', 'port': 40000}]
net_config_list: [{'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'bft-chain-1.bft-chain-headless-service', 'port': 40000}, {'ip': 'bft-chain-2.bft-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'bft-chain-0.bft-chain-headless-service', 'port': 40000}, {'ip': 'bft-chain-2.bft-chain-headless-service', 'port': 40000}]}, {'enable_tls': True, 'port': 40000, 'peers': [{'ip': 'bft-chain-0.bft-chain-headless-service', 'port': 40000}, {'ip': 'bft-chain-1.bft-chain-headless-service', 'port': 40000}]}]
kms create output: key_id:1,address:0xccfa85b374d245b55e3a35f96e60cbff14c5bdcf
device_id: XEZTSIF-I6V7QSP-LKA5IQN-2B7ZFWC-T3QU6ID-KYMB7TV-7EXK7XI-JL2RLA7
device_id: XEZTSIF-I6V7QSP-LKA5IQN-2B7ZFWC-T3QU6ID-KYMB7TV-7EXK7XI-JL2RLA7
device_id: 3BX5FXS-L2NT36Z-TDXVU7A-IAT6ZKA-FES5A2D-XOG57VU-WZUVAHP-UUMZBAL
device_id: 3BX5FXS-L2NT36Z-TDXVU7A-IAT6ZKA-FES5A2D-XOG57VU-WZUVAHP-UUMZBAL
device_id: XOUR2TX-KLGARBP-ZZ3WYF7-ZWZWHJC-UW7UOFZ-WHVFN2O-YWLL2MW-MSUFBQI
device_id: XOUR2TX-KLGARBP-ZZ3WYF7-ZWZWHJC-UW7UOFZ-WHVFN2O-YWLL2MW-MSUFBQI
sync_peers: [{'ip': 'bft-chain-0.bft-chain-headless-service', 'port': 22000, 'device_id': 'XEZTSIF-I6V7QSP-LKA5IQN-2B7ZFWC-T3QU6ID-KYMB7TV-7EXK7XI-JL2RLA7'}, {'ip': 'bft-chain-1.bft-chain-headless-service', 'port': 22000, 'device_id': '3BX5FXS-L2NT36Z-TDXVU7A-IAT6ZKA-FES5A2D-XOG57VU-WZUVAHP-UUMZBAL'}, {'ip': 'bft-chain-2.bft-chain-headless-service', 'port': 22000, 'device_id': 'XOUR2TX-KLGARBP-ZZ3WYF7-ZWZWHJC-UW7UOFZ-WHVFN2O-YWLL2MW-MSUFBQI'}]
Done!!!
```

生成的文件

```
$ cd /tmp/test 
$ ll
drwxr-xr-x 2 rink rink 120  5月 18 16:41 0xc15e880847b9c2a9b490f20ac31dc0e6a8ae36c7
drwx------ 2 rink rink  80  5月 18 16:41 4XDSWSW-MJAVKZZ-WUUQB5O-G3LXYA5-PSHKFBM-EQIY35K-WCUW6GH-DJW6CQG
drwxr-xr-x 4 rink rink 360  5月 18 16:41 bft-chain-0
drwxr-xr-x 4 rink rink 360  5月 18 16:41 bft-chain-1
drwxr-xr-x 4 rink rink 360  5月 18 16:41 bft-chain-2
drwxr-xr-x 4 rink rink 360  5月 18 16:41 bft-chain-3
drwx------ 2 rink rink  80  5月 18 16:41 N3YJJYW-7WTAFB3-TK5JCGT-CIZKIJH-V2YBHUA-YA3LTQC-GV4ET5E-TDMFDQ4
drwx------ 2 rink rink  80  5月 18 16:41 P7OEG2E-6SMC2QP-KB2Z55K-3XFUX2Q-DKP6Y65-YNF7HVB-5YBRYPL-6XHM3QY
drwx------ 2 rink rink  80  5月 18 16:41 UEFIRWR-P5K7NWC-IZEE3XD-GAMKZ7M-7IEYINA-PTQX4IQ-Q7RHHUD-M2GBZQ5

$ ll bft-chain-0
drwxr-xr-x 2 rink rink 100  5月 18 16:41 config
-rw-r--r-- 1 rink rink  57  5月 18 16:41 consensus-config.toml
-rw-r--r-- 1 rink rink 838  5月 18 16:41 consensus-log4rs.yaml
-rw-r--r-- 1 rink rink 127  5月 18 16:41 controller-config.toml
-rw-r--r-- 1 rink rink 840  5月 18 16:41 controller-log4rs.yaml
-rw-r--r-- 1 rink rink 836  5月 18 16:41 executor-log4rs.yaml
-rw-r--r-- 1 rink rink 106  5月 18 16:41 genesis.toml
-rw-r--r-- 1 rink rink 364  5月 18 16:41 init_sys_config.toml
-rw-r--r-- 1 rink rink   1  5月 18 16:41 key_id
-rw-r--r-- 1 rink rink 826  5月 18 16:41 kms-log4rs.yaml
-rw-r--r-- 1 rink rink 241  5月 18 16:41 network-config.toml
-rw-r--r-- 1 rink rink 834  5月 18 16:41 network-log4rs.yaml
-rw-r--r-- 1 rink rink  42  5月 18 16:41 node_address
-rw-r--r-- 1 rink rink  66  5月 18 16:41 node_key
-rw-r--r-- 1 rink rink 834  5月 18 16:41 storage-log4rs.yaml
drwxr-xr-x 2 rink rink  40  5月 18 16:41 tx_infos
```
