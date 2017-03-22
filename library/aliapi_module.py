__author__ = 'pangff'
from ansible.module_utils.basic import *
import datetime
from urllib import quote
from hashlib import sha1
import hmac
import base64

def percentEncode(encodeStr):
    encodeStr = str(encodeStr)
    if sys.stdin.encoding is None:
        res = quote(encodeStr.decode('cp936').encode('utf8'), '')
    else:
        res = quote(encodeStr.decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def createUrl(url,paramDic,AccessKeySecret):

        dict= sorted(paramDic.iteritems(), key=lambda d:d[0])

        canonicalizedQueryString="";

        for (k,v) in dict:
            url+=(percentEncode(k)+"="+percentEncode(v))+"&";
            canonicalizedQueryString+= ("&"+percentEncode(k)+"="+percentEncode(v));

        stringToSign = "GET" +"&"+percentEncode("/")+"&"+ percentEncode(canonicalizedQueryString[1:])

        my_sign = hmac.new(AccessKeySecret+"&", stringToSign, sha1).digest()
        my_sign = base64.b64encode(my_sign)
        url+="Signature="+percentEncode(my_sign);

        return url;

def getPublicParamDic(module):
    Timestamp = datetime.datetime.utcnow().isoformat()
    AccessKeyID=module.params["AccessKeyID"]
    Format=module.params["Format"]
    SignatureVersion=module.params["SignatureVersion"]
    ResourceOwnerAccount=module.params["ResourceOwnerAccount"]
    Version=module.params["Version"]
    paramDic = {"AccessKeyID":AccessKeyID, "Format":Format, "SignatureVersion": SignatureVersion, "ResourceOwnerAccount":ResourceOwnerAccount, "SignatureMethod":"HMAC-SHA1",'Timestamp':Timestamp,"Version":Version,"SignatureNonce":Timestamp};
    return paramDic;

def uploadCert(module):
    url = module.params["BaseUrl"];
    paramDic = getPublicParamDic(module);
    paramDic.setdefault('Action',module.params["Action"])
    paramDic.setdefault('RegionId',module.params["RegionId"])
    paramDic.setdefault('ServerCertificate',module.params["ServerCertificate"])
    paramDic.setdefault('ServerCertificateName',module.params["ServerCertificateName"])
    paramDic.setdefault('PrivateKey',module.params["PrivateKey"])
    url = createUrl(url,paramDic,module.params["AccessKeySecret"])
    return url;



def main():
    fields = {
        "AccessKeyID": {"required": True, "type": "str"},
        "AccessKeySecret": {"required": True, "type": "str"},
        "Version": {"required": True, "type": "str"},
        "Format": {"required": True, "type": "str"},
        "SignatureVersion":{"required": True, "type": "str"},
        "ResourceOwnerAccount":{"required": True, "type": "str"},
        "Action": {"required": True, "type": "str"},
        "RegionId": {"required": True, "type": "str"},
        "ServerCertificate": {"required": True, "type": "str"},
        "ServerCertificateName": {"required": True, "type": "str"},
        "PrivateKey": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    url = uploadCert(module)
    response = {"url":url}
    module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()