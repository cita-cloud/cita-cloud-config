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
drwxr-xr-x 2 rink rink 120  5月 18 18:08 0x06b9de6e9a7aea05f3e01060f9b7aa0594323596
drwxr-xr-x 2 rink rink 120  5月 18 18:08 0x54cc97ca9520fe0b431b568d8abf96cf4933741a
drwxr-xr-x 2 rink rink 120  5月 18 18:08 0x66029c9e0f56eabca666414daa9905faa8545240
drwxr-xr-x 2 rink rink 120  5月 18 18:08 0x6f12e2a3f7ae50c24a9c5108e4fba23d31d7f135
drwx------ 2 rink rink  80  5月 18 18:08 A4ZRFKB-QLREYUZ-ESHC6RV-HSFL6DB-APCTTM7-7GQIYYY-H227JGS-2M36HAA
drwx------ 2 rink rink  80  5月 18 18:08 DF7EYVK-6AHD5X7-NYBYNSQ-M3VTVRB-JFBTE6B-Y67SD4B-M7IDZHX-NEEW6AQ
drwx------ 2 rink rink  80  5月 18 18:08 Q47RRDO-MCOMD3N-XC5LSO5-67HIPRG-SROQKV2-QY7X45I-CVEHJ5I-B4LYFA7
drwxr-xr-x 2 rink rink  40  5月 18 18:08 test-chain
drwxr-xr-x 4 rink rink 380  5月 18 18:08 test-chain-0
drwxr-xr-x 4 rink rink 380  5月 18 18:08 test-chain-1
drwxr-xr-x 4 rink rink 380  5月 18 18:08 test-chain-2

$ ll test-chain-0 
drwxr-xr-x 2 rink rink 100  5月 18 18:08 config
-rw-r--r-- 1 rink rink  57  5月 18 18:08 consensus-config.toml
-rw-r--r-- 1 rink rink 838  5月 18 18:08 consensus-log4rs.yaml
-rw-r--r-- 1 rink rink 127  5月 18 18:08 controller-config.toml
-rw-r--r-- 1 rink rink 840  5月 18 18:08 controller-log4rs.yaml
-rw-r--r-- 1 rink rink 836  5月 18 18:08 executor-log4rs.yaml
-rw-r--r-- 1 rink rink 106  5月 18 18:08 genesis.toml
-rw-r--r-- 1 rink rink 318  5月 18 18:08 init_sys_config.toml
-rw-r--r-- 1 rink rink   1  5月 18 18:08 key_id
-rw-r--r-- 1 rink rink 12K  5月 18 18:08 kms.db
-rw-r--r-- 1 rink rink 826  5月 18 18:08 kms-log4rs.yaml
-rw-r--r-- 1 rink rink  66  5月 18 18:08 network_key
-rw-r--r-- 1 rink rink 175  5月 18 18:08 network-config.toml
-rw-r--r-- 1 rink rink 834  5月 18 18:08 network-log4rs.yaml
-rw-r--r-- 1 rink rink  42  5月 18 18:08 node_address
-rw-r--r-- 1 rink rink 834  5月 18 18:08 storage-log4rs.yaml
drwxr-xr-x 2 rink rink  40  5月 18 18:08 tx_infos
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
drwxr-xr-x 2 rink rink 120  5月 18 18:09 0x808f0ae267e5937bc32836ecc1ecb8107a51e3f5
drwxr-xr-x 2 rink rink  40  5月 18 18:09 bft-chain
drwxr-xr-x 4 rink rink 380  5月 18 18:09 bft-chain-0
drwxr-xr-x 4 rink rink 380  5月 18 18:09 bft-chain-1
drwxr-xr-x 4 rink rink 380  5月 18 18:09 bft-chain-2
drwx------ 2 rink rink  80  5月 18 18:09 J7EKZDI-46PMN3D-WZWHW5V-G6H66MO-VFI224Y-BO6RH3S-VXOLS7V-PPZMVQL
drwx------ 2 rink rink  80  5月 18 18:09 JCGC5C6-AGJKXRI-DQHP6ES-5AIWHR7-IFPIXW4-X5ZXUOC-OLF3IKS-VRKIBQI
drwx------ 2 rink rink  80  5月 18 18:09 XJE2D7J-PWH73MP-D2JTVGU-IUIVDZ3-X7A737L-THRUCB4-BZMJ3Z7-6CF23AH

$ ll bft-chain-0
drwxr-xr-x 2 rink rink 100  5月 18 18:09 config
-rw-r--r-- 1 rink rink  57  5月 18 18:09 consensus-config.toml
-rw-r--r-- 1 rink rink 838  5月 18 18:09 consensus-log4rs.yaml
-rw-r--r-- 1 rink rink 127  5月 18 18:09 controller-config.toml
-rw-r--r-- 1 rink rink 840  5月 18 18:09 controller-log4rs.yaml
-rw-r--r-- 1 rink rink 836  5月 18 18:09 executor-log4rs.yaml
-rw-r--r-- 1 rink rink 106  5月 18 18:09 genesis.toml
-rw-r--r-- 1 rink rink 318  5月 18 18:09 init_sys_config.toml
-rw-r--r-- 1 rink rink   1  5月 18 18:09 key_id
-rw-r--r-- 1 rink rink 826  5月 18 18:09 kms-log4rs.yaml
-rw-r--r-- 1 rink rink  66  5月 18 18:09 network_key
-rw-r--r-- 1 rink rink 171  5月 18 18:09 network-config.toml
-rw-r--r-- 1 rink rink 834  5月 18 18:09 network-log4rs.yaml
-rw-r--r-- 1 rink rink  42  5月 18 18:09 node_address
-rw-r--r-- 1 rink rink  66  5月 18 18:09 node_key
-rw-r--r-- 1 rink rink 834  5月 18 18:09 storage-log4rs.yaml
drwxr-xr-x 2 rink rink  40  5月 18 18:09 tx_infos

```
