import time
import json
import hmac
import base64
import requests
import time

class Utils():
    
    def __init__(self, apikey, secretkey, passphrase, use_server_time=False):
        self.apikey = apikey
        self.secretkey = secretkey
        self.passphrase = passphrase
        self.use_server_time = use_server_time
    
    base_url = "https://api.bitget.com"
    server_timestamp_url='/api/spot/v1/public/time'
    
    def get_timestamp(self):
        timestamp = time.time_ns() // 1000000
        return timestamp
    
    def signature(self, timestamp, method, request_path, body):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(self.secretkey, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)
    
    def get_header(self, sign, timestamp):
        header = dict()
        header["Content-Type"] = "application/json"
        header["ACCESS-KEY"] = self.apikey
        header["ACCESS-SIGN"] = sign
        header["ACCESS-TIMESTAMP"] = str(timestamp)
        header["ACCESS-PASSPHRASE"] = self.passphrase
        header["locale"] = "en-US"
    
        return header
    
    def params_to_str(self,params):
        url = '?'
        for key, value in params.items():
            url = url + str(key) + '=' + str(value) + '&'
    
        return url[0:-1]
    
    def server_timestamp(self):
        url = self.base_url + self.server_timestamp_url
        response = requests.get(url)
        if response.status_code == 200:  #200 indicates a successful response
            return response.json()['data']
        else:
            return ""
        
    def request(self, method, request_path, params,use_server_time=False):
        
        if method == "GET":
            request_path = request_path + self.params_to_str(params)
        
        url = self.base_url + request_path
        
        timestamp = self.get_timestamp()
        
        if use_server_time:
            timestamp = self.server_timestamp()
        
        if method == "POST":
            body = json.dumps(params)  #Converting Python primitive types into JSON
        else:
            body = ""
        sign = self.signature(timestamp, method, request_path, body)
        header = self.get_header(sign,timestamp)
            
        response = None
        if method == "GET":
            response = requests.get(url, headers=header)
            text = response.json()
            print("response : ", json.dumps(text, indent=2))
            
        elif method == "POST":
            response = requests.post(url, data=body, headers=header)
            text = response.json()
            print("response : ",json.dumps(text, indent=2))
            
        elif method == "DELETE":
            response = requests.delete(url, headers=header)
    
        print("status:", response.status_code)
        
class Market(Utils):

    def __init__(self, apikey, secretkey, passphrase, use_server_time=False):
        Utils.__init__(self, apikey, secretkey, passphrase, use_server_time)

    def contracts(self,productType):
        method = "GET"
        params = {}
        params['productType'] = productType
        request_path = "/api/mix/v1/market/contracts"
        self.request(method,request_path,params,self.use_server_time)

    def depth(self,symbol, limit="100"):
        method = "GET"
        params = {}
        params['symbol'] = symbol
        params['limit'] = limit
        request_path = "/api/mix/v1/market/depth"
        self.request(method,request_path,params,self.use_server_time)

    def tickers(self,productType): 
        method = "GET"
        params = {}
        params['productType'] = productType
        request_path = "/api/mix/v1/market/tickers"
        self.request(method,request_path,params,self.use_server_time)

    def ticker(self,symbol):   
        method = "GET"
        params = {}
        params['symbol'] = symbol
        request_path = "/api/mix/v1/market/ticker"
        self.request(method,request_path,params,self.use_server_time)

    def fills(self,symbol,limit="100"):  
        method = "GET"
        params = {}
        params['symbol'] = symbol
        params['limit'] = limit
        request_path = "/api/mix/v1/market/fills"
        self.request(method,request_path,params,self.use_server_time)

    def candle_data(self,symbol,granularity,startTime,endTime): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        params['granularity'] = granularity
        params['startTime'] = startTime
        params['endTime']= endTime
        request_path = "/api/mix/v1/market/candles"
        self.request(method,request_path,params,self.use_server_time)

    def index_price(self,symbol): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        request_path = "/api/mix/v1/market/index"
        self.request(method,request_path,params,self.use_server_time)

    def next_funding_time(self,symbol): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        request_path = "/api/mix/v1/market/funding-time"
        self.request(method,request_path,params,self.use_server_time)

    def history_funding_rate(self,symbol,pageSize=20,pageNo=1,nextPage = False): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        params['pageSize'] = pageSize
        params['pageNo'] = pageNo
        params['nextPage'] = nextPage
        request_path = "/api/mix/v1/market/history-fundRate"
        self.request(method,request_path,params,self.use_server_time)

    def current_funding_rate(self,symbol): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        request_path = "/api/mix/v1/market/current-fundRate"
        self.request(method,request_path,params,self.use_server_time)

    def open_interest(self,symbol): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        request_path = "/api/mix/v1/market/open-interest"
        self.request(method,request_path,params,self.use_server_time)

    def mark_price(self,symbol): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        request_path = "/api/mix/v1/market/mark-price"
        self.request(method,request_path,params,self.use_server_time)

    def leverage(self,symbol): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        request_path = "/api/mix/v1/market/symbol-leverage"
        self.request(method,request_path,params,self.use_server_time)
        
class Account(Utils):
    
    def __init__(self, apikey, secretkey, passphrase, use_server_time=False):
        Utils.__init__(self, apikey, secretkey, passphrase, use_server_time)

    def account(self,symbol,marginCoin): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        params['marginCoin'] = marginCoin
        request_path = "/api/mix/v1/account/account"
        self.request(method,request_path,params,self.use_server_time)

    def account_list(self,productType): 
        method = "GET"
        params = {}
        params['productType'] = productType
        request_path = "/api/mix/v1/account/accounts"
        self.request(method,request_path,params,self.use_server_time)

    def open_count(self,symbol,marginCoin,openPrice,openAmount,leverage="20"): 
        method = "POST"
        params = {}
        params['symbol'] = symbol
        params['marginCoin'] = marginCoin
        params['openPrice'] = openPrice
        params['leverage'] = leverage
        params['openAmount'] = openAmount
        request_path = "/api/mix/v1/account/open-count"
        self.request(method,request_path,params,self.use_server_time)

    def position(self,symbol,marginCoin): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        params['marginCoin'] = marginCoin
        request_path = "/api/mix/v1/position/singlePosition"
        self.request(method,request_path,params,self.use_server_time)

    def allposition(self,productType,marginCoin): 
        method = "GET"
        params = {}
        params['productType'] = productType
        params['marginCoin'] = marginCoin
        request_path = "/api/mix/v1/position/allPosition"
        self.request(method,request_path,params,self.use_server_time)

    def account_bill(self,symbol,marginCoin,startTime,endTime,pageSize=20,lastEndId='',next=False): 
        method = "GET"
        params = {}
        params['symbol'] = symbol
        params['marginCoin'] = marginCoin
        params['startTime'] = startTime
        params['endTime'] = endTime
        params['pageSize'] = pageSize
        params['lastEndId'] = lastEndId
        params['next'] = next
        request_path = "/api/mix/v1/account/accountBill"
        self.request(method,request_path,params,self.use_server_time)

    def business_account_bill(self,productType,startTime,endTime,pageSize=20,lastEndId='',next=False): 
        method = "GET"
        params = {}
        params['productType'] = productType
        params['startTime'] = startTime
        params['endTime'] = endTime
        params['pageSize'] = pageSize
        params['lastEndId'] = lastEndId
        params['next'] = next
        request_path = "/api/mix/v1/account/accountBusinessBill"
        self.request(method,request_path,params,self.use_server_time)

    def change_leverage(self,symbol,marginCoin,leverage,holdSide=''): 
        method = "POST"
        params = {}
        params['symbol'] = symbol
        params['marginCoin'] = marginCoin
        params['leverage'] = leverage
        params['holdSide'] = holdSide
        request_path = "/api/mix/v1/account/setLeverage"
        self.request(method,request_path,params,self.use_server_time)

    def change_margin(self,symbol,marginCoin,amount,holdSide=''): 
        method = "POST"
        params = {}
        params['symbol'] = symbol
        params['marginCoin'] = marginCoin
        params['amount'] = amount
        params['holdSide'] = holdSide
        request_path = "/api/mix/v1/account/setMargin"
        self.request(method,request_path,params,self.use_server_time)

    def change_margin_mode(self,symbol,marginCoin,marginMode): 
        method = "POST"
        params = {}
        params['symbol'] = symbol
        params['marginCoin'] = marginCoin
        params['marginMode'] = marginMode
        request_path = "/api/mix/v1/account/setMarginMode"
        self.request(method,request_path,params,self.use_server_time)
        
print("done")
