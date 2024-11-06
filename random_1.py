

import http.client

conn = http.client.HTTPSConnection("apisetu.gov.in")

payload = "{\"txnId\":\"f7f1469c-29b0-4325-9dfc-c567200a70f7\",\"format\":\"pdf\",\"certificateParameters\":{\"PolicyNumber\":\"1574564656\",\"FullName\":\"Sunil Kumar\"},\"consentArtifact\":{\"consent\":{\"consentId\":\"ea9c43aa-7f5a-4bf3-a0be-e1caa24737ba\",\"timestamp\":\"2019-08-24T14:15:22Z\",\"dataConsumer\":{\"id\":\"string\"},\"dataProvider\":{\"id\":\"string\"},\"purpose\":{\"description\":\"string\"},\"user\":{\"idType\":\"string\",\"idNumber\":\"string\",\"mobile\":\"string\",\"email\":\"string\"},\"data\":{\"id\":\"string\"},\"permission\":{\"access\":\"string\",\"dateRange\":{\"from\":\"2019-08-24T14:15:22Z\",\"to\":\"2019-08-24T14:15:22Z\"},\"frequency\":{\"unit\":\"string\",\"value\":0,\"repeats\":0}}},\"signature\":{\"signature\":\"string\"}}}"

headers = {
    'X-APISETU-CLIENTID': "REPLACE_KEY_VALUE",
    'content-type': "application/json"
    }

conn.request("POST", "/certificate/v3/tataaig/podoc", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))