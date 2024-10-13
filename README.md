# MoMo_OpenAPI_Debit_Request
### <b>Api_user and APi_Key</b>
Each country has a specific partner portal where  the API Keys and User are configured.<br>
This flow is different from SandBox where specific APIs are called.<br><br>

Login onto the Portal<br>
under your profile, find APIAcess<br>
Configure the provider Callback Host & Payment Server URL as illustrated below.<br>

If the URL for your callback is https://webhook.com/mysite/status  then,<br>
configure <ins><b>Provider Callback Host</b></ins> as webhook.com<br>
and <ins><b>Payment Server URL</b></ins> as  https://webhook.com/mysite/status <br>

### <b>Subscription Keys</b>
<ins><b>Please use the primary Subscription Keys</b></ins>

### <b>Target_Environment per country with Currency</b> 
| Country | X-Target-Environment | Currency |
| --- | --- | --- |
MTN Uganda | mtnuganda | UGX
MTN Ghana |	mtnghana |	GHS
MTN Ivory | Coast	mtnivorycoast |	XOF
MTN Zambia |	mtnzambia |	ZMW
MTN Cameroon |	mtncameroon |	XAF
MTN Benin |	mtnbenin |	XOF
MTN Congo B |	mtncongo |	XAF
MTN Swaziland |	mtnswaziland |	SZL
MTN GuineaConakry |	mtnguineaconakry |	GNF
MTN SouthAfrica |	mtnsouthafrica |	ZAR
MTN Liberia |	mtnliberia |	LRD

### <b>Request To Pay Body</b>
| Field | Format | Description |
| --- | --- | --- |
amount | (string) | The amount to be requested.
currency | (string): | The currency in which the amount is requested.
externalId | (string) | The unique identifier for the request.
payer | (object):
payer:partyIdType | (string)| The type of party ID for the payer.(MSISDN/ALIAS/EMAIL)
payer:partyId | (string) | The ID of the payer.
payerMessage | (string)| Message from the payer.
payeeNote | (string) | Note for the payee.


# <br>Download and run the Notebook "Debit Request.ipynb" </br>
