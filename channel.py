import os
import yaml

with open('./NodeDeployment.yaml') as f:
    deployment = yaml.load(f, Loader=yaml.FullLoader)

n_orderer = deployment['Deployment']['orderer']
n_org = deployment['Deployment']['organization']
n_peer = deployment['Deployment']['peer']
n_server = deployment['Deployment']['server']

os.system('docker exec cli peer channel create \
          -o orderer.example.com:7050 \
          -c channel1 \
          -f ./channel-artifacts/channel1.tx \
          --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem')

os.system('docker exec cli peer channel join -b channel1.block')
os.system('docker exec -e CORE_PEER_ADDRESS=peer1.org1.example.com:8101 \
          -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer1.org1.example.com/tls/ca.crt \
          cli peer channel join \
          -b channel1.block')

for org in range(2,n_org + 1):
    for peer in range(0,n_peer):
        peer_port = 8000 + org * 100 ## 8100, 8200. 8300
        peer_port = peer_port + peer
        os.system('docker exec \
                  -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org{}.example.com/users/Admin@org{}.example.com/msp \
                  -e CORE_PEER_ADDRESS=peer{}.org{}.example.com:{} \
                  -e CORE_PEER_LOCALMSPID="Org{}MSP" \
                  -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org{}.example.com/peers/peer{}.org{}.example.com/tls/ca.crt \
                  cli peer channel join -b channel1.block'.format(org, org, peer, org, peer_port, org, org, peer, org))


