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

##### generate connection profile ########
with open('./ccp-template.yaml') as f:
    ccp_config = yaml.load(f, Loader=yaml.FullLoader)


print(ccp_config['peers']['peer0.org${{ORG}}.example.com'.format()])

for peer in range(1, n_peer):
    peer_address = 'peer{}.org${{ORG}}.example.com'.format(peer)
    ccp_config['organizations']['Org${{ORG}}'.format()]['peers'].append(peer_address)

    ccp_config['peers']['peer{}.org${{ORG}}.example.com'.format(peer)] = {'url':'grpcs://${{IP}}:${{P0PORT{}}}'.format(peer + 1), \
                                                                          'tlsCACerts':{'pem':'${{PEERPEM}}\n'.format()}, \
                                                                          'grpcOptions':{'ssl-target-name-override': 'peer{}.org${{ORG}}.example.com'.format(peer),
                                                                                         'hostnameOverride': 'peer{}.org${{ORG}}.example.com'.format(peer)}}
    print(ccp_config['peers']['peer{}.org${{ORG}}.example.com'.format(peer)])

with open('test.yaml', 'w') as f:
    yaml.dump(ccp_config,f,sort_keys=False)

# IP=$1
# ORG=$2
# P0PORT1=$3
# CAPORT1=$4
# P0PORT2=$5




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
#     url: grpcs://localhost:${P0PORT}
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