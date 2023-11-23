import yaml
import os


##### the number of orderer, the number of organization #########
##### location of peer node #################
with open('./NodeDeployment.yaml') as f:
    deployment = yaml.load(f, Loader=yaml.FullLoader)

n_orderer = deployment['Deployment']['orderer']
n_org = deployment['Deployment']['organization']
n_peer = deployment['Deployment']['peer']
n_server = deployment['Deployment']['server']

server_list = []
server_ip = {}
for i in range(0, n_server):
    server_list.append(deployment['Deployment']['deployment'][i]['configuration'])
    for j in deployment['Deployment']['deployment'][i]['configuration']:
        server_ip[j] = deployment['Deployment']['deployment'][i]['ip']


##### networkConfig for caliper-benchmarks ########
with open('./networkConfig.yaml') as f:
    network_config = yaml.load(f, Loader=yaml.FullLoader)

del network_config['organizations'][1]

for org in range(2, n_org + 1):

    temp_org = {'mspid': 'Org{}MSP'.format(org), \
                'identities': {'certificates': [{'name': 'User1', 'clientPrivateKey':{'path':'../organizations/peerOrganizations/org{}.example.com/users/User1@org{}.example.com/msp/keystore/priv_sk'.format(org,org)},\
                                                 'clientSignedCert':{'path':'../organizations/peerOrganizations/org{}.example.com/users/User1@org{}.example.com/msp/signcerts/User1@org{}.example.com-cert.pem'.format(org,org,org)}}]}, \
                'connectionProfile': {'path':'../organizations/peerOrganizations/org{}.example.com/connection-org{}.yaml'.format(org, org), 'discover': True}}
    network_config['organizations'].append(temp_org)






with open('./caliper-benchmarks/networks/networkConfig.yaml', 'w') as f:
    yaml.dump(network_config,f,sort_keys=False)



##### mv start file to caliper-benchmarks ####
if os.path.isfile('startfabcar.sh'):
    os.system('mv startfabcar.sh ./caliper-benchmarks')

##### mv start file to caliper-benchmarks ####
if os.path.isfile('caliper.yaml'):
    os.system('mv caliper.yaml ./caliper-benchmarks')

##### generate connection profile ########





#ip, PEER_PORT, peerpem,CAPEM, ca_port


for org in range(1, n_org + 1):
    with open('./ccp-template.yaml') as f:
        ccp_config = yaml.load(f, Loader=yaml.FullLoader)
    f2 = open('organizations/peerOrganizations/org{}.example.com/tlsca/tlsca.org{}.example.com-cert.pem'.format(org,org),'r')
    peerpem = f2.readlines()
    pem = ''
    for sen in peerpem:
        pem = pem + sen
    f2.close()
    print(peerpem)
    f3 = open('organizations/peerOrganizations/org{}.example.com/ca/ca.org{}.example.com-cert.pem'.format(org,org),'r')
    capem = f3.readlines()
    f3.close()
    print(capem)

    ccp_config['name'] = 'test-network-org{}'.format(org)
    ccp_config['client']['organization'] = 'Org{}'.format(org)
    ccp_config['organizations'] = {'Org{}'.format(org):{'mspid': 'Org{}MSP'.format(org),\
                                                        'peers': [],\
                                                        'certificateAuthorities':['ca.org{}.example.com'.format(org)]}}
    ###just do in from the scratch...
    if org != 1:
        del ccp_config['peers']['peer0.org1.example.com']
        del ccp_config['certificateAuthorities']['ca.org1.example.com']
    
    caport = 10000 + org
    for peer in range(0, n_peer):
        IP = server_ip['peer{}.org{}'.format(peer, org)]
        peer_port = 8000 + org * 100 + peer ## 8100, 8200. 8300
        peer_address = 'peer{}.org{}.example.com'.format(peer, org)
        ccp_config['organizations']['Org{}'.format(org)]['peers'].append(peer_address)

        ccp_config['peers']['peer{}.org{}.example.com'.format(peer,org)] = {'url':'grpcs://{}:{}'.format(IP, peer_port), \
                                                                            'tlsCACerts':{'pem':'{}\n'.format(pem)}, \
                                                                            'grpcOptions':{'ssl-target-name-override': 'peer{}.org{}.example.com'.format(peer, org),
                                                                                            'hostnameOverride': 'peer{}.org{}.example.com'.format(peer, org)}}

    ccp_config['certificateAuthorities'] = {'ca.org{}.example.com'.format(org):{'url':'http://localhost:{}'.format(caport),\
                                                                                'caName': 'ca-org{}'.format(org),\
                                                                                'tlsCACerts':{'pem':capem},\
                                                                                'httpOptions':{'verify': False}}}

    with open('./organizations/peerOrganizations/org{}.example.com/connection-org{}.yaml'.format(org, org), 'w') as f:
        yaml.dump(ccp_config,f,sort_keys=False)
# name: test-network-org${ORG}
# version: 1.0.0
# client:
#   organization: Org${ORG}
#   connection:
#     timeout:
#       peer:
#         endorser: '300'
# organizations:
#   Org${ORG}:
#     mspid: Org${ORG}MSP
#     peers:
#     - peer0.org${ORG}.example.com
#     certificateAuthorities:
#     - ca.org${ORG}.example.com
# peers:
#   peer0.org${ORG}.example.com:
#     url: grpcs://localhost:${P0PORT1}
#     tlsCACerts:
#       pem: |
#           ${PEERPEM}
#     grpcOptions:
#       ssl-target-name-override: peer0.org${ORG}.example.com
#       hostnameOverride: peer0.org${ORG}.example.com
# certificateAuthorities:
#   ca.org${ORG}.example.com:
#     url: https://localhost:${CAPORT}
#     caName: ca-org${ORG}
#     tlsCACerts:
#       pem: 
#         - |
#           ${CAPEM}
#     httpOptions:
#       verify: false

# for peer in range(1, n_peer):
#     peer_address = 'peer{}.org${{ORG}}.example.com'.format(peer)
#     ccp_config['organizations']['Org${{ORG}}'.format()]['peers'].append(peer_address)

#     ccp_config['peers']['peer{}.org${{ORG}}.example.com'.format(peer)] = {'url':'grpcs://${{IP}}:${{P0PORT{}}}'.format(peer + 1), \
#                                                                           'tlsCACerts':{'pem':'${{PEERPEM}}\n'.format()}, \
#                                                                           'grpcOptions':{'ssl-target-name-override': 'peer{}.org${{ORG}}.example.com'.format(peer),
#                                                                                          'hostnameOverride': 'peer{}.org${{ORG}}.example.com'.format(peer)}}
#     print(ccp_config['peers']['peer{}.org${{ORG}}.example.com'.format(peer)])

