# %% [markdown]
# ### <b>Api_user and APi_Key</b>
# Each country has a specific partner portal where  the API Keys and User are configured.<br>
# This flow is different from SandBox where specific APIs are called.<br><br>
# 
# Login onto the Portal<br>
# under your profile, find APIAcess<br>
# Configure the provider Callback Host & Payment Server URL as illustrated below.<br>
# 
# If the URL for your callback is https://webhook.com/mysite/status  then,<br>
# configure <ins><b>Provider Callback Host</b></ins> as webhook.com<br>
# and <ins><b>Payment Server URL</b></ins> as  https://webhook.com/mysite/status <br>
# 
# ### <b>Subscription Keys</b>
# <ins><b>Please use the primary Subscription Keys</b></ins>
# 
# ### <b>Target_Environment per country with Currency</b> 
# | Country | X-Target-Environment | Currency |
# | --- | --- | --- |
# MTN Uganda | mtnuganda | UGX
# MTN Ghana |	mtnghana |	GHS
# MTN Ivory | Coast	mtnivorycoast |	XOF
# MTN Zambia |	mtnzambia |	ZMW
# MTN Cameroon |	mtncameroon |	XAF
# MTN Benin |	mtnbenin |	XOF
# MTN Congo B |	mtncongo |	XAF
# MTN Swaziland |	mtnswaziland |	SZL
# MTN GuineaConakry |	mtnguineaconakry |	GNF
# MTN SouthAfrica |	mtnsouthafrica |	ZAR
# MTN Liberia |	mtnliberia |	LRD
# 
# ### <b>Request To Pay Body</b>
# | Field | Format | Description |
# | --- | --- | --- |
# amount | (string) | The amount to be requested.
# currency | (string): | The currency in which the amount is requested.
# externalId | (string) | The unique identifier for the request.
# payer | (object):
# payer:partyIdType | (string)| The type of party ID for the payer.(MSISDN/ALIAS/EMAIL)
# payer:partyId | (string) | The ID of the payer.
# payerMessage | (string)| Message from the payer.
# payeeNote | (string) | Note for the payee.
# 
# 
# 
# 
# 

# %% [markdown]
# 

# %%
from datetime import datetime
Api_User = "***************" 
Api_Key = "****************"
Token=""
Token_expiry_time = ""
Token_expired = False
Token_expiry_time = datetime.now()
Environment = "mtnuganda" #Target Environment  
Collection_Subscription_Primary_Key  = "*******************"#Primary Key for Collection Subscription.https://momoapi.mtn.com/profile
Request_ID_Debit = "" #UUID String Request Reference 
Base_Url = "https://proxy.momoapi.mtn.com" #Production Base URL


# %%

#Function to generate Token and set Token expiry. 
def Get_Token():# function to return token (renews token if expired)
    import requests as rq
    from datetime import datetime, timedelta
    global Token 
    global Token_expiry_time
    global Api_User
    global Api_Key    
    EndPoint = Base_Url+"/collection/token/"
    Auth = bytes(Api_User + ':' + Api_Key, "utf-8")
    headers = {    
    "Ocp-Apim-Subscription-Key": Collection_Subscription_Primary_Key,
    }
    resp = rq.request("post", EndPoint,auth=(Api_User,Api_Key), headers=headers)
    ResponseJson = resp.json()
    #print(ResponseJson)    
    Token = ResponseJson.get('access_token')
    Token_expiry = ResponseJson.get('expires_in')
    Token_expiry_time = datetime.now() + timedelta(seconds= int(Token_expiry)) #Track Token Expiry Time

# %%
#Function to Validate  Status of Token
#If the Token is Expired a new one will be generated. 
def Token_Status():
    global Token
    global Token_expiry_time
    global Token_expired 
    if Token_expiry_time >= datetime.now():
        Token_expired = False    
        print ("Token not Expired: Expiring at "+ str(Token_expiry_time))
        #print(Token)
    else:
        Token_expired = True
        Get_Token()
        print ("New Token Generated Expiring at "+ str(Token_expiry_time))
        #print(Token)


# %%
#Function that initiates a Debit USSD Prompt to the Payer to approve wit PIN
def Request_Debit_Payment(Environment,Payer_ID,Amount,Subscription):
  import requests as rq
  from datetime import datetime, timedelta
  import json
  import uuid
  global Request_ID_Debit
  Token_Status()
  Request_ID_Debit = str(uuid.uuid4())
  url = Base_Url+"/collection/v1_0/requesttopay"
  headers = {
    "X-Reference-Id": Request_ID_Debit, #Unique for every request, used to validate status of the request. 
    "X-Target-Environment": Environment,
    "Ocp-Apim-Subscription-Key": Subscription,
    "Authorization":"Bearer "+Token, #Avoid creating new tokens for every request,  track the Expiry 
    "Content-Type": "application/json"
    ### You can add X-Callback-Url to receive the callback  ("X-Callback-Url":"https://webhook.com/mysite/status")
  }
  body = {    
    "amount": Amount,
    "currency": "UGX", #use the currency as per country mentioned above
    "externalId": str(uuid.uuid1()), #Used for Reconciliation between application and MoMo platform. 
    "payer": {
      "partyIdType": "MSISDN",#EMAIL and ALIAS apply as well 
      "partyId": Payer_ID
  },
    "payerMessage": "MoMo Debit API Python Code Example", #Message sent to the Payer
    "payeeNote": "MoMo Debit API Python Code Example" #Message Note to the  Payee
  }
  resp = rq.request("post", url, json=body, headers=headers)
  print("Debit request to MSISDN "+Payer_ID+" Amount "+Amount+" "+ "Response Code "+str(resp.status_code))
  #print(resp.text)

# %%
#Check Status 
def Check_Status(Request_ID,Subscription,Target_Environment):
    import requests as rq
    import json
    Token_Status()
    url = Base_Url+"/collection/v1_0/requesttopay/"+Request_ID
    headers = {
    "X-Target-Environment": Target_Environment,
    "Ocp-Apim-Subscription-Key": Subscription,
    "Authorization":"Bearer "+Token,
    }
    resp = rq.request("get", url,headers=headers)
    Status_Json = resp.json()
    print(Status_Json)



# %%
#Invokes the Debit Request function 
Request_Debit_Payment("mtnuganda","256700000000","600",Collection_Subscription_Primary_Key)

# %%
#Invokes the Debit Request status function
Check_Status(Request_ID_Debit,Collection_Subscription_Primary_Key,Environment)


