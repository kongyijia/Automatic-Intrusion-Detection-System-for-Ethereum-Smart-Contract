# this website provides dapps info with categories, add category label at the end of this url
stateofthedapps = 'https://www.stateofthedapps.com/rankings/platform/ethereum/category/'
# require param: page number
page_ = "?page="
# etherscan api, we only get data from the main net
mainnet = "https://api.etherscan.io/api?"
module = "module=account"
# require param: txlist or txlistinternal
action_ = "&action="
# require param: smart contract address
address_ = "&address="
start_block = '&startblock=0'
end_block = '&endblock=99999999'
sort = "&sort=asc"
# replace the key with your own api_key, this one is invalid
api_key = "&apikey=36469EJX2XV2XYMIHJY1G4RFXD7Z7AYVJN"


def make_stateofdapps_url(category, page_num):
    url = stateofthedapps + category + page_ + str(page_num)
    return url


def make_etherscan_tx_url(address, action):
    url = mainnet + module + action_ + action + address_ + address + start_block + end_block + sort + api_key
    return url
