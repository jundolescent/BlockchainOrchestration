import yaml
import sys
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
extra_hosts = []
total = []
total_hosts = []
for i in range(0, n_server):
    extra_hosts = []
    server_list.append(deployment['Deployment']['deployment'][i]['configuration'])
    for j in deployment['Deployment']['deployment'][i]['configuration']:
        extra_hosts.append('{}.example.com:{}'.format(j,deployment['Deployment']['deployment'][i]['ip']))
        total.append('{}.example.com:{}'.format(j,deployment['Deployment']['deployment'][i]['ip']))
    total_hosts.append(extra_hosts)
#total_hosts = list(set(temp) - set(extra_hosts))
result = []
for j in total_hosts:
    j = list(set(total) - set(j))
    result.append(j)
print(result)
print(server_list)

for i in server_list:
    for j in i:
        

